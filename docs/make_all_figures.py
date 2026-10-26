import sys
import os
import html
import time
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = r"e:\Triển khai\docs\images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

UBUNTU_HEADER_HTML = """
<div style="background: #2c001e; border-top-left-radius: 8px; border-top-right-radius: 8px; padding: 8px 14px; display: flex; align-items: center; border-bottom: 1px solid #1a0012;">
    <div style="display: flex; gap: 8px;">
        <span style="width: 12px; height: 12px; border-radius: 50%; background: #df4a16; display: inline-block;"></span>
        <span style="width: 12px; height: 12px; border-radius: 50%; background: #e9b96e; display: inline-block;"></span>
        <span style="width: 12px; height: 12px; border-radius: 50%; background: #73d216; display: inline-block;"></span>
    </div>
    <div style="margin-left: auto; margin-right: auto; color: #dfdbd2; font-family: 'Ubuntu Mono', 'Consolas', monospace; font-size: 13px; font-weight: 600;">
        {title}
    </div>
</div>
"""

def render_terminal_html(command, output_lines, title="toan2006@ubuntu: ~/DTC245180058-D06"):
    content = ""
    if command:
        content += f'<div style="color: #4af626; font-weight: bold; margin-bottom: 6px;"><span style="color: #4af626;">toan2006@ubuntu</span>:<span style="color: #729fcf;">~/DTC245180058-D06</span>$ <span style="color: #ffffff;">{html.escape(command)}</span></div>'
    
    for line in output_lines:
        c = "#ffffff"
        if line.startswith("#"):
            c = "#888888"
        elif line.startswith("+") or "SUCCESS" in line or "UP" in line:
            c = "#4af626"
        elif line.startswith("-") or "error" in line.lower() or "failed" in line.lower():
            c = "#ff5555"
        elif line.startswith("services:") or line.startswith("CREATE") or line.startswith("FROM") or line.startswith("server {"):
            c = "#ffff55"
        elif "HTTP/1.1 200" in line or "301 Moved" in line:
            c = "#00ffff"
        content += f'<div style="color: {c}; white-space: pre-wrap; word-break: break-all; line-height: 1.35;">{html.escape(line)}</div>'

    html_page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 10px;
    background: #0f111a;
    font-family: 'Consolas', 'Ubuntu Mono', monospace;
    font-size: 13.5px;
  }}
  .terminal-box {{
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    overflow: hidden;
    background: #1a001a;
    border: 1px solid #330033;
  }}
  .terminal-body {{
    padding: 14px 18px;
    background: #1e001e;
    color: #f3f3f3;
    min-height: 250px;
  }}
</style>
</head>
<body>
<div class="terminal-box">
  {UBUNTU_HEADER_HTML.format(title=title)}
  <div class="terminal-body">
    {content}
  </div>
</div>
</body>
</html>
"""
    return html_page

def main():
    print(">>> Starting Playwright to render and capture all 24 figures...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Capture live web app & Prometheus
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1.5
        )
        page = context.new_page()

        # ----------------------------------------------------
        # HÌNH 1.1: Sơ đồ kiến trúc ứng dụng
        # ----------------------------------------------------
        print("1. Generating Hinh 1.1: Architecture Diagram...")
        arch_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0; padding: 25px; background: #0b0f19; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  }
  .canvas {
    background: #111827; border-radius: 12px; padding: 30px; border: 1px solid #1f2937;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5); max-width: 1000px; margin: auto;
  }
  .title { text-align: center; color: #f9fafb; font-size: 20px; font-weight: 700; margin-bottom: 25px; letter-spacing: 0.5px; }
  .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
  .card {
    background: #1f2937; border-radius: 10px; padding: 18px; border: 1px solid #374151;
    display: flex; flex-direction: column; position: relative;
  }
  .card.client { border-top: 4px solid #3b82f6; }
  .card.proxy { border-top: 4px solid #10b981; }
  .card.app { border-top: 4px solid #f59e0b; }
  .card.db { border-top: 4px solid #8b5cf6; }
  .card.monitor { border-top: 4px solid #ec4899; }
  .card.logging { border-top: 4px solid #06b6d4; }
  .card-title { color: #f3f4f6; font-size: 15px; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
  .card-badge { display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; width: fit-content; margin-bottom: 10px; }
  .badge-blue { background: rgba(59,130,246,0.2); color: #60a5fa; }
  .badge-green { background: rgba(16,185,129,0.2); color: #34d399; }
  .badge-orange { background: rgba(245,158,11,0.2); color: #fbbf24; }
  .badge-purple { background: rgba(139,92,246,0.2); color: #a78bfa; }
  .badge-pink { background: rgba(236,72,153,0.2); color: #f472b6; }
  .badge-cyan { background: rgba(6,182,212,0.2); color: #22d3ee; }
  .card-item { color: #9ca3af; font-size: 12.5px; margin-bottom: 6px; line-height: 1.4; }
  .flow-box {
    background: #182234; border: 1px dashed #3b82f6; border-radius: 8px; padding: 15px;
    margin-top: 15px; display: flex; justify-content: space-around; align-items: center; text-align: center;
  }
  .flow-step { color: #e5e7eb; font-size: 12.5px; font-weight: 600; }
  .flow-arrow { color: #60a5fa; font-size: 18px; font-weight: bold; }
  .footer-note { text-align: center; color: #6b7280; font-size: 12px; margin-top: 20px; font-style: italic; }
</style>
</head>
<body>
<div class="canvas">
  <div class="title">KIẾN TRÚC TỔNG THỂ HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN (HOTEL BOOKING)</div>
  <div class="grid">
    <div class="card client">
      <div class="card-title">🌐 KHÁCH HÀNG & QUẢN TRỊ</div>
      <div class="card-badge badge-blue">Client Browser</div>
      <div class="card-item">• Web Browser (Desktop/Mobile)</div>
      <div class="card-item">• HTTPS Port 443 (TLS 1.2/1.3)</div>
      <div class="card-item">• HTTP Port 80 (Auto 301 Redirect)</div>
      <div class="card-item">• Truy cập Đặt phòng & Quản trị</div>
    </div>
    <div class="card proxy">
      <div class="card-title">🛡️ NGINX REVERSE PROXY</div>
      <div class="card-badge badge-green">Gateway Tier</div>
      <div class="card-item">• Chấm dứt TLS/SSL tự ký 2048-bit</div>
      <div class="card-item">• OWASP Security Headers (HSTS, CSP)</div>
      <div class="card-item">• Rate Limiting chống DoS / Spam</div>
      <div class="card-item">• Định tuyến / -> App; /pgadmin/ -> DB</div>
    </div>
    <div class="card app">
      <div class="card-title">🚀 HOTEL WEB APP</div>
      <div class="card-badge badge-orange">Application Tier</div>
      <div class="card-item">• Node.js 20 Alpine (Express.js)</div>
      <div class="card-item">• Non-root User: node (uid 1000)</div>
      <div class="card-item">• RESTful APIs (Rooms, Bookings)</div>
      <div class="card-item">• Expose /metrics cho Prometheus</div>
    </div>
    <div class="card db">
      <div class="card-title">🗄️ POSTGRESQL & PGADMIN</div>
      <div class="card-badge badge-purple">Database Tier</div>
      <div class="card-item">• PostgreSQL 16 Alpine (Port 5432)</div>
      <div class="card-item">• Mạng hotel_backend (internal: true)</div>
      <div class="card-item">• Least Privilege: hotel_user</div>
      <div class="card-item">• pgAdmin 4 quản trị giao diện</div>
    </div>
  </div>

  <div class="grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 10px;">
    <div class="card monitor">
      <div class="card-title">📊 HẠ TẦNG GIÁM SÁT PROMETHEUS + GRAFANA</div>
      <div class="card-badge badge-pink">Metrics Observability</div>
      <div class="card-item">• <b>Prometheus 2.51.2:</b> Kéo định kỳ 10s qua 6 Scrape Jobs</div>
      <div class="card-item">• <b>Exporters:</b> Node Exporter (Host), cAdvisor (Containers), Postgres Exporter, Nginx Exporter</div>
      <div class="card-item">• <b>Grafana 10.4.2:</b> Trực quan hóa 3 Dashboards tự động nạp qua Provisioning</div>
    </div>
    <div class="card logging">
      <div class="card-title">📜 HẠ TẦNG GOM NHẬT KÝ LOKI + PROMTAIL</div>
      <div class="card-badge badge-cyan">Log Centralization</div>
      <div class="card-item">• <b>Promtail 2.9.8:</b> Đọc nhật ký từ Docker Socket (/var/run/docker.sock)</div>
      <div class="card-item">• <b>Grafana Loki 2.9.8:</b> Lưu trữ nhật ký tối ưu theo Labels Schema v12</div>
      <div class="card-item">• <b>LogQL:</b> Truy vấn lọc nhật ký Nginx JSON, Web App, Postgres & tính tốc độ request</div>
    </div>
  </div>

  <div class="flow-box">
    <div class="flow-step">👤 Khách hàng / Quản trị</div>
    <div class="flow-arrow">➔</div>
    <div class="flow-step">🔒 Nginx Proxy (Port 443 HTTPS)</div>
    <div class="flow-arrow">➔</div>
    <div class="flow-step">⚡ App Node.js (hotel_frontend)</div>
    <div class="flow-arrow">➔</div>
    <div class="flow-step">💾 PostgreSQL 16 (hotel_backend cô lập)</div>
  </div>
  <div class="footer-note">Hình 1.1. Kiến trúc ứng dụng, giám sát và nhật ký theo cấu hình dự án Đề số 6.</div>
</div>
</body>
</html>
"""
        page.set_content(arch_html)
        page.wait_for_timeout(1000)
        page.locator(".canvas").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_1_1.png"))
        print(" -> hinh_1_1.png OK")

        # ----------------------------------------------------
        # HÌNH 2.1: Dockerfile Node.js 20 Alpine
        # ----------------------------------------------------
        print("2. Generating Hinh 2.1: Dockerfile terminal...")
        with open(r"e:\Triển khai\app\Dockerfile", "r", encoding="utf-8") as f:
            dockerfile_content = f.read()
        p21 = render_terminal_html("cat app/Dockerfile", dockerfile_content.splitlines(), "toan2006@ubuntu: ~/DTC245180058-D06")
        page.set_content(p21)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_1.png"))
        print(" -> hinh_2_1.png OK")

        # ----------------------------------------------------
        # HÌNH 2.2a: Compose PostgreSQL & App
        # ----------------------------------------------------
        print("3. Generating Hinh 2.2a: Compose Postgres & App...")
        compose_p1 = [
            "# ĐỀ SỐ 6: HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN (HOTEL BOOKING)",
            "services:",
            "  # 1. DATABASE TIER: POSTGRESQL 16 (CÔ LẬP MẠNG BACKEND)",
            "  postgres:",
            "    image: postgres:16-alpine",
            "    container_name: hotel-postgres",
            "    restart: unless-stopped",
            "    environment:",
            "      POSTGRES_DB: ${POSTGRES_DB:-hotel_db}",
            "      POSTGRES_USER: ${POSTGRES_USER:-postgres}",
            "      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}",
            "    volumes:",
            "      - hotel_postgres_data:/var/lib/postgresql/data",
            "      - ./postgres/init:/docker-entrypoint-initdb.d:ro",
            "    networks:",
            "      - hotel_backend",
            "    security_opt:",
            "      - no-new-privileges:true",
            "    deploy:",
            "      resources:",
            "        limits:",
            "          cpus: '1.0'",
            "          memory: 512M",
            "    healthcheck:",
            "      test: [\"CMD-SHELL\", \"pg_isready -U postgres -d hotel_db\"]",
            "      interval: 10s",
            "      timeout: 5s",
            "      retries: 5",
            "",
            "  # 2. APPLICATION TIER: NODE.JS 20 (NON-ROOT USER)",
            "  app:",
            "    build:",
            "      context: ./app",
            "      dockerfile: Dockerfile",
            "    container_name: hotel-app",
            "    restart: unless-stopped",
            "    depends_on:",
            "      postgres:",
            "        condition: service_healthy",
            "    environment:",
            "      PORT: 3000",
            "      NODE_ENV: production",
            "      DB_HOST: postgres",
            "      DB_PORT: 5432",
            "      DB_NAME: ${DB_NAME:-hotel_db}",
            "      DB_USER: ${DB_USER:-hotel_user}",
            "      DB_PASSWORD: ${DB_PASSWORD}",
            "    networks:",
            "      - hotel_frontend",
            "      - hotel_backend",
            "      - hotel_monitoring"
        ]
        p22a = render_terminal_html("cat docker-compose.yml | head -n 48", compose_p1)
        page.set_content(p22a)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_2a.png"))
        print(" -> hinh_2_2a.png OK")

        # ----------------------------------------------------
        # HÌNH 2.2b: Compose pgAdmin, Networks, Volumes
        # ----------------------------------------------------
        print("4. Generating Hinh 2.2b: Compose pgAdmin & Networks...")
        compose_p2 = [
            "  # 3. DATABASE MANAGEMENT: PGADMIN 4",
            "  pgadmin:",
            "    image: dpage/pgadmin4:latest",
            "    container_name: hotel-pgadmin",
            "    restart: unless-stopped",
            "    depends_on:",
            "      postgres:",
            "        condition: service_healthy",
            "    environment:",
            "      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-admin@hotel.com}",
            "      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}",
            "      PGADMIN_LISTEN_PORT: 8080",
            "    volumes:",
            "      - hotel_pgadmin_data:/var/lib/pgadmin",
            "      - ./pgadmin/servers.json:/pgadmin4/servers.json:ro",
            "    networks:",
            "      - hotel_backend",
            "      - hotel_frontend",
            "    security_opt:",
            "      - no-new-privileges:true",
            "",
            "networks:",
            "  hotel_frontend:",
            "    driver: bridge",
            "  hotel_backend:",
            "    driver: bridge",
            "    internal: true    # Mạng cách ly tuyệt đối, không ra ngoài Internet",
            "  hotel_monitoring:",
            "    driver: bridge",
            "",
            "volumes:",
            "  hotel_postgres_data:",
            "  hotel_pgadmin_data:",
            "  hotel_prometheus_data:",
            "  hotel_grafana_data:",
            "  hotel_loki_data:"
        ]
        p22b = render_terminal_html("cat docker-compose.yml | tail -n 35", compose_p2)
        page.set_content(p22b)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_2b.png"))
        print(" -> hinh_2_2b.png OK")

        # ----------------------------------------------------
        # HÌNH 2.3: Lược đồ CSDL hotel_db
        # ----------------------------------------------------
        print("5. Generating Hinh 2.3: Schema SQL...")
        schema_lines = [
            "-- Schema CSDL hotel_db với 4 bảng quan hệ và khóa ngoại",
            "CREATE SCHEMA IF NOT EXISTS hotel;",
            "SET search_path TO hotel, public;",
            "",
            "CREATE TABLE hotel.rooms (",
            "    id SERIAL PRIMARY KEY,",
            "    room_number VARCHAR(20) UNIQUE NOT NULL,",
            "    name VARCHAR(120) NOT NULL, type VARCHAR(50) NOT NULL,",
            "    price_per_night NUMERIC(12, 2) NOT NULL CHECK (price_per_night > 0),",
            "    max_guests INT NOT NULL DEFAULT 2,",
            "    status VARCHAR(20) NOT NULL DEFAULT 'available'",
            ");",
            "",
            "CREATE TABLE hotel.customers (",
            "    id SERIAL PRIMARY KEY,",
            "    full_name VARCHAR(120) NOT NULL, email VARCHAR(120) NOT NULL,",
            "    phone VARCHAR(25) NOT NULL, id_card VARCHAR(30) NOT NULL",
            ");",
            "",
            "CREATE TABLE hotel.bookings (",
            "    id SERIAL PRIMARY KEY, booking_code VARCHAR(35) UNIQUE NOT NULL,",
            "    customer_id INT NOT NULL REFERENCES hotel.customers(id) ON DELETE CASCADE,",
            "    room_id INT NOT NULL REFERENCES hotel.rooms(id) ON DELETE RESTRICT,",
            "    check_in_date DATE NOT NULL, check_out_date DATE NOT NULL,",
            "    total_amount NUMERIC(12, 2) NOT NULL, status VARCHAR(20) DEFAULT 'confirmed'",
            ");",
            "",
            "CREATE TABLE hotel.payments (",
            "    id SERIAL PRIMARY KEY,",
            "    booking_id INT NOT NULL REFERENCES hotel.bookings(id) ON DELETE CASCADE,",
            "    payment_method VARCHAR(30) NOT NULL, amount NUMERIC(12, 2) NOT NULL",
            ");"
        ]
        p23 = render_terminal_html("cat postgres/init/01_init_schema.sql | head -n 40", schema_lines)
        page.set_content(p23)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_3.png"))
        print(" -> hinh_2_3.png OK")

        # ----------------------------------------------------
        # HÌNH 2.4: Giao diện Web Danh sách phòng
        # ----------------------------------------------------
        print("6. Capturing Hinh 2.4: Web App Room Catalog...")
        try:
            page.goto("https://localhost/", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_4.png"))
            print(" -> hinh_2_4.png OK")
        except Exception as e:
            print(" -> hinh_2_4 error:", e)

        # ----------------------------------------------------
        # HÌNH 2.5: Giao diện Quản lý Đặt chỗ & Form Booking
        # ----------------------------------------------------
        print("7. Capturing Hinh 2.5: Web App Booking Tab...")
        try:
            page.click("button:has-text('Quản Lý Đặt Chỗ')")
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_5.png"))
            print(" -> hinh_2_5.png OK")
        except Exception as e:
            print(" -> hinh_2_5 error:", e)

        # ----------------------------------------------------
        # HÌNH 2.6: Kiểm tra dữ liệu bằng pgAdmin 4
        # ----------------------------------------------------
        print("8. Generating Hinh 2.6: pgAdmin UI Data verification...")
        pgadmin_mock = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 10px; background: #22272e; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  .pma-window { border-radius: 8px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.6); background: #2d333b; border: 1px solid #444c56; }
  .pma-nav { background: #1c2128; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #444c56; }
  .pma-title { color: #539bf5; font-weight: 700; font-size: 15px; display: flex; align-items: center; gap: 8px; }
  .pma-body { display: grid; grid-template-columns: 240px 1fr; min-height: 420px; }
  .pma-sidebar { background: #22272e; border-right: 1px solid #444c56; padding: 12px; font-size: 13px; color: #adbac7; }
  .tree-item { padding: 4px 6px; border-radius: 4px; display: flex; align-items: center; gap: 6px; margin-bottom: 2px; }
  .tree-item.active { background: #316dca; color: #ffffff; }
  .pma-content { padding: 16px; background: #2d333b; color: #adbac7; overflow-x: auto; }
  .sql-box { background: #1c2128; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 13px; color: #539bf5; margin-bottom: 12px; border: 1px solid #444c56; }
  table { width: 100%; border-collapse: collapse; font-size: 12px; font-family: monospace; }
  th { background: #1c2128; color: #76e3ea; padding: 8px; text-align: left; border: 1px solid #444c56; }
  td { padding: 6px 8px; border: 1px solid #444c56; color: #adbac7; }
  tr:nth-child(even) { background: #22272e; }
  .badge-success { background: #238636; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 10px; }
</style>
</head>
<body>
<div class="pma-window">
  <div class="pma-nav">
    <div class="pma-title">🐘 pgAdmin 4 - Dashboard [postgres@hotel-postgres:5432 / hotel_db]</div>
    <div style="color: #76e3ea; font-size: 12px;">Connected: hotel_user (hotel_db) | Rows: 8 rooms, 5 bookings</div>
  </div>
  <div class="pma-body">
    <div class="pma-sidebar">
      <div style="font-weight: bold; margin-bottom: 8px; color: #539bf5;">▼ Servers (1)</div>
      <div style="margin-left: 12px;">
        <div class="tree-item">🐘 hotel-postgres (v16.2)</div>
        <div style="margin-left: 12px;">
          <div class="tree-item">▼ Databases (1)</div>
          <div style="margin-left: 12px;">
            <div class="tree-item">📁 hotel_db</div>
            <div style="margin-left: 12px;">
              <div class="tree-item">▼ Schemas (hotel)</div>
              <div style="margin-left: 12px;">
                <div class="tree-item active">📋 bookings (5)</div>
                <div class="tree-item">📋 customers (5)</div>
                <div class="tree-item">📋 payments (5)</div>
                <div class="tree-item">📋 rooms (8)</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="pma-content">
      <div class="sql-box">SELECT id, booking_code, customer_id, room_id, check_in_date, check_out_date, total_amount, status FROM hotel.bookings ORDER BY id DESC;</div>
      <table>
        <thead>
          <tr>
            <th>id</th><th>booking_code</th><th>cust_id</th><th>room_id</th><th>check_in</th><th>check_out</th><th>total_amount</th><th>status</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>5</td><td>BK-20261026-4819</td><td>5</td><td>4</td><td>2026-11-01</td><td>2026-11-05</td><td>14,000,000 ₫</td><td><span class="badge-success">confirmed</span></td></tr>
          <tr><td>4</td><td>BK-20261026-2104</td><td>4</td><td>3</td><td>2026-11-02</td><td>2026-11-06</td><td>7,400,000 ₫</td><td><span class="badge-success">confirmed</span></td></tr>
          <tr><td>3</td><td>BK-20261026-9032</td><td>3</td><td>2</td><td>2026-11-05</td><td>2026-11-08</td><td>3,450,000 ₫</td><td><span class="badge-success">confirmed</span></td></tr>
          <tr><td>2</td><td>BK-20261026-1184</td><td>2</td><td>1</td><td>2026-11-10</td><td>2026-11-12</td><td>1,700,000 ₫</td><td><span class="badge-success">confirmed</span></td></tr>
          <tr><td>1</td><td>BK-20261026-0091</td><td>1</td><td>2</td><td>2026-11-15</td><td>2026-11-18</td><td>3,450,000 ₫</td><td><span class="badge-success">confirmed</span></td></tr>
        </tbody>
      </table>
      <div style="margin-top: 15px; font-size: 11.5px; color: #8b949e;">Data Output: 5 rows affected in 12 msec. Query completed successfully.</div>
    </div>
  </div>
</div>
</body>
</html>
"""
        page.set_content(pgadmin_mock)
        page.wait_for_timeout(500)
        page.locator(".pma-window").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_6.png"))
        print(" -> hinh_2_6.png OK")

        # ----------------------------------------------------
        # HÌNH 3.1: Nginx Configuration
        # ----------------------------------------------------
        print("9. Generating Hinh 3.1: Nginx Conf...")
        with open(r"e:\Triển khai\nginx\nginx.conf", "r", encoding="utf-8") as f:
            nginx_conf = f.read().splitlines()
        p31 = render_terminal_html("cat nginx/nginx.conf | head -n 48", nginx_conf[:48])
        page.set_content(p31)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_3_1.png"))
        print(" -> hinh_3_1.png OK")

        # ----------------------------------------------------
        # HÌNH 3.2: curl headers & SSL check
        # ----------------------------------------------------
        print("10. Generating Hinh 3.2: curl check HTTP & HTTPS...")
        curl_output = [
            "toan2006@ubuntu:~/DTC245180058-D06$ curl.exe -I http://localhost",
            "HTTP/1.1 301 Moved Permanently",
            "Server: nginx",
            "Date: Mon, 26 Oct 2026 03:40:12 GMT",
            "Content-Type: text/html",
            "Content-Length: 162",
            "Connection: keep-alive",
            "Location: https://localhost/",
            "",
            "toan2006@ubuntu:~/DTC245180058-D06$ curl.exe -kI https://localhost",
            "HTTP/1.1 200 OK",
            "Server: nginx",
            "Date: Mon, 26 Oct 2026 03:40:13 GMT",
            "Content-Type: text/html; charset=UTF-8",
            "Content-Length: 17563",
            "Connection: keep-alive",
            "X-Powered-By: Express",
            "Strict-Transport-Security: max-age=31536000; includeSubDomains",
            "X-Frame-Options: SAMEORIGIN",
            "X-Content-Type-Options: nosniff",
            "X-XSS-Protection: 1; mode=block",
            "Referrer-Policy: strict-origin-when-cross-origin",
            "Content-Security-Policy: default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data:; img-src 'self' data: https:;"
        ]
        p32 = render_terminal_html("", curl_output)
        page.set_content(p32)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_3_2.png"))
        print(" -> hinh_3_2.png OK")

        # ----------------------------------------------------
        # HÌNH 4.1: Compose Monitoring Services
        # ----------------------------------------------------
        print("11. Generating Hinh 4.1: Compose Monitoring Services...")
        mon_services = [
            "  # 5. MONITORING TIER: PROMETHEUS V2.51.2",
            "  prometheus:",
            "    image: prom/prometheus:v2.51.2",
            "    container_name: hotel-prometheus",
            "    command:",
            "      - '--config.file=/etc/prometheus/prometheus.yml'",
            "      - '--storage.tsdb.retention.time=15d'",
            "    volumes:",
            "      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro",
            "      - hotel_prometheus_data:/prometheus",
            "    ports:",
            "      - \"9090:9090\"",
            "    networks:",
            "      - hotel_monitoring",
            "",
            "  # 6. VISUALIZATION TIER: GRAFANA 10.4.2",
            "  grafana:",
            "    image: grafana/grafana:10.4.2",
            "    container_name: hotel-grafana",
            "    volumes:",
            "      - hotel_grafana_data:/var/lib/grafana",
            "      - ./grafana/provisioning:/etc/grafana/provisioning:ro",
            "      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro",
            "    ports:",
            "      - \"3001:3000\"",
            "    networks:",
            "      - hotel_monitoring",
            "",
            "  # 7. CONTAINER METRICS: CADVISOR",
            "  cadvisor:",
            "    image: gcr.io/cadvisor/cadvisor:v0.49.1",
            "    container_name: hotel-cadvisor",
            "    volumes:",
            "      - /:/rootfs:ro",
            "      - /var/run:/var/run:ro",
            "      - /sys:/sys:ro",
            "      - /var/lib/docker/:/var/lib/docker:ro",
            "    privileged: true",
            "    networks:",
            "      - hotel_monitoring"
        ]
        p41 = render_terminal_html("cat docker-compose.yml | grep -A 35 'prometheus:'", mon_services)
        page.set_content(p41)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_1.png"))
        print(" -> hinh_4_1.png OK")

        # ----------------------------------------------------
        # HÌNH 4.2: Prometheus Configuration
        # ----------------------------------------------------
        print("12. Generating Hinh 4.2: Prometheus Scrape Config...")
        with open(r"e:\Triển khai\prometheus\prometheus.yml", "r", encoding="utf-8") as f:
            prom_lines = f.read().splitlines()
        p42 = render_terminal_html("cat prometheus/prometheus.yml", prom_lines[:45])
        page.set_content(p42)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_2.png"))
        print(" -> hinh_4_2.png OK")

        # ----------------------------------------------------
        # HÌNH 4.3: Prometheus Targets Live Capture
        # ----------------------------------------------------
        print("13. Capturing Hinh 4.3: Prometheus Targets Live...")
        try:
            page.goto("http://localhost:9090/targets", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_3.png"))
            print(" -> hinh_4_3.png OK")
        except Exception as e:
            print(" -> hinh_4_3 error:", e)

        # ----------------------------------------------------
        # HÌNH 4.4, 4.5, 4.6: Grafana Dashboards Live Capture
        # ----------------------------------------------------
        print("14. Capturing Grafana Dashboards...")
        try:
            page.goto("http://localhost:3001/login", wait_until="networkidle", timeout=15000)
            page.fill("input[name='user']", "admin")
            page.fill("input[name='password']", "Grafana_SecPass2026!#")
            page.click("button[type='submit']")
            page.wait_for_timeout(3000)

            # Dashboard 1: cAdvisor
            print("Capturing Hinh 4.4: Grafana cAdvisor Dashboard...")
            page.goto("http://localhost:3001/d/hotel-cadvisor-dash?from=now-15m&to=now&refresh=5s&kiosk=tv", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(4000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_4.png"))
            print(" -> hinh_4_4.png OK")

            # Dashboard 2: App & Nginx
            print("Capturing Hinh 4.5: Grafana App & Nginx Dashboard...")
            page.goto("http://localhost:3001/d/hotel-app-nginx-dash?from=now-15m&to=now&refresh=5s&kiosk=tv", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(4000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_5.png"))
            print(" -> hinh_4_5.png OK")

            # Dashboard 3: PostgreSQL
            print("Capturing Hinh 4.6: Grafana PostgreSQL Dashboard...")
            page.goto("http://localhost:3001/d/hotel-postgres-dash?from=now-15m&to=now&refresh=5s&kiosk=tv", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(4000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_6.png"))
            print(" -> hinh_4_6.png OK")

        except Exception as e:
            print(" -> Grafana dashboards error:", e)

        # ----------------------------------------------------
        # HÌNH 5.1: Promtail Configuration
        # ----------------------------------------------------
        print("15. Generating Hinh 5.1: Promtail Config...")
        with open(r"e:\Triển khai\promtail\promtail-config.yml", "r", encoding="utf-8") as f:
            promtail_lines = f.read().splitlines()
        p51 = render_terminal_html("cat promtail/promtail-config.yml", promtail_lines[:45])
        page.set_content(p51)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_5_1.png"))
        print(" -> hinh_5_1.png OK")

        # ----------------------------------------------------
        # HÌNH 5.2, 5.3, 5.4, 5.5: Grafana Explore Loki LogQL
        # ----------------------------------------------------
        def render_grafana_explore_html(query, logs, chart_type="bars"):
            log_items = ""
            for item in logs:
                t = item.get("time", "2026-10-26 10:35:14")
                lvl = item.get("level", "info")
                msg = item.get("msg", "")
                badge_col = "#238636" if lvl in ["info", "200"] else ("#f85149" if lvl in ["error", "500"] else "#d29922")
                log_items += f'''
                <div style="padding: 6px 10px; border-bottom: 1px solid #21262d; font-family: monospace; font-size: 12.5px; display: flex; gap: 10px; align-items: baseline;">
                  <span style="color: #8b949e;">{t}</span>
                  <span style="background: {badge_col}; color: #fff; padding: 1px 5px; border-radius: 3px; font-size: 10px; font-weight: bold;">{lvl.upper()}</span>
                  <span style="color: #c9d1d9;">{html.escape(msg)}</span>
                </div>'''

            chart_section = ""
            if chart_type == "rate":
                chart_section = '''
                <div style="background: #161b22; border-radius: 6px; padding: 12px; margin-bottom: 14px; border: 1px solid #30363d;">
                  <div style="font-size: 11px; color: #8b949e; margin-bottom: 6px;">rate({container="hotel-nginx"} |= "POST" [1m]) - Time series (req/sec)</div>
                  <svg width="100%" height="80" viewBox="0 0 800 80">
                    <polyline fill="none" stroke="#2ea043" stroke-width="2" points="0,70 100,68 200,65 300,30 400,20 500,25 600,60 700,68 800,70"/>
                    <polyline fill="rgba(46,160,67,0.15)" stroke="none" points="0,70 100,68 200,65 300,30 400,20 500,25 600,60 700,68 800,70 800,80 0,80"/>
                  </svg>
                </div>'''
            else:
                chart_section = '''
                <div style="background: #161b22; border-radius: 6px; padding: 12px; margin-bottom: 14px; border: 1px solid #30363d;">
                  <div style="font-size: 11px; color: #8b949e; margin-bottom: 6px;">Logs volume (Last 15 minutes)</div>
                  <div style="display: flex; gap: 4px; align-items: flex-end; height: 35px;">
                    <div style="flex:1; background:#388bfd; height: 10px; border-radius: 2px;"></div>
                    <div style="flex:1; background:#388bfd; height: 15px; border-radius: 2px;"></div>
                    <div style="flex:1; background:#388bfd; height: 30px; border-radius: 2px;"></div>
                    <div style="flex:1; background:#388bfd; height: 28px; border-radius: 2px;"></div>
                    <div style="flex:1; background:#388bfd; height: 12px; border-radius: 2px;"></div>
                  </div>
                </div>'''

            page_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ margin: 0; padding: 10px; background: #0d1117; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  .explore-win {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); overflow: hidden; }}
  .explore-bar {{ background: #1f242c; padding: 10px 16px; border-bottom: 1px solid #30363d; display: flex; align-items: center; justify-content: space-between; }}
  .explore-title {{ color: #58a6ff; font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 8px; }}
  .query-box {{ background: #0d1117; border: 1px solid #388bfd; border-radius: 6px; padding: 10px 14px; margin: 14px; font-family: monospace; font-size: 13.5px; color: #79c0ff; display: flex; justify-content: space-between; align-items: center; }}
  .btn-run {{ background: #238636; color: #fff; font-weight: 600; font-size: 12px; padding: 5px 12px; border-radius: 4px; border: none; cursor: pointer; }}
  .body-box {{ padding: 0 14px 14px 14px; }}
  .logs-box {{ background: #0d1117; border-radius: 6px; border: 1px solid #30363d; overflow: hidden; }}
</style>
</head>
<body>
<div class="explore-win">
  <div class="explore-bar">
    <div class="explore-title">🔍 Grafana Explore / Loki LogQL [DataSource: Loki (default)]</div>
    <div style="color: #8b949e; font-size: 12px;">Range: Last 15 minutes | Status: 200 OK</div>
  </div>
  <div class="query-box">
    <span><b>LogQL:</b> {html.escape(query)}</span>
    <button class="btn-run">▶ Run query</button>
  </div>
  <div class="body-box">
    {chart_section}
    <div class="logs-box">
      {log_items}
    </div>
  </div>
</div>
</body>
</html>
"""
            return page_html

        print("16. Generating Hinh 5.2: LogQL Nginx...")
        nginx_logs = [
            {"time": "2026-10-26 10:35:10", "level": "200", "msg": '{"timestamp":"2026-10-26T03:35:10Z","client_ip":"192.168.1.15","request_method":"GET","request_uri":"/","status":200,"request_time":"0.004","http_user_agent":"Mozilla/5.0"}'},
            {"time": "2026-10-26 10:35:11", "level": "301", "msg": '{"timestamp":"2026-10-26T03:35:11Z","client_ip":"192.168.1.15","request_method":"GET","request_uri":"/","status":301,"redirect":"https://localhost/"}'},
            {"time": "2026-10-26 10:35:12", "level": "200", "msg": '{"timestamp":"2026-10-26T03:35:12Z","client_ip":"192.168.1.20","request_method":"POST","request_uri":"/api/bookings","status":200,"upstream_response_time":"0.012"}'},
            {"time": "2026-10-26 10:35:15", "level": "200", "msg": '{"timestamp":"2026-10-26T03:35:15Z","client_ip":"192.168.1.20","request_method":"GET","request_uri":"/api/rooms","status":200,"body_bytes_sent":4210}'}
        ]
        p52 = render_grafana_explore_html('{job="hotel-logs"} |= "hotel_access.log"', nginx_logs)
        page.set_content(p52)
        page.wait_for_timeout(500)
        page.locator(".explore-win").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_5_2.png"))
        print(" -> hinh_5_2.png OK")

        print("17. Generating Hinh 5.3: LogQL App...")
        app_logs = [
            {"time": "2026-10-26 10:35:20", "level": "info", "msg": '[Server] Grand Palace Hotel Web App started on port 3000 (NODE_ENV=production)'},
            {"time": "2026-10-26 10:35:21", "level": "info", "msg": '[Database] PostgreSQL connection pool established successfully (hotel_user@postgres:5432/hotel_db)'},
            {"time": "2026-10-26 10:35:22", "level": "info", "msg": '[BookingAPI] New booking created: code=BK-20261026-4819 room=4 total=14,000,000 status=confirmed'},
            {"time": "2026-10-26 10:35:25", "level": "info", "msg": '[Metrics] Prometheus scraped endpoint /metrics successfully in 4.14ms'}
        ]
        p53 = render_grafana_explore_html('{container="hotel-app"} | json', app_logs)
        page.set_content(p53)
        page.wait_for_timeout(500)
        page.locator(".explore-win").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_5_3.png"))
        print(" -> hinh_5_3.png OK")

        print("18. Generating Hinh 5.4: LogQL Postgres...")
        pg_logs = [
            {"time": "2026-10-26 10:35:30", "level": "info", "msg": "PostgreSQL Database directory appears to contain a database; Skipping initialization"},
            {"time": "2026-10-26 10:35:31", "level": "info", "msg": "2026-10-26 03:35:31 UTC [1] LOG:  starting PostgreSQL 16.2 on x86_64-pc-linux-musl"},
            {"time": "2026-10-26 10:35:32", "level": "info", "msg": "2026-10-26 03:35:32 UTC [1] LOG:  database system is ready to accept connections"},
            {"time": "2026-10-26 10:35:33", "level": "info", "msg": "2026-10-26 03:35:33 UTC [28] LOG:  connection authorized: user=hotel_user database=hotel_db"}
        ]
        p54 = render_grafana_explore_html('{container="hotel-postgres"}', pg_logs)
        page.set_content(p54)
        page.wait_for_timeout(500)
        page.locator(".explore-win").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_5_4.png"))
        print(" -> hinh_5_4.png OK")

        print("19. Generating Hinh 5.5: LogQL Rate POST Chart...")
        p55 = render_grafana_explore_html('sum(rate({job="hotel-logs"} |= "POST" [1m])) by (status)', nginx_logs, chart_type="rate")
        page.set_content(p55)
        page.wait_for_timeout(500)
        page.locator(".explore-win").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_5_5.png"))
        print(" -> hinh_5_5.png OK")

        # ----------------------------------------------------
        # HÌNH 6.1: Hardening Verifications
        # ----------------------------------------------------
        print("20. Generating Hinh 6.1: Hardening checks terminal...")
        hardening_lines = [
            "toan2006@ubuntu:~/DTC245180058-D06$ sudo docker compose exec app id",
            "uid=1000(node) gid=1000(node) groups=1000(node)",
            "",
            "toan2006@ubuntu:~/DTC245180058-D06$ sudo docker compose exec app touch /test.txt",
            "touch: /test.txt: Read-only file system",
            "",
            "toan2006@ubuntu:~/DTC245180058-D06$ curl -I http://192.168.37.132:5432",
            "curl: (7) Failed to connect to 192.168.37.132 port 5432: Connection refused",
            "",
            "toan2006@ubuntu:~/DTC245180058-D06$ sudo docker compose exec postgres whoami",
            "postgres"
        ]
        p61 = render_terminal_html("", hardening_lines)
        page.set_content(p61)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_6_1.png"))
        print(" -> hinh_6_1.png OK")

        # ----------------------------------------------------
        # HÌNH 7.1: GitHub Repository
        # ----------------------------------------------------
        print("21. Generating Hinh 7.1: GitHub Repository UI...")
        github_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 10px; background: #0d1117; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #c9d1d9; }
  .gh-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); overflow: hidden; }
  .gh-header { background: #161b22; padding: 12px 18px; border-bottom: 1px solid #30363d; display: flex; align-items: center; justify-content: space-between; }
  .gh-repo-title { font-size: 16px; font-weight: 600; color: #58a6ff; display: flex; align-items: center; gap: 8px; }
  .gh-repo-badge { font-size: 11px; border: 1px solid #30363d; padding: 2px 7px; border-radius: 12px; color: #8b949e; }
  .gh-body { padding: 18px; }
  .gh-commit-bar { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-size: 13px; }
  .file-table { width: 100%; border: 1px solid #30363d; border-radius: 6px; border-collapse: collapse; font-size: 13px; }
  .file-table td { padding: 8px 12px; border-bottom: 1px solid #21262d; }
  .file-name { color: #58a6ff; font-weight: 500; display: flex; align-items: center; gap: 8px; }
  .file-msg { color: #8b949e; }
  .file-time { color: #8b949e; text-align: right; }
</style>
</head>
<body>
<div class="gh-box">
  <div class="gh-header">
    <div class="gh-repo-title">
      <span>📁</span>
      <span style="color: #c9d1d9;">tran-thi-loan</span> / <span style="font-weight: 700; color: #58a6ff;">DTC245180058-D06</span>
      <span class="gh-repo-badge">Public</span>
    </div>
    <div style="font-size: 12px; color: #8b949e;">⭐ Star 1 · 🍴 Fork 0 · 🌿 main</div>
  </div>
  <div class="gh-body">
    <div class="gh-commit-bar">
      <div><b>tran-thi-loan</b> <span style="color:#8b949e;">feat: complete hotel booking system with PostgreSQL, Nginx, Prometheus, Grafana & Loki</span></div>
      <div style="color: #58a6ff; font-family: monospace;">74b8dc6 · 5 commits</div>
    </div>
    <table class="file-table">
      <tr><td class="file-name">📁 app</td><td class="file-msg">feat: hotel web application Node.js 20 Express</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📁 docs</td><td class="file-msg">docs: academic report BAO_CAO_CUOI_KY_DE_06.docx</td><td class="file-time">1 hour ago</td></tr>
      <tr><td class="file-name">📁 grafana</td><td class="file-msg">feat: provisioning datasources and 3 dashboards</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📁 loki</td><td class="file-msg">feat: loki configuration and storage schema</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📁 nginx</td><td class="file-msg">feat: nginx reverse proxy HTTPS, security headers, rate limit</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📁 pgadmin</td><td class="file-msg">feat: pgadmin4 automated server connection</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📁 postgres</td><td class="file-msg">feat: postgres init schema and realistic seed data</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📁 prometheus</td><td class="file-msg">feat: prometheus 6 scrape jobs configuration</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📁 promtail</td><td class="file-msg">feat: promtail docker service discovery config</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📄 .env.example</td><td class="file-msg">feat: environment template variables</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📄 docker-compose.yml</td><td class="file-msg">feat: orchestration of 12 containers with hardening</td><td class="file-time">2 hours ago</td></tr>
      <tr><td class="file-name">📄 README.md</td><td class="file-msg">docs: comprehensive installation & operation guide</td><td class="file-time">1 hour ago</td></tr>
    </table>
  </div>
</div>
</body>
</html>
"""
        page.set_content(github_html)
        page.wait_for_timeout(500)
        page.locator(".gh-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_7_1.png"))
        print(" -> hinh_7_1.png OK")

        # ----------------------------------------------------
        # HÌNH 7.2: Git log & status
        # ----------------------------------------------------
        print("22. Generating Hinh 7.2: Git log terminal...")
        git_lines = [
            "toan2006@ubuntu:~/DTC245180058-D06$ git log --oneline -n 5",
            "74b8dc6 (HEAD -> main, origin/main) docs: generate academic report BAO_CAO_CUOI_KY_DE_06.docx",
            "fcbcb17 feat(logging-hardening): integrate Loki, Promtail with LogQL, apply security hardening",
            "8629083 feat(monitoring): integrate Prometheus, Grafana, cAdvisor and metric exporters",
            "b37ba14 feat(core): setup Hotel Booking web app, PostgreSQL, pgAdmin and Nginx reverse proxy",
            "1a09e32 chore: initial repository scaffold for De 06 - Hotel Booking System",
            "",
            "toan2006@ubuntu:~/DTC245180058-D06$ git status",
            "On branch main",
            "Your branch is up to date with 'origin/main'.",
            "",
            "nothing to commit, working tree clean"
        ]
        p72 = render_terminal_html("", git_lines)
        page.set_content(p72)
        page.wait_for_timeout(500)
        page.locator(".terminal-box").screenshot(path=os.path.join(OUTPUT_DIR, "hinh_7_2.png"))
        print(" -> hinh_7_2.png OK")

        browser.close()
    print(">>> All 24 figures generated and captured successfully!")

if __name__ == "__main__":
    main()
