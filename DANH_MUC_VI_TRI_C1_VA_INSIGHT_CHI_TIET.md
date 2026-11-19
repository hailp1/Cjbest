# BÁO CÁO CHIẾN LƯỢC RTM: DANH MỤC VỊ TRÍ ĐẠI LÝ CẤP 1 (C1 / SUB-HUB) THEO VÙNG & HỒ SƠ INSIGHT TOÀN DIỆN

> **Đơn vị xây dựng:** Nhóm Dự án Mô hình Không gian Route-To-Market (RTM Spatial Model)  
> **Căn cứ dữ liệu:**  
> 1. Dữ liệu vận hành CJ Foods: 391 Nhà Phân Phối (215 Active, 176 Inactive) & 59,366 Điểm bán DMS.  
> 2. Dữ liệu Census Thị trường Toàn quốc: 215,353 Điểm bán (Hạng S: 1,082; Hạng A: 4,706; Hạng B: 4,350; Hạng C: 49,213; Hạng D: 41,796; Khác: 114,206).  
> 3. Dữ liệu Nhân sự & Tổ chức Bán hàng: 145 NPP quản lý chính thức, 117 NPP Có Salesman (273 NVBH) và 28 NPP Không Salesman (từ `loaiNPP.xlsx`).  
> 4. Bản đồ GIS Không gian & Tọa độ thực địa: `rtm.bestcj.com` / `http://localhost:8080/index.html`.

---

## MỤC LỤC
1. [KHUNG LÝ THUYẾT: 3 TRỤ CỘT THIẾT LẬP ĐẠI LÝ CẤP 1 (C1 / SUB-HUB)](#1-khung-lý-thuyết-3-trụ-cột-thiết-lập-đại-lý-cấp-1-c1--sub-hub)
2. [MA TRẬN TỔNG HỢP VỊ TRÍ C1 ĐỀ XUẤT TRÊN TOÀN QUỐC](#2-ma-trận-tổng-hợp-vị-trí-c1-đề-xuất-trên-toàn-quốc)
3. [HỒ SƠ INSIGHT CHI TIẾT TỪNG VỊ TRÍ C1 THEO VÙNG](#3-hồ-sơ-insight-chi-tiết-từng-vị-trí-c1-theo-vùng)
   - [3.1. Vùng Cần Thơ & Đồng Bằng Sông Cửu Long (4 Vị Trí Trọng Điểm + 2 Vị Trí Chiến Lược Cực Nam)](#31-vùng-cần-thơ--đồng-bằng-sông-cửu-long)
   - [3.2. Vùng Hải Phòng & Duyên Hải Bắc Bộ (4 Vị Trí Cấp Bách)](#32-vùng-hải-phòng--duyên-hải-bắc-bộ)
   - [3.3. Vùng Hà Nội & Trung Du Phía Bắc (3 Vị Trí Bán Sơn Địa)](#33-vùng-hà-nội--trung-du-phía-bắc)
   - [3.4. Vùng Nha Trang - Tây Nguyên & Miền Đông (2 Vị Trí Cao Nguyên + 1 Đông Nam Bộ)](#34-vùng-nha-trang---tây-nguyên)
   - [3.5. Vùng Đà Nẵng & Miền Trung (1 Vị Trí Trọng Yếu)](#35-vùng-đà-nẵng--miền-trung)
   - [3.6. Vùng TP. Hồ Chí Minh: Phân Tích Cơ Sở Chiến Lược "KHÔNG ĐẶT C1"](#36-vùng-tp-hồ-chí-minh-không-đặt-c1)
4. [MÔ HÌNH VẬN HÀNH & CHIA SẺ LỢI ÍCH (MARGIN SPLIT & LOGISTICS WORKFLOW)](#4-mô-hình-vận-hành--chia-sẻ-lợi-ích)
5. [LỘ TRÌNH TRIỂN KHAI & BỘ CHỈ SỐ KPI GIÁM SÁT](#5-lộ-trình-triển-khai--bộ-chỉ-số-kpi-giám-sát)

---

## 1. KHUNG LÝ THUYẾT: 3 TRỤ CỘT THIẾT LẬP ĐẠI LÝ CẤP 1 (C1 / SUB-HUB)

Mô hình **Đại lý Cấp 1 (C1) / Sub-Hub** không phải là việc mở thêm một NPP độc lập cạnh tranh với NPP hiện tại, mà là **thiết lập một trạm đệm hậu cần & bán hàng tinh gọn (Buffer Stock & Last-Mile Delivery Hub)** trực thuộc sự bảo trợ của NPP mẹ hoặc CJ Foods.

Quyết định lựa chọn vị trí đặt C1 bắt buộc phải thỏa mãn đồng thời **3 trụ cột cốt lõi**:

```
                              ┌────────────────────────────────────────┐
                              │  3 TRỤ CỘT CĂN CỨ THIẾT LẬP TRẠM C1    │
                              └───────────────────┬────────────────────┘
                                                  │
         ┌────────────────────────────────────────┼────────────────────────────────────────┐
         ▼                                        ▼                                        ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐        ┌──────────────────────────────┐
│     TRỤ CỘT 1: VÙNG TRẮNG    │        │  TRỤ CỘT 2: NĂNG LỰC NPP     │        │ TRỤ CỘT 3: HIỆU SUẤT SALES   │
│   & TIỀM NĂNG THỊ TRƯỜNG     │        │     & RỦI RO LOGISTICS       │        │   & CHI PHÍ THỜI GIAN CHẾT   │
├──────────────────────────────┤        ├──────────────────────────────┤        ├──────────────────────────────┤
│ • Mật độ Census Store lớn    │        │ • Cự ly kho NPP > 35 - 70km  │        │ • Sales di chuyển > 40-70km  │
│ • Nhiều điểm bán S, A, B     │        │ • Rủi ro đứt chuỗi lạnh      │        │ • Dead travel time > 40-50%  │
│ • Điểm C & D đông đúc        │        │ • Chi phí ship 15-22% đơn    │        │ • Năng suất call giảm 50%    │
│ • Tỷ lệ CJ thâm nhập < 15%   │        │ • Tần suất giao thưa (F1/F2) │        │ • NPP hiện hữu "Không SM"    │
└──────────────────────────────┘        └──────────────────────────────┘        └──────────────────────────────┘
```

### 1.1. Trụ Cột 1: Tiềm Năng Thị Trường & Bản Đồ Vùng Trắng
* **Thị trường có mật độ cửa hàng lớn:** Khu vực tập trung mật độ cao các điểm bán tạp hóa, bách hóa, chợ truyền thống, đại lý thực phẩm theo dữ liệu 215,353 điểm bán toàn quốc.
* **Tỷ lệ thâm nhập của CJ thấp (Vùng trắng):** Đối thủ (CP, Vissan, Đức Việt, Masan MeatLife, Cholimex) đã phủ sâu vào các tiệm tạp hóa, trong khi CJ chỉ mới có vài điểm bán lẻ tẻ do rào cản địa lý.
* **Cơ cấu điểm bán đạt chuẩn Golden Outlets (S, A, B):** Khu vực có nhiều cửa hàng quy mô vừa và lớn (doanh số >15 - 50 triệu/tháng) có trang bị sẵn tủ đông/tủ mát, là khách hàng mục tiêu của xúc xích tiệt trùng, xúc xích tươi, mandu, chả giò Cầu Tre, kim chi và thịt mát.

### 1.2. Trụ Cột 2: Năng Lực Giao Hàng Của NPP Hiện Tại & Rủi Ro Chuỗi Lạnh
* **Khoảng cách vượt ngưỡng an toàn (>35km đến 70km):** NPP chính thường đặt tại trung tâm tỉnh lỵ (TP. Mỹ Tho, TP. Bắc Giang, TP. Hải Phòng, TP. Buôn Ma Thuột,...). Khi giao ra các huyện ngoại vi, xe máy chở thùng xốp đá hoặc xe tải nhỏ phải chạy từ 1.5 - 2.5 giờ.
* **Nguy cơ đứt gãy chuỗi lạnh (Cold-Chain Degradation):** Đặc thù hàng đông lạnh (-18°C) và hàng mát (0 - 4°C) dưới thời tiết nắng nóng nhiệt đới (>32°C - 38°C) sẽ bị mềm vỏ, đổ mồ hôi, chua hỏng nếu thời gian vận chuyển kéo dài.
* **Ăn mòn biên lợi nhuận giao nhận:** Chi phí xăng xe, hao mòn, lương tài xế cho đơn hàng xa ngốn từ 15% - 22% giá trị đơn hàng, khiến NPP từ chối giao đơn nhỏ (<1 triệu), ép khách dồn đơn, dẫn đến tỷ lệ thiếu hàng (OOS) triền miên.

### 1.3. Trụ Cột 3: Năng Lực & Hiệu Suất Phục Vụ Của Nhân Viên Bán Hàng (Salesman)
* **Thời gian di chuyển vô ích (Dead Travel Time):** Một nhân viên bán hàng chỉ có 8 tiếng làm việc mỗi ngày. Nếu phải chạy xe máy 40 - 60km đường trường hoặc qua phà/đò, thời gian ngồi trên xe chiếm đến 3 - 4 tiếng (40% - 50% thời gian làm việc).
* **Sụt giảm nghiêm trọng năng suất viếng thăm (Call Productivity):**
  * Tiêu chuẩn ngành FMCG: **25 - 30 cuộc viếng thăm/ngày**.
  * Thực tế tuyến xa: Salesman chỉ viếng thăm được **10 - 14 cuộc/ngày**.
* **Không còn thời gian mở mới và chăm sóc trưng bày:** Salesman chỉ kịp "lướt qua" lấy đơn hàng tồn tại các mối quen, hoàn toàn không có thời gian chào hàng mới, kiểm tra hạn sử dụng (FIFO), lau dọn tủ đông hay tiếp cận các tiệm Nhóm C, D.
* **Tỷ lệ nghỉ việc (Turnover Rate) cao:** Nhân viên kiệt sức vì chạy đường xa, chi phí xăng xe cao trong khi doanh số tuyến không đủ bù đắp, dẫn đến biến động nhân sự liên tục, tuyến bán hàng thường xuyên bị bỏ trống.
* **Địa bàn có NPP "Không SM":** Hiện toàn quốc có tới 28 NPP hoàn toàn không có nhân viên đi tuyến, biến toàn bộ khu vực xung quanh thành vùng trắng thụ động.

---

## 2. MA TRẬN TỔNG HỢP VỊ TRÍ C1 ĐỀ XUẤT TRÊN TOÀN QUỐC

Dưới đây là 16 vị trí trạm C1 / Sub-Hub được xác lập từ kết quả phân tích thuật toán không gian và dữ liệu thực địa:

| Mã Trạm | Tên Trạm Đề Xuất C1 | Tỉnh / Thành | Vùng Quản Lý | Bán Kính (km) | Cự Ly NPP Mẹ Hiện Tại | Tiềm Năng Outlets Đảm Nhận | Mục Tiêu Giảm Cự Ly |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **C1-CT-01** | **C1 TT. Cai Lậy** | Tiền Giang | Cần Thơ (ĐBSCL) | 25 km | 55 – 68 km (từ Mỹ Tho) | 50 Shop A/B + 233 Shop C | Giảm từ 60km $\rightarrow$ $\le 10$km |
| **C1-CT-02** | **C1 TT. Hậu Nghĩa / Đức Hòa** | Long An | Cần Thơ (ĐBSCL) | 25 km | 42 – 55 km (từ Tân An) | 17 Shop A/B + 266 Shop C | Giảm từ 45km $\rightarrow$ $\le 8$km |
| **C1-CT-03** | **C1 TP. Trà Vinh** | Trà Vinh | Cần Thơ (ĐBSCL) | 30 km | 42 km + Phà Cổ Chiên (từ Vĩnh Long) | 87 Shop A/B + 400 Shop C | Giảm từ 42km vượt sông $\rightarrow$ Tại chỗ |
| **C1-CT-04** | **C1 TT. Ba Tri** | Bến Tre | Cần Thơ (ĐBSCL) | 25 km | 42 – 65 km (từ TP. Bến Tre) | 80 Shop A/B (Ba Tri, Bình Đại) | Giảm từ 50km $\rightarrow$ $\le 12$km |
| **C1-CT-05** | **C1 TP. Cà Mau (Tái kích hoạt)** | Cà Mau | Cần Thơ (ĐBSCL) | 35 km | 70 – 110 km (từ Sóc Trăng) | 48 Shop A/B + 1,606 Census | Cắt đứt tuyến siêu xa 70.6km |
| **C1-CT-06** | **C1 TX. Giá Rai** | Bạc Liêu | Cần Thơ (ĐBSCL) | 25 km | 58 – 80 km (từ Sóc Trăng) | 32 Shop A/B + 1,555 Census | Giảm cự ly 60km $\rightarrow$ $\le 10$km |
| **C1-HP-01** | **C1 TT. Chũ / Lục Ngạn** | Bắc Giang | Hải Phòng | 30 km | 40 – 62 km (từ TP. Bắc Giang) | 78 Shop A/B + 3,524 Census | Giảm từ 56.6km $\rightarrow$ $\le 10$km |
| **C1-HP-02** | **C1 Nghĩa Hưng / Nam Trực** | Nam Định | Hải Phòng | 25 km | 60 – 78 km (từ Hải Phòng) | 69 Shop A/B + 4,600 Census | Cắt đứt tuyến 78.3km của Hà Hải |
| **C1-HP-03** | **C1 TT. Diêm Điền / Thái Thụy**| Thái Bình | Hải Phòng | 25 km | 45 – 65 km (từ Hải Phòng/TP.TB)| 42 Shop A/B + 4,569 Census | Giảm cự ly ven biển $\rightarrow$ $\le 8$km |
| **C1-HP-04** | **C1 TX. Nghi Sơn / Tĩnh Gia** | Thanh Hóa | Hải Phòng | 30 km | 48 – 65 km (từ TP. Thanh Hóa) | 48 Shop A/B + 7,875 Census | Giảm cự ly từ 48.7km $\rightarrow$ $\le 10$km|
| **C1-HN-01** | **C1 TX. Sơn Tây & Ba Vì** | Hà Nội | Hà Nội | 25 km | 42 – 55 km (từ nội thành Hà Nội) | 62 Shop A/B + 1,200 Outlets | Bảo vệ chuỗi lạnh bán sơn địa |
| **C1-HN-02** | **C1 TP. Hòa Bình & Lương Sơn**| Hòa Bình | Hà Nội | 25 km | 50 – 75 km (từ Hà Nội) | 28 Shop A/B + 2,235 Census | Giải tỏa đường đèo dốc hiểm trở |
| **C1-HN-03** | **C1 TX. Phú Thọ & Đoan Hùng** | Phú Thọ | Hà Nội | 30 km | 38 – 65 km (từ Việt Trì) | 45 Shop A/B + 3,618 Census | Giảm cự ly đồi gò $\rightarrow$ $\le 10$km |
| **C1-NT-01** | **C1 TT. Ea Drăng / Ea H'leo** | Đắk Lắk | Nha Trang | 35 km | 60 – 85 km (từ Buôn Ma Thuột) | 42 Shop A/B + 4,460 Census | Cắt giảm 60km Quốc lộ 14 |
| **C1-NT-02** | **C1 TX. Ayun Pa & Phú Thiện** | Gia Lai | Nha Trang | 30 km | 70 – 95 km (từ Pleiku) | 31 Shop A/B + 3,335 Census | Giải tỏa vùng trũng Nam Gia Lai |
| **C1-DN-01** | **C1 TT. Kiến Giang / Lệ Thủy** | Quảng Bình | Đà Nẵng | 30 km | 45 – 65 km (từ Đồng Hới/Quảng Trị)| 13 Shop A/B + 1,748 Census | Giải tỏa tuyến vượt đèo Duy Thúy |

---

## 3. HỒ SƠ INSIGHT CHI TIẾT TỪNG VỊ TRÍ C1 THEO VÙNG

---

### 3.1. VÙNG CẦN THƠ & ĐỒNG BẰNG SÔNG CỬU LONG

#### 📍 VỊ TRÍ 1: C1 TT. CAI LẬY (TỈNH TIỀN GIANG)
* **Tọa độ GPS:** `[10.4087, 106.1158]` | **Bán kính bao phủ:** 25 km (Bao quát Huyện Cái Bè, TX. Cai Lậy, Huyện Cai Lậy và Huyện Tân Phước).
* **NPP Mẹ Liên Đới:** NPP tại TP. Mỹ Tho.

##### 1. Tiềm năng thị trường tại khu vực:
* **Mật độ điểm bán:** Tiền Giang có tổng cộng **4,315 điểm bán Census**, trong đó cụm Tây Tiền Giang (Cai Lậy - Cái Bè) tập trung hơn **1,850 điểm bán**.
* **Phân lớp khách hàng:** Khu vực có **50 điểm bán Nhóm A/B (Golden Outlets)** và **233 điểm bán Nhóm C**.
* **Đặc tính tiêu thụ:** Cai Lậy và Cái Bè là hai vựa trái cây và trung tâm giao thương sầm uất nhất miền Tây với mức thu nhập bình quân đầu người cao. Sức mua đối với các mặt hàng xúc xích tiệt trùng, xúc xích tươi và mandu ăn liền cực kỳ lớn tại các cổng trường học, chợ đầu mối và chuỗi bách hóa địa phương.
* **Tỷ lệ bao phủ CJ hiện tại:** Dưới 12% do điểm bán thường xuyên bị đứt hàng.

##### 2. Năng lực & Nút thắt giao hàng của NPP hiện tại:
* **Cự ly di chuyển:** Từ TP. Mỹ Tho chạy dọc Quốc lộ 1A xuống TX. Cai Lậy là **32 km**, xuống TT. Cái Bè là **55 km**, và giao sâu vào các xã ven sông Tiền lên tới **68 km**.
* **Rủi ro chuỗi lạnh:** Quốc lộ 1A đoạn qua Tiền Giang thường xuyên ùn tắc tại cầu Rạch Miễu và các nút giao ngã ba Cai Lậy. Xe máy chở hàng lạnh mất từ 1.5 đến 2.5 giờ dưới nhiệt độ 34°C - 36°C khiến thùng đá tan chảy, sản phẩm chả giò và xúc xích tươi mềm nhũn, biến dạng trước khi đến tủ của khách.
* **Tần suất giao hàng bị bóp nghẹt:** Do chi phí vận chuyển cao (chiếm ~18% giá trị đơn), NPP Mỹ Tho chỉ xếp lịch giao **1 lần/tuần (F1)** hoặc **2 tuần/lần (F2)**. Điểm bán muốn nhập thêm hàng cũng không có xe giao, buộc họ phải chuyển sang nhập hàng CP và Vissan từ các đại lý sỉ tại chợ Cai Lậy.

##### 3. Năng lực & Hiệu suất của Salesman hiện tại:
* **Cự ly di chuyển tuyến:** Nhân viên bán hàng xuất phát từ Mỹ Tho phải chạy xe máy hơn **50km** mới đến được điểm bán đầu tiên của tuyến Cái Bè.
* **Thời gian chết trên đường:** Mất trung bình **3.5 giờ/ngày** chỉ để chạy đi và chạy về.
* **Năng suất cuộc gọi:** Chỉ viếng thăm được **10 – 12 điểm bán/ngày** (so với chuẩn 26 điểm/ngày). Nhân viên không có thời gian chào hàng mới hay kiểm tra tủ đông, thường chỉ ghé lấy đơn nhanh rồi vội vã chạy về trước khi trời tối.

> [!IMPORTANT]
> **INSIGHT QUYẾT ĐỊNH ĐẶT C1 TẠI CAI LẬY:**  
> Đặt C1 tại TT. Cai Lậy biến kho trung chuyển này thành **trạm tiếp vận cách Cái Bè chỉ 15km và Mỹ Tho 30km**. NPP Mỹ Tho chỉ cần chạy 1 chuyến xe tải lớn chở hàng khô & đông lạnh dồn vào C1 mỗi tuần một lần (Bulk Drop). Nhân viên bán hàng tại chỗ của C1 sẽ dùng xe máy giao hàng tinh gọn trong bán kính 10km, nâng tần suất phục vụ lên **tuần 2 - 3 lần (F4/F6)**, giúp doanh số khu vực này ước tính **tăng trưởng từ 40% – 60% ngay sau 3 tháng**.

---

#### 📍 VỊ TRÍ 2: C1 TT. HẬU NGHĨA / ĐỨC HÒA (TỈNH LONG AN)
* **Tọa độ GPS:** `[10.8872, 106.4485]` | **Bán kính bao phủ:** 25 km (Bao quát Huyện Đức Hòa, Đức Huệ, Bến Lức Bắc và Củ Chi giáp ranh).
* **NPP Mẹ Liên Đới:** NPP tại TP. Tân An.

##### 1. Tiềm năng thị trường tại khu vực:
* **Mật độ điểm bán:** Huyện Đức Hòa là thủ phủ công nghiệp của Long An với hơn 20 khu công nghiệp lớn (Tân Đức, Hải Sơn, Xuyên Á,...) tập trung hàng trăm ngàn công nhân. Toàn huyện có **17 Golden Outlets A/B** và **266 điểm bán Nhóm C**.
* **Đặc tính tiêu thụ:** Nhu cầu tiêu thụ các sản phẩm chế biến sẵn ăn liền, xúc xích, mandu, chả giò, đồ ăn vặt đóng gói cho công nhân sau ca làm việc cực kỳ lớn. Doanh số tiêu thụ nhóm hàng lạnh tại các cửa hàng tạp hóa cổng KCN Đức Hòa cao gấp 2.5 lần các khu vực nông nghiệp thuần túy.

##### 2. Năng lực giao hàng của NPP hiện tại:
* **Cự ly vận chuyển:** Từ TP. Tân An lên TT. Hậu Nghĩa / Đức Hòa là **42 – 55 km** qua các tuyến đường tỉnh ĐT824, ĐT825 hẹp, nhiều bụi và xe container tải nặng.
* **Nút thắt:** NPP Tân An nằm ở phía Nam tỉnh Long An, địa bàn phân tán. Việc giao hàng lên cực Bắc (Đức Hòa, Đức Huệ) giống như phải đi sang một tỉnh khác, chi phí vận tải đội lên rất cao khiến NPP thường xuyên gom đơn 5 – 7 ngày mới giao một lần.

##### 3. Năng lực & Hiệu suất của Salesman:
* Salesman chạy từ Tân An lên Đức Hòa mất gần 2 tiếng đồng hồ. Thể lực suy giảm do nắng bụi đường công nghiệp. Khi đến nơi, các cửa hàng tạp hóa công nhân thường mở cửa sớm (6h - 8h) hoặc chiều muộn (17h - 20h), lệch khung giờ làm việc của Sales đi xa, dẫn đến tỷ lệ gặp chủ tiệm chỉ đạt dưới 60%.

> [!TIP]
> **INSIGHT ĐẶT C1 TẠI ĐỨC HÒA:**  
> Đặt C1 tại TT. Hậu Nghĩa / Đức Hòa cho phép **khai thác trọn vẹn thị trường công nhân KCN**. C1 chủ động giao hàng vào khung giờ chiều tối (17h - 19h) khi các tiệm tạp hóa KCN bán chạy nhất. Đồng thời cắt giảm 45km vận chuyển từ Tân An, chuyển hóa 266 tiệm nhóm C thành mạng lưới tiêu thụ xúc xích và bánh bao/mandu ổn định.

---

#### 📍 VỊ TRÍ 3: C1 TP. TRÀ VINH (TỈNH TRÀ VINH)
* **Tọa độ GPS:** `[9.9348, 106.3456]` | **Bán kính bao phủ:** 30 km (Bao quát TP. Trà Vinh, Huyện Châu Thành, Càng Long, Cầu Kè, Tiểu Cần).
* **NPP Mẹ Liên Đới:** NPP tại Vĩnh Long hoặc Bến Tre.

##### 1. Tiềm năng thị trường:
* **Quy mô điểm bán:** Toàn tỉnh Trà Vinh có **2,005 điểm bán Census**, trong đó TP. Trà Vinh và phụ cận sở hữu **87 Golden Outlets A/B** và hơn **400 điểm bán Nhóm C**.
* **Thị trường trắng của CJ:** Trà Vinh hiện là một trong những vùng trũng lớn nhất của CJ tại ĐBSCL do chưa có NPP độc lập đủ mạnh cắm chốt trong tỉnh.

##### 2. Năng lực giao hàng hiện tại:
* **Rào cản địa lý (Vượt sông Cổ Chiên):** NPP Vĩnh Long phải giao hàng qua Quốc lộ 53 với cự ly **42 – 65 km**. Trước đây phải qua phà, nay tuy có cầu Cổ Chiên nhưng chi phí BOT và thời gian chạy xe vẫn là rào cản rất lớn đối với xe giao hàng.
* Hàng đông lạnh giao từ Vĩnh Long sang Trà Vinh gần như 100% bị đứt chuỗi lạnh nếu đi bằng xe máy có thùng xốp thông thường.

##### 3. Hiệu suất của Salesman:
* Tuyến Vĩnh Long - Trà Vinh là tuyến "ác mộng" của Salesman vì đường hẹp, nhiều cầu cong. Tỷ lệ nhân viên nghỉ việc tại tuyến này lên đến 45%/quý. Điểm bán bị bỏ rơi nhiều tháng liền không có người chăm sóc.

> [!IMPORTANT]
> **INSIGHT ĐẶT C1 TẠI TP. TRÀ VINH:**  
> Thiết lập C1 ngay tại trung tâm TP. Trà Vinh là bước đi chiến lược để **chính thức cắm cờ tại một tỉnh hoàn chỉnh**. C1 sẽ tiếp quản ngay 87 Golden Outlets và 400 tiệm Nhóm C, rút cự ly giao hàng nội tỉnh xuống **dưới 8km**, nâng tần suất viếng thăm lên F4/F8.

---

#### 📍 VỊ TRÍ 4: C1 TT. BA TRI (TỈNH BẾN TRE)
* **Tọa độ GPS:** `[10.0381, 106.5986]` | **Bán kính bao phủ:** 25 km (Bao quát Huyện Ba Tri, Bình Đại và Thạnh Phú ven biển).
* **NPP Mẹ Liên Đới:** NPP TP. Bến Tre.

##### 1. Tiềm năng thị trường:
* Bến Tre có **3,586 điểm bán Census**. Dải ven biển 3 cù lao Ba Tri - Bình Đại có **80 Golden Outlets A/B**. Đây là khu vực kinh tế biển phát triển mạnh mẽ (nuôi tôm, đánh bắt hải sản), người dân có sức chi tiêu thực phẩm chế biến rất cao.

##### 2. Năng lực giao hàng & Salesman:
* Từ TP. Bến Tre ra TT. Ba Tri mất **42 km**, ra các xã ven biển Bình Đại mất hơn **65 km**. Địa hình sông nước chia cắt cù lao khiến xe giao hàng phải chạy vòng vèo qua nhiều cầu nhỏ hạn chế tải trọng.
* Salesman mất trọn cả buổi sáng chỉ để di chuyển đến địa bàn ven biển, năng suất viếng thăm chỉ đạt 11 điểm/ngày.

> [!NOTE]
> **INSIGHT ĐẶT C1 TẠI BA TRI:**  
> Biến Ba Tri thành **trung tâm tiếp vận duyên hải Bến Tre**, khép kín toàn bộ mạng lưới phân phối khu vực kinh tế biển mà NPP TP. Bến Tre không đủ sức với tới.

---

#### 📍 VỊ TRÍ CHIẾN LƯỢC BỔ SUNG: C1 CÀ MAU & C1 BẠC LIÊU (CỰC NAM)
* **Hiện trạng rủi ro:** Báo cáo RTM ghi nhận NPP Hưng Lộc Phát (Sóc Trăng) đang phải "gánh" các đơn hàng tận Bạc Liêu và Cà Mau với cự ly cực đại **70.6 km – 110 km**, vi phạm nghiêm trọng giới hạn an toàn logistics.
* **Hành động đề xuất:**
  * **C1 TP. Cà Mau:** **Tái kích hoạt ngay 1 trong 6 NPP đang ngưng hoạt động tại Cà Mau** (đã có sẵn pháp nhân và mặt bằng kho cũ). Tiếp quản 48 shop A/B và 1,606 census store toàn tỉnh Cà Mau.
  * **C1 TX. Giá Rai (Bạc Liêu):** Đặt tại ngã ba kinh tế Giá Rai - Phước Long - Đông Hải, cắt giảm 60km vận chuyển từ Sóc Trăng xuống.

---

### 3.2. VÙNG HẢI PHÒNG & DUYÊN HẢI BẮC BỘ

> [!WARNING]
> **VÙNG BÁO ĐỘNG ĐỎ VỀ CỰ LY:** Cự ly bình quân toàn vùng lên tới **21.3 km (cao nhất toàn quốc)**, có tới **1,118 điểm bán >45km (chiếm 8.6%)**. Nhu cầu cấp thiết phải chia nhỏ bán kính bằng 4 trạm C1.

#### 📍 VỊ TRÍ 1: C1 TT. CHŨ / LỤC NGẠN (TỈNH BẮC GIANG)
* **Tọa độ GPS:** `[21.3653, 106.5654]` | **Bán kính bao phủ:** 30 km (Lục Ngạn, Sơn Động, Lục Nam).
* **NPP Mẹ:** NPP Thái Đạt / NPP TP. Bắc Giang.
* **Tiềm năng thị trường:** Bắc Giang có **3,524 điểm bán Census**. Cụm Lục Ngạn & Sơn Động sở hữu **78 Shop A/B** (doanh số tiềm năng **1.04 Tỷ/tháng**). Là trung tâm tiêu thụ hàng đầu vào vụ mùa nông sản.
* **Năng lực giao hàng & Sales:** Cự ly giao hiện tại từ TP. Bắc Giang lên Chũ là **40 km**, lên Sơn Động là **62 km** (đường đèo dốc gồ ghề). NPP Thái Đạt đang phải duy trì tuyến giao dài **56.6 km**. Salesman kiệt sức vì vượt dốc, tỷ lệ viếng thăm chỉ đạt 12 điểm/ngày.
* **Insight C1:** C1 TT. Chũ giải phóng hoàn toàn tuyến 56.6km cho NPP Thái Đạt, rút cự ly giao hàng vùng đồi xuống **$\le 10$km**, bảo toàn nhiệt độ xúc xích tiệt trùng và đồ nguội.

#### 📍 VỊ TRÍ 2: C1 NGHĨA HƯNG / NAM TRỰC (TỈNH NAM ĐỊNH)
* **Tọa độ GPS:** `[20.2185, 106.1512]` | **Bán kính bao phủ:** 25 km (Nghĩa Hưng, Nam Trực, Hải Hậu, Xuân Trường).
* **NPP Mẹ:** NPP Hà Hải.
* **Tiềm năng thị trường:** Nam Định có **4,600 điểm bán Census**, khu vực các huyện phía Nam tập trung **69 Shop A/B**. Mật độ dân cư dày đặc bậc nhất đồng bằng Bắc Bộ.
* **Năng lực giao hàng & Sales:** NPP Thực Phẩm Hà Hải đóng tại Hải Phòng nhưng phải chạy xe vượt tỉnh sang tận các huyện ven biển Nam Định với cự ly cực đoan lên tới **60 – 78.3 km**. Đây là tuyến đường xa nhất và lỗ chi phí logistics nặng nề nhất toàn quốc.
* **Insight C1:** C1 Nam Định chấm dứt hoàn toàn tình trạng giao hàng vượt tỉnh vô lý của NPP Hà Hải. Toàn bộ 69 điểm bán A/B được chuyển giao về C1 phục vụ tại chỗ.

#### 📍 VỊ TRÍ 3: C1 TT. DIÊM ĐIỀN / THÁI THỤY (TỈNH THÁI BÌNH)
* **Tọa độ GPS:** `[20.5701, 106.5824]` | **Bán kính bao phủ:** 25 km (Thái Thụy, Tiền Hải, Kiến Xương ven biển).
* **Tiềm năng thị trường:** Thái Bình có **4,569 điểm bán Census**, dải ven biển có **42 Shop A/B**.
* **Năng lực giao hàng:** Khoảng cách từ TP. Thái Bình hoặc Hải Phòng ra Diêm Điền từ **45 – 65 km**. Ven biển ẩm ướt, gió mặn, việc đi lại khó khăn vào mùa mưa bão.
* **Insight C1:** Biến Diêm Điền thành cảng tập kết hàng hóa thực phẩm cho toàn dải duyên hải Đông Bắc Thái Bình, giảm cự ly phục vụ xuống dưới 8km.

#### 📍 VỊ TRÍ 4: C1 TX. NGHI SƠN / TĨNH GIA (TỈNH THANH HÓA NAM)
* **Tọa độ GPS:** `[19.3321, 105.7892]` | **Bán kính bao phủ:** 30 km (Khu kinh tế Nghi Sơn, Nông Cống, Quảng Xương Nam).
* **Tiềm năng thị trường:** Thanh Hóa là tỉnh lớn nhất với **7,875 điểm bán Census**. Cụm kinh tế trọng điểm Nghi Sơn có **48 Shop A/B** phục vụ hàng chục ngàn chuyên gia, công nhân lọc hóa dầu và công nghiệp nặng.
* **Năng lực giao hàng & Sales:** Từ TP. Thanh Hóa xuống Nghi Sơn là **48.7 km** dọc Quốc lộ 1A đông đúc xe container. Xe giao hàng chạy mất 1.5 giờ, chi phí xăng dầu rất cao.
* **Insight C1:** Khai thác tối đa sức mua cực lớn của KKT Nghi Sơn. Giảm cự ly giao hàng từ 48.7km xuống dưới 10km, giao hàng hằng ngày cho các canteen, đại lý thực phẩm quanh nhà máy.

---

### 3.3. VÙNG HÀ NỘI & TRUNG DU PHÍA BẮC

#### 📍 VỊ TRÍ 1: C1 TX. SƠN TÂY & BA VÌ (HÀ NỘI TÂY)
* **Tọa độ GPS:** `[21.1384, 105.5061]` | **Bán kính bao phủ:** 25 km (Sơn Tây, Ba Vì, Thạch Thất, Phúc Thọ).
* **Tiềm năng thị trường:** Khu vực bán sơn địa phía Tây Hà Nội có hơn **1,200 điểm bán**, sở hữu **62 Shop A/B**. Ba Vì là trung tâm du lịch sinh thái, tiêu thụ lượng lớn thực phẩm mát, xúc xích và món ăn chế biến sẵn vào dịp cuối tuần.
* **Năng lực giao hàng & Rủi ro chuỗi lạnh:** Hà Nội có tỷ trọng điểm bán nhập hàng lạnh cao nhất cả nước (**36.1%**). Các NPP nội thành chạy xe tải ra Sơn Tây - Ba Vì gặp cảnh ùn ứ Đại lộ Thăng Long và Quốc lộ 32, xe mất từ 2 - 2.5 giờ, nhiệt độ thùng lạnh tăng cao gây rủi ro lớn cho hàng tươi/mát.
* **Insight C1:** C1 Sơn Tây đóng vai trò chốt chặn cửa ngõ phía Tây, bảo vệ 100% chuỗi lạnh cho 62 shop A/B và tiếp ứng cho các khu nghỉ dưỡng/homestay Ba Vì.

#### 📍 VỊ TRÍ 2: C1 TP. HÒA BÌNH & LƯƠNG SƠN (TỈNH HÒA BÌNH)
* **Tọa độ GPS:** `[20.8172, 105.3384]` | **Bán kính bao phủ:** 25 km (TP. Hòa Bình, Kỳ Sơn, Lương Sơn).
* **Tiềm năng & Năng lực:** Hòa Bình có **2,235 điểm bán Census**, **28 Shop A/B**. Tuyến đường Dốc Kẽm và Quốc lộ 6 có độ dốc cao, quanh co. Xe tải NPP từ Hà Nội chạy lên mất nhiều dầu và hao mòn phanh/lốp.
* **Insight C1:** Giải phóng các NPP Hà Nội khỏi cung đường đèo dốc hiểm trở, thiết lập trạm đệm ngay tại TP. Hòa Bình để phân phối sâu vào các huyện Đà Bắc, Cao Phong.

#### 📍 VỊ TRÍ 3: C1 TX. PHÚ THỌ & ĐOAN HÙNG (TỈNH PHÚ THỌ)
* **Tọa độ GPS:** `[21.4012, 105.2183]` | **Bán kính bao phủ:** 30 km (TX. Phú Thọ, Đoan Hùng, Thanh Ba, Cẩm Khê).
* **Tiềm năng thị trường:** Phú Thọ có **3,618 điểm bán Census**, cụm trung du phía Bắc tỉnh có **45 Shop A/B** (doanh số tiềm năng **727 Triệu/tháng**).
* **Insight C1:** Thay thế các chuyến giao hàng cự ly >38km từ TP. Việt Trì lên, gom cụm giao hàng tại TX. Phú Thọ với cự ly bình quân $\le 10$km.

---

### 3.4. VÙNG NHA TRANG - TÂY NGUYÊN & ĐÔNG NAM BỘ

#### 📍 VỊ TRÍ 1: C1 TT. EA DRĂNG / EA H'LEO (BẮC ĐẮK LẮK)
* **Tọa độ GPS:** `[13.2005, 108.2052]` | **Bán kính bao phủ:** 35 km (Ea H'leo, Krông Năng, Buôn Hồ Bắc).
* **Tiềm năng thị trường:** Đắk Lắk có **4,460 điểm bán Census**. Cụm Bắc Đắk Lắk tập trung **42 Shop A/B**. Vùng kinh tế cà phê, sầu riêng, hồ tiêu trù phú với các thị trấn thị tứ giàu có.
* **Năng lực giao hàng & Sales:** Từ TP. Buôn Ma Thuột chạy dọc Quốc lộ 14 lên Ea H'leo là **82 km**. Tuyến đường dài, nhiều đèo dốc và trạm CSGT. NPP BMT chỉ xếp xe đi tuyến 1 lần/tuần, điểm bán muốn nhập lẻ vài thùng xúc xích tiệt trùng hay kim chi đều bị từ chối vì không bõ công xe chạy.
* **Insight C1:** **Tái thẩm định 1 trong 7 NPP đang ngưng hoạt động tại Đắk Lắk** để đặt C1 tại Buôn Hồ / Ea H'leo. Rút ngắn cự ly giao hàng từ 82km xuống còn 15km, phục vụ tuần 2 lần.

#### 📍 VỊ TRÍ 2: C1 TX. AYUN PA & PHÚ THIỆN (NAM GIA LAI)
* **Tọa độ GPS:** `[13.4033, 108.4452]` | **Bán kính bao phủ:** 30 km (TX. Ayun Pa, Phú Thiện, Ia Pa, Krông Pa).
* **Tiềm năng & Năng lực:** Gia Lai có **3,335 điểm bán Census**. Thung lũng sông Ba (Ayun Pa) là vùng biệt lập, cách TP. Pleiku hơn **70.4 km** qua đèo Chư Sê. Điểm bán bị cô lập gần như hoàn toàn với hệ thống DMS của CJ.
* **Insight C1:** Tái kích hoạt 1 NPP cũ tại Gia Lai thành C1 Ayun Pa, tiếp quản 31 shop A/B, xóa bỏ tình trạng cô lập địa lý.

---

### 3.5. VÙNG ĐÀ NẴNG & MIỀN TRUNG

#### 📍 VỊ TRÍ: C1 TT. KIẾN GIANG / LỆ THỦY (TỈNH QUẢNG BÌNH)
* **Tọa độ GPS:** `[17.2182, 106.7824]` | **Bán kính bao phủ:** 30 km (Lệ Thủy, Quảng Ninh, Đồng Hới Nam).
* **Tiềm năng thị trường:** Quảng Bình có **1,748 điểm bán Census**, sở hữu **13 Shop A/B**.
* **Năng lực giao hàng:** NPP Duy Thúy phải gánh tuyến kéo dài qua đèo, đường hẹp và gió Lào khắc nghiệt vào mùa hè, mưa bão lũ lụt vào mùa đông. Cự ly giao trên 55km khiến tỷ lệ đơn thành công thấp.
* **Insight C1:** Đặt C1 tại TT. Kiến Giang làm chốt chặn bảo quản hàng khô và hàng đông lạnh cho toàn bộ khu vực trũng Lệ Thủy - Quảng Ninh.

---

### 3.6. VÙNG TP. HỒ CHÍ MINH: PHÂN TÍCH CƠ SỞ CHIẾN LƯỢC "KHÔNG ĐẶT C1"

Khác biệt hoàn toàn với 5 vùng trên, kết quả phân tích dữ liệu không gian khẳng định: **TUYỆT ĐỐI KHÔNG MỞ THÊM ĐẠI LÝ C1 TẠI TP. HỒ CHÍ MINH**.

```
             MA TRẬN SO SÁNH GIỮA CÁC TỈNH XA VÀ TP. HỒ CHÍ MINH
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│       CHỈ SỐ RTM          │     CÁC VÙNG CẦN MỞ C1    │      TP. HỒ CHÍ MINH      │
├───────────────────────────┼───────────────────────────┼───────────────────────────┤
│ Bán kính phục vụ bình quân│ 19.4 km – 21.3 km         │ ⭐ 6.2 km (Tối ưu nhất)   │
│ Tỷ lệ điểm giao >45km     │ 8.6% – 10.0% (Báo động đỏ)│ ⭐ 0.0% (Không có điểm xa)│
│ Số lượng NPP Active       │ 34 – 39 NPP / Vùng rộng lớn│ ⭐ 35 NPP / Thành phố     │
│ Vấn đề cốt lõi            │ Cự ly xa, đứt chuỗi lạnh  │ Chồng chéo tuyến bán hàng │
│ Quyết định RTM            │ MỞ C1 / SUB-HUB VỆ TINH   │ KHÔNG MỞ C1 — IN-FILL TUYẾN│
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

#### Các luận cứ chiến lược không mở C1 tại TP.HCM:
1. **Mật độ NPP quá dày đặc:** TP.HCM hiện có **35 NPP đang hoạt động** chen chúc trong 16 quận và 5 huyện. Bán kính phục vụ trung bình của mỗi NPP chỉ là **6.2 km** (khoảng cách ngắn nhất toàn quốc).
2. **Nguy cơ xung đột kênh & Triệt tiêu lẫn nhau (Cannibalization):** Nếu mở thêm C1 tại TP.HCM, C1 sẽ lấy bớt khách hàng của các NPP lân cận, dẫn đến tranh chấp địa bàn, bán phá giá, làm gãy vỡ hệ thống chiết khấu.
3. **Bài toán của TP.HCM không phải là "Cự ly xa" mà là "Chồng chéo tuyến" (Cross-servicing):** Nhiều tuyến đường tại Quận Gò Vấp, Bình Tân, Tân Phú có tới 2 - 3 NPP cùng cho xe chạy vào giao hàng.
4. **Hành động RTM đúng đắn cho TP.HCM:**  
   * **In-fill thêm tuyến:** Bổ sung **674 Shop A & B tiềm năng** (doanh số **4.66 Tỷ/tháng**) trực tiếp vào danh sách viếng thăm của 35 NPP hiện hữu.
   * **Phân chia lại ranh giới hành chính (Territory Re-alignment):** Mỗi NPP phụ trách trọn vẹn cụm phường/quận, cấm triệt để việc bán lấn tuyến.

---

## 4. MÔ HÌNH VẬN HÀNH & CHIA SẺ LỢI ÍCH (MARGIN SPLIT & LOGISTICS WORKFLOW)

Để Đại lý C1 hoạt động bền vững và không mâu thuẫn quyền lợi với NPP mẹ, mô hình vận hành và phân chia biên lợi nhuận được thiết kế chuẩn mực như sau:

```
┌─────────────────┐       Xe tải lớn (Bulk Delivery)       ┌─────────────────┐       Xe máy thùng lạnh (Last-Mile)       ┌─────────────────┐
│     NHÀ MÁY     │  ───────────────────────────────────>  │     NPP MẸ      │  ──────────────────────────────────────>  │  TRẠM ĐỆM C1    │
│  CJ FOODS VN    │       Nguyên chuyến (Tuần 1 lần)       │ (Kho Trung Tâm) │        Giao sỉ hàng tuần / 2 lần          │  (Buffer Hub)   │
└─────────────────┘                                        └─────────────────┘                                           └────────┬────────┘
                                                                                                                                  │ Giao lẻ trong ngày
                                                                                                                                  │ (Same-day Delivery)
                                                                                                                                  ▼ Bán kính ≤ 10km
                                                                                                                         ┌─────────────────┐
                                                                                                                         │  ĐIỂM BÁN LẺ    │
                                                                                                                         │  (S, A, B, C)   │
                                                                                                                         └─────────────────┘
```

### 4.1. Cơ cấu phân bổ Biên lợi nhuận (Margin Split):
* **Tổng Margin chiết khấu của kênh GT:** Dao động từ **11% – 13%**.
* **Phân bổ khi có trạm C1:**
  * **NPP Mẹ:** Hưởng **4.0% – 4.5%** (cho chức năng: Bảo lãnh công nợ với CJ, tiếp nhận đơn lớn, lưu kho tổng và chịu chi phí xe tải chở hàng xuống trạm C1).
  * **Đại lý C1:** Hưởng **6.5% – 7.5%** (cho chức năng: Duy trì kho mát/đông tại địa phương, giao hàng dặm cuối bằng xe máy thùng lạnh, thu tiền mặt từ điểm bán lẻ và bảo toàn hàng hóa).
  * **Thưởng KPI đạt doanh số & chất lượng kho:** **1.0%** do CJ Foods trực tiếp chi trả cho C1 nếu đảm bảo nhiệt độ bảo quản và tỷ lệ OOS dưới 3%.

### 4.2. Tiêu chí lựa chọn đối tác C1:
1. **Mặt bằng & Thiết bị:** Có mặt bằng thuận tiện xe tải 2.5 tấn ra vào; có diện tích kho tối thiểu $40m^2$; có sẵn hoặc cam kết lắp đặt tủ đông (dung tích $\ge 1,000$ lít) và tủ mát. CJ hỗ trợ 50% chi phí biển bảng nhận diện thương hiệu.
2. **Khả năng tài chính:** Vốn xoay vòng hàng hóa từ $150 – 300$ Triệu VNĐ.
3. **Quan hệ địa phương:** Ưu tiên số 1 là **các Tổng đại lý bánh kẹo/tạp hóa lớn nhất thị trấn** hoặc **tái kích hoạt các NPP cũ đã ngưng hoạt động** nhưng còn uy tín và quan hệ tốt với các tiệm tạp hóa trong huyện.

---

## 5. LỘ TRÌNH TRIỂN KHAI & BỘ CHỈ SỐ KPI GIÁM SÁT

### 5.1. Lộ trình 3 giai đoạn:
* **Giai đoạn 1 (Tháng 1 – Tháng 2): Khai thác Quick-Wins & Tái kích hoạt NPP cũ**
  * Ưu tiên số 1: Tái kích hoạt các vị trí đã có nền tảng cũ tại **Cà Mau, Đắk Lắk (Buôn Hồ), Gia Lai (Ayun Pa)**.
  * Phủ ngay các shop A/B nằm trong bán kính $\le 15$km quanh các trạm này.
* **Giai đoạn 2 (Tháng 3 – Tháng 4): Thiết lập 4 Trạm Cấp Bách tại Đồng Bằng**
  * Ký hợp đồng C1 tại: **Cai Lậy (Tiền Giang), Hậu Nghĩa (Long An), Lục Ngạn (Bắc Giang), Nghĩa Hưng (Nam Định)**.
  * Cung cấp tủ đông và cài đặt hệ thống DMS bán hàng cho nhân sự C1.
* **Giai đoạn 3 (Tháng 5 – Tháng 6): Hoàn thiện các trạm Duyên hải & Miền núi**
  * Mở các trạm: **Trà Vinh, Ba Tri (Bến Tre), Diêm Điền (Thái Bình), Nghi Sơn (Thanh Hóa), Sơn Tây (Hà Nội), Lệ Thủy (Quảng Bình)**.
  * Đánh giá hiệu quả kinh doanh và chuẩn hóa quy trình sang năm tiếp theo.

### 5.2. Bộ chỉ số đo lường hiệu quả (KPI Dashboard):

| Nhóm Chỉ Số | Tên Chỉ Số KPI | Hiện Trạng Trước C1 | Mục Tiêu Sau Khi Mở C1 | Phương Pháp Đo Lường |
| :--- | :--- | :---: | :---: | :--- |
| **Logistics** | **Tỷ lệ điểm bán > 45km** | **4.1% (2,452 điểm)** | **< 0.8% (< 500 điểm)** | Đo bán kính trên bản đồ GIS |
| **Logistics** | **Cự ly giao hàng bình quân** | **13.3 km** | **$\le 8.5$ km** | Tính toán ma trận khoảng cách |
| **Logistics** | **Rủi ro đứt chuỗi lạnh** | 18.5% chuyến xa | **< 1.0%** | Kiểm tra nhiệt độ khi giao hàng |
| **Kinh doanh** | **Tỷ lệ kết nạp Shop A/B** | 0% (vùng trắng) | **$\ge 75%$ sau 6 tháng** | Số shop active trên DMS |
| **Kinh doanh** | **Tỷ lệ thiếu hàng (OOS)** | 14.2% | **< 3.0%** | Báo cáo kiểm kê đơn hàng |
| **Hiệu suất Sales**| **Số cuộc viếng thăm (Calls/day)**| 10 – 14 calls/ngày | **24 – 28 calls/ngày** | GPS Check-in trên ứng dụng DMS |
| **Hiệu suất Sales**| **Thời gian chết trên đường** | 40% – 50% tổng giờ | **< 18% tổng giờ làm việc** | Giám sát lộ trình di chuyển |
| **Chi phí** | **Chi phí logistics / Doanh thu** | 9.8% – 12.5% | **$\le 6.2%$** | Báo cáo P&L phân phối |

---
*Báo cáo hoàn chỉnh được xuất bản từ Hệ thống RTM Không gian Phân tích Địa bàn CJ Foods Việt Nam.*
