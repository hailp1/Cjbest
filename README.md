# RTM Spatial Model - Hệ Thống Bản Đồ Không Gian Phân Phối & Phân Tích Cự Ly Giao Hàng Toàn Quốc

> 🌐 **Live Website:** [https://rtm.bestcj.com/](https://rtm.bestcj.com/)  
> 📦 **Git Repository:** [https://github.com/hailp1/Cjbest.git](https://github.com/hailp1/Cjbest.git) (Nhánh `main`)  
> 📑 **Tài liệu bàn giao & Khôi phục trạng thái:** Xem chi tiết tại [`PROJECT_STATE.md`](PROJECT_STATE.md)

Hệ thống quản lý, phân tích cự ly giao hàng và trực quan hóa không gian phân phối Route-to-Market (RTM) toàn quốc cho **391 Nhà Phân Phối (NPP)** và **59,366 Điểm Bán Lẻ (Outlets)**.

---

## 🚀 Tính Năng Nổi Bật

### 1. Bản Đồ Không Gian Phân Phối Toàn Quốc (`index.html` & `ban_do_khong_gian_rtm_mekong.html`)
* **100% Mã Nguồn Mở (Leaflet GIS):** Không cần Google Maps API Key, không phụ thuộc dịch vụ tính phí.
* **Tối ưu hóa hoàn toàn cho Smartphone (Mobile Responsive):**
  - Mở trực tiếp trên điện thoại không bị tải file `document.txt`.
  - Tải trang siêu tốc (391 NPP hiển thị trong 0.2s, 59.4k outlets nạp bất đồng bộ không gây lag máy).
  - Thanh bộ lọc vuốt ngang (Horizontal Filter Chips) và bảng điều khiển kéo gập (Drawer).
* **Nút tích lọc bỏ NPP ngưng hoạt động (`[x] 🚫 Bỏ NPP Ngưng`):**
  - Tích chọn để lập tức ẩn toàn bộ **176 NPP đã ngưng hoạt động** (chấm đỏ), chỉ giữ lại **215 NPP đang hoạt động** (chấm xanh).
  - Nút bấm nhanh 1 chạm trực tiếp trên bản đồ.
* **Bộ điều khiển hiển thị lớp (Layer Visibility Toggles):**
  - `☑️ NPP (391)`: Bật/tắt mạng lưới NPP.
  - `☑️ Điểm Bán (59.4k)`: Bật/tắt điểm bán lẻ.
  - `☑️ Tia Nối (Spider Lines)`: Vẽ tia liên kết NPP với các điểm bán trực thuộc.
  - `☑️ Hàng Đông (Cold Chain)` / `☑️ Hàng Khô (Dry Chain)`: Lọc theo đặc tính bảo quản hàng hóa.
  - `☑️ Cự Ly > 45km`: Khoanh vùng các điểm nóng chi phí logistics cao.

### 2. Thẻ / Bảng Tổng Thể Phân Tích Cự Ly & Đề Xuất Trạm Hub (`📊 Cự Ly & Hub`)
* Bấm nút **`📊 Cự Ly & Hub`** trên Header hoặc nút **`📊 Báo Cáo Cự Ly`** trên bản đồ.
* Xem chi tiết:
  - Cự ly giao hàng trung bình của từng NPP.
  - Cự ly xa nhất và danh tính khách hàng xa nhất (Tên, cự ly km, phân loại hàng, địa chỉ).
  - Số lượng điểm bán >45km và tỷ lệ %.
  - Đề xuất mở trạm trung chuyển vệ tinh: ❄️ **Hub Đông Lạnh** hay 🌾 **Hub Hàng Khô**.
  - Nút **"Xem"** tự động điều hướng bản đồ đến NPP và vẽ mạng lưới giao hàng.

---

## 📊 Tóm Tắt Hiện Trạng Chuỗi Cung Ứng
* **Tổng số NPP:** 391 NPP (215 đang hoạt động, 176 ngưng hoạt động).
* **Tổng số điểm bán:** 59,366 điểm bán.
* **Cự ly trung bình toàn quốc:** **13.9 km** (Trung vị **7.5 km**).
  - `< 15 km (Vùng tối ưu):` 43,197 điểm (72.8%).
  - `15 - 30 km (Bình thường):` 10,863 điểm (18.3%).
  - `30 - 45 km (Chi phí cao):` 2,850 điểm (4.8%).
  - `> 45 km (Cần mở trạm trung chuyển):` 2,454 điểm (4.2%).
* **Điểm nóng ưu tiên mở trạm trung chuyển hàng đông (Cold Hub):**
  - **Hải Phòng (NPP Thực Phẩm Hà Hải):** 438 khách >45km (99.5%), 61.4% hàng đông.
  - **Tuyên Quang (NPP TM & DV Tuyên Quang):** 100 khách >45km (72.5%), 84.8% hàng đông đèo dốc.
* **Điểm nóng mở đại lý chuyển tiếp hàng khô (Dry Hub):**
  - **Cà Mau (NPP Dịch Vụ Vệ Sinh T):** 298 khách >45km (92.5%), 83.5% hàng khô.
  - **Cần Thơ (NPP Thương Mại Tổng Hợp):** 350 khách >45km (83.7%), 96.7% hàng khô.

---

## 🛠️ Cấu Trúc Dự Án
```
d:\SE_Project\RTM_Model/
├── index.html                           # Trang chủ chính phục vụ tại https://rtm.bestcj.com/
├── ban_do_khong_gian_rtm_mekong.html    # Bản đồ GIS không gian 391 NPP & 59.4k Outlets
├── rtm_dashboard_mien_tay.html          # Dashboard giám sát RTM miền Tây
├── outlets_data.js                      # Dữ liệu GPS 59.366 outlets dạng mảng compact (11.8MB)
├── npp_analytics_data.js                # Dữ liệu phân tích cự ly & hub 388 NPP (170KB)
├── vercel.json                          # Cấu hình routing & HTTP headers (Anti-download on Mobile)
├── PROJECT_STATE.md                     # Tài liệu bàn giao & cheat sheet khôi phục dự án
└── README.md
```
