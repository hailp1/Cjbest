# RTM Spatial Model - Hệ Thống Bản Đồ Không Gian Phân Phối & Phân Tích Cự Ly Giao Hàng Toàn Quốc

> 🌐 **Live Website:** [https://rtm.bestcj.com/](https://rtm.bestcj.com/)  
> 📦 **Git Repository:** [https://github.com/hailp1/Cjbest.git](https://github.com/hailp1/Cjbest.git) (Nhánh `main`)  
> 📑 **Tài liệu bàn giao & Khôi phục trạng thái:** Xem chi tiết tại [`PROJECT_STATE.md`](PROJECT_STATE.md)  
> 📊 **Báo cáo Chiến lược Mekong 2027:** [`BAO_CAO_PHAN_TICH_RTM_VUNG_TRANG_VA_DE_XUAT_C1.md`](BAO_CAO_PHAN_TICH_RTM_VUNG_TRANG_VA_DE_XUAT_C1.md) | Slide tương tác: [`slide_mekong_rtm_2027.html`](slide_mekong_rtm_2027.html)

Hệ thống quản lý, phân tích cự ly giao hàng, tối ưu hóa mạng lưới Route-to-Market (RTM) và phân tích doanh số không gian cho **391 Nhà Phân Phối (NPP)**, **59,366 Điểm Bán Lẻ (Outlets)** và **56,878 Cửa Hàng Census**.

---

## 🚀 Tính Năng Nổi Bật

### 1. Bản Đồ Không Gian Phân Phối Toàn Quốc (`index.html` & `ban_do_khong_gian_rtm_mekong.html`)
* **100% Mã Nguồn Mở (Leaflet GIS):** Không cần Google Maps API Key, không phụ thuộc dịch vụ tính phí.
* **Tối ưu hóa hoàn toàn cho Smartphone (Mobile Responsive):**
  - Mở trực tiếp trên điện thoại mượt mà, tải trang siêu tốc.
  - Thanh bộ lọc vuốt ngang (Horizontal Filter Chips) và bảng điều khiển kéo gập (Drawer).
* **Quản trị Nhân sự & Giám sát NPP (Có SM vs Không SM):**
  - 🟢 **NPP Có SM:** Màu xanh ngọc lục bảo (`#059669`) + icon `fa-user-tie`.
  - 🔴 **NPP Không SM:** Màu đỏ cảnh báo (`#dc2626`) + icon `fa-user-slash` + hiệu ứng nhấp nháy cảnh báo.
  - Nút bấm nhanh **`[Bỏ NPP Không SM]`**: Lập tức ẩn sạch 96 NPP không có giám sát và toàn bộ điểm bán trực thuộc.
  - Hover Tooltip: Rê chuột vào NPP có SM hiển thị gọn gàng: `NPP [Tên] ( X SM)`.
* **Quản lý & Hiển thị Điểm Bán (Outlets Controls):**
  - Nút nổi **`[🏪 Điểm Bán]`**: Bật/tắt nhanh 59,366 outlets trực tiếp trên bản đồ.
  - Bộ lọc Hàng Đông (`DONG`), Hàng Khô (`KHO`), hoặc cả hai.
  - Nút lọc **`Chỉ hiện điểm cự ly >45km`**.
  - Popup điểm bán hiển thị rõ Tên NPP quản lý và Mã NPP.

### 2. Công Cụ Khoanh Vùng Phân Tích Doanh Số (`Spatial Revenue Analytics`)
* **Nút bấm:** **`[📐 Khoanh Vùng Doanh Số]`**.
* **Chế độ khoanh vùng linh hoạt:**
  - **✏️ Đa giác tự do (Polygon/Lasso):** Click các đỉnh trên bản đồ để bao quanh một khu vực bất kỳ.
  - **⭕ Bán kính (Circle):** Click chọn tâm điểm và kéo bán kính (km).
* **Bảng điều khiển doanh số nổi (Floating Revenue Panel):**
  - Tự động phát hiện toàn bộ NPP trong vùng khoanh (thuật toán Ray-Casting & Haversine).
  - Thống kê Tổng doanh số T9/2026, Doanh số TB/NPP, số lượng NPP Có SM/Không SM.
  - Biểu đồ tiến trình phân bổ 3 nhóm ngành hàng: 🌾 **Ambient (Khô)**, 🥬 **Chilled (Mát)**, ❄️ **Frozen (Đông)**.
  - Danh sách chi tiết từng NPP và nút **Xuất CSV** tải ngay về máy.
  - Sẵn sàng mở rộng tích hợp phân tích doanh số theo Điểm bán (Outlet) trong tương lai.

### 3. Công Cụ Cắm Cờ Dự Kiến Mở NPP / C1
* **Nút bấm:** **`[🚩 Cắm Cờ Dự Kiến]`**.
* Click vào vị trí bất kỳ trên bản đồ để cắm cờ mở trạm C1 với hiệu ứng radar quét trực quan.
* Tùy chỉnh bán kính phủ sóng (10km - 50km).
* Tích hợp sẵn 4 Preset vùng trắng Mekong: **Cai Lậy** (25km), **Đức Hòa** (25km), **TP. Trà Vinh** (30km), **Ba Tri** (25km).

### 4. Slide Thuyết Trình Chiến Lược Mekong 2027
* **File:** `slide_mekong_rtm_2027.html` (12 slide tương tác với hiệu ứng chuyển trang, hỗ trợ phím mũi tên và chế độ Fullscreen).
* Báo cáo đánh giá cự ly phân phối, mật độ Golden Stores (S, A, B, C) và luận cứ mở 4 trạm C1 trọng điểm tại ĐBSCL.

---

## 🛠️ Hướng Dẫn Phát Triển & Build

Hệ thống được thiết kế theo mô hình Single-File Compiler bằng Python để đảm bảo tính tối giản, dễ bảo trì và tốc độ tải trang cao nhất:

```bash
# 1. Chạy lệnh build để tạo đồng bộ index.html và ban_do_khong_gian_rtm_mekong.html
python build_app.py

# 2. Đẩy thay đổi lên GitHub (Vercel tự động deploy sau 30s)
git add .
git commit -m "feat: mô tả tính năng mới"
git push origin main
```
