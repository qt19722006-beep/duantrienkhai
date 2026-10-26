-- ==========================================================
-- ĐỀ SỐ 6: HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN
-- 02_seed_data.sql: Dữ liệu mẫu thực tế cho phòng, khách hàng và đặt chỗ
-- ==========================================================

SET search_path TO hotel, public;

-- Dữ liệu 8 phòng khách sạn từ Standard đến Luxury Penthouse
INSERT INTO hotel.rooms (room_number, name, type, price_per_night, max_guests, bed_type, size_sqm, image_url, description, amenities, status)
VALUES
(
    '101', 
    'Standard King City View', 
    'Standard', 
    850000, 
    2, 
    '1 Giường King', 
    32, 
    'https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=800&q=80', 
    'Phòng tiêu chuẩn ấm cúng, tầm nhìn hướng phố nhộn nhịp, trang bị đầy đủ tiện nghi hiện đại cho kỳ nghỉ tiện lợi.', 
    '["Wifi tốc độ cao", "Điều hòa 2 chiều", "TV 50 inch 4K", "Bàn làm việc", "Minibar", "Máy sấy tóc"]'::jsonb, 
    'available'
),
(
    '102', 
    'Superior Twin Garden', 
    'Superior', 
    1150000, 
    2, 
    '2 Giường Đơn', 
    36, 
    'https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80', 
    'Phòng Superior không gian thoáng đãng ngắm trọn khu vườn nhiệt đới xanh mát, phù hợp cho bạn bè hoặc công tác.', 
    '["Wifi tốc độ cao", "Ban công riêng", "Két an toàn", "Trà & Cà phê miễn phí", "Vòi sen đứng cao cấp"]'::jsonb, 
    'available'
),
(
    '201', 
    'Deluxe Ocean View Balcony', 
    'Deluxe', 
    1850000, 
    2, 
    '1 Giường Super King', 
    45, 
    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80', 
    'Phòng Deluxe hướng biển trực diện với ban công rộng rãi đón hoàng hôn lãng mạn, trang bị bồn tắm nằm thư giãn.', 
    '["Ban công hướng biển", "Bồn tắm nằm", "Ăn sáng buffet miễn phí", "Smart TV 55 inch", "Minibar cao cấp", "Áo choàng lụa"]'::jsonb, 
    'available'
),
(
    '202', 
    'Executive Seafront Suite', 
    'Suite', 
    2650000, 
    3, 
    '1 Giường King + 1 Sofa Bed', 
    58, 
    'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=800&q=80', 
    'Hạng Suite đẳng cấp có phòng khách riêng biệt, quầy bar mini và view biển 180 độ tuyệt mỹ.', 
    '["Phòng khách riêng", "Bồn tắm sục Jacuzzi", "Đặc quyền Executive Lounge", "Check-in ưu tiên", "Dịch vụ phòng 24/7"]'::jsonb, 
    'occupied'
),
(
    '301', 
    'Grand Family Panorama', 
    'Family', 
    3200000, 
    4, 
    '2 Giường Queen Size', 
    65, 
    'https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=800&q=80', 
    'Căn hộ gia đình sang trọng với không gian sinh hoạt chung rộng rãi, bếp phụ và tầm nhìn toàn cảnh thành phố.', 
    '["2 Phòng ngủ tiện nghi", "Bếp nhỏ & Lò vi sóng", "Bàn ăn gia đình", "Máy pha cà phê Nespresso", "Khu vui chơi trẻ em"]'::jsonb, 
    'available'
),
(
    '302', 
    'Presidential Royal Penthouse', 
    'Presidential', 
    7500000, 
    4, 
    '2 Giường Emperor', 
    120, 
    'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=800&q=80', 
    'Dinh thự hoàng gia trên tầng cao nhất với hồ bơi vô cực mini riêng biệt, quản gia riêng và nội thất dát vàng.', 
    '["Hồ bơi riêng", "Quản gia 24/7", "Đưa đón sân bay Limousine", "Hầm rượu cá nhân", "Hệ thống âm thanh Hi-End Bose"]'::jsonb, 
    'available'
),
(
    '401', 
    'Romantic Honeymoon Villa', 
    'Bungalow', 
    2900000, 
    2, 
    '1 Giường tròn Luxury', 
    55, 
    'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=800&q=80', 
    'Bungalow biệt lập giữa vườn hoa dành cho các cặp đôi tận hưởng kỳ trăng mật ngọt ngào với nến, hoa và rượu vang.', 
    '["Sân vườn riêng", "Bồn tắm lộ thiên", "Rượu vang & Chocolate chào mừng", "Set nến lãng mạn", "Bữa sáng nổi tại hồ"]'::jsonb, 
    'available'
),
(
    '402', 
    'Eco Forest Loft', 
    'Superior', 
    1350000, 
    2, 
    '1 Giường Queen Gỗ Mộc', 
    40, 
    'https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?auto=format&fit=crop&w=800&q=80', 
    'Thiết kế phong cách Rustic thân thiện môi trường, trần nhà cao, ngập tràn ánh sáng tự nhiên từ giếng trời.', 
    '["Tinh dầu thiên nhiên", "Ban công ngắm rừng thông", "Vật liệu gỗ tái sinh", "Cửa sổ Panorama", "Trà thảo mộc hữu cơ"]'::jsonb, 
    'maintenance'
)
ON CONFLICT (room_number) DO NOTHING;

-- Dữ liệu khách hàng mẫu
INSERT INTO hotel.customers (id, full_name, email, phone, id_card, address)
VALUES
(1, 'Nguyễn Văn An', 'an.nguyen@gmail.com', '0912345678', '001200012345', '128 Cầu Giấy, Hà Nội'),
(2, 'Trần Thị Mai', 'mai.tran@yahoo.com', '0987654321', '079201004567', '45 Lê Duẩn, Quận 1, TP. Hồ Chí Minh'),
(3, 'Lê Hoàng Nam', 'nam.le@outlook.com', '0905123789', '048202008899', '88 Bạch Đằng, Hải Châu, Đà Nẵng'),
(4, 'Phạm Quỳnh Anh', 'quynhanh.pham@gmail.com', '0934567890', '036203001122', '15 Trần Phú, Nha Trang'),
(5, 'Đỗ Minh Tuấn', 'tuan.do@company.vn', '0978901234', '001201005544', '202 Hoàng Hoa Thám, Ba Đình, Hà Nội')
ON CONFLICT (id) DO NOTHING;

SELECT setval('hotel.customers_id_seq', (SELECT MAX(id) FROM hotel.customers));

-- Dữ liệu đặt phòng mẫu
INSERT INTO hotel.bookings (booking_code, customer_id, room_id, check_in_date, check_out_date, total_guests, total_nights, total_price, status, special_requests)
VALUES
(
    'BK-20261026-001', 
    1, 
    3, 
    CURRENT_DATE + INTERVAL '1 day', 
    CURRENT_DATE + INTERVAL '4 days', 
    2, 
    3, 
    5550000, 
    'confirmed', 
    'Yêu cầu phòng tầng cao, giường đôi không ghép'
),
(
    'BK-20261026-002', 
    2, 
    4, 
    CURRENT_DATE, 
    CURRENT_DATE + INTERVAL '2 days', 
    2, 
    2, 
    5300000, 
    'checked_in', 
    'Check-in sớm lúc 11h sáng'
),
(
    'BK-20261026-003', 
    3, 
    1, 
    CURRENT_DATE + INTERVAL '5 days', 
    CURRENT_DATE + INTERVAL '7 days', 
    1, 
    2, 
    1700000, 
    'pending', 
    'Cần xuất hóa đơn VAT điện tử cho công ty'
),
(
    'BK-20261026-004', 
    4, 
    7, 
    CURRENT_DATE + INTERVAL '10 days', 
    CURRENT_DATE + INTERVAL '13 days', 
    2, 
    3, 
    8700000, 
    'confirmed', 
    'Setup phòng kỷ niệm ngày cưới (hoa hồng và nến)'
),
(
    'BK-20261026-005', 
    5, 
    5, 
    CURRENT_DATE - INTERVAL '5 days', 
    CURRENT_DATE - INTERVAL '2 days', 
    4, 
    3, 
    9600000, 
    'completed', 
    'Gia đình có 2 bé nhỏ, cần thêm 2 bộ chăn gối'
),
(
    'BK-20261026-006', 
    1, 
    2, 
    CURRENT_DATE - INTERVAL '10 days', 
    CURRENT_DATE - INTERVAL '8 days', 
    2, 
    2, 
    2300000, 
    'cancelled', 
    'Khách bận lịch công tác đột xuất xin dời ngày'
)
ON CONFLICT (booking_code) DO NOTHING;
