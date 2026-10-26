// ==========================================================
// GRAND PALACE LUXURY HOTEL - FRONTEND APPLICATION JAVASCRIPT
// ==========================================================

let currentRooms = [];
let activeStatusFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
  // Thiết lập ngày mặc định cho bộ lọc (hôm nay và 2 ngày sau)
  const today = new Date().toISOString().split('T')[0];
  const next2Days = new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  
  const checkinInput = document.getElementById('filter-checkin');
  const checkoutInput = document.getElementById('filter-checkout');
  if (checkinInput) checkinInput.value = today;
  if (checkoutInput) checkoutInput.value = next2Days;

  // Tải dữ liệu ban đầu
  loadStats();
  loadRooms();
  checkSystemHealth();

  // Polling sức khỏe hệ thống mỗi 10 giây
  setInterval(checkSystemHealth, 10000);
});

// Chuyển đổi giữa các tab
function switchTab(tabId) {
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));

  const targetTab = document.getElementById(`tab-${tabId}`);
  if (targetTab) targetTab.classList.add('active');

  const navLinks = document.querySelectorAll('.nav-link');
  if (tabId === 'rooms' && navLinks[0]) navLinks[0].classList.add('active');
  if (tabId === 'bookings') {
    if (navLinks[1]) navLinks[1].classList.add('active');
    loadBookings();
  }
  if (tabId === 'customers') {
    if (navLinks[2]) navLinks[2].classList.add('active');
    loadCustomers();
  }
  if (tabId === 'system' && navLinks[3]) navLinks[3].classList.add('active');
}

// Kiểm tra sức khỏe hệ thống (Health check)
async function checkSystemHealth() {
  const pill = document.getElementById('system-health-pill');
  const text = document.getElementById('health-text');
  try {
    const res = await fetch('/health');
    const data = await res.json();
    if (data.status === 'UP') {
      pill.style.background = 'rgba(16, 185, 129, 0.15)';
      pill.style.borderColor = 'rgba(16, 185, 129, 0.4)';
      pill.style.color = '#10b981';
      text.textContent = 'Hệ Thống & DB Sẵn Sàng';
    } else {
      pill.style.background = 'rgba(239, 68, 68, 0.15)';
      pill.style.borderColor = 'rgba(239, 68, 68, 0.4)';
      pill.style.color = '#ef4444';
      text.textContent = 'Mất Kết Nối DB';
    }
  } catch (err) {
    pill.style.background = 'rgba(245, 158, 11, 0.15)';
    pill.style.borderColor = 'rgba(245, 158, 11, 0.4)';
    pill.style.color = '#f59e0b';
    text.textContent = 'Đang Tải Dịch Vụ...';
  }
}

// Tải thống kê tổng quan
async function loadStats() {
  try {
    const res = await fetch('/api/stats');
    const data = await res.json();
    
    document.getElementById('stat-total-rooms').textContent = data.rooms.total_rooms || 0;
    document.getElementById('stat-avail-rooms').textContent = data.rooms.available_rooms || 0;
    document.getElementById('stat-total-bookings').textContent = data.bookings.total_bookings || 0;
    
    const rev = Number(data.bookings.total_revenue || 0);
    document.getElementById('stat-total-revenue').textContent = formatVND(rev);
  } catch (err) {
    console.error('Lỗi khi tải thống kê:', err);
  }
}

// Định dạng tiền tệ VNĐ
function formatVND(amount) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
}

// Tải danh sách phòng
async function loadRooms() {
  const grid = document.getElementById('rooms-grid');
  try {
    const type = document.getElementById('filter-type')?.value || 'all';
    const guests = document.getElementById('filter-guests')?.value || '';
    
    let url = `/api/rooms?status=${activeStatusFilter}`;
    if (type !== 'all') url += `&type=${encodeURIComponent(type)}`;
    if (guests) url += `&guests=${encodeURIComponent(guests)}`;

    const res = await fetch(url);
    currentRooms = await res.json();
    renderRooms(currentRooms);
  } catch (err) {
    grid.innerHTML = `<div class="loading-state"><p class="text-danger">Không thể kết nối máy chủ. Hãy thử lại sau.</p></div>`;
  }
}

// Hiển thị danh sách phòng lên Grid
function renderRooms(rooms) {
  const grid = document.getElementById('rooms-grid');
  if (!rooms || rooms.length === 0) {
    grid.innerHTML = `<div class="loading-state" style="grid-column: 1/-1;"><p>Không tìm thấy phòng phù hợp với tiêu chí lọc.</p></div>`;
    return;
  }

  grid.innerHTML = rooms.map(r => {
    const amenities = Array.isArray(r.amenities) ? r.amenities : [];
    const statusText = {
      'available': 'Phòng Trống',
      'occupied': 'Đang Ở',
      'maintenance': 'Bảo Trì'
    }[r.status] || r.status;

    return `
      <div class="room-card">
        <div class="room-img-wrap">
          <img src="${r.image_url}" alt="${r.name}" class="room-img" loading="lazy">
          <span class="room-status-badge badge-${r.status}">${statusText}</span>
          <span class="room-type-tag">${r.type}</span>
        </div>
        <div class="room-body">
          <div class="room-header">
            <h3 class="room-name">${r.name}</h3>
            <span class="room-number">P.${r.room_number}</span>
          </div>
          <div class="room-meta-info">
            <span>👥 Tối đa ${r.max_guests} khách</span>
            <span>🛏️ ${r.bed_type}</span>
            <span>📐 ${r.size_sqm} m²</span>
          </div>
          <p class="room-desc">${r.description || ''}</p>
          <div class="room-amenities">
            ${amenities.slice(0, 3).map(a => `<span class="amenity-chip">✓ ${a}</span>`).join('')}
            ${amenities.length > 3 ? `<span class="amenity-chip">+${amenities.length - 3} tiện ích</span>` : ''}
          </div>
          <div class="room-footer">
            <div class="room-price-wrap">
              <span class="price-val">${formatVND(r.price_per_night)}</span>
              <span class="price-unit">/ đêm (đã gồm thuế)</span>
            </div>
            <div class="room-actions">
              <button class="btn btn-outline btn-sm" onclick="openDetailModal(${r.id})">Chi Tiết</button>
              ${r.status === 'available' 
                ? `<button class="btn btn-primary btn-sm" onclick="openBookingModal(${r.id})">Đặt Ngay</button>` 
                : `<button class="btn btn-sm" disabled style="opacity:0.5; cursor:not-allowed;">Hết Phòng</button>`
              }
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// Bộ lọc trạng thái phòng
function filterByStatus(status, btn) {
  activeStatusFilter = status;
  document.querySelectorAll('#room-status-filter .pill-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  loadRooms();
}

function applyFilters() {
  loadRooms();
}

// MODAL ĐẶT PHÒNG
function openBookingModal(roomId) {
  const room = currentRooms.find(r => r.id === roomId);
  if (!room) return;

  document.getElementById('book-room-id').value = room.id;
  document.getElementById('book-room-rate').value = room.price_per_night;
  document.getElementById('modal-room-title').textContent = `Đặt Phòng ${room.name} (P.${room.room_number})`;
  document.getElementById('modal-room-price').textContent = `${formatVND(room.price_per_night)} / đêm`;

  const today = new Date().toISOString().split('T')[0];
  const tomorrow = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  
  const inElem = document.getElementById('book-checkin');
  const outElem = document.getElementById('book-checkout');
  inElem.min = today;
  inElem.value = document.getElementById('filter-checkin')?.value || today;
  outElem.min = tomorrow;
  outElem.value = document.getElementById('filter-checkout')?.value || tomorrow;

  calculateBookingTotal();
  document.getElementById('booking-modal').classList.add('active');
}

function closeBookingModal() {
  document.getElementById('booking-modal').classList.remove('active');
}

function calculateBookingTotal() {
  const checkinVal = document.getElementById('book-checkin').value;
  const checkoutVal = document.getElementById('book-checkout').value;
  const rate = parseFloat(document.getElementById('book-room-rate').value) || 0;

  if (checkinVal && checkoutVal) {
    const diff = new Date(checkoutVal) - new Date(checkinVal);
    const nights = Math.ceil(diff / (1000 * 60 * 60 * 24));
    if (nights > 0) {
      document.getElementById('calc-nights').textContent = `${nights} đêm`;
      document.getElementById('calc-total').textContent = formatVND(nights * rate);
      return;
    }
  }
  document.getElementById('calc-nights').textContent = '0 đêm';
  document.getElementById('calc-total').textContent = '0 VNĐ';
}

// Xử lý gửi form đặt phòng
async function handleBookingSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById('btn-submit-booking');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳ Đang xử lý...</span>';

  const payload = {
    room_id: parseInt(document.getElementById('book-room-id').value, 10),
    check_in_date: document.getElementById('book-checkin').value,
    check_out_date: document.getElementById('book-checkout').value,
    customer_name: document.getElementById('book-name').value.trim(),
    customer_phone: document.getElementById('book-phone').value.trim(),
    customer_email: document.getElementById('book-email').value.trim(),
    customer_id_card: document.getElementById('book-idcard').value.trim(),
    customer_address: document.getElementById('book-address').value.trim(),
    special_requests: document.getElementById('book-requests').value.trim(),
    total_guests: 2
  };

  try {
    const res = await fetch('/api/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
      alert(`🎉 ĐẶT PHÒNG THÀNH CÔNG!\n\nMã đặt phòng của bạn là: ${data.booking_code}\nTổng thanh toán: ${formatVND(data.booking.total_price)}\nNhân viên khách sạn sẽ liên hệ xác nhận trong ít phút.`);
      closeBookingModal();
      document.getElementById('booking-form').reset();
      loadStats();
      loadRooms();
    } else {
      alert(`❌ Lỗi: ${data.error || 'Không thể tạo đơn đặt phòng'}`);
    }
  } catch (err) {
    alert('❌ Không thể kết nối tới máy chủ. Vui lòng thử lại!');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>🔒 Xác Nhận Đặt Phòng</span>';
  }
}

// MODAL XEM CHI TIẾT PHÒNG
async function openDetailModal(roomId) {
  const modal = document.getElementById('room-detail-modal');
  const body = document.getElementById('detail-body');
  const title = document.getElementById('detail-title');

  try {
    const res = await fetch(`/api/rooms/${roomId}`);
    const r = await res.json();
    title.textContent = `${r.name} (Phòng ${r.room_number})`;

    const amenities = Array.isArray(r.amenities) ? r.amenities : [];
    body.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:1.25rem;">
        <img src="${r.image_url}" alt="${r.name}" style="width:100%; height:260px; object-fit:cover; border-radius:var(--radius-md);">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span class="room-type-tag" style="position:static;">${r.type}</span>
          <span style="font-size:1.5rem; font-weight:800; color:var(--gold-primary);">${formatVND(r.price_per_night)} / đêm</span>
        </div>
        <p style="color:var(--text-muted); font-size:0.95rem; line-height:1.6;">${r.description}</p>
        <div>
          <h4 style="font-size:0.95rem; color:var(--gold-primary); margin-bottom:0.75rem;">Tiện Nghi & Dịch Vụ Đi Kèm:</h4>
          <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
            ${amenities.map(a => `<span class="amenity-chip" style="font-size:0.85rem; padding:0.3rem 0.8rem;">✓ ${a}</span>`).join('')}
          </div>
        </div>
        <div style="background:rgba(255,255,255,0.03); padding:1rem; border-radius:var(--radius-sm); border:1px solid var(--border-subtle); font-size:0.85rem; color:var(--text-dim);">
          <p>• Nhận phòng: từ 14:00 | Trả phòng: trước 12:00 trưa</p>
          <p>• Miễn phí hủy phòng trước 24 giờ</p>
          <p>• Đã bao gồm thuế GTGT và phí dịch vụ 5 sao</p>
        </div>
      </div>
    `;
    modal.classList.add('active');
  } catch (err) {
    alert('Không thể tải chi tiết phòng');
  }
}

function closeDetailModal() {
  document.getElementById('room-detail-modal').classList.remove('active');
}

// TẢI VÀ RENDER DANH SÁCH BOOKINGS
let searchDebounceTimer;
function debounceBookingSearch() {
  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(loadBookings, 300);
}

async function loadBookings() {
  const tbody = document.getElementById('bookings-table-body');
  const status = document.getElementById('booking-status-select')?.value || 'all';
  const search = document.getElementById('booking-search-input')?.value || '';

  try {
    let url = `/api/bookings?status=${status}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;

    const res = await fetch(url);
    const bookings = await res.json();

    if (!bookings || bookings.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:2rem; color:var(--text-dim);">Không có đơn đặt phòng nào.</td></tr>`;
      return;
    }

    const statusMap = {
      'pending': 'Chờ duyệt',
      'confirmed': 'Đã xác nhận',
      'checked_in': 'Đang ở (Check-in)',
      'completed': 'Đã hoàn tất',
      'cancelled': 'Đã hủy'
    };

    tbody.innerHTML = bookings.map(b => `
      <tr>
        <td><span class="booking-code">${b.booking_code}</span></td>
        <td>
          <strong style="color:var(--text-main);">${b.customer_name}</strong><br>
          <small style="color:var(--text-dim);">${b.customer_phone}</small>
        </td>
        <td>Phòng ${b.room_number} <br><small style="color:var(--text-dim);">${b.room_type}</small></td>
        <td>
          ${new Date(b.check_in_date).toLocaleDateString('vi-VN')} →<br>
          ${new Date(b.check_out_date).toLocaleDateString('vi-VN')}
        </td>
        <td>${b.total_nights} đêm</td>
        <td><strong style="color:var(--gold-primary);">${formatVND(b.total_price)}</strong></td>
        <td><span class="status-pill status-${b.status}">${statusMap[b.status] || b.status}</span></td>
        <td>
          <div style="display:flex; gap:0.35rem;">
            ${b.status === 'confirmed' ? `<button class="btn btn-sm btn-success" onclick="updateBookingStatus(${b.id}, 'checked_in')">Check-in</button>` : ''}
            ${b.status === 'checked_in' ? `<button class="btn btn-sm btn-primary" onclick="updateBookingStatus(${b.id}, 'completed')">Hoàn tất</button>` : ''}
            ${b.status !== 'cancelled' && b.status !== 'completed' ? `<button class="btn btn-sm btn-danger" onclick="updateBookingStatus(${b.id}, 'cancelled')">Hủy</button>` : '<span style="color:var(--text-dim);">-</span>'}
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:var(--danger-color);">Lỗi tải danh sách đặt phòng.</td></tr>`;
  }
}

async function updateBookingStatus(bookingId, newStatus) {
  if (!confirm(`Xác nhận chuyển trạng thái đơn đặt này thành "${newStatus}"?`)) return;

  try {
    const res = await fetch(`/api/bookings/${bookingId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });

    if (res.ok) {
      loadBookings();
      loadStats();
    } else {
      alert('Không thể cập nhật trạng thái');
    }
  } catch (err) {
    alert('Lỗi kết nối máy chủ');
  }
}

// TẢI VÀ RENDER DANH SÁCH KHÁCH HÀNG
async function loadCustomers() {
  const tbody = document.getElementById('customers-table-body');
  try {
    const res = await fetch('/api/customers');
    const customers = await res.json();

    if (!customers || customers.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:2rem; color:var(--text-dim);">Chưa có dữ liệu khách hàng.</td></tr>`;
      return;
    }

    tbody.innerHTML = customers.map(c => `
      <tr>
        <td><strong>#KH-${String(c.id).padStart(4, '0')}</strong></td>
        <td style="color:var(--text-main); font-weight:600;">${c.full_name}</td>
        <td>${c.email}</td>
        <td>${c.phone}</td>
        <td>${c.id_card}</td>
        <td>${c.address || 'Chưa cập nhật'}</td>
        <td><strong style="color:var(--accent-blue);">${c.total_bookings} lượt</strong></td>
        <td><strong style="color:var(--gold-primary);">${formatVND(c.total_spent)}</strong></td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:var(--danger-color);">Lỗi tải khách hàng.</td></tr>`;
  }
}
