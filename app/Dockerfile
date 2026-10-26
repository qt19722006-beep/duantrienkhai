# ==========================================================
# ĐỀ SỐ 6: HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN
# Dockerfile: Ứng dụng Node.js với cơ chế Hardening (Non-root user)
# ==========================================================

FROM node:20-alpine AS builder

WORKDIR /app

# Cài đặt dependencies
COPY package*.json ./
RUN npm install --omit=dev --no-audit

# Runtime Stage
FROM node:20-alpine

WORKDIR /app

# Biện pháp Hardening: Tạo non-root user và group chuyên dụng
RUN addgroup -g 10001 -S hotelgroup && \
    adduser -u 10001 -S hoteluser -G hotelgroup

# Copy dependencies từ builder
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
COPY server.js ./
COPY db.js ./
COPY logger.js ./
COPY metrics.js ./
COPY public ./public

# Tạo thư mục log và phân quyền cho non-root user
RUN mkdir -p /app/logs && \
    chown -R hoteluser:hotelgroup /app

# Chuyển sang user không có đặc quyền root
USER hoteluser

# Khai báo cổng
EXPOSE 3000

# Healthcheck nội bộ container
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/health || exit 1

# Khởi chạy server
CMD ["node", "server.js"]
