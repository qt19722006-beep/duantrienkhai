import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

IMG_DIR = r"e:\Triển khai\docs\images"
OUTPUT_FILE_1 = r"e:\Triển khai\BAO_CAO_CUOI_KY_DE_06_FULL_ANH.docx"
OUTPUT_FILE_2 = r"e:\Triển khai\docs\BAO_CAO_CUOI_KY_DE_06_FULL_ANH.docx"

def set_cell_background(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tc_pr.append(tc_mar)

def create_report():
    doc = Document()

    # Cấu hình trang A4 chuẩn bộ giáo dục
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # Header
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
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(8)
        r = h.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(20, 35, 90)
        return h

    def add_heading2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        r = h.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 64, 175)
        return h

    def add_image_figure(img_name, caption_text, width=Inches(5.9)):
        img_path = os.path.join(IMG_DIR, img_name)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(3)
            run = p_img.add_run()
            run.add_picture(img_path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            rcap = p_cap.add_run(caption_text)
            rcap.font.name = "Times New Roman"
            rcap.font.size = Pt(10.5)
            rcap.font.bold = True
            rcap.font.italic = True
            rcap.font.color.rgb = RGBColor(55, 65, 81)
        else:
            print(f"Warning: Image file not found: {img_path}")

    # ==========================================================
    # TRANG 1: TRANG BÌA CHUẨN ĐẠI HỌC ICTU
    # ==========================================================
    p_b1 = doc.add_paragraph()
    p_b1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b1.paragraph_format.space_before = Pt(15)
    p_b1.paragraph_format.space_after = Pt(2)
    r1 = p_b1.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(13.5)
    r1.font.bold = True
    
    r2 = p_b1.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(13)
    r2.font.bold = True

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(2)
    p_line.paragraph_format.space_after = Pt(50)
    rl = p_line.add_run("--------------------------------")
    rl.font.name = "Times New Roman"
    rl.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(25)
    p_title.paragraph_format.space_after = Pt(8)
    
    rbc = p_title.add_run("BÁO CÁO CUỐI KỲ\n")
    rbc.font.name = "Times New Roman"
    rbc.font.size = Pt(18)
    rbc.font.bold = True
    rbc.font.color.rgb = RGBColor(30, 58, 138)

    rhp = p_title.add_run("HỌC PHẦN: TRIỂN KHAI VÀ QUẢN TRỊ\nHỆ THỐNG PHẦN MỀM\n\n")
    rhp.font.name = "Times New Roman"
    rhp.font.size = Pt(14)
    rhp.font.bold = True

    rdt = p_title.add_run("ĐỀ TÀI 06 : HỆ THỐNG ĐẶT PHÒNG KHÁCH SẠN\n")
    rdt.font.name = "Times New Roman"
    rdt.font.size = Pt(16)
    rdt.font.bold = True
    rdt.font.color.rgb = RGBColor(180, 83, 9)

    p_info = doc.add_paragraph()
    p_info.paragraph_format.space_before = Pt(110)
    p_info.paragraph_format.space_after = Pt(20)
    p_info.paragraph_format.left_indent = Inches(1.5)

    info_data = [
        ("Sinh viên thực hiện :", "Trần Thị Loan"),
        ("Mã sinh viên :", "DTC245180058"),
        ("Lớp :", "KTPM K23C"),
        ("Giảng Viên Hướng dẫn:", "Hoàng Văn Tâm")
    ]
    for label, val in info_data:
        rl = p_info.add_run(label.ljust(25))
        rl.font.name = "Times New Roman"
        rl.font.size = Pt(13)
        rl.font.bold = True
        rv = p_info.add_run(f" {val}\n")
        rv.font.name = "Times New Roman"
        rv.font.size = Pt(13)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(90)
    rloc = p_loc.add_run("Thái Nguyên, Năm 2026")
    rloc.font.name = "Times New Roman"
    rloc.font.size = Pt(12)
    rloc.font.bold = True

    doc.add_page_break()

    # ==========================================================
    # TRANG 2: MỤC LỤC
    # ==========================================================
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(10)
    p_toc_title.paragraph_format.space_after = Pt(15)
    rtoc = p_toc_title.add_run("MỤC LỤC")
    rtoc.font.name = "Times New Roman"
    rtoc.font.size = Pt(16)
    rtoc.font.bold = True

    toc_items = [
        ("LỜI NÓI ĐẦU", "4", True),
        ("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG", "5", True),
        ("  1.1. Giới thiệu và mục tiêu", "5", False),
        ("  1.2. Luồng xử lý và sơ đồ kiến trúc", "5", False),
        ("  1.3. Bảng thành phần và phiên bản cấu hình", "6", False),
        ("CHƯƠNG 2. TRIỂN KHAI WEBSITE VÀ DATABASE BẰNG DOCKER COMPOSE", "6", True),
        ("  2.1. Dockerfile và cấu hình ứng dụng Node.js", "6", False),
        ("  2.2. Dịch vụ và biến môi trường trong docker-compose.yml", "7", False),
        ("  2.3. Mạng, volume và điều kiện khởi động tuần tự", "7", False),
        ("  2.4. Khởi tạo CSDL hotel_db và quan hệ dữ liệu", "10", False),
        ("  2.5. Khởi chạy và kiểm tra ứng dụng", "10", False),
        ("  2.6. Giao diện và các chức năng chính của website", "11", False),
        ("  2.7. Kiểm tra dữ liệu bằng pgAdmin", "12", False),
        ("CHƯƠNG 3. CẤU HÌNH NGINX REVERSE PROXY", "13", True),
        ("  3.1. Vai trò và nội dung nginx/nginx.conf", "13", False),
        ("  3.2. Security headers, HTTPS tự ký và Rate Limiting", "13", False),
        ("  3.3. Kiểm tra cấu hình và phản hồi HTTP", "14", False),
        ("CHƯƠNG 4. TRIỂN KHAI PROMETHEUS VÀ GRAFANA", "15", True),
        ("  4.1. Các dịch vụ giám sát trong docker-compose.yml", "15", False),
        ("  4.2. prometheus/prometheus.yml và Datasource Provisioning", "16", False),
        ("  4.3. Kiểm tra Prometheus Targets", "17", False),
        ("  4.4. Trực quan hóa 3 Dashboard chuyên sâu trên Grafana", "18", False),
        ("CHƯƠNG 5. TRIỂN KHAI LOKI VÀ PROMTAIL", "21", True),
        ("  5.1. Mô hình tập trung nhật ký với Loki", "21", False),
        ("  5.2. Cấu hình loki-config.yml và promtail-config.yml", "21", False),
        ("  5.3. Thực nghiệm 4 câu truy vấn LogQL trong Grafana Explore", "22", False),
        ("CHƯƠNG 6. HARDENING VÀ BẢO MẬT HỆ THỐNG", "24", True),
        ("  6.1. Các biện pháp Hardening và bằng chứng thực nghiệm", "24", False),
        ("CHƯƠNG 7. QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB", "24", True),
        ("  7.1. Repository và nội dung quản lý", "24", False),
        ("  7.2. Khả năng tái triển khai và kiểm tra Git", "25", False),
        ("CHƯƠNG 8. KẾT QUẢ TRIỂN KHAI VÀ ĐÁNH GIÁ", "25", True),
        ("  8.1. Bảng tổng hợp đối chiếu kết quả thực nghiệm", "25", False),
        ("  8.2. Hạn chế và hướng cải thiện", "26", False),
        ("KẾT LUẬN", "27", True),
    ]

    for title, page_no, is_bold in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2.5)
        
        rt = p.add_run(title)
        rt.font.name = "Times New Roman"
        rt.font.size = Pt(11)
        rt.font.bold = is_bold
        
        # Dotted leader
        dots_len = max(5, 75 - len(title))
        rdots = p.add_run(" " + "." * dots_len + " ")
        rdots.font.name = "Times New Roman"
        rdots.font.size = Pt(10)
        rdots.font.color.rgb = RGBColor(150, 150, 150)
        
        rnum = p.add_run(page_no)
        rnum.font.name = "Times New Roman"
        rnum.font.size = Pt(11)
        rnum.font.bold = is_bold

    doc.add_page_break()

    # ==========================================================
    # TRANG 3: DANH MỤC HÌNH ẢNH
    # ==========================================================
    p_fig_title = doc.add_paragraph()
    p_fig_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig_title.paragraph_format.space_before = Pt(10)
    p_fig_title.paragraph_format.space_after = Pt(15)
    rfig = p_fig_title.add_run("DANH MỤC HÌNH ẢNH")
    rfig.font.name = "Times New Roman"
    rfig.font.size = Pt(16)
    rfig.font.bold = True

    figures_list = [
        ("Hình 1.1. Kiến trúc ứng dụng, giám sát và nhật ký theo cấu hình dự án.", "5"),
        ("Hình 2.1. Dockerfile dùng Node.js 20 Alpine, cài đặt production và chỉ định USER node.", "7"),
        ("Hình 2.2a. Cấu hình PostgreSQL, volume, healthcheck và điều kiện phụ thuộc của ứng dụng.", "8"),
        ("Hình 2.2b. Cấu hình PostgreSQL, volume, healthcheck và điều kiện phụ thuộc của ứng dụng (tiếp).", "9"),
        ("Hình 2.2b. Phần tiếp của compose gồm pgAdmin, networks cách ly và volume bền vững.", "9"),
        ("Hình 2.3. Lược đồ cơ sở dữ liệu hotel_db, cấu trúc bảng và khóa ngoại quan hệ.", "10"),
        ("Hình 2.4. Giao diện Tìm kiếm và Form đặt phòng khách sạn trực tuyến có hình ảnh, giá phòng.", "11"),
        ("Hình 2.5. Giao diện Quản lý Đặt chỗ và Danh sách đơn đặt của khách hàng.", "12"),
        ("Hình 2.6. Bảng rooms, bookings và customers trong pgAdmin chứng minh dữ liệu lưu trữ thành công.", "12"),
        ("Hình 3.1. Cấu hình Nginx Reverse Proxy, chứng chỉ HTTPS, Security Headers và Rate Limiting.", "14"),
        ("Hình 3.2. Kết quả kiểm tra Header HTTP và chứng chỉ HTTPS bằng lệnh curl.exe -kI.", "14"),
        ("Hình 4.1. Cấu hình dịch vụ Prometheus, Grafana, cAdvisor và các Exporter trong compose.", "16"),
        ("Hình 4.2. Sáu job thu thập số liệu giám sát trong tệp cấu hình prometheus.yml.", "17"),
        ("Hình 4.3. Giao diện Prometheus Targets hiển thị đầy đủ 6 trên 6 endpoint ở trạng thái UP.", "18"),
        ("Hình 4.4. Grafana Dashboard 1 - Giám sát tài nguyên CPU, RAM của các Container.", "19"),
        ("Hình 4.5. Grafana Dashboard 2 - Giám sát Web Server Nginx và số lượng đặt phòng.", "19"),
        ("Hình 4.6. Grafana Dashboard 3 - Giám sát kết nối và truy vấn Cơ sở dữ liệu PostgreSQL.", "20"),
        ("Hình 5.1. Cấu hình dịch vụ Loki, Promtail trong compose và tệp cấu hình promtail-config.yml.", "21"),
        ("Hình 5.2. Kết quả truy vấn LogQL toàn bộ nhật ký Nginx Reverse Proxy.", "22"),
        ("Hình 5.3. Kết quả truy vấn LogQL lọc sự kiện trong ứng dụng Web Hotel.", "22"),
        ("Hình 5.4. Kết quả truy vấn LogQL kiểm tra nhật ký CSDL PostgreSQL.", "23"),
        ("Hình 5.5. Biểu đồ LogQL thống kê tốc độ gửi yêu cầu POST qua Nginx.", "23"),
        ("Hình 6.1. Kiểm chứng thực tế các lệnh Hardening (Non-root, Read-only và Network Isolation).", "24"),
        ("Hình 7.1. Kho lưu trữ GitHub chính thức DTC245180058-D06.", "25"),
        ("Hình 7.2. Lệnh git log và trạng thái đồng bộ hoàn hảo với GitHub.", "25"),
    ]

    for fig_caption, pno in figures_list:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2.5)
        
        rf = p.add_run(fig_caption)
        rf.font.name = "Times New Roman"
        rf.font.size = Pt(10.5)
        
        dots_len = max(5, 78 - len(fig_caption))
        rdots = p.add_run(" " + "." * dots_len + " ")
        rdots.font.name = "Times New Roman"
        rdots.font.size = Pt(10)
        rdots.font.color.rgb = RGBColor(160, 160, 160)
        
        rp = p.add_run(pno)
        rp.font.name = "Times New Roman"
        rp.font.size = Pt(10.5)

    doc.add_page_break()

    # ==========================================================
    # TRANG 4: LỜI NÓI ĐẦU
    # ==========================================================
    p_intro_title = doc.add_paragraph()
    p_intro_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_intro_title.paragraph_format.space_before = Pt(10)
    p_intro_title.paragraph_format.space_after = Pt(15)
    r_intro = p_intro_title.add_run("LỜI NÓI ĐẦU")
    r_intro.font.name = "Times New Roman"
    r_intro.font.size = Pt(16)
    r_intro.font.bold = True

    add_p("Việc triển khai phần mềm không chỉ dừng ở xây dựng chức năng mà còn bao gồm chuẩn bị môi trường, lưu trữ dữ liệu và theo dõi hoạt động sau khi đưa ứng dụng vào sử dụng. Docker giúp đóng gói ứng dụng cùng các thành phần phụ thuộc, còn Docker Compose cho phép mô tả nhiều dịch vụ trong các tệp cấu hình thống nhất. Cách triển khai này phù hợp với mục tiêu thực hành của học phần Triển khai và Quản trị Hệ thống Phần mềm.")
    add_p("Trong đề tài số 06, em xây dựng và triển khai 'Hệ thống Đặt phòng Khách sạn (Hotel Reservation System)'. Đây là ứng dụng thương mại dịch vụ thiết thực phục vụ khách hàng tìm kiếm phòng nghỉ dưỡng theo hạng phòng, xem tiện nghi chi tiết, đặt phòng trực tuyến có tính toán số đêm lưu trú và tổng tiền tự động, cùng hệ thống quản lý đơn đặt phòng và thông tin khách hàng chuyên nghiệp. Website được viết bằng Node.js kết hợp framework Express, sử dụng cơ sở dữ liệu quan hệ PostgreSQL 16 để lưu trữ phòng, khách hàng, đơn đặt phòng và hóa đơn; Nginx tiếp nhận yêu cầu, xử lý mã hóa HTTPS tự ký, chuyển hướng bắt buộc HTTP sang HTTPS và chuyển tiếp đến ứng dụng. pgAdmin 4 hỗ trợ quan sát dữ liệu trong quá trình kiểm tra.")
    add_p("Bên cạnh chức năng website, đề tài triển khai Prometheus và Grafana để thu thập, hiển thị số liệu giám sát qua 3 Dashboard chuyên dụng (Container cAdvisor, Web Server Nginx + App, Database PostgreSQL); Loki và Promtail để tập trung nhật ký Docker và thực hiện các truy vấn LogQL. Các biện pháp hardening gồm phân tách 3 vùng mạng biệt lập, hệ thống file container chỉ đọc (read-only), non-root container, hạn chế cổng CSDL nội bộ và rate limiting Nginx. Git và GitHub lưu lại toàn bộ tiến trình triển khai theo 5 commit rõ ràng. Qua quá trình thực hiện, em hiểu rõ hơn mối liên hệ giữa ứng dụng, hạ tầng và công tác vận hành, đồng thời nhận thấy những nội dung cần tiếp tục cải thiện trước khi áp dụng ngoài môi trường thực hành.")

    doc.add_page_break()

    # ==========================================================
    # TRANG 5: CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG
    # ==========================================================
    add_heading1("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG")
    
    add_heading2("1.1. Giới thiệu và mục tiêu")
    add_p("Hệ thống Đặt phòng Khách sạn cung cấp giao diện trực quan cho khách hàng tìm kiếm phòng (Standard, Superior, Deluxe, Suite, VIP), lọc theo số khách, ngày nhận/trả phòng, xem chi tiết tiện nghi và tạo đơn đặt phòng trực tuyến tức thời. Mục tiêu là triển khai một ứng dụng web có cơ sở dữ liệu quan hệ mạnh mẽ, reverse proxy, giám sát và nhật ký tập trung hoàn toàn bằng Docker Compose. Hệ thống gồm 12 dịch vụ được điều phối thống nhất, phân tách rõ ràng giữa hạ tầng ứng dụng và hạ tầng quan sát.")

    add_heading2("1.2. Luồng xử lý và sơ đồ kiến trúc")
    add_p("Người dùng truy cập HTTPS (hoặc HTTP được tự động chuyển hướng sang HTTPS) đến Nginx trên cổng 443 của máy chủ. Nginx kiểm tra SSL/TLS, thêm các security headers, áp dụng rate limit rồi chuyển tiếp yêu cầu sang app:3000 qua mạng frontend. Ứng dụng Node.js dùng connection pool kết nối PostgreSQL qua mạng backend nội bộ bằng tài khoản quyền hạn chế hotel_user (áp dụng nguyên tắc Least Privilege). pgAdmin 4 kết nối PostgreSQL nhưng chỉ công bố giao diện an toàn qua Nginx tại đường dẫn /pgadmin/.")
    
    add_image_figure("hinh_1_1.png", "Hình 1.1. Kiến trúc ứng dụng, giám sát và nhật ký theo cấu hình dự án.")

    add_p("Prometheus chủ động kéo (pull) metrics định kỳ mỗi 10 giây từ chính nó, cAdvisor, Node Exporter, Postgres Exporter, Nginx Exporter và endpoint /metrics của ứng dụng web. Grafana truy vấn Prometheus để hiển thị số liệu qua 3 dashboard chuyên sâu. Với nhật ký, Promtail phát hiện container qua Docker socket, gán nhãn container và gửi log đến Loki; Grafana truy vấn Loki khi người quản trị dùng Explore bằng ngôn ngữ LogQL. Các mũi tên trong sơ đồ thể hiện hướng truy vấn hoặc gửi dữ liệu tương ứng.")

    add_heading2("1.3. Bảng thành phần và phiên bản cấu hình")
    add_p("Dưới đây là bảng tổng hợp các nhóm thành phần công nghệ và phiên bản cố định (pinned version) được sử dụng trong toàn bộ đề tài:")

    # Table 1.1
    tbl = doc.add_table(rows=6, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Nhóm", "Thành phần và phiên bản cấu hình"]
    rows_data = [
        ("Môi trường", "Ubuntu 22.04 LTS trên VMware hoặc Docker Desktop Windows; Docker Engine và Compose v2."),
        ("Ứng dụng", "Node.js 20.12.2 Alpine (Express, Vanilla JS, Pino JSON logger, prom-client); PostgreSQL 16 Alpine; pgAdmin 4."),
        ("Proxy", "Nginx 1.25.4-alpine (HTTPS tự ký, TLS 1.2/1.3, Rate limiting, OWASP Security headers)."),
        ("Giám sát", "Prometheus v2.51.2; Grafana 10.4.2; cAdvisor v0.49.1; Node Exporter v1.7.0; Nginx Exporter 1.1.0; Postgres Exporter v0.15.0."),
        ("Nhật ký", "Grafana Loki 2.9.8 và Promtail 2.9.8 (Schema v12, Docker socket service discovery); Git/GitHub quản lý cấu hình.")
    ]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
    for i, (col1, col2) in enumerate(rows_data):
        cell1 = tbl.cell(i+1, 0)
        cell2 = tbl.cell(i+1, 1)
        bg = "F1F5F9" if i % 2 == 1 else "FFFFFF"
        set_cell_background(cell1, bg)
        set_cell_background(cell2, bg)
        set_cell_margins(cell1, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell2, top=60, bottom=60, left=100, right=100)
        p1 = cell1.paragraphs[0]
        r1 = p1.add_run(col1)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        r1.font.bold = True
        p2 = cell2.paragraphs[0]
        r2 = p2.add_run(col2)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10.5)

    doc.add_page_break()

    # ==========================================================
    # TRANG 6: CHƯƠNG 2. TRIỂN KHAI WEBSITE VÀ DATABASE BẰNG DOCKER COMPOSE
    # ==========================================================
    add_heading1("CHƯƠNG 2. TRIỂN KHAI WEBSITE VÀ DATABASE BẰNG DOCKER COMPOSE")
    
    add_heading2("2.1. Dockerfile và cấu hình ứng dụng Node.js")
    add_p("Dockerfile của ứng dụng sử dụng image chính thức node:20-alpine nhằm tối ưu hóa kích thước và bảo mật. Lệnh npm ci --only=production chỉ cài đặt các thư viện sản xuất cần thiết, loại bỏ các công cụ phát triển không an toàn. Mã nguồn được đặt trong thư mục /app và cấp quyền sở hữu cho người dùng thông thường node (uid 1000). Chỉ thị USER node kích hoạt trạng thái non-root ngay trong ảnh đóng gói. EXPOSE 3000 mô tả cổng ứng dụng; cổng này không publish trực tiếp ra máy host.")

    add_image_figure("hinh_2_1.png", "Hình 2.1. Dockerfile dùng Node.js 20 Alpine, cài đặt production và chỉ định USER node.")

    add_p("Tệp server.js khởi tạo ứng dụng Express, kích hoạt trust proxy để nhận diện chính xác địa chỉ IP của khách hàng từ Nginx. Tệp db.js tạo connection pool với PostgreSQL thông qua thư viện pg (node-postgres), sử dụng Parameterized Queries ($1, $2...) để chống tấn công SQL Injection triệt để. Khi mất kết nối cơ sở dữ liệu, ứng dụng tự động kết nối lại và trả về mã lỗi HTTP 500 kèm thông báo lịch sự cho người dùng.")

    add_heading2("2.2. Dịch vụ và biến môi trường trong docker-compose.yml")
    add_p("PostgreSQL nhận các tham số khởi tạo (database hotel_db, user root và user ứng dụng) từ tệp .env. Ứng dụng web được build tại thư mục ./app và chờ PostgreSQL đạt trạng thái service_healthy mới khởi động. pgAdmin 4 nhận biến cấu hình và kết nối tự động tới máy chủ db qua tệp cấu hình servers.json. Nginx lắng nghe cổng 80 và 443 chuyển tiếp lưu lượng vào ứng dụng. Các giá trị mật khẩu thực tế tuyệt đối không đưa vào báo cáo mà lưu trong tệp .env được bảo vệ.")

    add_heading2("2.3. Mạng, volume và điều kiện khởi động tuần tự")
    add_p("Cơ sở dữ liệu PostgreSQL chỉ tham gia mạng hotel_backend có internal: true; ứng dụng web tham gia cả hotel_frontend, hotel_backend và hotel_monitoring. pgAdmin tham gia hotel_backend và hotel_frontend. Nginx tham gia hotel_frontend. Volume hotel_postgres_data lưu trữ bền vững dữ liệu tại /var/lib/postgresql/data; các tệp SQL khởi tạo được mount chỉ đọc (:ro) vào thư mục /docker-entrypoint-initdb.d/.")

    add_image_figure("hinh_2_2a.png", "Hình 2.2a. Cấu hình PostgreSQL, volume, healthcheck và điều kiện phụ thuộc của ứng dụng.")

    add_p("Phần tiếp theo của cấu hình compose xác định dịch vụ pgAdmin, mạng nội bộ hotel_backend và các volume bền vững. Nhờ đó cơ sở dữ liệu được cách ly an toàn và ứng dụng chỉ bắt đầu tiếp nhận yêu cầu khi cơ sở dữ liệu đã hoàn toàn sẵn sàng.")

    add_image_figure("hinh_2_2b.png", "Hình 2.2b. Phần tiếp của compose gồm pgAdmin, networks cách ly và volume bền vững.")

    doc.add_page_break()

    # ==========================================================
    # TRANG 10: 2.4 KHỞI TẠO CSDL
    # ==========================================================
    add_heading2("2.4. Khởi tạo CSDL hotel_db và quan hệ dữ liệu")
    add_p("Tệp postgres/init/01_init_schema.sql tạo schema hotel trong cơ sở dữ liệu hotel_db. Bảng rooms lưu trữ danh mục phòng (số phòng, tên phòng, loại phòng, giá theo đêm, sức chứa tối đa, loại giường, diện tích, ảnh và tiện nghi JSON). Bảng customers lưu trữ thông tin khách đặt phòng (họ tên, email, số điện thoại, căn cước công dân). Bảng bookings lưu đơn đặt phòng có mã duy nhất (booking_code), ngày check-in, check-out, tổng tiền và trạng thái (confirmed, cancelled). Bảng payments ghi nhận phương thức thanh toán.")

    add_image_figure("hinh_2_3.png", "Hình 2.3. Lược đồ cơ sở dữ liệu hotel_db, cấu trúc bảng và khóa ngoại quan hệ.")

    add_heading2("2.5. Khởi chạy và kiểm tra ứng dụng")
    add_p("Tại thư mục dự án, tạo file .env từ .env.example, thiết lập mật khẩu an toàn rồi khởi động toàn bộ 12 dịch vụ bằng lệnh:")
    add_p("docker compose up -d\ndocker compose ps", bold_prefix="Lệnh thực thi: ")
    add_p("Sau khi khởi chạy, script postgres/init/02_seed_data.sql tự động nạp sẵn 8 hạng phòng tiêu chuẩn và các đơn đặt phòng mẫu để sẵn sàng phục vụ kiểm thử.")

    add_heading2("2.6. Giao diện và các chức năng chính của website")
    add_p("Website Đặt phòng Khách sạn được thiết kế theo phong cách Luxury Resort 5 sao thanh lịch, hiện đại:")
    add_p("• Chức năng Danh mục & Bộ lọc phòng: Hiển thị đầy đủ danh sách phòng kèm hình ảnh chất lượng cao, giá niêm yết theo đêm, sức chứa và tiện nghi (Wifi, bể bơi, bồn tắm...). Bộ lọc cho phép tìm kiếm theo ngày nhận phòng, trả phòng, số lượng khách và hạng phòng.")
    add_p("• Chức năng Đặt phòng trực tuyến: Khách hàng chọn phòng, nhập thông tin liên hệ và khoảng thời gian lưu trú. Hệ thống tự động tính toán tổng số đêm, tổng tiền và tạo mã đặt phòng độc nhất (BK-YYYYMMDD-XXXX).")
    add_p("• Chức năng Quản lý Đặt chỗ: Cho phép nhân viên và khách hàng tra cứu trạng thái đơn đặt, quản lý lịch sử đặt phòng và thống kê doanh thu.")

    add_image_figure("hinh_2_4.png", "Hình 2.4. Giao diện Tìm kiếm và Form đặt phòng khách sạn trực tuyến có hình ảnh, giá phòng.")

    add_image_figure("hinh_2_5.png", "Hình 2.5. Giao diện Quản lý Đặt chỗ và Danh sách đơn đặt của khách hàng.")

    add_heading2("2.7. Kiểm tra dữ liệu bằng pgAdmin")
    add_p("Truy cập pgAdmin qua Nginx tại đường dẫn https://localhost/pgadmin/ hoặc qua cổng 5050, đăng nhập bằng tài khoản email quản trị admin@hotel.com. Giao diện hiển thị đầy đủ các bảng trong schema hotel của CSDL hotel_db, dữ liệu đặt phòng được ghi nhận tức thời và nhất quán.")

    add_image_figure("hinh_2_6.png", "Hình 2.6. Bảng rooms, bookings và customers trong pgAdmin chứng minh dữ liệu lưu trữ thành công.")

    doc.add_page_break()

    # ==========================================================
    # TRANG 13: CHƯƠNG 3. CẤU HÌNH NGINX REVERSE PROXY
    # ==========================================================
    add_heading1("CHƯƠNG 3. CẤU HÌNH NGINX REVERSE PROXY")
    
    add_heading2("3.1. Vai trò và nội dung nginx/nginx.conf")
    add_p("Nginx đóng vai trò là điểm tiếp nhận duy nhất (Edge Gateway) cho toàn bộ hệ thống. Máy chủ thứ nhất lắng nghe tại cổng 80, nhận các yêu cầu HTTP và chuyển hướng vĩnh viễn (301 Moved Permanently) sang giao thức an toàn HTTPS tại cổng 443. Máy chủ thứ hai lắng nghe tại cổng 443 với chứng chỉ SSL tự ký, giải mã TLS rồi chuyển tiếp lưu lượng đến app:3000 hoặc pgadmin:8080.")

    add_heading2("3.2. Security headers, HTTPS tự ký và Rate Limiting")
    add_p("Cấu hình bảo mật tại Nginx bao gồm:")
    add_p("• Chứng chỉ SSL tự ký: Được sinh bằng OpenSSL với thuật toán RSA 2048-bit, thời hạn 365 ngày qua script tạo chứng chỉ tự động.")
    add_p("• HTTP Security Headers: Bổ sung Strict-Transport-Security (HSTS), X-Frame-Options: SAMEORIGIN (chống Clickjacking), X-Content-Type-Options: nosniff (chống MIME sniffing), X-XSS-Protection và Content-Security-Policy (CSP).")
    add_p("• Che giấu phiên bản máy chủ: Chỉ thị server_tokens off loại bỏ số hiệu phiên bản Nginx trong tiêu đề HTTP phản hồi.")
    add_p("• Rate Limiting: Định nghĩa vùng nhớ limit_req_zone giới hạn tối đa 30 request/giây với burst 50 nhằm triệt tiêu các cuộc tấn công DoS và brute-force.")
    add_p("• Endpoint giám sát nội bộ: Location /nginx_status lắng nghe để phục vụ Nginx Prometheus Exporter thu thập số liệu kết nối.")

    add_image_figure("hinh_3_1.png", "Hình 3.1. Cấu hình Nginx Reverse Proxy, chứng chỉ HTTPS, Security Headers và Rate Limiting.")

    add_heading2("3.3. Kiểm tra cấu hình và phản hồi HTTP")
    add_p("Kiểm tra cú pháp cấu hình Nginx bằng lệnh docker compose exec nginx nginx -t cho kết quả thành công. Sử dụng curl.exe -kI https://localhost ghi nhận phản hồi HTTP/1.1 200 OK với đầy đủ các tiêu đề bảo mật. Kiểm tra cổng 80 bằng curl.exe -I http://localhost trả về mã 301 Moved Permanently chuyển hướng sang HTTPS.")

    add_image_figure("hinh_3_2.png", "Hình 3.2. Kết quả kiểm tra Header HTTP và chứng chỉ HTTPS bằng lệnh curl.exe -kI.")

    doc.add_page_break()

    # ==========================================================
    # TRANG 15: CHƯƠNG 4. TRIỂN KHAI PROMETHEUS VÀ GRAFANA
    # ==========================================================
    add_heading1("CHƯƠNG 4. TRIỂN KHAI PROMETHEUS VÀ GRAFANA")
    
    add_heading2("4.1. Các dịch vụ giám sát trong docker-compose.yml")
    add_p("Hạ tầng giám sát gồm 6 dịch vụ trên mạng hotel_monitoring: Prometheus v2.51.2 lưu dữ liệu tại hotel_prometheus_data với thời gian lưu trữ 15 ngày; Grafana 10.4.2 lưu cấu hình tại hotel_grafana_data, nạp tự động Datasource cùng 3 Dashboard qua cơ chế Provisioning cục bộ. Cổng quản trị được định tuyến rõ ràng: Prometheus 9090:9090 và Grafana 3001:3000.")
    add_p("cAdvisor đọc số liệu container qua các mount /sys, /var/run và /var/lib/docker với cờ privileged: true. Node Exporter đọc tài nguyên máy chủ host. Nginx Exporter truy vấn cổng nội bộ stub_status. Postgres Exporter kết nối PostgreSQL bằng chuỗi DATA_SOURCE_NAME an toàn. Ứng dụng web xuất metrics trực tiếp tại endpoint /metrics qua thư viện prom-client.")

    add_image_figure("hinh_4_1.png", "Hình 4.1. Cấu hình dịch vụ Prometheus, Grafana, cAdvisor và các Exporter trong compose.")

    add_heading2("4.2. prometheus/prometheus.yml và Datasource Provisioning")
    add_p("scrape_interval và evaluation_interval được thiết lập bằng 10 giây. Sáu job thu thập số liệu gồm: prometheus (localhost:9090), hotel-app (app:3000), cadvisor (cadvisor:8080), node-exporter (node-exporter:9100), hotel-postgres (postgres-exporter:9187) và hotel-nginx (nginx-exporter:9113).")
    add_p("Tệp grafana/provisioning/datasources/datasources.yml tạo sẵn datasource Prometheus mặc định tại http://prometheus:9090 và datasource Loki tại http://loki:3100.")

    add_image_figure("hinh_4_2.png", "Hình 4.2. Sáu job thu thập số liệu giám sát trong tệp cấu hình prometheus.yml.")

    add_heading2("4.3. Kiểm tra Prometheus Targets")
    add_p("Màn hình trạng thái Targets của Prometheus tại http://localhost:9090/targets ghi nhận toàn bộ 6 nhóm endpoint đều hiển thị trạng thái UP (1/1) màu xanh lá. Điều này khẳng định kết nối mạng nội bộ giữa Prometheus và các exporter, ứng dụng hoạt động trơn tru.")

    add_image_figure("hinh_4_3.png", "Hình 4.3. Giao diện Prometheus Targets hiển thị đầy đủ 6 trên 6 endpoint ở trạng thái UP.")

    add_heading2("4.4. Trực quan hóa 3 Dashboard chuyên sâu trên Grafana")
    add_p("Grafana tự động nạp 3 dashboard JSON lưu trữ cục bộ trong thư mục grafana/dashboards/, hoàn toàn không phụ thuộc kết nối Internet:")
    add_p("1. Dashboard 1 - Giám sát Container (cAdvisor): Hiển thị mức sử dụng CPU từng container theo thời gian (CPU Usage Rate), dung lượng bộ nhớ RAM (Memory Usage Bytes) và lưu lượng mạng nhận/gửi (Network I/O).")
    add_p("2. Dashboard 2 - Giám sát Web Server & App (Nginx + Express): Hiển thị số kết nối Nginx đang hoạt động (Active Connections), tần suất request HTTP theo giây, tổng số lượt đặt phòng và mã trạng thái HTTP phản hồi.")
    add_p("3. Dashboard 3 - Giám sát Database (PostgreSQL 16): Hiển thị số kết nối đang mở (Active Connections), tần suất thực thi câu truy vấn (Queries/sec), dung lượng cơ sở dữ liệu và tỉ lệ trúng cache bộ nhớ (Buffer Cache Hit Ratio).")

    add_image_figure("hinh_4_4.png", "Hình 4.4. Grafana Dashboard 1 - Giám sát tài nguyên CPU, RAM của các Container.")
    add_image_figure("hinh_4_5.png", "Hình 4.5. Grafana Dashboard 2 - Giám sát Web Server Nginx và số lượng đặt phòng.")
    add_image_figure("hinh_4_6.png", "Hình 4.6. Grafana Dashboard 3 - Giám sát kết nối và truy vấn Cơ sở dữ liệu PostgreSQL.")

    doc.add_page_break()

    # ==========================================================
    # TRANG 21: CHƯƠNG 5. TRIỂN KHAI LOKI VÀ PROMTAIL
    # ==========================================================
    add_heading1("CHƯƠNG 5. TRIỂN KHAI LOKI VÀ PROMTAIL")
    
    add_heading2("5.1. Mô hình tập trung nhật ký với Loki")
    add_p("Nhật ký phân tán là một thách thức lớn trong kiến trúc container. Thay vì dùng ELK Stack nặng nề, hệ thống sử dụng Grafana Loki 2.9.8 kết hợp Promtail 2.9.8. Loki chỉ đánh chỉ mục (index) các nhãn metadata, còn nội dung log được nén thô lưu vào volume hotel_loki_data, giúp giảm thiểu tối đa tài nguyên RAM và CPU máy chủ.")

    add_heading2("5.2. Cấu hình loki-config.yml và promtail-config.yml")
    add_p("Loki được cấu hình schema v12 tương thích chuẩn giáo trình, lưu trữ cục bộ tại /loki. Promtail kết nối socket Docker qua mount /var/run/docker.sock:ro hoặc đọc trực tiếp file log JSON từ thư mục log mount của Nginx và Web App.")

    add_image_figure("hinh_5_1.png", "Hình 5.1. Cấu hình dịch vụ Loki, Promtail trong compose và tệp cấu hình promtail-config.yml.")

    add_heading2("5.3. Thực nghiệm 4 câu truy vấn LogQL trong Grafana Explore")
    add_p("Sau khi người dùng thao tác duyệt phòng và tạo đơn đặt phòng, nhật ký được chuyển về Loki và có thể truy vấn dễ dàng trên giao diện Grafana Explore:")
    add_p("1. Truy vấn toàn bộ nhật ký Nginx: {job=\"hotel-logs\"} |= \"hotel_access.log\"")
    add_p("2. Truy vấn nhật ký ứng dụng Web Hotel và bóc tách JSON: {container=\"hotel-app\"} | json")
    add_p("3. Truy vấn nhật ký cơ sở dữ liệu PostgreSQL: {container=\"hotel-postgres\"}")
    add_p("4. Biểu đồ thống kê tốc độ gửi yêu cầu POST: sum(rate({job=\"hotel-logs\"} |= \"POST\" [1m])) by (status)")

    add_image_figure("hinh_5_2.png", "Hình 5.2. Kết quả truy vấn LogQL toàn bộ nhật ký Nginx Reverse Proxy.")
    add_image_figure("hinh_5_3.png", "Hình 5.3. Kết quả truy vấn LogQL lọc sự kiện trong ứng dụng Web Hotel.")
    add_image_figure("hinh_5_4.png", "Hình 5.4. Kết quả truy vấn LogQL kiểm tra nhật ký CSDL PostgreSQL.")
    add_image_figure("hinh_5_5.png", "Hình 5.5. Biểu đồ LogQL thống kê tốc độ gửi yêu cầu POST qua Nginx.")

    doc.add_page_break()

    # ==========================================================
    # TRANG 24: CHƯƠNG 6 & 7
    # ==========================================================
    add_heading1("CHƯƠNG 6. HARDENING VÀ BẢO MẬT HỆ THỐNG")
    
    add_heading2("6.1. Các biện pháp Hardening và bằng chứng thực nghiệm")
    add_p("Hệ thống áp dụng 10 biện pháp bảo mật thực tế nhằm thu hẹp tối đa diện tích tấn công (Attack Surface):")
    add_p("1. Non-root Container: Ứng dụng chạy dưới người dùng node (uid 1000).")
    add_p("2. Read-only Root Filesystem: Container ứng dụng không cho phép ghi file vào root fs (chỉ ghi vào volume /app/logs).")
    add_p("3. Network Isolation: Mạng hotel_backend được cấu hình internal: true, ngăn chặn truy cập trực tiếp từ Internet vào CSDL PostgreSQL.")
    add_p("4. Least Privilege Database User: Tạo tài khoản chuyên dụng hotel_user chỉ có quyền trên schema hotel, không dùng quyền superuser postgres.")
    add_p("5. Ngăn chặn leo thang đặc quyền: Cấu hình security_opt: [\"no-new-privileges:true\"].")
    add_p("6. Giới hạn tài nguyên (Resource Limits): Thiết lập ngưỡng CPU (1.0) và RAM (512MB) cho từng container.")
    add_p("7. Rate Limiting trên Nginx: Giới hạn tần suất request chống DDoS và brute-force.")
    add_p("8. Che giấu thông tin máy chủ: server_tokens off.")
    add_p("9. Mã hóa bắt buộc HTTPS với TLS 1.2/1.3 và HSTS.")
    add_p("10. Bảo vệ biến môi trường mật khẩu an toàn trong tệp .env.")

    add_image_figure("hinh_6_1.png", "Hình 6.1. Kiểm chứng thực tế các lệnh Hardening (Non-root, Read-only và Network Isolation).")

    add_heading1("CHƯƠNG 7. QUẢN LÝ MÃ NGUỒN VỚI GIT VÀ GITHUB")
    
    add_heading2("7.1. Repository và nội dung quản lý")
    add_p("Toàn bộ mã nguồn, cấu hình hạ tầng và tài liệu được quản lý tập trung trên GitHub tại repository:")
    add_p("https://github.com/tran-thi-loan/DTC245180058-D06", bold_prefix="URL Repository: ")
    add_p("Tên repository tuân thủ nghiêm ngặt quy định đặt theo Mã sinh viên kết hợp Số đề tài (DTC245180058-D06). Nhánh chính main lưu trữ mã nguồn hoàn thiện, không chứa tệp rác hay mật khẩu nhạy cảm.")

    add_image_figure("hinh_7_1.png", "Hình 7.1. Kho lưu trữ GitHub chính thức DTC245180058-D06.")

    add_heading2("7.2. Khả năng tái triển khai và kiểm tra Git")
    add_p("Lệnh git log --oneline -5 hiển thị đầy đủ 5 commit chuẩn mực. Trạng thái git status xác nhận working tree hoàn toàn sạch sẽ, nhánh main đã đồng bộ 100% với origin/main trên GitHub.")

    add_image_figure("hinh_7_2.png", "Hình 7.2. Lệnh git log và trạng thái đồng bộ hoàn hảo với GitHub.")

    doc.add_page_break()

    # ==========================================================
    # TRANG 25: CHƯƠNG 8 & KẾT LUẬN
    # ==========================================================
    add_heading1("CHƯƠNG 8. KẾT QUẢ TRIỂN KHAI VÀ ĐÁNH GIÁ")
    
    add_heading2("8.1. Bảng tổng hợp đối chiếu kết quả thực nghiệm")
    add_p("Hệ thống cấu hình đầy đủ 12 dịch vụ: PostgreSQL, Web App, Nginx, pgAdmin, Prometheus, Grafana, cAdvisor, Node Exporter, Postgres Exporter, Nginx Exporter, Loki và Promtail. Toàn bộ 12 container đều ở trạng thái Up và Healthy.")

    # Table 8.1
    eval_table = doc.add_table(rows=12, cols=3)
    eval_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_eval = ["Tiêu chí đánh giá", "Minh chứng thực nghiệm và nhận xét", "Trạng thái"]
    rows_eval = [
        ("1. Docker Compose và Database", "12 container Up; PostgreSQL healthy; CSDL hotel_db lưu trữ bền vững qua volume.", "Đã xác minh thành công"),
        ("2. Website qua Nginx HTTPS", "Giao diện web truy cập an toàn qua https://localhost; tự động chuyển hướng HTTP 301.", "Đã xác minh thành công"),
        ("3. Chức năng Đặt phòng khách sạn", "Danh mục 8 phòng, tìm kiếm, lọc theo ngày/khách, đặt phòng tự động tính tiền, lưu CSDL.", "Đã xác minh thành công"),
        ("4. Nginx Security Headers", "nginx -t thành công; curl trả về đầy đủ HSTS, X-Frame-Options, CSP, server_tokens off.", "Đã xác minh thành công"),
        ("5. Prometheus Targets", "Sáu trên sáu endpoint hiển thị trạng thái UP (1/1) trên giao diện Web UI.", "Đã xác minh thành công"),
        ("6. Grafana 3 Dashboard JSON", "Tự nạp tự động 3 Dashboard (Container, Web, Database) không cần Internet qua Provisioning.", "Đã xác minh thành công"),
        ("7. Giám sát CPU/RAM Container", "cAdvisor thu thập chính xác CPU rate, Memory bytes và Network I/O của từng container.", "Đã xác minh thành công"),
        ("8. Loki và LogQL", "Promtail thu thập nhật ký Docker; thực thi 4 câu truy vấn LogQL chuẩn xác trong Grafana Explore.", "Đã xác minh thành công"),
        ("9. Hardening 10 biện pháp", "Có lệnh kiểm chứng thực tế: Non-root uid=1000, Read-only filesystem, Network isolation.", "Đã xác minh thành công"),
        ("10. GitHub và lịch sử Commit", "Repo DTC245180058-D06 có 5 commit logic, .env được bảo vệ tuyệt đối.", "Đã xác minh thành công"),
        ("11. Khả năng tái triển khai", "Khởi chạy toàn bộ hệ thống bằng 1 lệnh docker compose up -d duy nhất.", "Đã xác minh thành công")
    ]
    for j, h in enumerate(h_eval):
        cell = eval_table.cell(0, j)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
    for i, (col1, col2, col3) in enumerate(rows_eval):
        c1 = eval_table.cell(i+1, 0)
        c2 = eval_table.cell(i+1, 1)
        c3 = eval_table.cell(i+1, 2)
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for c in [c1, c2, c3]:
            set_cell_background(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=80, right=80)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(col1)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        p2 = c2.paragraphs[0]
        r2 = p2.add_run(col2)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(9.5)
        p3 = c3.paragraphs[0]
        r3 = p3.add_run(col3)
        r3.font.name = "Times New Roman"
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(22, 101, 52)
        r3.font.bold = True

    add_heading2("8.2. Hạn chế và hướng cải thiện")
    add_p("Mặc dù hệ thống đã đáp ứng vượt mức toàn bộ yêu cầu của đề tài, một số điểm có thể tiếp tục nâng cấp trong thực tế:")
    add_p("• Chứng chỉ SSL hiện tại là chứng chỉ tự ký (Self-signed) phù hợp môi trường thực hành. Khi đưa ra tên miền công cộng Internet, cần tích hợp Let's Encrypt Certbot tự động cấp chứng chỉ tin cậy.")
    add_p("• Promtail và cAdvisor hiện cần quyền truy cập Docker socket /var/run/docker.sock. Cần áp dụng Docker socket proxy để giới hạn các lệnh API cho phép.")
    add_p("• Hệ thống hiện chạy trên một máy chủ đơn lẻ. Trong tương lai cần mở rộng thành cụm Docker Swarm hoặc Kubernetes để đảm bảo tính sẵn sàng cao (High Availability).")

    add_heading1("KẾT LUẬN")
    add_p("Đề tài số 06 đã kết hợp thành công ứng dụng web đặt phòng khách sạn trực tuyến Node.js Express với hệ sinh thái quản trị và triển khai hiện đại bằng Docker Compose. Nginx cung cấp điểm truy cập an toàn qua HTTPS; pgAdmin 4 hỗ trợ quan sát dữ liệu CSDL; Prometheus và Grafana cung cấp cái nhìn trực quan về hiệu năng hệ thống qua 3 dashboard chuyên sâu; Loki và Promtail thu thập nhật ký tập trung và hỗ trợ truy vấn thông minh bằng LogQL.")
    add_p("Qua đề tài, em đã nắm vững cách phân chia mạng 3 vùng cách ly (hotel_frontend, hotel_backend internal, hotel_monitoring); lưu trữ dữ liệu bền vững bằng Docker volume; cấu hình Nginx reverse proxy an toàn; thiết lập các exporter đo lường và bóc tách nhật ký theo nhãn. Năm commit trên GitHub thể hiện rõ ràng tiến trình làm việc khoa học. Mười biện pháp Hardening thực tế đã chứng minh khả năng bảo vệ hạ tầng ở mức cao.")
    add_p("Em xin chân thành cảm ơn Thầy giáo Hoàng Văn Tâm và các Thầy Cô trong bộ môn Triển Khai Và Quản Trị Hệ Thống đã tận tình hướng dẫn, truyền đạt kiến thức quý báu giúp em hoàn thành xuất sắc đề tài này!")

    # Lưu file
    doc.save(OUTPUT_FILE_1)
    doc.save(OUTPUT_FILE_2)
    print(f">>> Report saved successfully to:\n1. {OUTPUT_FILE_1}\n2. {OUTPUT_FILE_2}")

if __name__ == "__main__":
    create_report()
