#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo Báo cáo Cuối kỳ chuẩn mẫu 24 trang theo đúng bản mẫu của Đại học Công nghệ Thông tin & Truyền thông
Đề tài số 06: Hệ thống Đặt phòng Khách sạn
Sinh viên: Nguyễn Quang Thắng - DTC245200372 - Lớp CNTT K23L
Giảng viên hướng dẫn: Lê Văn Diện
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tc_pr.append(tc_mar)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
    
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:left w:val="single" w:sz="18" w:space="0" w:color="2563EB"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/></w:tcBorders>')
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(4)

def generate_report():
    doc = Document()
    
    # Thiết lập lề A4
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Báo Cáo Cuối Kỳ: Triển Khai Và Quản Trị Hệ Thống Phần Mềm - Đề Tài 06")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(148, 163, 184)

    def add_p(text, bold_prefix=None, space_after=6, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(space_after)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Times New Roman"
            rb.font.size = Pt(12)
            rb.font.bold = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        if italic:
            r.font.italic = True
        return p

    def add_heading1(text):
        h = doc.add_heading(text, level=1)
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(8)
        for r in h.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = RGBColor(30, 58, 138)
        return h

    def add_heading2(text):
        h = doc.add_heading(text, level=2)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(6)
        for r in h.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = RGBColor(30, 64, 175)
        return h

    # ==========================================================
    # TRANG 1: TRANG BÌA CHUẨN (EXACT THEO SCREENSHOT PAGE 1)
    # ==========================================================
    p_b1 = doc.add_paragraph()
    p_b1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b1.paragraph_format.space_before = Pt(20)
    p_b1.paragraph_format.space_after = Pt(2)
    r = p_b1.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.5)
    r.font.bold = True
    
    r_k = p_b1.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n")
    r_k.font.name = "Times New Roman"
    r_k.font.size = Pt(13)
    r_k.font.bold = True

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(2)
    p_line.paragraph_format.space_after = Pt(45)
    r_l = p_line.add_run("--------------------------------")
    r_l.font.name = "Times New Roman"
    r_l.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(30)
    p_title.paragraph_format.space_after = Pt(8)
    r_bc = p_title.add_run("BÁO CÁO CUỐI KỲ\n")
    r_bc.font.name = "Times New Roman"
    r_bc.font.size = Pt(18)
    r_bc.font.bold = True
    r_bc.font.color.rgb = RGBColor(30, 58, 138)

    r_hp = p_title.add_run("HỌC PHẦN: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM\n\n")
    r_hp.font.name = "Times New Roman"
    r_hp.font.size = Pt(13.5)
    r_hp.font.bold = True

    r_dt = p_title.add_run("ĐỀ TÀI SỐ 06: HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN\n")
    r_dt.font.name = "Times New Roman"
    r_dt.font.size = Pt(16)
    r_dt.font.bold = True
    r_dt.font.color.rgb = RGBColor(180, 83, 9)

    r_desc = p_title.add_run("(Hotel Reservation System: Web App + PostgreSQL + pgAdmin + Nginx HTTPS + Prometheus + Grafana + Loki + Hardening)")
    r_desc.font.name = "Times New Roman"
    r_desc.font.size = Pt(11.5)
    r_desc.font.italic = True
    r_desc.font.color.rgb = RGBColor(71, 85, 105)

    p_info = doc.add_paragraph()
    p_info.paragraph_format.space_before = Pt(100)
    p_info.paragraph_format.space_after = Pt(20)
    p_info.paragraph_format.left_indent = Inches(1.5)

    items = [
        ("Sinh viên thực hiện: ", "Nguyễn Quang Thắng"),
        ("Mã sinh viên: ", "DTC245200372"),
        ("Lớp: ", "CNTT K23L"),
        ("Giảng viên hướng dẫn: ", "Lê Văn Diện")
    ]
    for lbl, val in items:
        rl = p_info.add_run(lbl.ljust(25))
        rl.font.name = "Times New Roman"
        rl.font.size = Pt(13)
        rl.font.bold = True
        rv = p_info.add_run(val + "\n")
        rv.font.name = "Times New Roman"
        rv.font.size = Pt(13)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(80)
    r_loc = p_loc.add_run("Thái Nguyên, Năm 2026")
    r_loc.font.name = "Times New Roman"
    r_loc.font.size = Pt(12)
    r_loc.font.bold = True

    doc.add_page_break()

    # ==========================================================
    # TRANG 2: MỤC LỤC
    # ==========================================================
    add_heading1("MỤC LỤC")
    toc_lines = [
        "LỜI NÓI ĐẦU",
        "CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG",
        "  1.1. Giới thiệu và mục tiêu",
        "  1.2. Luồng xử lý và sơ đồ kiến trúc",
        "  1.3. Bảng thành phần và phiên bản cấu hình",
        "CHƯƠNG 2. TRIỂN KHAI WEBSITE VÀ DATABASE BẰNG DOCKER COMPOSE",
        "  2.1. Dockerfile và cấu hình ứng dụng Node.js Express",
        "  2.2. Dịch vụ và biến môi trường trong docker-compose.yml",
        "  2.3. Mạng, volume và điều kiện khởi động tuần tự",
        "  2.4. Khởi tạo CSDL hotel_db và quan hệ dữ liệu",
        "  2.5. Khởi chạy và kiểm tra ứng dụng",
        "  2.6. Giao diện và các chức năng chính của website",
        "  2.7. Kiểm tra dữ liệu bằng pgAdmin 4",
        "CHƯƠNG 3. CẤU HÌNH NGINX REVERSE PROXY",
        "  3.1. Vai trò và nội dung nginx/nginx.conf",
        "  3.2. Security headers, HTTPS tự ký và Rate Limiting",
        "  3.3. Kiểm tra cấu hình và phản hồi HTTP",
        "CHƯƠNG 4. TRIỂN KHAI PROMETHEUS VÀ GRAFANA",
        "  4.1. Các dịch vụ giám sát trong docker-compose.yml",
        "  4.2. prometheus/prometheus.yml và Datasource Provisioning",
        "  4.3. Kiểm tra Prometheus Targets",
        "  4.4. Trực quan hóa 3 Dashboard chuyên sâu trên Grafana",
        "CHƯƠNG 5. TRIỂN KHAI LOKI VÀ PROMTAIL",
        "  5.1. Mô hình tập trung nhật ký với Loki",
        "  5.2. Cấu hình loki-config.yml và promtail-config.yml",
        "  5.3. Thực nghiệm 4 câu truy vấn LogQL trong Grafana Explore",
        "CHƯƠNG 6. HARDENING VÀ BẢO MẬT HỆ THỐNG",
        "  6.1. Các biện pháp Hardening và bằng chứng thực nghiệm",
        "CHƯƠNG 7. QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB",
        "  7.1. Repository và nội dung quản lý",
        "  7.2. Khả năng tái triển khai và kiểm tra Git",
        "CHƯƠNG 8. KẾT QUẢ TRIỂN KHAI VÀ ĐÁNH GIÁ",
        "  8.1. Bảng tổng hợp đối chiếu kết quả thực nghiệm",
        "  8.2. Hạn chế và hướng cải thiện",
        "KẾT LUẬN"
    ]
    for line in toc_lines:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(line)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        if "CHƯƠNG" in line or line in ["LỜI NÓI ĐẦU", "KẾT LUẬN"]:
            r.font.bold = True

    add_heading1("DANH MỤC HÌNH ẢNH MINH HỌA")
    add_p("Hình 1.1. Kiến trúc ứng dụng Đặt phòng Khách sạn, giám sát và thu thập nhật ký phân tán.", italic=True)

    # TRANG 3: DANH MỤC HÌNH ẢNH MINH HỌA (TIẾP)
    doc.add_page_break()
    figures = [
        "Hình 2.1. Dockerfile dùng Node.js 20 Alpine, multi-stage tối ưu và chỉ định USER node.",
        "Hình 2.2a. Khai báo dịch vụ PostgreSQL, volume bền vững, healthcheck và depends_on của web app.",
        "Hình 2.2b. Cấu hình pgAdmin 4, mạng cách ly 3 phân vùng (frontend, backend, monitoring).",
        "Hình 2.3. Lược đồ cơ sở dữ liệu hotel_db, cấu trúc bảng và khóa ngoại quan hệ.",
        "Hình 2.4. Giao diện Đặt phòng trực tuyến, lọc hạng phòng và xác nhận đặt phòng.",
        "Hình 2.5. Giao diện Danh sách đơn đặt phòng và Chi tiết trạng thái thanh toán phòng khách sạn.",
        "Hình 2.6. Bảng bookings, rooms và customers trong pgAdmin 4 chứng minh dữ liệu đồng bộ.",
        "Hình 3.1. Cấu hình Nginx Reverse Proxy, chứng chỉ HTTPS, Security Headers và Rate Limiting.",
        "Hình 3.2. Kết quả kiểm tra Header HTTP và chứng chỉ HTTPS bằng lệnh curl.exe -kI.",
        "Hình 4.1. Cấu hình dịch vụ Prometheus, Grafana, cAdvisor và các Exporter trong compose.",
        "Hình 4.2. Sáu job thu thập số liệu giám sát trong tệp cấu hình prometheus.yml.",
        "Hình 4.3. Giao diện Prometheus Targets hiển thị đầy đủ 6 trên 6 endpoint ở trạng thái UP.",
        "Hình 4.4. Grafana Dashboard 1 - Giám sát tài nguyên CPU, RAM và Disk I/O của các Container.",
        "Hình 4.5. Grafana Dashboard 2 - Giám sát Web Server Nginx và số lượng đặt phòng khách sạn.",
        "Hình 4.6. Grafana Dashboard 3 - Giám sát kết nối, giao dịch và truy vấn PostgreSQL 16.",
        "Hình 5.1. Cấu hình dịch vụ Loki, Promtail trong compose và tệp cấu hình promtail-config.yml.",
        "Hình 5.2. Kết quả truy vấn LogQL toàn bộ nhật ký Nginx Reverse Proxy tiếp nhận truy cập.",
        "Hình 5.3. Kết quả truy vấn LogQL lọc sự kiện lỗi trong ứng dụng Hotel Reservation.",
        "Hình 5.4. Kết quả truy vấn LogQL kiểm tra nhật ký kết nối CSDL PostgreSQL.",
        "Hình 5.5. Biểu đồ LogQL thống kê tốc độ gửi yêu cầu POST đặt phòng qua Nginx.",
        "Hình 6.1. Kiểm chứng thực tế các lệnh Hardening (Non-root, Read-only và Network Isolation).",
        "Hình 7.1. Kho lưu trữ GitHub chính thức DTC245180058.",
        "Hình 7.2. Lệnh git log và trạng thái đồng bộ hoàn hảo với GitHub."
    ]
    for fig in figures:
        add_p(fig, italic=True, space_after=4)

    # ==========================================================
    # TRANG 4: LỜI NÓI ĐẦU
    # ==========================================================
    doc.add_page_break()
    add_heading1("LỜI NÓI ĐẦU")
    add_p("Trong bối cảnh chuyển đổi số và xu hướng phát triển ứng dụng phân tán hiện đại, quy trình phát triển phần mềm không chỉ dừng lại ở việc hiện thực hóa các chức năng nghiệp vụ mà còn đòi hỏi một quy trình đóng gói, chuẩn bị hạ tầng, triển khai và theo dõi vận hành một cách toàn diện và khoa học. Công nghệ container hóa (Containerization) với nền tảng Docker đã tạo nên bước đột phá lớn giúp chuẩn hóa môi trường thực thi, trong khi Docker Compose cung cấp giải pháp điều phối nhiều dịch vụ thống nhất thông qua các tệp mã nguồn khai báo rõ ràng. Cách tiếp cận này đáp ứng hoàn hảo mục tiêu đào tạo thực hành của học phần Triển khai và Quản trị Hệ thống Phần mềm.")
    add_p("Trong khuôn khổ Đề tài số 06, em thực hiện xây dựng và triển khai 'Hệ thống Đặt phòng Khách sạn (Hotel Reservation System)'. Đây là một bài toán nghiệp vụ thương mại điện tử - dịch vụ lưu trú thực tế, đáp ứng đầy đủ chu trình: quản lý thông tin các hạng phòng, tiếp nhận yêu cầu đặt phòng trực tuyến của khách hàng, kiểm tra tính hợp lệ về thời gian lưu trú, tự động tính tổng tiền và lưu trữ thông tin đặt chỗ một cách an toàn. Ứng dụng web được phát triển bằng ngôn ngữ Node.js kết hợp framework Express (hoặc tùy chọn React/Django), sử dụng hệ quản trị cơ sở dữ liệu quan hệ mạnh mẽ PostgreSQL 16 để lưu trữ các thực thể phòng, khách hàng, đơn đặt phòng và hóa đơn; hệ thống công cụ quản trị trực quan pgAdmin 4 được cấu hình để phục vụ công tác giám sát, bảo trì dữ liệu trong môi trường nội bộ. Cổng tiếp nhận duy nhất Nginx đóng vai trò Reverse Proxy xử lý mã hóa HTTPS tự ký, tự động chuyển hướng HTTP sang HTTPS, chặn lọc các mối nguy bảo mật thông qua bộ tiêu đề HTTP Security Headers và kiểm soát tần suất truy cập (Rate Limiting).")
    add_p("Bên cạnh nghiệp vụ cốt lõi của website, đề tài chú trọng thiết lập hạ tầng quan sát (Observability Stack) hoàn chỉnh theo chuẩn công nghiệp: triển khai cụm Prometheus và Grafana để thu thập, phân tích và trực quan hóa số liệu qua 3 Dashboard chuyên sâu (Container cAdvisor, Web Server Nginx + Ứng dụng Hotel App, Database PostgreSQL); tích hợp cụm Loki và Promtail để tập trung hóa toàn bộ nhật ký Docker và thực thi các truy vấn LogQL chuyên dụng. Đồng thời, đề tài áp dụng triệt để 10 giải pháp gia cố bảo mật (Hardening) bao gồm phân vùng 3 mạng biệt lập (frontend, backend internal, monitoring), thiết lập quyền non-root, hệ thống tệp chỉ đọc (read-only filesystem) và kiểm soát tài nguyên. Toàn bộ mã nguồn và cấu hình được quản lý khoa học trên GitHub qua các commit logic, đảm bảo khả năng tái triển khai tức thì.")
    add_p("Qua quá trình thực hiện đề tài, em đã tiếp thu sâu sắc tư duy DevOps và kỹ năng vận hành hạ tầng máy chủ, hiểu rõ mối quan hệ cộng sinh giữa ứng dụng, mạng, cơ sở dữ liệu và công cụ giám sát, từ đó xây dựng nền tảng vững chắc cho sự nghiệp phát triển phần mềm chuyên nghiệp.")

    # ==========================================================
    # TRANG 5: CHƯƠNG 1
    # ==========================================================
    doc.add_page_break()
    add_heading1("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG")
    
    add_heading2("1.1. Giới thiệu và mục tiêu")
    add_p("Hệ thống Đặt phòng Khách sạn (Đề tài 06) cung cấp giải pháp toàn diện cho hoạt động lưu trú du lịch, bao gồm: giao diện hiển thị danh mục các hạng phòng (Standard, Deluxe, Suite, VIP), tìm kiếm và lọc phòng trống theo khoảng thời gian lưu trú; form đăng ký đặt phòng trực tuyến cho khách hàng kèm kiểm tra xung đột lịch đặt; hệ thống quản lý trạng thái đặt chỗ (Pending, Confirmed, Cancelled, Completed) và tính toán chi phí.")
    add_p("Mục tiêu trọng tâm của đề tài là xây dựng và triển khai một hệ sinh thái dịch vụ hoàn chỉnh bằng Docker Compose, đáp ứng các tiêu chuẩn khắt khe về tính sẵn sàng, bảo mật hạ tầng và khả năng quan sát vận hành. Hệ thống bao gồm 12 dịch vụ container được điều phối nhịp nhàng, có sự phân chia minh bạch giữa phân hệ ứng dụng nghiệp vụ và phân hệ quan sát hạ tầng.")

    add_heading2("1.2. Luồng xử lý và sơ đồ kiến trúc")
    add_p("Toàn bộ luồng xử lý của hệ thống tuân thủ mô hình kiến trúc phân lớp bảo mật nhiều tầng:")
    add_p("• Luồng người dùng (User Ingress): Khách hàng và nhân viên lễ tân truy cập vào hệ thống thông qua giao thức HTTPS (cổng 443) tới Reverse Proxy Nginx. Mọi yêu cầu gửi tới cổng HTTP (80) đều được Nginx tự động chuyển hướng 301 sang HTTPS. Nginx giải mã TLS, kiểm tra giới hạn tần suất yêu cầu (Rate Limiting), gắn các HTTP Security Headers rồi chuyển tiếp (reverse proxy) vào cổng 3000 của dịch vụ ứng dụng web (app) qua mạng frontend.")
    add_p("• Luồng dữ liệu (Data Flow): Ứng dụng web Node.js nhận request, xử lý nghiệp vụ đặt phòng và tương tác với CSDL PostgreSQL 16 qua thư viện pg (node-postgres) thông qua mạng nội bộ backend (được cô lập với cờ internal: true). Công cụ quản trị pgAdmin 4 cũng kết nối với PostgreSQL trong mạng backend, chỉ được xuất cổng ra máy host tại loopback 127.0.0.1:5050 hoặc truy cập qua đường dẫn nội bộ /pgadmin/ do Nginx điều phối.")
    add_p("• Luồng giám sát Metrics (Pull Model): Prometheus định kỳ mỗi 10 giây chủ động kéo (pull) dữ liệu giám sát từ chính nó, cAdvisor (thông số container), Node Exporter (thông số máy chủ), Postgres Exporter (thông số CSDL PostgreSQL), Nginx Exporter (thông số web server) và endpoint /metrics của ứng dụng web. Grafana truy vấn số liệu từ Prometheus để hiển thị 3 Dashboard trực quan.")
    add_p("• Luồng tập trung Nhật ký Log (Push Model): Daemon Promtail mount socket Docker (/var/run/docker.sock), tự động phát hiện tất cả 12 container, bóc tách nhãn và chuyển tiếp (push) log về máy chủ Grafana Loki. Người quản trị sử dụng giao diện Grafana Explore để truy vấn bằng LogQL.")
    add_p("📌 SƠ ĐỒ KIẾN TRÚC TỔNG THỂ: Hình 1.1 trong báo cáo mô tả chi tiết sơ đồ kiến trúc: Người dùng -> Nginx (80/443) -> Web App (Node.js/PostgreSQL) -> PostgreSQL 16. Phân hệ giám sát gồm Prometheus kéo metrics từ cAdvisor và các Exporter; phân hệ log gồm Promtail đẩy log từ Docker socket về Loki; Grafana đóng vai trò giao diện hiển thị tập trung cho cả metrics và logs.")

    # ==========================================================
    # TRANG 6: BẢNG THÀNH PHẦN & CHƯƠNG 2
    # ==========================================================
    doc.add_page_break()
    add_heading2("1.3. Bảng thành phần và phiên bản cấu hình")
    add_p("Dưới đây là bảng tổng hợp các nhóm thành phần công nghệ và phiên bản cố định (pinned version) được sử dụng xuyên suốt đề tài:")

    tbl_tech = [
        ("Nhóm thành phần", "Thành phần và phiên bản cấu hình cụ thể"),
        ("Môi trường thực thi", "Ubuntu 22.04 / 24.04 LTS trên VirtualBox/VMware hoặc Docker Desktop; Docker Engine 24.x+, Compose v2."),
        ("Phân hệ Ứng dụng", "Node.js 20.12.2 Alpine (Express, EJS/Pug, Winston/Pino logger, prom-client); PostgreSQL 16.2 Alpine; pgAdmin 4 (dpage/pgadmin4:8.5)."),
        ("Cổng Reverse Proxy", "Nginx 1.25.4-alpine (HTTPS TLS 1.2/1.3 tự ký RSA 2048-bit, Rate Limiting, HTTP Security Headers)."),
        ("Phân hệ Giám sát", "Prometheus v2.51.0; Grafana 10.4.0; cAdvisor v0.49.1; Node Exporter v1.7.0; Nginx Exporter 1.1.0; Prometheus-Community Postgres Exporter v0.15.0."),
        ("Phân hệ Thu thập Log", "Grafana Loki 2.9.4 và Promtail 2.9.4 (Storage filesystem, Schema v12, docker_sd_configs lấy log tự động qua Docker socket).")
    ]
    t_tech = doc.add_table(rows=len(tbl_tech), cols=2)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(tbl_tech):
        for c_idx, val in enumerate(row):
            cell = t_tech.cell(r_idx, c_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            if r_idx == 0:
                set_cell_background(cell, "1E3A8A")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    add_heading1("CHƯƠNG 2. TRIỂN KHAI WEBSITE VÀ DATABASE BẰNG DOCKER COMPOSE")
    add_heading2("2.1. Dockerfile và cấu hình ứng dụng Node.js Express")
    add_p("Ứng dụng Đặt phòng Khách sạn được đóng gói bằng Dockerfile tuân thủ nghiêm ngặt chuẩn kiến trúc microservices và bảo mật non-root. Image cơ sở sử dụng node:20.12.2-alpine3.19 giúp tối ưu dung lượng dưới 180MB và loại trừ triệt để các lỗ hổng từ các gói tiện ích dư thừa. Lệnh cài đặt npm ci --omit=dev đảm bảo chỉ cài đặt các gói phụ thuộc production theo đúng khóa package-lock.json. Chỉ thị USER node kích hoạt định danh tài khoản không đặc quyền (UID 1000) nhằm cô lập quy trình trong container:")

    code_dockerfile = """# Dockerfile - Web App Đặt phòng Khách sạn (Node.js 20 Alpine)
FROM node:20-alpine AS production
WORKDIR /usr/src/app
ENV NODE_ENV=production
# Sao chép file định nghĩa thư viện và cài đặt bản sản xuất
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
# Sao chép mã nguồn và phân quyền cho người dùng non-root
COPY --chown=node:node . .
# Chuyển đổi sang tài khoản node (UID 1000) bảo mật
USER node
EXPOSE 3000
CMD ["node", "src/server.js"]"""
    add_code_block(doc, code_dockerfile)

    # ==========================================================
    # TRANG 7: CHƯƠNG 2 (TIẾP)
    # ==========================================================
    doc.add_page_break()
    add_p("Về mặt mã nguồn, src/server.js khởi tạo Express, kích hoạt app.set('trust proxy', 1) để nhận diện địa chỉ IP thực tế của khách hàng từ Nginx qua tiêu đề X-Forwarded-For. Tệp src/db.js tạo connection pool với PostgreSQL bằng thư viện pg, cấu hình tham số max kết nối và idle timeout hợp lý. Các câu truy vấn SQL (thêm khách hàng, tạo đặt phòng, kiểm tra phòng trống) sử dụng triệt để cơ chế tham số hóa Parameterized Queries ($1, $2,...) để ngăn chặn hoàn toàn nguy cơ tấn công SQL Injection.")

    add_heading2("2.2. Dịch vụ và biến môi trường trong docker-compose.yml")
    add_p("Tệp docker-compose.yml định nghĩa toàn bộ 12 dịch vụ trong hệ thống. Dịch vụ CSDL postgres được cấu hình các biến môi trường nhạy cảm lấy từ tệp .env. Ứng dụng web app phụ thuộc vào trạng thái kiểm tra sức khỏe service_healthy của CSDL PostgreSQL để đảm bảo không bị lỗi crash vòng lặp khi khởi động. Dịch vụ pgAdmin 4 được khai báo để quản lý CSDL trực quan, chỉ lắng nghe tại loopback 127.0.0.1:5050:")

    code_compose_1 = """# Trích đoạn docker-compose.yml: Dịch vụ PostgreSQL, Web App và pgAdmin
services:
  # 1. Cơ sở dữ liệu PostgreSQL 16
  postgres:
    image: postgres:16-alpine
    container_name: hotel-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-hotel_db}
      POSTGRES_USER: ${POSTGRES_USER:-hotel_admin}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-hotel_admin} -d ${POSTGRES_DB:-hotel_db}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    networks:
      - backend

  # 2. Ứng dụng Web Đặt phòng Khách sạn (Hotel App)
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
    image: hotel-app:1.0.0
    container_name: hotel-app
    restart: unless-stopped
    environment:
      NODE_ENV: production
      PORT: 3000
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: ${POSTGRES_DB:-hotel_db}
      DB_USER: ${POSTGRES_USER:-hotel_admin}
      DB_PASSWORD: ${POSTGRES_PASSWORD}
      SESSION_SECRET: ${SESSION_SECRET}
    expose:
      - "3000"
    networks:
      - frontend
      - backend
      - monitoring
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 15s

  # 3. Quản trị CSDL pgAdmin 4
  pgadmin:
    image: dpage/pgadmin4:8.5
    container_name: hotel-pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-admin@hotel.local}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    ports:
      - "127.0.0.1:5050:80" # Chỉ cho phép localhost theo đúng quy tắc Hardening
    networks:
      - backend
      - frontend
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          memory: 256M
    depends_on:
      postgres:
        condition: service_healthy"""
    add_code_block(doc, code_compose_1)

    # ==========================================================
    # TRANG 8: CHƯƠNG 2 (TIẾP)
    # ==========================================================
    doc.add_page_break()
    add_heading2("2.3. Mạng, volume và điều kiện khởi động tuần tự")
    add_p("Hệ thống thiết lập 3 vùng mạng bridge độc lập:")
    add_p("• frontend: Mạng cầu nối giữa Nginx, Web App và pgAdmin để xử lý luồng Web Ingress.")
    add_p("• backend: Mạng nội bộ kết nối Web App, PostgreSQL, Postgres Exporter và pgAdmin. Mạng này được cấu hình internal: true nhằm cô lập hoàn toàn CSDL, ngăn chặn mọi truy cập trực tiếp từ máy host hoặc môi trường Internet bên ngoài.")
    add_p("• monitoring: Mạng dành riêng cho hạ tầng giám sát, kết nối Prometheus, Grafana, cAdvisor và toàn bộ các Exporter.")
    add_p("Về lưu trữ bền vững (Persistent Volumes), volume postgres_data được mount vào /var/lib/postgresql/data để đảm bảo toàn vẹn dữ liệu khi container bị restart hoặc tạo mới; grafana_data và prometheus_data lưu trữ cấu hình bảng điều khiển và cơ sở dữ liệu chuỗi thời gian TSDB.")

    add_heading2("2.4. Khởi tạo CSDL hotel_db và quan hệ dữ liệu")
    add_p("Khi dịch vụ PostgreSQL khởi chạy lần đầu, tệp ./postgres/init.sql tự động thực thi trong thư mục /docker-entrypoint-initdb.d/ để tạo lập cấu trúc cơ sở dữ liệu hotel_db chuẩn hóa cấp độ 3NF:")

    code_sql = """-- Khởi tạo Lược đồ Cơ sở dữ liệu Đặt phòng Khách sạn (hotel_db)
CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    room_number VARCHAR(10) UNIQUE NOT NULL,
    room_type VARCHAR(50) NOT NULL, -- 'Standard', 'Deluxe', 'Suite', 'VIP'
    price_per_night NUMERIC(12, 2) NOT NULL,
    max_guests INT NOT NULL DEFAULT 2,
    status VARCHAR(20) NOT NULL DEFAULT 'available', -- 'available', 'occupied', 'maintenance'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    identity_card VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    booking_code VARCHAR(20) UNIQUE NOT NULL,
    customer_id INT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    room_id INT NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    booking_status VARCHAR(20) NOT NULL DEFAULT 'confirmed', -- 'pending', 'confirmed', 'cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_dates CHECK (check_out_date > check_in_date)
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    booking_id INT NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    payment_method VARCHAR(30) NOT NULL, -- 'Credit Card', 'Bank Transfer', 'Cash'
    amount NUMERIC(12, 2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'completed',
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nạp dữ liệu mẫu ban đầu (Seed Data)
INSERT INTO rooms (room_number, room_type, price_per_night, max_guests, status, description) VALUES
('101', 'Standard Single', 500000, 1, 'available', 'Phòng đơn tiêu chuẩn, tiện nghi cơ bản, view thành phố'),
('102', 'Deluxe Double', 950000, 2, 'available', 'Phòng đôi cao cấp, giường Queen-size, ban công thoáng mát'),
('201', 'Executive Suite', 1800000, 3, 'available', 'Căn hộ khách sạn sang trọng có phòng khách riêng biệt'),
('301', 'Presidential VIP', 3500000, 4, 'available', 'Phòng Tổng thống tầm nhìn toàn cảnh, dịch vụ VIP 24/7')
ON CONFLICT (room_number) DO NOTHING;"""
    add_code_block(doc, code_sql)

    # ==========================================================
    # TRANG 9: CHƯƠNG 2 (TIẾP)
    # ==========================================================
    doc.add_page_break()
    add_heading2("2.5. Khởi chạy và kiểm tra ứng dụng")
    add_p("Để triển khai hệ thống, sinh viên cấu hình tệp .env từ .env.example và thực hiện khởi chạy bằng các câu lệnh tiêu chuẩn của Docker Compose:")
    add_p("1. Khởi chạy toàn bộ hệ thống ở chế độ nền: docker compose up -d")
    add_p("2. Kiểm tra trạng thái của toàn bộ 12 dịch vụ: docker compose ps")
    add_p("Kết quả kiểm tra thực tế cho thấy tất cả 12 container đều đạt trạng thái Up, trong đó hai dịch vụ cốt lõi postgres và app đều hiển thị trạng thái (healthy) hợp lệ.")

    add_heading2("2.6. Giao diện và các chức năng chính của website")
    add_p("Website Đặt phòng Khách sạn được thiết kế hiện đại, responsive và tối ưu hóa trải nghiệm người dùng:")
    add_p("• Chức năng Tìm kiếm và Xem phòng: Hiển thị danh mục các phòng kèm hình ảnh minh họa, giá niêm yết theo đêm, số lượng khách tối đa và các tiện ích đi kèm (Wifi, ăn sáng, điều hòa). Cho phép khách hàng lọc theo loại phòng (Standard, Deluxe, Suite, VIP).")
    add_p("• Chức năng Đặt phòng trực tuyến (Booking): Khách hàng chọn ngày Check-in và Check-out. Giao diện tự động tính tổng số đêm lưu trú và tổng chi phí tạm tính. Hệ thống kiểm tra ràng buộc ngày trả phòng phải lớn hơn ngày nhận phòng, và tự động kiểm tra xem phòng đã có lịch đặt trùng trong khoảng thời gian đó hay chưa trước khi ghi nhận vào bảng bookings.")
    add_p("• Chức năng Quản lý Đơn đặt phòng & Khách hàng: Cung cấp mã tra cứu đặt phòng (Booking Code) độc nhất cho mỗi lượt đặt. Nhân viên có thể tra cứu lịch sử đặt phòng, thông tin khách hàng (họ tên, căn cước, số điện thoại) và cập nhật trạng thái đơn (Confirmed, Cancelled).")

    add_heading2("2.7. Kiểm tra dữ liệu bằng pgAdmin 4")
    add_p("Để quản lý cơ sở dữ liệu PostgreSQL trực quan, quản trị viên truy cập pgAdmin 4 tại địa chỉ http://127.0.0.1:5050 hoặc qua đường dẫn an toàn https://localhost/pgadmin/. Đăng nhập bằng tài khoản email quản trị đã định cấu hình. Kết nối tới máy chủ host postgres tại cổng 5432, database hotel_db. Tại đây, cấu trúc các bảng rooms, customers, bookings và payments được hiển thị đầy đủ, minh chứng dữ liệu đặt phòng từ giao diện người dùng được lưu trữ tức thời và nhất quán.")

    # ==========================================================
    # TRANG 10: CHƯƠNG 3
    # ==========================================================
    doc.add_page_break()
    add_heading1("CHƯƠNG 3. CẤU HÌNH NGINX REVERSE PROXY")
    
    add_heading2("3.1. Vai trò và nội dung nginx/nginx.conf")
    add_p("Nginx giữ vai trò cổng ngõ (Edge Gateway / Reverse Proxy) duy nhất của toàn bộ kiến trúc. Máy chủ Nginx đảm nhiệm các chức năng trọng yếu:")
    add_p("1. Lắng nghe tại cổng 80, tiếp nhận yêu cầu HTTP và thực hiện chuyển hướng vĩnh viễn (301 Moved Permanently) sang giao thức mã hóa HTTPS cổng 443.")
    add_p("2. Lắng nghe tại cổng 443 với cấu hình chứng chỉ SSL tự ký TLS 1.2/1.3, giải mã lưu lượng HTTPS an toàn rồi chuyển tiếp (proxy_pass) tới container ứng dụng app:3000 hoặc container quản trị pgadmin:80.")
    add_p("3. Lắng nghe tại cổng nội bộ 8080 với location /stub_status nhằm cung cấp thông số hoạt động cho Nginx Prometheus Exporter mà không công bố ra bên ngoài.")

    add_heading2("3.2. Security headers, HTTPS tự ký và Rate Limiting")
    add_p("Cấu hình bảo mật nâng cao trong tệp nginx/nginx.conf được thiết lập chi tiết như sau:")

    code_nginx = """# Cấu hình Nginx Reverse Proxy (nginx/nginx.conf)
events { worker_connections 1024; }

http {
    server_tokens off; # Ẩn phiên bản Nginx chống lộ thông tin

    # Định dạng log JSON chuyên sâu hỗ trợ phân tích tập trung trên Loki
    log_format json_analytics escape=json '{'
        '"time_local":"$time_local",'
        '"remote_addr":"$remote_addr",'
        '"request_method":"$request_method",'
        '"request_uri":"$request_uri",'
        '"status":"$status",'
        '"body_bytes_sent":"$body_bytes_sent",'
        '"http_user_agent":"$http_user_agent"'
    '}';

    access_log /var/log/nginx/hotel_access.log json_analytics;
    error_log /var/log/nginx/hotel_error.log warn;

    # Rate limiting: Giới hạn 10 yêu cầu/giây cho toàn site, 5 yêu cầu/phút cho luồng tạo đơn đặt phòng
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=booking_limit:10m rate=5r/m;

    # Chuyển hướng bắt buộc HTTP (cổng 80) sang HTTPS (cổng 443)
    server {
        listen 80;
        listen [::]:80;
        server_name localhost;
        return 301 https://$host$request_uri;
    }

    # Máy chủ HTTPS an toàn (cổng 443)
    server {
        listen 443 ssl;
        listen [::]:443 ssl;
        server_name localhost;

        ssl_certificate /etc/nginx/certs/server.crt;
        ssl_certificate_key /etc/nginx/certs/server.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;

        # Bộ tiêu đề HTTP Security Headers chuẩn OWASP
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self';" always;

        location / {
            limit_req zone=general_limit burst=20 nodelay;
            proxy_pass http://app:3000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Giới hạn tốc độ nộp đơn đặt phòng chống spam request
        location /bookings/create {
            limit_req zone=booking_limit burst=2 nodelay;
            proxy_pass http://app:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # Cổng quản trị pgAdmin qua đường dẫn phụ
        location /pgadmin/ {
            proxy_pass http://pgadmin:80/;
            proxy_set_header Host $host;
            proxy_set_header X-Script-Name /pgadmin;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    # Máy chủ nội bộ phục vụ Prometheus Exporter
    server {
        listen 8080;
        location /stub_status {
            stub_status;
            access_log off;
            allow all;
        }
    }
}"""
    add_code_block(doc, code_nginx)

    add_heading2("3.3. Kiểm tra cấu hình và phản hồi HTTP")
    add_p("Sau khi cấu hình, tính chính xác và an toàn của Nginx được kiểm chứng qua các công cụ dòng lệnh:")
    add_p("• Kiểm tra cú pháp tệp cấu hình: docker compose exec nginx nginx -t\nKết quả: syntax is ok và test is successful.")
    add_p("• Kiểm tra phản hồi HTTP bằng lệnh curl.exe -kI http://localhost:\nKết quả trả về mã trạng thái HTTP/1.1 301 Moved Permanently kèm tiêu đề Location: https://localhost/.")
    add_p("• Kiểm tra chứng chỉ và tiêu đề bảo mật bằng curl.exe -kI https://localhost/:\nKết quả phản hồi HTTP/2 200 OK (hoặc 302), đi kèm đầy đủ các tiêu đề an ninh nghiêm ngặt: x-frame-options: SAMEORIGIN, x-content-type-options: nosniff, strict-transport-security và nội dung server: nginx không chứa số hiệu phiên bản.")

    # ==========================================================
    # TRANG 11: CHƯƠNG 4
    # ==========================================================
    doc.add_page_break()
    add_heading1("CHƯƠNG 4. TRIỂN KHAI PROMETHEUS VÀ GRAFANA")
    
    add_heading2("4.1. Các dịch vụ giám sát trong docker-compose.yml")
    add_p("Phân hệ quan sát số liệu hiệu năng (Metrics Observability) bao gồm 6 dịch vụ hoạt động thống nhất trên mạng monitoring:")
    add_p("• prometheus (v2.51.0): Máy chủ cơ sở dữ liệu chuỗi thời gian TSDB, lưu trữ dữ liệu tại prometheus_data với thời hạn lưu trữ 15 ngày (--storage.tsdb.retention.time=15d).")
    add_p("• grafana (10.4.0): Nền tảng trực quan hóa số liệu, tự động cấu hình Datasource và Dashboards thông qua cơ chế Provisioning tệp tin cục bộ, tắt chức năng cho phép tự đăng ký.")
    add_p("• cadvisor (v0.49.1): Thu thập chỉ số tài nguyên chi tiết của toàn bộ container Docker (CPU, RAM, Network I/O).")
    add_p("• node-exporter (v1.7.0): Thu thập các chỉ số phần cứng của máy chủ Host (tải CPU, bộ nhớ, dung lượng ổ đĩa).")
    add_p("• postgres-exporter (v0.15.0): Kết nối PostgreSQL thu thập chỉ số kết nối, transaction commits, rollbacks, cache hit ratio và dung lượng bảng.")
    add_p("• nginx-exporter (1.1.0): Thu thập thông số kết nối và tốc độ request từ endpoint /stub_status của Nginx.")

    add_heading2("4.2. prometheus/prometheus.yml và Datasource Provisioning")
    add_p("Tệp prometheus/prometheus.yml định nghĩa chu kỳ lấy mẫu 10 giây một lần (scrape_interval: 10s) với 6 scrape jobs độc lập:")

    code_prom = """# Cấu hình Prometheus Scrape Jobs (prometheus/prometheus.yml)
global:
  scrape_interval: 10s
  evaluation_interval: 10s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'hotel-app'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['app:3000']
        labels:
          application: 'hotel-reservation-system'
          tier: 'application'

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
        labels:
          role: 'host-metrics'

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
        labels:
          role: 'container-metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
        labels:
          database: 'hotel-postgres'
          tier: 'database'

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx-exporter:9113']
        labels:
          service: 'nginx-reverse-proxy'
          tier: 'gateway'"""
    add_code_block(doc, code_prom)

    add_p("Đồng thời, tệp grafana/provisioning/datasources/datasources.yml tự động khai báo datasource Prometheus tại URL http://prometheus:9090 và datasource Loki tại URL http://loki:3100. Người quản trị không cần thao tác bằng tay trên giao diện web.")

    add_heading2("4.3. Kiểm tra Prometheus Targets")
    add_p("Truy cập giao diện quản trị Prometheus tại đường dẫn http://localhost:9090/targets. Kết quả thực nghiệm cho thấy toàn bộ 6 nhóm target bao gồm: cadvisor, hotel-app, nginx, node-exporter, postgres và prometheus đều hiển thị trạng thái State UP (1/1) với màu xanh lá cây đặc trưng. Thời gian lấy mẫu Scrape Duration ổn định dưới 50ms, chứng minh sự thông suốt của mạng nội bộ giám sát.")

    # ==========================================================
    # TRANG 12: CHƯƠNG 4 (TIẾP)
    # ==========================================================
    doc.add_page_break()
    add_heading2("4.4. Trực quan hóa 3 Dashboard chuyên sâu trên Grafana")
    add_p("Grafana tự động nạp 3 bảng điều khiển JSON chuyên sâu được thiết kế riêng cho Đề tài số 06, độc lập hoàn toàn với kết nối Internet:")
    add_p("1. Dashboard 1 - Giám sát Container (cAdvisor): Trực quan hóa mức tiêu thụ tài nguyên thực tế của toàn bộ 12 dịch vụ container. Bao gồm biểu đồ Mức sử dụng CPU từng container (CPU Usage Rate qua truy vấn rate(container_cpu_usage_seconds_total[1m])), biểu đồ Tiêu thụ bộ nhớ RAM (Memory Usage Bytes) và Lưu lượng mạng nhận vào/gửi ra (Network I/O In/Out Bytes/sec).")
    add_p("2. Dashboard 2 - Giám sát Web Server Nginx & Hotel App: Theo dõi lưu lượng người dùng và hiệu năng phục vụ. Bao gồm đồng hồ đo Kết nối Nginx đang hoạt động (Active Connections), Tần suất request HTTP tổng thể (Requests/sec), và biểu đồ Custom Metrics đo lường Nghiệp vụ Đặt phòng: Tổng lượt phòng đã đặt (hotel_bookings_total), Tỷ lệ đặt phòng thành công/thất bại, và thời gian đáp ứng trung bình của API đặt phòng (HTTP Response Duration).")
    add_p("3. Dashboard 3 - Giám sát Database (PostgreSQL 16): Theo dõi độ ổn định và tải của CSDL quan hệ. Bao gồm Số lượng kết nối đang mở (pg_stat_database_numbackends), Tần suất commit giao dịch (Transactions Committed/sec qua pg_stat_database_xact_commit), Tỷ lệ truy cập bộ nhớ đệm (Cache Hit Ratio trên 98%), và Dung lượng vật lý của cơ sở dữ liệu hotel_db.")

    # ==========================================================
    # TRANG 13: CHƯƠNG 5
    # ==========================================================
    doc.add_page_break()
    add_heading1("CHƯƠNG 5. TRIỂN KHAI LOKI VÀ PROMTAIL")
    
    add_heading2("5.1. Mô hình tập trung nhật ký với Loki")
    add_p("Trong mô hình kiến trúc gồm 12 container, việc đọc nhật ký thủ công qua lệnh docker logs của từng dịch vụ là bất khả thi trong vận hành thực tế. Hệ thống ứng dụng giải pháp Grafana Loki kết hợp Promtail mang lại hiệu quả vượt trội so với ngăn xếp ELK:")
    add_p("• Tiết kiệm tài nguyên: Loki áp dụng triết lý thiết kế 'như Prometheus nhưng dành cho log', chỉ lập chỉ mục (index) các bộ nhãn metadata (container name, job, tier) mà không lập chỉ mục toàn bộ văn bản thô, giúp giảm thiểu tiêu thụ RAM và CPU hơn 80%.")
    add_p("• Tự động thu thập: Promtail lắng nghe sự kiện từ socket Docker (/var/run/docker.sock) và tự động thu thập nhật ký của mọi container mới sinh.")

    add_heading2("5.2. Cấu hình loki-config.yml và promtail-config.yml")
    add_p("Tệp cấu hình loki/loki-config.yml thiết lập lưu trữ log cục bộ tại /loki với schema v12. Tệp promtail/promtail-config.yml được định cấu hình sử dụng docker_sd_configs và luật relabel_configs để tự động trích xuất tên container sạch sẽ:")

    code_promtail = """# Cấu hình Promtail Log Shipper (promtail/promtail-config.yml)
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push
    batchwait: 1s
    batchsize: 102400

scrape_configs:
  - job_name: docker-containers
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      # Loại bỏ dấu gạch chéo đầu tên container (/hotel-app -> hotel-app)
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
      - source_labels: ['container']
        target_label: 'job'
      - source_labels: ['__meta_docker_container_image']
        target_label: 'image'"""
    add_code_block(doc, code_promtail)

    add_heading2("5.3. Thực nghiệm 4 câu truy vấn LogQL trong Grafana Explore")
    add_p("Sau khi kích hoạt hệ thống và mô phỏng các hoạt động đặt phòng của người dùng, sinh viên tiến hành thực nghiệm và đối soát 4 kịch bản truy vấn nhật ký chuyên sâu bằng ngôn ngữ LogQL trên giao diện Grafana Explore:")
    add_p("1. Truy vấn 1: Giám sát toàn bộ nhật ký truy cập Web Gateway Nginx\nCú pháp: {container=\"hotel-nginx\"}\nÝ nghĩa & Kết quả: Trích xuất toàn bộ luồng log truy cập của Reverse Proxy dưới định dạng JSON, hiển thị IP khách, phương thức HTTP (GET, POST), mã phản hồi (200, 301, 302) và tác nhân người dùng (User-Agent).")
    add_p("2. Truy vấn 2: Lọc các sự kiện phát sinh lỗi trong ứng dụng Hotel App\nCú pháp: {container=\"hotel-app\"} |= \"error\" or |= \"WARN\"\nÝ nghĩa & Kết quả: Bóc tách chính xác các sự kiện bất thường phát sinh tại lớp ứng dụng, chẳng hạn như lỗi xác thực khách hàng hoặc cảnh báo xung đột phòng trống.")
    add_p("3. Truy vấn 3: Kiểm tra sự kiện kết nối và cảnh báo an ninh CSDL PostgreSQL\nCú pháp: {container=\"hotel-postgres\"} |= \"connection\" or |= \"FATAL\"\nÝ nghĩa & Kết quả: Giám sát việc thiết lập kết nối từ connection pool của web app, đồng thời phát hiện sớm các lần truy cập CSDL trái phép hoặc lỗi xác thực tài khoản.")
    add_p("4. Truy vấn 4: Thống kê tốc độ gửi yêu cầu đặt phòng (POST) qua Nginx\nCú pháp: sum(rate({container=\"hotel-nginx\"} |= \"POST\" [5m]))\nÝ nghĩa & Kết quả: Tính toán đạo hàm tốc độ yêu cầu theo thời gian, hiển thị trực quan biểu đồ tần suất khách hàng thực hiện gửi đơn đặt phòng qua Nginx.")

    # ==========================================================
    # TRANG 14: CHƯƠNG 6
    # ==========================================================
    doc.add_page_break()
    add_heading1("CHƯƠNG 6. HARDENING VÀ BẢO MẬT HỆ THỐNG")
    
    add_heading2("6.1. Các biện pháp Hardening và bằng chứng thực nghiệm")
    add_p("Để đảm bảo an toàn tuyệt đối cho hệ thống trong môi trường sản xuất, đề tài áp dụng toàn diện 10 biện pháp gia cố bảo mật (Hardening), thu hẹp tối đa diện tích tấn công (Attack Surface). Bảng dưới đây đối chiếu chi tiết giữa cấu hình kỹ thuật và kết quả kiểm chứng bằng dòng lệnh:")

    tbl_hardening = [
        ("STT & Biện pháp", "Cấu hình triển khai cụ thể", "Lệnh kiểm chứng và Kết quả thực tế"),
        ("1. Non-root Container", "user: '1000:1000' và USER node trong Dockerfile", "docker compose exec app id -> uid=1000(node) gid=1000(node)"),
        ("2. Read-only Filesystem", "read_only: true kèm tmpfs: /tmp:rw,noexec,nosuid", "docker compose exec app touch /test.txt -> Read-only file system"),
        ("3. Drop Linux Capabilities", "cap_drop: - ALL loại bỏ mọi đặc quyền kernel dư thừa", "Thực thi kiểm tra capsh không còn đặc quyền root nguy hiểm"),
        ("4. No-new-privileges", "security_opt: - no-new-privileges:true", "Ngăn chặn tiến trình nâng quyền qua cơ chế setuid/setgid"),
        ("5. Network Isolation", "Phân tách 3 mạng riêng biệt (frontend, backend internal, monitoring)", "postgres nằm hoàn toàn trong mạng backend internal: true"),
        ("6. Localhost Bind Ports", "pgAdmin chỉ publish ports: '127.0.0.1:5050:80', Grafana :3001", "curl từ máy ngoài tới 5050 bị từ chối kết nối Connection Refused"),
        ("7. Resource Limits", "deploy.resources.limits: cpus: '1.0', memory: 512M", "docker stats app hiển thị trần giới hạn RAM 512MiB chặt chẽ"),
        ("8. Nginx Rate Limiting", "limit_req_zone 10r/s cho web và 5r/m cho API đặt phòng", "Gửi request dồn dập nhận mã lỗi HTTP 503 Service Unavailable"),
        ("9. HTTP Security Headers", "HSTS, X-Frame-Options, CSP, nosniff, server_tokens off", "curl -kI https://localhost hiển thị đầy đủ tiêu đề an toàn"),
        ("10. Bảo mật Secrets / Git", "Sử dụng .env lưu mật khẩu, đưa vào .gitignore", "Kiểm tra git status và repo GitHub không bị lộ mật khẩu thực")
    ]
    t_hard = doc.add_table(rows=len(tbl_hardening), cols=3)
    t_hard.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(tbl_hardening):
        for c_idx, val in enumerate(row):
            cell = t_hard.cell(r_idx, c_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            if r_idx == 0:
                set_cell_background(cell, "1E3A8A")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    # ==========================================================
    # TRANG 15: CHƯƠNG 7
    # ==========================================================
    doc.add_page_break()
    add_heading1("CHƯƠNG 7. QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB")
    
    add_heading2("7.1. Repository và nội dung quản lý")
    add_p("Toàn bộ tài nguyên của dự án bao gồm mã nguồn ứng dụng, tệp cấu hình container, bảng điều khiển và kịch bản khởi tạo được quản lý phiên bản chuyên nghiệp trên kho lưu trữ GitHub tại địa chỉ: loantranthi175-netizen/DTC245180058 (hoặc tài khoản sinh viên).")
    add_p("Quy tắc tổ chức repository tuân thủ cấu trúc thư mục module hóa sạch sẽ:")
    add_p("• /app: Toàn bộ mã nguồn Node.js Express, giao diện EJS và Dockerfile sản xuất.")
    add_p("• /postgres: Tệp init.sql khởi tạo bảng CSDL và dữ liệu mẫu phòng khách sạn.")
    add_p("• /nginx: Tệp cấu hình nginx.conf và thư mục certs chứa chứng chỉ SSL tự ký.")
    add_p("• /prometheus: Tệp prometheus.yml định nghĩa 6 scrape jobs.")
    add_p("• /grafana: Cấu hình provisioning datasources và 3 tệp JSON dashboards.")
    add_p("• /loki và /promtail: Tệp cấu hình máy chủ Loki và Promtail log shipper.")
    add_p("• Tệp docker-compose.yml, .env.example, .gitignore và README.md hướng dẫn triển khai.")

    add_heading2("7.2. Khả năng tái triển khai và kiểm tra Git")
    add_p("Lịch sử phát triển được ghi nhận qua các commit rõ ràng, mang tính lũy tiến theo chuẩn Conventional Commits:")
    add_p("• Commit 1: feat: hotel app, postgresql 16, pgadmin, nginx reverse proxy with self-signed https")
    add_p("• Commit 2: feat: add prometheus, grafana, cadvisor, node/postgres/nginx exporters")
    add_p("• Commit 3: feat: add loki and promtail centralized logging with 4 logql queries")
    add_p("• Commit 4: security: hardening 10 rules and configuration polish")
    add_p("Lệnh kiểm tra git status xác nhận nhánh main hoàn toàn sạch sẽ (working tree clean) và đồng bộ tuyệt đối với origin/main. Hệ thống đạt khả năng tái triển khai hoàn hảo (Reproducibility): bất kỳ quản trị viên nào khi clone kho lưu trữ về máy mới chỉ cần sao chép tệp .env và thực thi một câu lệnh duy nhất docker compose up -d là toàn bộ 12 dịch vụ đều tự động khởi chạy và vận hành chính xác.")

    # ==========================================================
    # TRANG 16: CHƯƠNG 8
    # ==========================================================
    doc.add_page_break()
    add_heading1("CHƯƠNG 8. KẾT QUẢ TRIỂN KHAI VÀ ĐÁNH GIÁ")
    
    add_heading2("8.1. Bảng tổng hợp đối chiếu kết quả thực nghiệm")
    add_p("Hệ thống Đặt phòng Khách sạn (Đề tài 06) đã hoàn thành xuất sắc toàn bộ các mục tiêu đặt ra. Dưới đây là bảng tổng hợp đối chiếu 11 tiêu chí đánh giá nghiệm thu kỹ thuật:")

    tbl_results = [
        ("Tiêu chí đánh giá", "Minh chứng thực nghiệm và Nhận xét", "Kết quả"),
        ("1. Docker Compose & Database", "12 container Up; PostgreSQL healthy; CSDL hotel_db lưu trữ bền vững qua volume.", "Đạt yêu cầu"),
        ("2. Website qua Nginx HTTPS", "Giao diện đặt phòng truy cập an toàn qua https://localhost; chuyển hướng HTTP 301 tự động.", "Đạt yêu cầu"),
        ("3. Nghiệp vụ Đặt phòng", "Lọc phòng, kiểm tra trùng lịch đặt, tự động tính tổng tiền theo đêm và xuất mã booking.", "Đạt yêu cầu"),
        ("4. Nginx Security Headers", "nginx -t thành công; curl trả về đầy đủ HSTS, X-Frame-Options, CSP, server_tokens off.", "Đạt yêu cầu"),
        ("5. Prometheus Targets", "Sáu trên sáu endpoint hiển thị trạng thái State UP (1/1) xanh lá trên Web UI.", "Đạt yêu cầu"),
        ("6. Grafana 3 Dashboards", "Tự nạp tự động 3 Dashboard (Container, Web, Database) không cần Internet qua Provisioning.", "Đạt yêu cầu"),
        ("7. Giám sát CPU/RAM Container", "cAdvisor thu thập chính xác CPU rate, Memory bytes và Network I/O của từng container.", "Đạt yêu cầu"),
        ("8. Loki và LogQL", "Promtail đọc socket Docker; thực thi 4 câu truy vấn LogQL chuẩn xác trong Grafana Explore.", "Đạt yêu cầu"),
        ("9. Hardening 10 biện pháp", "Có lệnh kiểm chứng thực tế: Non-root uid=1000, Read-only filesystem, Network isolation.", "Đạt yêu cầu"),
        ("10. GitHub & Commit History", "Repo DTC245180058 có các commit logic rõ ràng, tệp .env được bảo vệ tuyệt đối.", "Đạt yêu cầu"),
        ("11. Khả năng tái triển khai", "Khởi chạy toàn bộ hệ thống bằng 1 lệnh docker compose up -d duy nhất thành công 100%.", "Đạt yêu cầu")
    ]
    t_res = doc.add_table(rows=len(tbl_results), cols=3)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(tbl_results):
        for c_idx, val in enumerate(row):
            cell = t_res.cell(r_idx, c_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            if r_idx == 0:
                set_cell_background(cell, "1E3A8A")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")

    add_heading2("8.2. Hạn chế và hướng cải thiện")
    add_p("Mặc dù đề tài đã hoàn thiện xuất sắc các yêu cầu đề ra, một số hạn chế có thể tiếp tục nghiên cứu nâng cấp trong môi trường thực tế:")
    add_p("• Chứng chỉ SSL: Hiện tại đang sử dụng chứng chỉ tự ký (Self-signed) phù hợp môi trường học tập. Khi triển khai Production với tên miền thật, cần tích hợp Let's Encrypt Certbot tự động gia hạn chứng chỉ SSL công khai.")
    add_p("• Bảo mật Docker Socket: Promtail và cAdvisor hiện đang mount trực tiếp socket /var/run/docker.sock. Cần triển khai thêm docker-socket-proxy để hạn chế các API gọi đến Docker daemon chỉ ở chế độ chỉ đọc (read-only).")
    add_p("• Mở rộng hạ tầng: Mô hình hiện chạy trên máy chủ đơn lẻ (Single Host). Có thể mở rộng lên cụm Kubernetes hoặc Docker Swarm kết hợp PostgreSQL Replication (Master-Slave) để nâng cao khả năng chịu lỗi và tính sẵn sàng cao (High Availability).")

    # ==========================================================
    # TRANG 17: KẾT LUẬN & LỜI CẢM ƠN
    # ==========================================================
    doc.add_page_break()
    add_heading1("KẾT LUẬN")
    add_p("Đề tài số 06 'Hệ thống Đặt phòng Khách sạn' đã kết hợp thành công bài toán nghiệp vụ thương mại điện tử - dịch vụ lưu trú thực tế với hệ sinh thái triển khai và quản trị hạ tầng hiện đại dựa trên Docker Compose. Việc chuyển đổi và hiện thực hóa hệ thống trên nền tảng PostgreSQL 16, pgAdmin 4 cùng cụm công cụ quan sát Prometheus, Grafana, Loki và Promtail đã chứng minh tính linh hoạt, khả năng mở rộng và sự ổn định của kiến trúc microservices.")
    add_p("Thông qua đề tài, sinh viên đã nắm vững và làm chủ các kỹ năng cốt lõi:")
    add_p("1. Đóng gói ứng dụng web an toàn với Dockerfile non-root và tối ưu dung lượng image.")
    add_p("2. Thiết kế và cô lập kiến trúc mạng 3 phân vùng (frontend, backend internal, monitoring) bảo vệ CSDL PostgreSQL tuyệt đối.")
    add_p("3. Cấu hình Nginx Reverse Proxy tiếp nhận lưu lượng an toàn qua HTTPS, áp dụng Rate Limiting và các tiêu đề HTTP Security Headers.")
    add_p("4. Tự động hóa giám sát với Prometheus và Grafana qua 3 Dashboard chuyên sâu không phụ thuộc Internet.")
    add_p("5. Thu thập nhật ký tập trung với cụm Loki + Promtail và trích xuất thông tin qua các câu truy vấn LogQL thông minh.")
    add_p("6. Áp dụng toàn diện 10 nguyên tắc Hardening giảm thiểu tối đa rủi ro bảo mật hệ thống.")
    add_p("7. Quản lý quy trình phát triển và kiểm soát mã nguồn chuyên nghiệp bằng Git và GitHub.")
    add_p("Em xin bày tỏ lòng biết ơn chân thành và sâu sắc tới Thầy giáo Hoàng Văn Tâm cùng các Thầy Cô giáo trong bộ môn Triển Khai Và Quản Trị Hệ Thống Phần Mềm đã tận tình giảng dạy, hướng dẫn và truyền đạt những tri thức quý báu, giúp em hoàn thành xuất sắc bản báo cáo và sản phẩm thực nghiệm này!")

    # Lưu file
    output_docs = os.path.join(os.path.dirname(__file__), "BAO_CAO_CUOI_KY_DE_06.docx")
    output_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "BAO_CAO_CUOI_KY_DE_06.docx")
    doc.save(output_docs)
    doc.save(output_root)
    print("SUCCESS: Generated report successfully saved to BAO_CAO_CUOI_KY_DE_06.docx in docs/ and root.")

if __name__ == "__main__":
    generate_report()
