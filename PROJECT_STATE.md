# TÀI LIỆU HIỆN TRẠNG DỰ ÁN RTM SPATIAL MODEL (HANDOVER & RESTART CHEAT SHEET)
> **Cập nhật lúc:** 27/10/2026 16:30  
> **Repository Git:** https://github.com/hailp1/Cjbest.git (Branch: `main`)  
> **Production Live URL:** https://rtm.bestcj.com/  
> **Nền tảng Hosting:** Vercel (Auto-deployment khi push commit vào nhánh `main`)

---

## 1. MỤC TIÊU & BÀI TOÁN KINH DOANH (BUSINESS CONTEXT)
Dự án nhằm giải quyết bài toán tối ưu hóa mạng lưới phân phối Route-To-Market (RTM) toàn quốc cho hệ thống thực phẩm CJ Foods:
1. **Đo lường cự ly giao hàng thực tế:** Tính toán khoảng cách (km) theo công thức Haversine giữa tọa độ GPS của từng Nhà Phân Phối (NPP) và các Điểm Bán Lẻ (Outlets) do NPP đó quản lý.
2. **Xác định các điểm nóng chi phí logistics:** Các khách hàng có cự ly > 45km, khiến chi phí giao hàng cao, rủi ro rã đông hàng lạnh.
3. **Phân tích Vùng Trắng & Đề xuất mở NPP C1:**
   - Đánh giá các vùng lõm phân phối xa NPP hiện hữu (>25-35km), mật độ Golden Stores cao nhưng chưa được bao phủ trực tiếp.
   - 4 khu vực ưu tiên Mekong: **Cai Lậy** (Tiền Giang), **Đức Hòa** (Long An), **TP. Trà Vinh** (Trà Vinh), **Ba Tri** (Bến Tre).
4. **Phân loại & Giám sát quản trị nhân sự NPP (Có SM vs Không SM):**
   - Giám sát 119 NPP có nhân viên thị trường (Có SM) và 96 NPP chưa có giám sát (Không SM), cần củng cố lực lượng bán hàng.
5. **Khoanh vùng phân tích doanh số không gian (Spatial Revenue Analytics):**
   - Cho phép người dùng vẽ vùng tự do (Polygon) hoặc vòng tròn bán kính trên bản đồ để tính tổng doanh số và cơ cấu ngành hàng (**Ambient - Chilled - Frozen**) của nhóm NPP trong vùng khoanh từ dữ liệu T9/2026.
   - Sẵn sàng mở rộng tích hợp phân tích doanh số chi tiết theo từng Điểm bán (Outlet) trong các phiên làm việc tiếp theo.

---

## 2. DỮ LIỆU ĐÃ TÍCH HỢP (DATA SOURCES)

| Tên Dữ Liệu | Nguồn File Gốc | File Đã Chuẩn Hóa | Số Lượng Bản Ghi | Trạng Thái / Ghi Chú |
|:---|:---|:---|:---:|:---|
| **Danh Sách NPP** | `final_combined_391_map_data.json` | Nhúng trực tiếp trong `ALL_NPPS` | **391 NPP** | 215 Active, 176 Inactive, đầy đủ Lat/Lng, địa chỉ, tỉnh thành, miền. |
| **Phân Loại NPP & Nhân Sự** | `loaiNPP.xlsx` (Fasoo DRM) | `loai_npp.csv` | **391 NPP** | 119 Có SM, 96 Không SM. Chứa Tên GSBH, ASM/RSM, Office, Top 50, Số NVBH. |
| **Dữ Liệu Điểm Bán (Outlets)** | `Shop_all.csv` (Fasoo DRM) | `outlets_data.js` | **59,366 Outlets** | Đầy đủ tọa độ GPS, mã cửa hàng, loại hàng (Đông/Khô), cự ly đến NPP. |
| **Census Cửa Hàng Mekong** | `shop.csv` / Báo cáo Census | Trực tiếp trong phân tích | **56,878 Cửa hàng** | 639 Golden Stores (Hạng S, A, B), tăng lên khi lấy thêm nhóm C. |
| **Doanh Số T9/2026 NPP** | `Doanhso_t92026.xlsx` (Fasoo DRM) | `doanh_so_t92026_clean.csv` | **159 NPP** | Khớp 100% với NPP trên bản đồ. Tổng doanh số: **134.3 Tỷ VNĐ** (Ambient 40.1 Tỷ, Chilled 6.95 Tỷ, Frozen 87.2 Tỷ). |
| **Doanh Số & Thiết Bị Điểm Bán T9/2026** | `DoanhsoOUTLET_t92026.xlsx` (Fasoo DRM) | `outlet_sales_clean.csv` -> nhúng `outlets_data.js` | **53,441 Điểm Bán** | Khớp 50,342 điểm (84.8% điểm bán trên bản đồ). Tổng DS MTD: **38.33 Tỷ VNĐ**. **2,598 điểm có Tủ đông/mát** (Sanaky, Alaska). |

---

## 3. CÁC TÍNH NĂNG ĐÃ HOÀN THIỆN TRÊN HỆ THỐNG

### 3.1. Bản Đồ Không Gian Phân Phối (`index.html` & `ban_do_khong_gian_rtm_mekong.html`)
* **Kiến trúc Leaflet GIS:** Chạy 100% offline/tự chủ, không phụ thuộc API key trả phí.
* **Bộ lọc đa tầng:**
  - Lọc theo Miền, Vùng, Tỉnh/Thành phố.
  - Lọc theo trạng thái hoạt động: Nút `[Bỏ NPP Ngưng]` lọc bỏ 176 NPP ngưng hoạt động.
  - Lọc theo nhân sự giám sát: Nút `[Bỏ NPP Không SM]` (`btnQuickHideKhongSM`), khi bấm sẽ ẩn hoàn toàn 96 NPP không có nhân viên thị trường và toàn bộ điểm bán của các NPP này.
  - Lọc điểm bán theo ngành hàng: Hàng Đông (`DONG`), Hàng Khô (`KHO`), hoặc cả hai.
  - Lọc điểm bán xa: `Chỉ hiện điểm xa >45km`.
* **Hiển thị Marker & Phân Biệt Màu Sắc Trực Quan:**
  - 🟢 **NPP Có SM:** Màu xanh ngọc lục bảo (`#059669`) + icon `fa-user-tie`.
  - 🔴 **NPP Không SM:** Màu đỏ cảnh báo (`#dc2626`) + icon `fa-user-slash` + hiệu ứng vòng nhấp nháy `pulse-sm-warning`.
  - ⚫ **NPP Ngưng Hoạt Động:** Màu xám đậm (`#475569`) + icon `fa-lock`.
* **Hiển thị Tooltip Rê Chuột (Hover):**
  - NPP Có SM: Hiển thị `NPP [Tên NPP] ( X SM)` (ví dụ: `NPP TRẦN ĐIỀN ( 3SM)`).
  - NPP Không SM: Giữ nguyên `⚠️ NPP Không Có SM (Cần giám sát)`.
  - NPP Ngưng: `NPP Ngưng Hoạt Động`.
* **Thẻ Thông Tin Popup Chi Tiết:**
  - Popup NPP: Hiển thị ngắn gọn tình trạng nhân sự: `⚠️ Không có nhân viên (0 NV)` hoặc `👤 Có X nhân viên`. Hiển thị thêm **Doanh số T9/2026** (Ambient, Chilled, Frozen, Tổng cộng).
  - Popup Điểm bán: Hiển thị rõ **Tên NPP Quản lý** kèm **Mã NPP**.

### 3.2. Tính Năng Cắm Cờ Dự Kiến Mở NPP / C1
* **Nút bấm:** `[🚩 Cắm Cờ Dự Kiến]`.
* **Chức năng:** Click vào vị trí bất kỳ trên bản đồ để cắm cờ mở trạm C1 với hiệu ứng sóng radar tỏa ra (`radar-pulse-flag`).
* **Tiện ích:** Điều chỉnh bán kính phục vụ (10km - 50km), có sẵn 4 Preset khu vực Mekong (Cai Lậy 25km, Đức Hòa 25km, Trà Vinh 30km, Ba Tri 25km), lưu trạng thái trong `localStorage`.

### 3.3. Tính Năng Khoanh Vùng Phân Tích Doanh Số (Spatial Revenue Selection)
* **Nút bấm:** `[📐 Khoanh Vùng Doanh Số]` (`btnSpatialSelect`).
* **Chế độ khoanh vùng:**
  1. **Đa giác tự do (Polygon/Lasso):** Click các đỉnh trên bản đồ để vẽ bao quanh cụm NPP, click đúp hoặc click điểm đầu để chốt vùng.
  2. **Bán kính (Circle):** Click 1 tâm điểm và click điểm thứ 2 để kéo bán kính (km).
  3. **Xóa vùng & Thoát.**
* **Bảng điều khiển nổi phân tích doanh số (`#spatialRevenuePanel`):**
  - Tự động lọc toàn bộ NPP nằm trong vùng khoanh (thuật toán Ray-Casting & Haversine).
  - Thống kê: Số NPP (Có SM / Không SM), Tổng doanh số T9/2026, Doanh số TB/NPP.
  - Stacked Progress Bar trực quan: Tỷ lệ % và giá trị tiền của **Ambient**, **Chilled**, **Frozen**.
  - Bảng danh sách chi tiết các NPP trong vùng.
  - **Nút "Xuất CSV":** Tải ngay báo cáo UTF-8 chi tiết cho nhóm NPP vừa khoanh.

### 3.4. Dữ Liệu Doanh Số Điểm Bán (Sell-out) & Thiết Bị Đầu Tư (Tủ Đông / Mát)
* **File nguồn:** `DoanhsoOUTLET_t92026.xlsx` -> `outlet_sales_clean.csv` -> Nhúng trực tiếp vào `outlets_data.js`.
* **Chỉ số tích hợp vào từng điểm bán:**
  - **Doanh số T9 (MTD) & Doanh số T8 (M-1):** Đo lường sell-out thực tế của cửa hàng.
  - **Thiết Bị Đầu Tư:** Phân loại thiết bị tủ đông/tủ mát (Sanaky 330L, Alaska 550L, Sanaky 300L, Alaska 300L,... hoặc "Chưa đầu tư tủ"). 2,598 điểm có tủ được hiển thị nổi bật với viền vàng kim (`#eab308`) và bán kính lớn hơn.
  - **Phân Khúc VPO & Đề Xuất Hành Động:** Duy trì (🟢), Xóa MCP (🔴), Kích hoạt lại (🟡), Cảnh báo (🟡), Thu hồi Tủ (🟠 - 163 điểm nguy cơ).
  - **Nhân Sự Bán Hàng:** Tên NVBH phụ trách và Tuyến bán hàng trực tiếp.
* **Nút bấm lọc nhanh:** `[❄️ Điểm Có Tủ (2.6k)]` (`btnQuickOnlyEquip`) trên thanh công cụ cho phép sales manager lọc và hiển thị riêng các điểm bán có trang bị tủ của CJ Foods chỉ với 1 click.
* **Tích hợp Khoanh Vùng:** Khi khoanh vùng (Polygon/Circle), hệ thống tự động tổng hợp cả **Doanh số Điểm bán T9**, **Số lượng Điểm bán** và **Số lượng Tủ đông đầu tư** bên cạnh Doanh số NPP.

### 3.5. Slide Báo Cáo Chiến Lược Mekong 2027
* **File:** [slide_mekong_rtm_2027.html](file:///d:/SE_Project/RTM_Model/slide_mekong_rtm_2027.html) (12 slides tương tác, có chế độ thuyết trình phím mũi tên).
* **Báo cáo phân tích chuyên sâu:** [BAO_CAO_PHAN_TICH_RTM_VUNG_TRANG_VA_DE_XUAT_C1.md](file:///d:/SE_Project/RTM_Model/BAO_CAO_PHAN_TICH_RTM_VUNG_TRANG_VA_DE_XUAT_C1.md).
* **Bản PowerPoint gốc:** `Regional Initiative_MKD_v2.pptx`.

---

### 3.5. Kiến Trúc Tải Nhẹ & Chống Treo Đơ Trình Duyệt (Performance Architecture)
* **Tách rời luồng nạp (Lazy Loading On-Demand):**
  - Loại bỏ hoàn toàn việc tải đồng bộ file 11.85 MB (`outlets_data.js`) lúc mở trang ban đầu.
  - Mặc định khi mở trang: `showOutlets = false`. Bản đồ **tải ngay lập tức trong 0.1s - 0.2s** chỉ với 391 NPP (~300 KB).
  - Điểm bán chỉ được tải ngầm (Background prefetch sau 2.5s) hoặc nạp khi người dùng chủ động bấm `[🏪 Hiện Điểm Bán]` hoặc bấm `Hiện Điểm Bán` của 1 NPP.
  - Sửa lỗi truyền sai chỉ số tọa độ chuỗi `[o[2], o[3]]` trong hàm tính cự ly cắm cờ `addPlannedFlag` thành `[o[0], o[1]]` chuẩn.

## 4. QUY TRÌNH BUILD & RELEASE MÃ NGUỒN

Tất cả các thay đổi giao diện và dữ liệu bản đồ đều được sinh tự động thông qua script `build_app.py`:

```bash
# 1. Chạy script build để tạo đồng bộ index.html và ban_do_khong_gian_rtm_mekong.html
python build_app.py

# 2. Kiểm tra trạng thái git
git status

# 3. Stage và commit
git add build_app.py index.html ban_do_khong_gian_rtm_mekong.html doanh_so_t92026_clean.csv PROJECT_STATE.md README.md
git commit -m "feat/fix: mô tả nội dung commit"

# 4. Push lên GitHub (Vercel tự động build & deploy lên production rtm.bestcj.com trong 30 giây)
git push origin main
```

> [!NOTE]
> **Lưu ý khi mở file Excel Fasoo DRM:**
> Các file gốc nội bộ của công ty (`.xlsx`, `.csv`) được bảo vệ bằng Fasoo DRM. Khi cần đọc các file mới do người dùng cung cấp (ví dụ: file doanh số outlet sau này), hãy sử dụng script PowerShell qua Excel COM object (như mẫu trong `scratch/export_doanhso_csv.ps1`) để chuyển sang CSV UTF-8 sạch trước khi nạp vào Python.

---

## 5. KẾ HOẠCH CHO PHIÊN LÀM VIỆC TIẾP THEO (NEXT STEPS)

Khi người dùng quay lại trong phiên tiếp theo, các công việc đã được chuẩn bị sẵn:
1. **Tích hợp file chi tiết doanh số theo Điểm bán (Outlet-level Sales Data):**
   - Khi người dùng gửi file doanh số chi tiết từng Outlet, nạp dữ liệu vào cấu trúc `filteredOutlets`.
   - Hàm `processSpatialSelection` trong `build_app.py` đã sẵn sàng module hóa để tính đồng thời cả doanh số NPP lẫn doanh số các Điểm bán nằm trong vùng khoanh.
2. **Nâng cấp công cụ khoanh vùng:**
   - Bổ sung tùy chọn chọn trực tiếp các NPP bằng cách giữ phím Shift + Click trên bản đồ (Multi-select NPPs).
   - Thêm bộ lọc doanh số (ví dụ: Chỉ khoanh các NPP có doanh số > 500 triệu/tháng).
3. **Mở rộng báo cáo đề xuất C1 Mekong:**
   - Kết hợp doanh số T9/2026 vào từng vùng trắng (Cai Lậy, Đức Hòa, Trà Vinh, Ba Tri) để dự phóng doanh thu khi chuyển đổi các cửa hàng sang C1 trực thuộc.
