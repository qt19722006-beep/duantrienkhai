-- ==========================================================
-- ĐỀ SỐ 6: HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN
-- 01_init_schema.sql: Khởi tạo Schema và Phân quyền Bảo mật (Hardening)
-- ==========================================================

-- Tạo user ứng dụng chuyên dụng với nguyên tắc Least Privilege (không dùng root postgres)
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'hotel_user') THEN
      CREATE ROLE hotel_user WITH LOGIN PASSWORD 'HotelApp_SecPass2026!#';
   END IF;
END
$do$;

-- Cấp quyền kết nối đến database hotel_db
GRANT CONNECT ON DATABASE hotel_db TO hotel_user;

-- Tạo schema riêng biệt cho ứng dụng
CREATE SCHEMA IF NOT EXISTS hotel;

-- Thiết lập search path mặc định
SET search_path TO hotel, public;

-- Cấp quyền sử dụng schema cho user ứng dụng
GRANT USAGE, CREATE ON SCHEMA hotel TO hotel_user;

-- 1. BẢNG PHÒNG KHÁCH SẠN (ROOMS)
CREATE TABLE IF NOT EXISTS hotel.rooms (
    id SERIAL PRIMARY KEY,
    room_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    type VARCHAR(50) NOT NULL,
    price_per_night NUMERIC(12, 2) NOT NULL CHECK (price_per_night > 0),
    max_guests INT NOT NULL DEFAULT 2 CHECK (max_guests > 0),
    bed_type VARCHAR(50) NOT NULL,
    size_sqm INT NOT NULL DEFAULT 30,
    image_url TEXT NOT NULL,
    description TEXT,
    amenities JSONB DEFAULT '[]'::jsonb,
    status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'occupied', 'maintenance')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. BẢNG KHÁCH HÀNG (CUSTOMERS)
CREATE TABLE IF NOT EXISTS hotel.customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(25) NOT NULL,
    id_card VARCHAR(30) NOT NULL,
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. BẢNG ĐẶT PHÒNG (BOOKINGS)
CREATE TABLE IF NOT EXISTS hotel.bookings (
    id SERIAL PRIMARY KEY,
    booking_code VARCHAR(35) UNIQUE NOT NULL,
    customer_id INT NOT NULL REFERENCES hotel.customers(id) ON DELETE CASCADE,
    room_id INT NOT NULL REFERENCES hotel.rooms(id) ON DELETE RESTRICT,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_guests INT NOT NULL DEFAULT 1 CHECK (total_guests > 0),
    total_nights INT NOT NULL CHECK (total_nights > 0),
    total_price NUMERIC(12, 2) NOT NULL CHECK (total_price >= 0),
    status VARCHAR(25) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'checked_in', 'completed', 'cancelled')),
    special_requests TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_dates CHECK (check_out_date > check_in_date)
);

-- Tạo Index để tối ưu hiệu năng truy vấn và báo cáo
CREATE INDEX IF NOT EXISTS idx_rooms_status ON hotel.rooms(status);
CREATE INDEX IF NOT EXISTS idx_rooms_type ON hotel.rooms(type);
CREATE INDEX IF NOT EXISTS idx_bookings_code ON hotel.bookings(booking_code);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON hotel.bookings(status);
CREATE INDEX IF NOT EXISTS idx_bookings_dates ON hotel.bookings(check_in_date, check_out_date);
CREATE INDEX IF NOT EXISTS idx_customers_phone ON hotel.customers(phone);

-- CẤP QUYỀN HẠN CHẾ (LEAST PRIVILEGE) CHO hotel_user
-- Chỉ cho phép thực hiện DML (SELECT, INSERT, UPDATE, DELETE), KHÔNG cấp quyền DDL (DROP, TRUNCATE)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA hotel TO hotel_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA hotel TO hotel_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA hotel 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO hotel_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA hotel 
GRANT USAGE, SELECT ON SEQUENCES TO hotel_user;
