import os
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"e:\Triển khai\docs\images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_browser_screenshots():
    print(">>> Starting Playwright to capture live browser screenshots...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 1366, "height": 768},
            device_scale_factor=1.5
        )
        page = context.new_page()

        # ----------------------------------------------------
        # 1. Hình 2.4: Giao diện Danh sách phòng khách sạn
        # ----------------------------------------------------
        print("Capturing Hình 2.4: Web App Room Catalog...")
        try:
            page.goto("https://localhost/", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_4.png"))
            print(" -> hinh_2_4.png OK")
        except Exception as e:
            print(" -> hinh_2_4 error:", e)

        # ----------------------------------------------------
        # 2. Hình 2.5: Giao diện Quản lý Đặt chỗ / Form Booking
        # ----------------------------------------------------
        print("Capturing Hình 2.5: Web App Booking Tab...")
        try:
            page.click("button:has-text('Quản Lý Đặt Chỗ')")
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_2_5.png"))
            print(" -> hinh_2_5.png OK")
        except Exception as e:
            print(" -> hinh_2_5 error:", e)

        # ----------------------------------------------------
        # 3. Hình 4.3: Prometheus Targets
        # ----------------------------------------------------
        print("Capturing Hình 4.3: Prometheus Targets...")
        try:
            page.goto("http://localhost:9090/targets", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_3.png"))
            print(" -> hinh_4_3.png OK")
        except Exception as e:
            print(" -> hinh_4_3 error:", e)

        # ----------------------------------------------------
        # 4. Grafana Login
        # ----------------------------------------------------
        print("Logging into Grafana...")
        try:
            page.goto("http://localhost:3001/login", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(1000)
            page.fill("input[name='user']", "admin")
            page.fill("input[name='password']", "Grafana_SecPass2026!#")
            page.click("button[type='submit']")
            page.wait_for_timeout(3000)
            print(" -> Logged into Grafana OK")
        except Exception as e:
            print(" -> Grafana login error:", e)

        # ----------------------------------------------------
        # 5. Hình 4.4: Grafana Dashboard 1 - cAdvisor Containers
        # ----------------------------------------------------
        print("Capturing Hình 4.4: Grafana Dashboard 1 (cAdvisor)...")
        try:
            page.goto("http://localhost:3001/d/hotel-cadvisor-dash?from=now-15m&to=now&refresh=5s&kiosk=tv", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(4000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_4.png"))
            print(" -> hinh_4_4.png OK")
        except Exception as e:
            print(" -> hinh_4_4 error:", e)

        # ----------------------------------------------------
        # 6. Hình 4.5: Grafana Dashboard 2 - App & Nginx
        # ----------------------------------------------------
        print("Capturing Hình 4.5: Grafana Dashboard 2 (App & Nginx)...")
        try:
            page.goto("http://localhost:3001/d/hotel-app-nginx-dash?from=now-15m&to=now&refresh=5s&kiosk=tv", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(4000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_5.png"))
            print(" -> hinh_4_5.png OK")
        except Exception as e:
            print(" -> hinh_4_5 error:", e)

        # ----------------------------------------------------
        # 7. Hình 4.6: Grafana Dashboard 3 - PostgreSQL
        # ----------------------------------------------------
        print("Capturing Hình 4.6: Grafana Dashboard 3 (PostgreSQL)...")
        try:
            page.goto("http://localhost:3001/d/hotel-postgres-dash?from=now-15m&to=now&refresh=5s&kiosk=tv", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(4000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "hinh_4_6.png"))
            print(" -> hinh_4_6.png OK")
        except Exception as e:
            print(" -> hinh_4_6 error:", e)

        browser.close()
    print(">>> Finished live browser captures.")

if __name__ == "__main__":
    generate_browser_screenshots()
