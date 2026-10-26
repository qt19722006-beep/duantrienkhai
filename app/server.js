const express = require('express');
const cors = require('cors');
const path = require('path');
const db = require('./db');
const logger = require('./logger');
const { 
  register, 
  httpRequestCounter, 
  httpRequestDuration, 
  roomStatusGauge, 
  bookingStatusGauge, 
  hotelRevenueGauge 
} = require('./metrics');

const app = express();
const PORT = process.env.APP_PORT || 3000;

// Middleware cơ bản
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Metrics and Request Logging Middleware
app.use((req, res, next) => {
  const start = process.hrtime();
  
  res.on('finish', () => {
    const diff = process.hrtime(start);
    const durationSeconds = diff[0] + diff[1] / 1e9;
    const durationMs = Math.round(durationSeconds * 1000);
    const route = req.route ? req.route.path : req.path;
    const statusCode = res.statusCode.toString();

    // Thu thập Metrics Prometheus
    httpRequestCounter.inc({ method: req.method, route, status_code: statusCode });
    httpRequestDuration.observe({ method: req.method, route, status_code: statusCode }, durationSeconds);

    // Ghi log tập trung (dành cho Promtail & Loki)
    if (!req.path.startsWith('/metrics')) {
      const level = res.statusCode >= 500 ? 'error' : res.statusCode >= 400 ? 'warn' : 'info';
      logger[level]('HTTP_REQUEST', {
        method: req.method,
        url: req.originalUrl,
        route,
        status: res.statusCode,
        duration_ms: durationMs,
        client_ip: req.ip || req.headers['x-forwarded-for'] || req.socket.remoteAddress,
        user_agent: req.headers['user-agent']
      });
    }
  });

  next();
});

// Phục vụ giao diện tĩnh (Frontend)
app.use(express.static(path.join(__dirname, 'public')));

// ==========================================
// MONITORING & HEALTH CHECK ENDPOINTS
// ==========================================

// Endpoint Prometheus Scrape Metrics
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (err) {
    res.status(500).end(err.message);
  }
});

// Endpoint Health Check (Liveness/Readiness probe)
app.get('/health', async (req, res) => {
  const dbHealth = await db.checkHealth();
  const status = dbHealth.healthy ? 'UP' : 'DOWN';
  const httpCode = dbHealth.healthy ? 200 : 503;

  res.status(httpCode).json({
    status,
    timestamp: new Date().toISOString(),
    uptime_seconds: Math.floor(process.uptime()),
    database: dbHealth,
    environment: process.env.NODE_ENV || 'production'
  });
});

// ==========================================
// HOTEL BUSINESS API ENDPOINTS
// ==========================================

// 1. Thống kê tổng quan hệ thống khách sạn
app.get('/api/stats', async (req, res) => {
  try {
    const roomsStats = await db.query(`
      SELECT 
        COUNT(*) as total_rooms,
        COUNT(*) FILTER (WHERE status = 'available') as available_rooms,
        COUNT(*) FILTER (WHERE status = 'occupied') as occupied_rooms,
        COUNT(*) FILTER (WHERE status = 'maintenance') as maintenance_rooms
      FROM hotel.rooms
    `);

    const bookingsStats = await db.query(`
      SELECT 
        COUNT(*) as total_bookings,
        COUNT(*) FILTER (WHERE status = 'pending') as pending_bookings,
        COUNT(*) FILTER (WHERE status = 'confirmed') as confirmed_bookings,
        COUNT(*) FILTER (WHERE status = 'checked_in') as active_guests,
        COALESCE(SUM(total_price) FILTER (WHERE status != 'cancelled'), 0) as total_revenue
      FROM hotel.bookings
    `);

    const customersCount = await db.query('SELECT COUNT(*) as total_customers FROM hotel.customers');

    res.json({
      rooms: roomsStats.rows[0],
      bookings: bookingsStats.rows[0],
      customers: customersCount.rows[0]
    });
  } catch (err) {
    logger.error('Error fetching stats', { error: err.message });
    res.status(500).json({ error: 'Failed to retrieve stats' });
  }
});

// 2. Danh sách phòng (Có bộ lọc loại phòng, trạng thái, giá tiền)
app.get('/api/rooms', async (req, res) => {
  try {
    const { type, status, max_price, guests } = req.query;
    let query = 'SELECT * FROM hotel.rooms WHERE 1=1';
    const params = [];

    if (type && type !== 'all') {
      params.push(type);
      query += ` AND type = $${params.length}`;
    }

    if (status && status !== 'all') {
      params.push(status);
      query += ` AND status = $${params.length}`;
    }

    if (max_price) {
      params.push(parseFloat(max_price));
      query += ` AND price_per_night <= $${params.length}`;
    }

    if (guests) {
      params.push(parseInt(guests, 10));
      query += ` AND max_guests >= $${params.length}`;
    }

    query += ' ORDER BY price_per_night ASC';

    const result = await db.query(query, params);
    res.json(result.rows);
  } catch (err) {
    logger.error('Error fetching rooms', { error: err.message, query: req.query });
    res.status(500).json({ error: 'Failed to retrieve rooms' });
  }
});

// 3. Chi tiết một phòng cụ thể
app.get('/api/rooms/:id', async (req, res) => {
  try {
    const result = await db.query('SELECT * FROM hotel.rooms WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Room not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    logger.error('Error fetching room detail', { id: req.params.id, error: err.message });
    res.status(500).json({ error: 'Failed to retrieve room' });
  }
});

// 4. Danh sách đặt phòng (Bookings) kèm thông tin khách và phòng
app.get('/api/bookings', async (req, res) => {
  try {
    const { status, search } = req.query;
    let sql = `
      SELECT 
        b.id,
        b.booking_code,
        b.check_in_date,
        b.check_out_date,
        b.total_guests,
        b.total_nights,
        b.total_price,
        b.status,
        b.special_requests,
        b.created_at,
        c.full_name as customer_name,
        c.email as customer_email,
        c.phone as customer_phone,
        c.id_card as customer_id_card,
        r.room_number,
        r.name as room_name,
        r.type as room_type,
        r.price_per_night
      FROM hotel.bookings b
      JOIN hotel.customers c ON b.customer_id = c.id
      JOIN hotel.rooms r ON b.room_id = r.id
      WHERE 1=1
    `;
    const params = [];

    if (status && status !== 'all') {
      params.push(status);
      sql += ` AND b.status = $${params.length}`;
    }

    if (search) {
      params.push(`%${search}%`);
      sql += ` AND (b.booking_code ILIKE $${params.length} OR c.phone ILIKE $${params.length} OR c.full_name ILIKE $${params.length})`;
    }

    sql += ' ORDER BY b.created_at DESC';

    const result = await db.query(sql, params);
    res.json(result.rows);
  } catch (err) {
    logger.error('Error fetching bookings', { error: err.message });
    res.status(500).json({ error: 'Failed to retrieve bookings' });
  }
});

// 5. Tạo đơn đặt phòng mới
app.post('/api/bookings', async (req, res) => {
  const { 
    room_id, 
    customer_name, 
    customer_email, 
    customer_phone, 
    customer_id_card, 
    customer_address, 
    check_in_date, 
    check_out_date, 
    total_guests, 
    special_requests 
  } = req.body;

  // Validation cơ bản
  if (!room_id || !customer_name || !customer_email || !customer_phone || !check_in_date || !check_out_date) {
    return res.status(400).json({ error: 'Missing required booking fields' });
  }

  const checkIn = new Date(check_in_date);
  const checkOut = new Date(check_out_date);
  const diffTime = checkOut.getTime() - checkIn.getTime();
  const totalNights = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (totalNights <= 0) {
    return res.status(400).json({ error: 'Ngày trả phòng phải sau ngày nhận phòng ít nhất 1 đêm' });
  }

  const client = await db.pool.connect();
  try {
    await client.query('BEGIN');

    // 1. Kiểm tra phòng tồn tại
    const roomRes = await client.query('SELECT * FROM hotel.rooms WHERE id = $1 FOR UPDATE', [room_id]);
    if (roomRes.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.status(404).json({ error: 'Phòng không tồn tại' });
    }
    const room = roomRes.rows[0];

    // 2. Tìm hoặc tạo khách hàng
    let customerId;
    const existingCust = await client.query(
      'SELECT id FROM hotel.customers WHERE phone = $1 OR email = $2', 
      [customer_phone, customer_email]
    );

    if (existingCust.rows.length > 0) {
      customerId = existingCust.rows[0].id;
      // Cập nhật thông tin nếu cần
      await client.query(
        'UPDATE hotel.customers SET full_name = $1, id_card = COALESCE($2, id_card), address = COALESCE($3, address) WHERE id = $4',
        [customer_name, customer_id_card, customer_address, customerId]
      );
    } else {
      const newCust = await client.query(
        `INSERT INTO hotel.customers (full_name, email, phone, id_card, address) 
         VALUES ($1, $2, $3, $4, $5) RETURNING id`,
        [customer_name, customer_email, customer_phone, customer_id_card || 'Chưa cung cấp', customer_address || '']
      );
      customerId = newCust.rows[0].id;
    }

    // 3. Tính tổng tiền
    const totalPrice = room.price_per_night * totalNights;
    const randomSuffix = Math.floor(1000 + Math.random() * 9000);
    const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const bookingCode = `BK-${dateStr}-${randomSuffix}`;

    // 4. Tạo bản ghi Booking
    const newBooking = await client.query(
      `INSERT INTO hotel.bookings 
        (booking_code, customer_id, room_id, check_in_date, check_out_date, total_guests, total_nights, total_price, status, special_requests)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'confirmed', $9)
       RETURNING *`,
      [bookingCode, customerId, room_id, check_in_date, check_out_date, total_guests || 1, totalNights, totalPrice, special_requests || '']
    );

    await client.query('COMMIT');

    logger.info('BOOKING_CREATED', {
      event: 'BOOKING_CREATED',
      booking_code: bookingCode,
      room_number: room.room_number,
      customer_name,
      total_nights: totalNights,
      total_price: totalPrice,
      status: 'confirmed'
    });

    res.status(201).json({
      message: 'Đặt phòng thành công!',
      booking: newBooking.rows[0],
      booking_code: bookingCode
    });
  } catch (err) {
    await client.query('ROLLBACK');
    logger.error('Failed to create booking', { error: err.message, body: req.body });
    res.status(500).json({ error: 'Không thể tạo đơn đặt phòng: ' + err.message });
  } finally {
    client.release();
  }
});

// 6. Cập nhật trạng thái đặt phòng
app.put('/api/bookings/:id/status', async (req, res) => {
  const { status } = req.body;
  const allowedStatuses = ['pending', 'confirmed', 'checked_in', 'completed', 'cancelled'];

  if (!allowedStatuses.includes(status)) {
    return res.status(400).json({ error: 'Trạng thái không hợp lệ' });
  }

  try {
    const result = await db.query(
      `UPDATE hotel.bookings 
       SET status = $1, updated_at = CURRENT_TIMESTAMP 
       WHERE id = $2 
       RETURNING *`,
      [status, req.params.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Không tìm thấy đơn đặt phòng' });
    }

    const updated = result.rows[0];

    logger.info('BOOKING_STATUS_UPDATED', {
      event: 'BOOKING_STATUS_UPDATED',
      booking_id: updated.id,
      booking_code: updated.booking_code,
      new_status: status
    });

    res.json({ message: 'Cập nhật trạng thái thành công', booking: updated });
  } catch (err) {
    logger.error('Error updating booking status', { id: req.params.id, status, error: err.message });
    res.status(500).json({ error: 'Không thể cập nhật trạng thái' });
  }
});

// 7. Danh sách khách hàng
app.get('/api/customers', async (req, res) => {
  try {
    const result = await db.query(`
      SELECT 
        c.*,
        COUNT(b.id) as total_bookings,
        COALESCE(SUM(b.total_price), 0) as total_spent
      FROM hotel.customers c
      LEFT JOIN hotel.bookings b ON c.id = b.customer_id
      GROUP BY c.id
      ORDER BY c.created_at DESC
    `);
    res.json(result.rows);
  } catch (err) {
    logger.error('Error fetching customers', { error: err.message });
    res.status(500).json({ error: 'Failed to retrieve customers' });
  }
});

// Định kỳ cập nhật Prometheus business gauges mỗi 15 giây
async function updateMetricsGauges() {
  try {
    const rooms = await db.query('SELECT type, status, COUNT(*) as count FROM hotel.rooms GROUP BY type, status');
    rooms.rows.forEach(r => {
      roomStatusGauge.set({ type: r.type, status: r.status }, parseInt(r.count, 10));
    });

    const bookings = await db.query('SELECT status, COUNT(*) as count FROM hotel.bookings GROUP BY status');
    bookings.rows.forEach(b => {
      bookingStatusGauge.set({ status: b.status }, parseInt(b.count, 10));
    });

    const revenue = await db.query("SELECT COALESCE(SUM(total_price), 0) as rev FROM hotel.bookings WHERE status != 'cancelled'");
    if (revenue.rows.length > 0) {
      hotelRevenueGauge.set(parseFloat(revenue.rows[0].rev));
    }
  } catch (err) {
    // Không log lỗi liên tục nếu DB đang khởi động
  }
}
setInterval(updateMetricsGauges, 15000);

// Khởi chạy server
app.listen(PORT, '0.0.0.0', () => {
  logger.info(`Hotel Booking Application started successfully on port ${PORT}`, {
    port: PORT,
    node_env: process.env.NODE_ENV || 'production'
  });
});
