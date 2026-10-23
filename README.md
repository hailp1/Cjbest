# RTM Model - Hệ Thống Bản Đồ Không Gian Phân Phối & Phân Tích RTM Toàn Quốc

Hệ thống quản lý, phân tích và trực quan hóa không gian phân phối Route-to-Market (RTM) toàn quốc cho 391 Nhà Phân Phối (NPP) và 59,367 Điểm Bán Lẻ (Outlets).

## 🚀 Tính Năng Chính

### 1. Bản Đồ Không Gian Phân Phối Toàn Quốc (`ban_do_khong_gian_rtm_mekong.html`)
- **100% Mã Nguồn Mở & Miễn Phí (Leaflet GIS):** Không phụ thuộc Google Maps / Mapbox, không cần API Key, không watermark.
- **5 Lớp Bản Đồ Chuyên Nghiệp:** Esri Topo (mặc định), Esri Street, Esri Satellite, Esri Light Gray, OpenStreetMap.
- **Phủ Sóng Toàn Quốc:** 
  - 391 Nhà Phân Phối (Miền Nam & Miền Bắc).
  - 59,367 Điểm bán (Outlets) với tọa độ GPS thực tế.
- **Bộ Điều Khiển Lớp (Layer Visibility Checkboxes):**
  - `☑️ NPP (391)`: Bật/tắt hiển thị mạng lưới kho NPP.
  - `☑️ Điểm Bán (59.4k Outlets)`: Bật/tắt hiển thị điểm bán lẻ.
- **Lọc Đa Tầng (Cascading Filters):** Miền (Bắc/Nam) -> Vùng (Hub) -> Tỉnh/Thành -> Trạng thái -> Tìm kiếm từ khóa.
- **Hiệu Năng Cao (HTML5 Canvas Renderer):** Hiển thị hàng chục nghìn điểm bán mượt mà 60 FPS.
- **Phân Tích Bán Kính Phục Vụ:** Vòng tròn bán kính 45km / 30km / 55km đánh giá độ phủ và vùng chồng lấn.
- **Xuất Dữ Liệu:** Xuất file CSV/Excel danh sách NPP kèm số lượng điểm bán trực thuộc.

### 2. Dashboard Phân Tích RTM Miền Tây (`rtm_dashboard_mien_tay.html`)
- Dashboard giám sát sức khỏe NPP, độ bao phủ không gian, tỷ lệ thất thoát (bleeding rate), và ma trận phân hạng.

## 📂 Cấu Trúc Dự Án

```
RTM_Model/
├── ban_do_khong_gian_rtm_mekong.html      # Bản đồ GIS không gian 391 NPP & 59.4k Outlets
├── rtm_dashboard_mien_tay.html            # Dashboard phân tích RTM miền Tây
├── outlets_data.js                        # Dữ liệu GPS 59,367 điểm bán toàn quốc
├── chart.min.js                           # Thư viện biểu đồ Chart.js
├── aso.csv                                # Dữ liệu ASO
├── doanhso.csv                            # Dữ liệu doanh số bán hàng
├── Raw Data Danh Sách Nhà Phân Phối...    # File dữ liệu gốc 391 NPP (.xlsb)
├── Raw Data Danh Sách Profile Khách Hàng... # File dữ liệu gốc Profile Điểm Bán (.xlsb)
└── README.md
```

## 💻 Hướng Dẫn Sử Dụng

Mở trực tiếp file `ban_do_khong_gian_rtm_mekong.html` bằng bất kỳ trình duyệt web hiện đại nào (Chrome, Edge, Firefox). Không cần cài đặt web server hay cấu hình API Key.
