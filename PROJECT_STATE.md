# TÀI LIỆU HIỆN TRẠNG DỰ ÁN RTM SPATIAL MODEL (HANDOVER & RESTART CHEAT SHEET)
> **Cập nhật lúc:** 23/10/2026 20:10  
> **Repository Git:** https://github.com/hailp1/Cjbest.git (Branch: `main`)  
> **Production Live URL:** https://rtm.bestcj.com/  
> **Nền tảng Hosting:** Vercel (Auto-deployment khi push commit vào nhánh `main`)

---

## 1. MỤC TIÊU & BÀI TOÁN KINH DOANH (BUSINESS CONTEXT)
Dự án nhằm giải quyết bài toán tối ưu hóa mạng lưới phân phối Route-To-Market (RTM) toàn quốc cho hệ thống hàng tiêu dùng / thực phẩm:
1. **Đo lường cự ly giao hàng thực tế:** Tính toán khoảng cách (km) theo công thức Haversine giữa tọa độ GPS của từng Nhà Phân Phối (NPP) và các Điểm Bán Lẻ (Outlets) do NPP đó quản lý.
2. **Xác định các "Điểm nóng chảy máu chi phí logistics":** Các khách hàng có cự ly > 45km, khiến chi phí giao hàng cao, thời gian quay vòng xe dài và biên lợi nhuận bị bào mòn.
3. **Bài toán mở Đại lý chuyển tiếp (Cross-dock / Sub-depot):**
   - Đánh giá xem tại các khu vực xa (>45km), nên mở trạm trung chuyển **HÀNG ĐÔNG (Cold Chain)** hay **HÀNG KHÔ (Dry Chain)**.
   - Hàng đông lạnh bắt buộc giới hạn cự ly <25-30km bằng xe máy thùng xốp để tránh rã đông; cự ly xa >45km bắt buộc phải có kho đệm đông lạnh (Sub-depot).
4. **Trực quan hóa không gian (GIS):** Bản đồ tương tác Leaflet 100% mã nguồn mở (không cần Google API key), hỗ trợ bộ lọc đa tầng, dấu tick bật/tắt lớp, tia nối mạng lưới (Spider lines), tối ưu hóa hoàn toàn cho thiết bị di động (Smartphone).

---

## 2. KẾT QUẢ PHÂN TÍCH CHUỖI CUNG ỨNG (SUPPLY CHAIN ANALYTICS)

### 2.1. Thống kê toàn mạng lưới:
* **Tổng số NPP trong hệ thống:** 391 NPP
  - 🟢 **Đang hoạt động:** 215 NPP (Quản lý 58.926 điểm bán thực tế)
  - 🔴 **Ngưng hoạt động:** 176 NPP (Có nút tick lọc bỏ nhanh trên bản đồ)
* **Tổng số Điểm Bán (Outlets):** 59.366 điểm bán có tọa độ GPS hợp lệ
* **Cự ly giao hàng toàn quốc:**
  - Cự ly trung bình (Mean): **13.9 km**
  - Cự ly trung vị (Median): **7.5 km** (50% khách hàng nằm trong bán kính 7.5km)
  - Phân vị 90% (P90): **28.5 km**
* **Phân bố khoảng cách:**
  - `< 15 km (Vùng an toàn giao trong ngày):` 43.197 điểm (**72.8%**)
  - `15 - 30 km (Vùng giao hàng bình thường):` 10.863 điểm (**18.3%**)
  - `30 - 45 km (Vùng chi phí cao):` 2.850 điểm (**4.8%**)
  - `> 45 km (Điểm nóng cần mở trạm trung chuyển):` 2.454 điểm (**4.2%**)
* **Phân loại theo nhóm sản phẩm:**
  - Điểm bán có mua **Hàng Đông (Cold Chain):** 16.205 điểm (**27.5%**)
  - Điểm bán có mua **Hàng Khô (Dry):** 56.740 điểm (**96.3%**)

### 2.2. Các Điểm nóng cần mở trạm trung chuyển gấp:
1. **Hải Phòng (NPP 1057559 - Thực Phẩm Hà Hải):**
   - 440 khách hàng, có tới **438 khách >45km (99.5%)**, cự ly TB 60.8 km, Max 78.3 km.
   - **61.4% là HÀNG ĐÔNG.**
   - 👉 **ƯU TIÊN SỐ 1: BẮT BUỘC MỞ TRẠM CHUYỂN TIẾP HÀNG ĐÔNG (COLD HUB).**
2. **Tuyên Quang (NPP 1065021 - TM & DV Tuyên Quang):**
   - 138 khách hàng, có **100 khách >45km (72.5%)**, cự ly TB 48.1 km, Max 111.9 km.
   - **84.8% là HÀNG ĐÔNG**, địa hình đèo dốc hiểm trở.
   - 👉 **BẮT BUỘC MỞ TRẠM TRUNG CHUYỂN HÀNG ĐÔNG (TỦ ĐÔNG ĐỆM).**
3. **Cà Mau (NPP 1064388 - Dịch Vụ Vệ Sinh T):**
   - 322 khách hàng, có **298 khách >45km (92.5%)**, cự ly TB 58.9 km, Max 95.2 km.
   - Hàng đông chỉ chiếm 16.5%, chủ yếu là hàng khô (83.5%).
   - 👉 **ĐỀ XUẤT: MỞ ĐẠI LÝ CHUYỂN TIẾP HÀNG KHÔ (DRY HUB/TRANSIT AGENT).**
4. **Cần Thơ (NPP 1061282 & 1029740):**
   - Hơn 410 khách hàng >45km, cự ly Max 92.2 km. Hàng đông dưới 4%, chủ yếu là hàng khô.
   - 👉 **ĐỀ XUẤT: MÔ HÌNH CHUYỂN TẢI HÀNG KHÔ VỆ TINH.**

---

## 3. KIẾN TRÚC DỰ ÁN & CÁC FILE QUAN TRỌNG

```
d:\SE_Project\RTM_Model/
│
├── index.html                           # Entrypoint chính (Vercel phục vụ tại /)
├── ban_do_khong_gian_rtm_mekong.html    # Bản đồ GIS Leaflet toàn quốc (cùng nội dung index.html)
├── rtm_dashboard_mien_tay.html          # Dashboard thống kê RTM miền Tây
├── vercel.json                          # Cấu hình Vercel Headers (Content-Type, Content-Disposition, Cache-Control)
│
├── outlets_data.js                      # Dữ liệu nén 59.366 outlets dạng mảng compact (~11.8MB, nạp defer)
│                                        # Cấu trúc phần tử: [lat, lng, name, code, npp_code, tinh, vung, mien, channel, addr, dist, ptype]
├── npp_analytics_data.js                # Dữ liệu phân tích cự ly & hub 388 NPP (~170KB, nạp defer)
│                                        # Cấu trúc: [{npp_code, npp_name, status, is_active, province, total_outlets, avg_dist, max_dist, remote_outlets_45km, cold_pct, farthest_outlet}]
├── chart.min.js                         # Thư viện Chart.js local
│
├── Raw Data Danh Sách Nhà Phân Phối...  # File nguồn NPP (.xlsb)
├── Raw Data Danh Sách Profile Khách Hàng... # File nguồn Profile khách hàng (.xlsb)
│
├── PROJECT_STATE.md                     # Tài liệu này (Lưu giữ hiện trạng dự án)
└── README.md                            # Hướng dẫn sử dụng & tổng quan
```

### Thư mục Scratch & Script tái tạo dữ liệu (khi cần build lại):
Được lưu tại: `C:\Users\IT-Backup\.gemini\antigravity-ide\brain\05b5759a-74ee-4579-a357-dad63829fe76\scratch\`
* `final_combined_391_map_data.json`: File JSON chứa thông tin chi tiết 391 NPP đã làm sạch.
* `cleaned_customers.json`: 59.367 khách hàng đã tính toán cự ly.
* `generate_npp_analytics.py`: Script tính toán trung bình cự ly, khách hàng xa nhất và tạo `npp_analytics_data.js`.
* `build_complete_app_with_analytics.py`: Script biên dịch và sinh ra `index.html` và `ban_do_khong_gian_rtm_mekong.html`.

---

## 4. CÁC TÍNH NĂNG ĐÃ TRIỂN KHAI HOÀN TẤT TRÊN WEB & MOBILE

1. **Khắc phục triệt để lỗi tải file `document.txt` trên điện thoại:**
   - Đã cấu hình chuẩn `Content-Type: text/html; charset=utf-8` và `Content-Disposition: inline` trong `vercel.json`.
   - Cơ chế tải nạp bất đồng bộ (`defer` + polling check): Màn hình và 391 NPP hiển thị trong 0.2s, 59.4k outlets tải ngầm không làm đơ giật máy.
2. **Bộ lọc Trạng thái NPP & Nút tích Bỏ NPP Ngưng hoạt động:**
   - Dropdown chọn trạng thái: `Tất cả Trạng thái (391)` / `🟢 Đang Hoạt Động (215)` / `🔴 Ngưng Hoạt Động (176)`.
   - **Nút tích `[x] 🚫 Bỏ NPP Ngưng (176)`** trên thanh công cụ: Chạm vào là ẩn ngay lập tức 176 NPP ngưng và các điểm bán của họ.
   - **Nút bấm 1 chạm trên bản đồ:** Nút nổi `🚫 Bỏ NPP Ngưng` rất tiện cho ngón tay cái khi lướt điện thoại.
3. **Thẻ / Bảng Tổng Thể Phân Tích Cự Ly & Hub (`📊 Cự Ly & Hub`):**
   - Nút bấm tím trên Header và nút nổi `📊 Báo Cáo Cự Ly` trên bản đồ.
   - **Bộ lọc theo Vùng & Miền tích hợp trực tiếp:** Tự động đồng bộ với bộ lọc chính của bản đồ (ví dụ: đang xem Vùng Cần Thơ trên bản đồ thì mở bảng sẽ lập tức lọc các NPP Vùng Cần Thơ). Có thể chuyển đổi các Vùng (Cần Thơ, HCM, Hà Nội, Hải Phòng, Nha Trang, Đà Nẵng) ngay trong modal.
   - **4 Thẻ KPI động theo vùng:** Tự động tính toán lại cự ly trung bình, tổng điểm nóng >45km, số điểm hàng đông/khô cự ly xa của vùng được lọc.
   - Nút **"Xem"**: Tự động zoom đến NPP và vẽ tia nối đến khách hàng xa nhất.
   - Nút **"Hiện Outlet"**: Tự động đóng modal, bay đến NPP và bật hiển thị toàn bộ mạng lưới điểm bán trực thuộc.
4. **Nút Hiện Outlet & Quản lý hiển thị điểm bán đa tầng:**
   - **Nút nổi trên bản đồ:** `[🏪 Hiện/Ẩn Điểm Bán]` trên thanh điều khiển nhanh `map-quick-controls`, bấm 1 chạm để bật/tắt toàn bộ điểm bán toàn quốc (đồng bộ checkbox thanh lọc).
   - **Nút trên Popup NPP:** `[🏪 Hiện Điểm Bán (X)]` cho phép lọc nhanh chỉ hiển thị các điểm bán của NPP đó, vẽ tia nối và zoom vừa vặn cụm outlets.
   - **Thanh Banner nổi khôi phục:** Khi đang xem riêng điểm bán của 1 NPP, xuất hiện thanh thông báo nổi trên đầu bản đồ với nút `[Hiện Tất Cả]` để quay lại góc nhìn tổng thể.
   - **Nút trên từng thẻ NPP ở Sidebar & Mobile Drawer:** Xem nhanh tia nối hoặc bật các điểm bán trực thuộc.
5. **Bộ dấu tick hiển thị lớp (Layer Visibility Toggles):**
   - `☑️ NPP (391)`: Bật/tắt hiển thị NPP.
   - `☑️ Điểm Bán (59.4k)`: Bật/tắt hiển thị khách hàng.
   - `☑️ Tia Nối`: Vẽ mạng lưới liên kết NPP -> Khách hàng.
   - `☑️ Hàng Đông` / `☑️ Hàng Khô`: Lọc theo phân loại sản phẩm.
   - `☑️ Cự Ly > 45km`: Điểm sáng các vị trí cần mở hub trung chuyển.

---

## 5. HƯỚNG DẪN DÀNH CHO AGENT TIẾP THEO (DEVELOPER WORKFLOW)

Khi restart lại Antigravity, **KHÔNG CẦN ĐỌC LẠI TOÀN BỘ CODE**, chỉ cần làm theo các bước sau:

1. **Để chỉnh sửa hoặc biên dịch lại bản đồ:**
   - Script build chính thức đặt trực tiếp tại: `d:\SE_Project\RTM_Model\build_app.py`
   - Chạy: `python d:\SE_Project\RTM_Model\build_app.py` (Script tự động ghi đè chuẩn xác vào cả `index.html` và `ban_do_khong_gian_rtm_mekong.html`).
2. **Để commit và deploy lên Vercel:**
   ```powershell
   git add ban_do_khong_gian_rtm_mekong.html index.html vercel.json npp_analytics_data.js build_app.py PROJECT_STATE.md README.md
   git commit -m "feat: filter cu ly hub theo vung va lay lai nut hien outlet"
   git push origin main
   ```
   *(Lưu ý trên Windows PowerShell dùng `;` để phân tách lệnh, không dùng `&&`)*.
3. **Kiểm tra live:**
   Truy cập `https://rtm.bestcj.com/`. Vercel tự động build và cập nhật trong 10-15 giây.
