const { Pool } = require('pg');
const logger = require('./logger');

const pool = new Pool({
  host: process.env.DB_HOST || 'postgres',
  port: parseInt(process.env.DB_PORT || '5432', 10),
  database: process.env.DB_NAME || 'hotel_db',
  user: process.env.DB_USER || 'hotel_user',
  password: process.env.DB_PASSWORD || 'HotelApp_SecPass2026!#',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('connect', () => {
  logger.info('Connected to PostgreSQL Database successfully as hotel_user', {
    database: process.env.DB_NAME || 'hotel_db',
    user: process.env.DB_USER || 'hotel_user'
  });
});

pool.on('error', (err) => {
  logger.error('Unexpected error on idle PostgreSQL client', { error: err.message, stack: err.stack });
});

// Helper thực thi truy vấn an toàn
async function query(text, params) {
  const start = Date.now();
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    if (duration > 500) {
      logger.warn('Slow query detected', { text, duration, rows: res.rowCount });
    }
    return res;
  } catch (error) {
    logger.error('Database query error', { text, error: error.message });
    throw error;
  }
}

// Kiểm tra sức khỏe kết nối DB
async function checkHealth() {
  try {
    const res = await pool.query('SELECT NOW() as current_time, current_user as user_name');
    return {
      healthy: true,
      time: res.rows[0].current_time,
      user: res.rows[0].user_name
    };
  } catch (err) {
    return {
      healthy: false,
      error: err.message
    };
  }
}

module.exports = {
  pool,
  query,
  checkHealth
};
