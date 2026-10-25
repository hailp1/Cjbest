# BÁO CÁO PHÂN TÍCH RTM CHUYÊN SÂU: HIỆN TRẠNG 6 VÙNG, CỰ LY GIAO HÀNG, BẢN ĐỒ VÙNG TRẮNG & ĐỀ XUẤT THIẾT LẬP ĐẠI LÝ CẤP 1 (C1 / SUB-HUB)

> **Căn cứ dữ liệu:**
> * Dữ liệu vận hành thực tế CJ: **391 Nhà Phân Phối** (215 đang hoạt động, 176 ngưng hoạt động) & **59,366 Điểm bán (Outlets)**.
> * Dữ liệu thị trường tiềm năng: **215,376 Điểm bán GT toàn quốc** (Trích xuất từ tệp `GT Potentail Shop_12'25.xlsb`), lọc trọng tâm **9,056 Điểm bán Nhóm A & B** (9,038 điểm có tọa độ GPS chuẩn xác).
> * Dữ liệu phân bổ lực lượng bán hàng: **145 Nhà Phân Phối chính thức** (Trích xuất từ tệp `loaiNPP.xlsx`), phân loại chi tiết **117 NPP Có SM (273 NVBH)** và **28 NPP Không SM**.
> * Đơn vị phân tích: Mô hình RTM Không gian (Spatial Route-To-Market) CJ Foods Việt Nam.

---

## MỤC LỤC
1. [TỔNG HỢP MA TRẬN PHÂN PHỐI & CỰ LY GIAO HÀNG 6 VÙNG](#1-tổng-hợp-ma-trận-phân-phối--cự-ly-giao-hàng-6-vùng)
2. [ĐÁNH GIÁ CHI TIẾT TÌNH HÌNH PHÂN PHỐI & LOGISTICS CỰ LY THEO VÙNG](#2-đánh-giá-chi-tiết-tình-hình-phân-phối--logistics-cự-ly-theo-vùng)
3. [PHÂN TÍCH LỰC LƯỢNG BÁN HÀNG: CƠ CẤU NPP CÓ SM VS KHÔNG SM (TỪ TỆP LOAINPP)](#3-phân-tích-lực-lượng-bán-hàng-cơ-cấu-npp-có-sm-vs-không-sm-từ-tệp-loainpp)
4. [PHÂN TÍCH VÙNG TRẮNG & TIỀM NĂNG OUTLET NHÓM A & B](#4-phân-tích-vùng-trắng--tiềm-năng-outlet-nhóm-a--b)
5. [ĐỀ XUẤT THIẾT LẬP ĐẠI LÝ CẤP 1 (C1 / SUB-HUB) TẠI TỪNG VÙNG](#5-đề-xuất-thiết-lập-đại-lý-cấp-1-c1--sub-hub-tại-từng-vùng)
6. [LỘ TRÌNH TRIỂN KHAI VÀ KHUYẾN NGHỊ VẬN HÀNH](#6-lộ-trình-triển-khai-và-khuyến-nghị-vận-hành)

---

## 1. TỔNG HỢP MA TRẬN PHÂN PHỐI & CỰ LY GIAO HÀNG 6 VÙNG

| Vùng Kinh Doanh | Số NPP (Active/Tắt) | Tổng Outlet CJ | Tỷ Lệ Hàng Lạnh (%) | Cự Ly Bình Quân (km) | Điểm >45km (Điểm nóng) | Số Shop A & B Tiềm Năng | Doanh Số A & B (Tỷ/tháng) | Mức Độ Rủi Ro Logistics |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hải Phòng** | 78 (39 / 39) | 13,028 | 28.4% | **21.3 km** | **1,118 (8.6%)** | 2,738 | **35.38 Tỷ** | 🔴 Cực kỳ rủi ro (Cự ly xa nhất) |
| **Cần Thơ (Miền Tây)** | 62 (34 / 28) | 8,271 | 12.6% | **19.4 km** | **831 (10.0%)** | 405 | **1.49 Tỷ** | 🔴 Tỷ lệ điểm >45km cao nhất |
| **Hà Nội** | 70 (35 / 35) | 11,021 | **36.1%** | 10.8 km | 242 (2.2%) | 3,259 | **44.32 Tỷ** | 🟡 Rủi ro đứt chuỗi lạnh |
| **Nha Trang** | 90 (45 / 45) | 13,718 | 18.9% | 11.3 km | 158 (1.2%) | 1,135 | 8.17 Tỷ | 🟢 Rủi ro thấp (Chia cắt địa hình) |
| **Đà Nẵng** | 44 (27 / 17) | 6,224 | 30.7% | 10.7 km | 103 (1.7%) | 810 | 5.93 Tỷ | 🟢 Rủi ro thấp |
| **TP. Hồ Chí Minh** | 47 (35 / 12) | 7,104 | 11.5% | **6.2 km** | **0 (0.0%)** | 691 | 4.75 Tỷ | 🟢 Bán kính tối ưu (Chồng chéo tuyến) |
| **TOÀN QUỐC** | **391 (215 / 176)** | **59,366** | **24.8%** | **13.3 km** | **2,452 (4.1%)** | **9,038** | **100.26 Tỷ** | **Cần tái cấu trúc mạng lưới** |

---

## 2. ĐÁNH GIÁ CHI TIẾT TÌNH HÌNH PHÂN PHỐI & LOGISTICS CỰ LY THEO VÙNG

### 2.1. Vùng Hải Phòng & Duyên Hải Bắc Bộ (🔴 Báo Động Đỏ)
* **Hiện trạng phân phối:** 78 NPP (chỉ 39 NPP đang hoạt động, 39 NPP ngưng hoạt động). Quản lý 13,028 điểm bán trên địa bàn rộng lớn từ Quảng Ninh, Hải Phòng, Hải Dương, Nam Định, Thái Bình sang đến Thanh Hóa, Nghệ An, Hà Tĩnh.
* **Logistics cự ly giao hàng:**
  * Cự ly bình quân: **21.3 km** — Cao nhất toàn quốc.
  * Có tới **1,118 điểm bán nằm ngoài bán kính an toàn (>45km)**, chiếm 8.6% toàn vùng.
  * Cực đoan: NPP Thực Phẩm Hà Hải có cự ly bình quân lên tới **60.8 km**, xa nhất **78.3 km** (giao từ trung tâm Hải Phòng sang các huyện ven biển Thái Bình/Nam Định).
* **Nút thắt cốt lõi:**
  1. Thiếu kho lạnh trung chuyển tại khu vực Nam Định/Thái Bình và Thanh Hóa.
  2. Tuyến giao hàng dài vượt quá 2 giờ chạy xe tải thường, trong khi 28.4% điểm bán có nhập hàng lạnh (xúc xích, mandu, chả giò) $\rightarrow$ Nguy cơ suy giảm chất lượng và tan đông hàng hóa.

### 2.2. Vùng Cần Thơ & Đồng Bằng Sông Cửu Long (🔴 Báo Động Đỏ)
* **Hiện trạng phân phối:** 62 NPP (34 NPP hoạt động, 28 NPP ngưng hoạt động), 8,271 điểm bán. Địa bàn chia cắt bởi hệ thống sông ngòi, kênh rạch chằng chịt qua 13 tỉnh Miền Tây.
* **Logistics cự ly giao hàng:**
  * Cự ly bình quân: **19.4 km**.
  * Tỷ lệ điểm giao >45km cao nhất cả nước: **10.0% (831 điểm bán)**.
  * Nút thắt điển hình: NPP Hưng Lộc Phát (Sóc Trăng) phải giao đơn xuống tận Bạc Liêu và Cà Mau với cự ly cực đại **70.6 km**. NPP quản lý tủ đông MT giao cự ly lên tới **150+ km**.
* **Nút thắt cốt lõi:**
  1. Bán kính giao hàng quá rộng vượt quá sức tải của xe máy chở thùng lạnh. Chi phí giao nhận trên mỗi đơn hàng chiếm từ 15% – 22% giá trị đơn, ăn mòn toàn bộ biên lợi nhuận phân phối.
  2. Bạc Liêu và Cà Mau hiện không có NPP hoạt động đủ năng lực bao quát, phải phụ thuộc hàng tiếp ứng từ Cần Thơ / Sóc Trăng.

### 2.3. Vùng Hà Nội & Trung Du Phía Bắc (🟡 Rủi Ro Đứt Chuỗi Lạnh)
* **Hiện trạng phân phối:** 70 NPP (35 NPP hoạt động, 35 NPP ngưng hoạt động), 11,021 điểm bán.
* **Logistics cự ly giao hàng:**
  * Cự ly bình quân toàn vùng: **10.8 km** (khá tốt tại nội thành).
  * Điểm nóng cự ly xa: **242 điểm >45km (2.2%)**, tập trung ở khu vực bán sơn địa và vùng núi: Ba Vì, Sơn Tây, Hòa Bình, Phú Thọ.
* **Nút thắt cốt lõi:**
  * Tỷ trọng hàng lạnh cao nhất cả nước: **36.1% điểm bán có nhập hàng lạnh/đông**.
  * Cung đường đèo dốc và bán sơn địa phía Tây (Hòa Bình, Phú Thọ) khiến xe giao hàng mất nhiều thời gian, làm suy giảm nhiệt độ tủ đông trên xe.

### 2.4. Vùng Nha Trang - Tây Nguyên & Đông Nam Bộ (🟢 Ổn Định)
* **Hiện trạng phân phối:** 90 NPP (45 hoạt động, 45 ngưng hoạt động), 13,718 điểm bán.
* **Logistics cự ly giao hàng:** Cự ly bình quân **11.3 km**, chỉ có 158 điểm >45km (1.2%).
* **Nút thắt:** Sự chia cắt địa hình rõ rệt giữa dải Duyên hải (Nha Trang, Phan Thiết, Phan Rang) và vùng Cao nguyên (Đắk Lắk, Gia Lai, Kon Tum, Lâm Đồng). Các huyện phía Bắc Đắk Lắk (Ea H'leo, Krông Năng) và Bình Phước (Bù Đăng, Bù Gia Mập) bị cách xa kho trung tâm từ 45 – 60 km.

### 2.5. Vùng Đà Nẵng & Miền Trung (🟢 Ổn Định)
* **Hiện trạng phân phối:** 44 NPP (27 hoạt động, 17 ngưng hoạt động), 6,224 điểm bán.
* **Logistics cự ly giao hàng:** Cự ly bình quân **10.7 km**, 103 điểm >45km (1.7%).
* **Nút thắt:** Khu vực Quảng Bình (Lệ Thủy, Ba Đồn) và khu vực giáp ranh Lăng Cô (Thừa Thiên Huế) - Đà Nẵng. NPP Duy Thúy phải gánh tuyến kéo dài qua đèo.

### 2.6. Vùng TP. Hồ Chí Minh (🟢 Tối Ưu Cự Ly - Thách Thức Chồng Tuyến)
* **Hiện trạng phân phối:** 47 NPP (35 hoạt động, 12 ngưng hoạt động), 7,104 điểm bán.
* **Logistics cự ly giao hàng:** Cự ly bình quân lý tưởng **6.2 km**, **0 điểm bán >45km (0.0%)**.
* **Nút thắt:** Vấn đề không nằm ở cự ly xa mà là **chồng chéo tuyến bán hàng (Cross-servicing)** giữa 35 NPP trong các quận nội thành chật hẹp, kẹt xe giờ cao điểm và cấm tải xe lớn.

---

---

## 3. PHÂN TÍCH LỰC LƯỢNG BÁN HÀNG: CƠ CẤU NPP CÓ SM VS KHÔNG SM (TỪ TỆP `loaiNPP.xlsx`)

Từ tệp dữ liệu tổ chức bán hàng `loaiNPP.xlsx` (gồm **145 Nhà Phân Phối chính thức** có GSBH/ASM quản lý), phân tích chuyên sâu về lực lượng bán hàng (Sales Representative / Salesman - SM) cho thấy cơ cấu phân bổ nhân sự như sau:

* **Tổng NPP Có SM:** **117 NPP (80.7%)** với tổng cộng **273 nhân viên bán hàng (NVBH)** phụ trách tuyến (dao động từ 1 đến 6 NVBH/NPP).
* **Tổng NPP "Không SM":** **28 NPP (19.3%)** — Đây là các NPP hoàn toàn **không có nhân viên bán hàng của CJ phụ trách đi tuyến viếng thăm**, chỉ vận hành theo hình thức đại lý nhận đơn thụ động hoặc bán sỉ.

### 3.1. Bảng Ma Trận Phân Bổ NPP Có SM vs Không SM Theo 6 Vùng

| Vùng Kinh Doanh | Tổng NPP Quản Lý | NPP Có SM | NPP Không SM | Tỷ Lệ Không SM (%) | Tổng Số NVBH | NVBH Bình Quân/NPP Có SM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Cần Thơ (Miền Tây)** | 26 | 18 | **8** | **30.8%** | 41 | 2.3 NVBH |
| **TP. Hồ Chí Minh** | 13 | 8 | **5** | **38.5%** | 31 | 3.9 NVBH |
| **Hà Nội** | 22 | 17 | **5** | **22.7%** | 48 | 2.8 NVBH |
| **Nha Trang & ĐNB** | 34 | 30 | **4** | 11.8% | 63 | 2.1 NVBH |
| **Đà Nẵng** | 17 | 14 | **3** | 17.6% | 30 | 2.1 NVBH |
| **Hải Phòng** | 33 | 30 | **3** | 9.1% | 60 | 2.0 NVBH |
| **TỔNG CỘNG** | **145** | **117** | **28** | **19.3%** | **273** | **2.3 NVBH** |

> [!WARNING]
> **CẢNH BÁO NÚT THẮT TẠI MIỀN TÂY & HÀ NỘI:**
> * **Vùng Cần Thơ (Miền Tây)** có tỷ lệ "Không SM" cao vượt trội (**30.8%**, 8/26 NPP), trong đó có tới **3 NPP thuộc nhóm TOP 50 Doanh Số Toàn Quốc** (Food House, Shiba, Cúc Tuấn). Việc thiếu vắng lực lượng bán hàng chuyên trách khiến địa bàn Miền Tây vừa bị cự ly xa, vừa không có người mở mới điểm bán.
> * **Vùng Hà Nội:** Toàn bộ **4 NPP tại Tỉnh Sơn La** (Thu Hương, Tú Anh, BTH, Nguyễn Duy Tiệp) đều ở trạng thái **"Không SM"**, khiến thị trường Tây Bắc bị cô lập hoàn toàn về mặt phát triển kinh doanh.

### 3.2. Danh Mục Chi Tiết 28 Nhà Phân Phối Trạng Thái "Không SM"

| STT | Mã NPP | Tên Nhà Phân Phối | Vùng CJ | Area | Văn Phòng / Tỉnh | GSBH Quản Lý | Xếp Hạng Top 50 | Ghi Chú & Đánh Giá Tác Động |
| :---: | :---: | :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| 1 | **1029803** | THU HƯƠNG | Hà Nội | Hà Nội | Son La | NEW_SUP_SONLA1 | - | Thị trường Sơn La không có DSR đi tuyến |
| 2 | **1055883** | TÚ ANH | Hà Nội | Hà Nội | Son La | NEW_SUP_SONLA1 | - | Thị trường Sơn La không có DSR đi tuyến |
| 3 | **1055987** | BTH | Hà Nội | Hà Nội | Son La | NEW_SUP_SONLA1 | - | Thị trường Sơn La không có DSR đi tuyến |
| 4 | **1057620** | NGUYỄN DUY TIỆP | Hà Nội | Hà Nội | Son La | NEW_SUP_SONLA1 | - | Thị trường Sơn La không có DSR đi tuyến |
| 5 | **1029779** | TIÊN PHONG | Hà Nội | Hà Nội | H.Noi 5 | Vũ Thị Huệ | ⭐ **Top 50** | NPP lớn nội thành nhưng đại lý tự bán |
| 6 | **1057474** | HƯNG THẢO | Hải Phòng | DH & BMT | N.An | Lê Văn Bảo | - | Khu vực Nghệ An cần bổ sung DSR |
| 7 | **1057558** | KHANG NA | Hải Phòng | DH & BMT | N.An | Lê Văn Bảo | - | Khu vực Nghệ An cần bổ sung DSR |
| 8 | **1059078** | CHI LÂM | Hải Phòng | DH & BMT | N.Binh 2 | Phạm Văn Sơn | - | Khu vực Ninh Bình |
| 9 | **1035885** | THIỆN NHÂN | Đà Nẵng | Đà Nẵng 2 | Hue | Trương Phước Cao | - | Thừa Thiên Huế |
| 10 | **1039535** | HỒNG ÂN PARIS | Đà Nẵng | Đà Nẵng 2 | Hue | Trương Phước Cao | - | Thừa Thiên Huế |
| 11 | **1035470** | THU THỦY | Đà Nẵng | Đà Nẵng 2 | Bình Định | Lê Hoàng Y Ron | - | Bình Định |
| 12 | **1029754** | TÙNG LOAN | Nha Trang | Nha Trang | B.Thuan | Nguyễn Xuân Sáu | - | Bình Thuận |
| 13 | **1057464** | KIM PHƯỢNG ĐỨC LINH | Nha Trang | Nha Trang | B.Thuan | Nguyễn Xuân Sáu | - | Đức Linh (Bình Thuận) |
| 14 | **1029762** | FOODCOMART | Nha Trang | Nha Trang | Dlak | Lê Quốc Cường | - | Đắk Lắk |
| 15 | **1063980** | CẨM LY FOODS | Nha Trang | Nha Trang | Dlak | Lê Quốc Cường | - | Đắk Lắk |
| 16 | **1029721** | THĂNG LONG | HCM | HCM | HCM 3 | Hà Minh Long | - | Đối tác kênh đặc biệt / Wholesale |
| 17 | **1035180** | MARIS | HCM | HCM | HCM 3 | Hà Minh Long | - | Đối tác Horeca / Bán sỉ |
| 18 | **1029725** | KHỞI THỊNH | HCM | HCM | HCM 4 | Huỳnh Hưng Long | - | Bán sỉ |
| 19 | **1029726** | THUẬN PHÁT THÀNH | HCM | HCM | HCM 4 | Huỳnh Hưng Long | - | Bán sỉ |
| 20 | **1029724** | NGUYÊN HÀ | HCM | HCM | HCM 5 | Nguyễn Khắc Lợi | - | Kênh buôn thực phẩm |
| 21 | **1029737** | FOOD HOUSE | Cần Thơ | Cần Thơ | An Giang | Tô Bá Vinh | ⭐ **Top 50** | NPP trọng điểm An Giang nhưng thiếu SM |
| 22 | **1033606** | NGỌC KHÁNH AN | Cần Thơ | Cần Thơ | An Giang | Tô Bá Vinh | - | An Giang |
| 23 | **1037766** | SHIBA | Cần Thơ | Cần Thơ | An Giang | Tô Bá Vinh | ⭐ **Top 50** | NPP trọng điểm An Giang nhưng thiếu SM |
| 24 | **1057019** | AB HAPPY | Cần Thơ | Cần Thơ | An Giang | Tô Bá Vinh | - | An Giang |
| 25 | **1057032** | AN NGỌC NGÂN | Cần Thơ | Cần Thơ | An Giang | Tô Bá Vinh | - | An Giang |
| 26 | **1029735** | CẦU TRE | Cần Thơ | Cần Thơ | C. Thơ | Nguyễn Hồng Đạt | - | Trung tâm Cần Thơ |
| 27 | **1029740** | CÚC TUẤN | Cần Thơ | Cần Thơ | C. Thơ | Nguyễn Hồng Đạt | ⭐ **Top 50** | NPP trọng điểm Cần Thơ nhưng thiếu SM |
| 28 | **1063689** | LY NHƯ Ý | Cần Thơ | Cần Thơ | C. Thơ | Nguyễn Hồng Đạt | - | Cần Thơ |

### 3.3. Tác Động Của Trạng Thái "Không SM" Đến Khai Thác Vùng Trắng
1. **Không thể kết nạp điểm bán tiềm năng (Golden Outlets):** Tại các địa bàn có NPP "Không SM", dù có nhiều Golden Outlets tiềm năng (ví dụ An Giang có hơn 80 Golden Outlets, Cần Thơ có hơn 90 Golden Outlets), CJ hoàn toàn không thể đưa sản phẩm vào vì không có DSR đi viếng thăm, giới thiệu chương trình khuyến mãi hay đặt đơn trên DMS.
2. **Nguy cơ mất thị phần vào tay đối thủ:** Các NPP "Không SM" thường phân phối đa nhãn hàng. Nếu CJ không có nhân sự cắm chốt, NPP sẽ ưu tiên đẩy hàng của các nhãn hàng khác có nhân viên hỗ trợ bán lẻ.
3. **Khuyến nghị RTM cấp bách:**
   * **Bổ sung ngay DSR cho 4 NPP Top 50 "Không SM"** (Food House, Shiba, Cúc Tuấn, Tiên Phong) để tối đa hóa doanh số bán ra.
   * Chuyển đổi các NPP "Không SM" nhỏ lẻ thành mô hình **Đại lý C1 / Sub-Hub** tự quản có cam kết chỉ tiêu hoặc gom tuyến giao lại cho NPP lân cận có SM phụ trách.

## 4. PHÂN TÍCH VÙNG TRẮNG & TIỀM NĂNG OUTLET NHÓM A & B

Từ cơ sở dữ liệu **215,376 điểm bán GT toàn quốc**, lọc ra **9,056 điểm bán Nhóm A & B** (9,038 điểm có tọa độ GPS hợp lệ). Doanh số Sellout thị trường của nhóm này đạt **100.26 Tỷ VNĐ/tháng** (~ **1.20 Nghìn Tỷ VNĐ/năm**).

Bằng thuật toán phân tích không gian đa chiều đo cự ly từ 9,038 điểm A & B đến 215 NPP Active của CJ, kết quả chia thành 3 phân khúc chiến lược:

```
                      TỔNG THỊ TRƯỜNG A & B: 9,038 OUTLETS (100.3 TỶ/THÁNG)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         ▼                                 ▼                                 ▼
[VÙNG TRẮNG PHỦ NHANH]           [VÙNG TRẮNG ĐỊNH KỲ]             [VÙNG TRẮNG TRỌNG YẾU]
   Cự ly ≤ 15 km                    Cự ly 15 - 30 km                 Cự ly > 30 km
  6,744 Outlets (74.6%)            1,555 Outlets (17.2%)            739 Outlets (8.2%)
   74.96 Tỷ VNĐ/tháng               17.86 Tỷ VNĐ/tháng               7.44 Tỷ VNĐ/tháng
 (Khai thác mở beat ngay)         (Gom tuyến F2/F4 + MOQ)         (MỞ C1 / SUB-HUB MỚI)
```

### 3.1. Phân khúc 1: Vùng Trắng Khai Thác Nhanh ($\le 15$ km) — 6,744 Shop (74.6 Tỷ/tháng)
* **Đặc điểm:** Nằm ngay sát nách các NPP đang hoạt động của CJ nhưng hiện tại chưa được kết nạp vào DMS hoặc chưa được nhân viên bán hàng (DSR) ghé thăm.
* **Phân bổ:**
  * Hà Nội: **2,583 shop** (35.36 Tỷ/tháng)
  * Hải Phòng: **1,865 shop** (24.58 Tỷ/tháng)
  * TP.HCM: **674 shop** (4.66 Tỷ/tháng)
  * Nha Trang: **768 shop** (5.27 Tỷ/tháng)
  * Đà Nẵng: **548 shop** (3.99 Tỷ/tháng)
  * Cần Thơ: **306 shop** (1.11 Tỷ/tháng)
* **Hành động RTM:** **Thêm tuyến ngay (In-fill Route Addition)**. Chỉ cần cập nhật Master Data vào hệ thống định tuyến, giao cho DSR phụ trách mở mới điểm bán (New Outlet Acquisition) với chi phí mở rộng gần như bằng 0.

### 3.2. Phân khúc 2: Vùng Trắng Gom Tuyến Định Kỳ (15 – 30 km) — 1,555 Shop (17.9 Tỷ/tháng)
* **Đặc điểm:** Nằm ở vùng ven đô thị hoặc các huyện ngoại thành. NPP hiện hữu có thể giao hàng nhưng cần tối ưu hiệu quả chuyến xe.
* **Hành động RTM:** Áp dụng tần suất viếng thăm **F2 (2 tuần/lần)** hoặc **F4 (hàng tháng)** và áp sàn giá trị đơn hàng tối thiểu **MOQ $\ge 1,000,000$ VNĐ** để bù đắp chi phí vận chuyển.

### 3.3. Phân khúc 3: Vùng Trắng Trọng Yếu Cần Mở Đại Lý C1 / Sub-Hub (> 30 km) — 739 Shop (7.44 Tỷ/tháng)
* **Đặc điểm:** Tập trung thành từng cụm mật độ cao tại các huyện vùng xa, nằm ngoài bán kính giao hàng an toàn của các NPP hiện tại (>30km – 80km).
* **Nguy cơ:** Nếu để NPP trung tâm giao sẽ lỗ chi phí vận hành và đứt chuỗi lạnh. Nếu bỏ qua sẽ mất toàn bộ thị trường loại A/B vào tay đối thủ cạnh tranh.
* **Giải pháp bắt buộc:** **Thành lập Đại lý Cấp 1 (C1) hoặc thiết lập Sub-Hub kho vệ tinh tại chỗ**.

---

## 5. ĐỀ XUẤT THIẾT LẬP ĐẠI LÝ CẤP 1 (C1 / SUB-HUB) TẠI TỪNG VÙNG

Dựa trên thuật toán gom cụm mật độ không gian của các điểm bán A & B nằm ngoài bán kính 30km kết hợp với 2,452 điểm bán hiện hữu bị cự ly xa, dưới đây là **danh mục chi tiết các vị trí đề xuất thành lập Đại lý Cấp 1 (C1 / Sub-Hub)** cho từng vùng:

```
====================================================================================================
DANH MỤC ĐỀ XUẤT MỞ MỚI / TÁI KÍCH HOẠT ĐẠI LÝ CẤP 1 (C1 / SUB-HUB) TOÀN QUỐC
====================================================================================================
```

### 📍 1. VÙNG HẢI PHÒNG & DUYÊN HẢI BẮC (Đề xuất: 3 Đại Lý C1 / Sub-Hub)

#### C1-HP-01: Đại Lý C1 / Sub-Hub Lục Ngạn & Sơn Động (Tỉnh Bắc Giang)
* **Vị trí đặt kho:** Thị trấn Chũ, Huyện Lục Ngạn, Bắc Giang.
* **Địa bàn phụ trách:** Huyện Lục Ngạn, Huyện Sơn Động, Huyện Lục Nam.
* **Dữ liệu tiềm năng giải quyết:**
  * Tiếp nhận **78 điểm bán tiềm năng Nhóm A & B** (Lục Ngạn: 59 shop; Sơn Động: 19 shop). Doanh số tiềm năng: **1.04 Tỷ VNĐ/tháng**.
  * Cắt giảm cự ly giao hàng từ 38.9 km (từ TP. Bắc Giang) xuống còn **$\le 10$ km**.
* **Hình thức triển khai:** Tuyển mới 01 NPP/C1 có sẵn xe tải thùng kín hoặc hợp tác với Tổng đại lý tạp hóa lớn nhất thị trấn Chũ.

#### C1-HP-02: Đại Lý C1 Diễn Châu & Quỳnh Lưu (Tỉnh Nghệ An)
* **Vị trí đặt kho:** Thị trấn Diễn Châu, Huyện Diễn Châu, Nghệ An.
* **Địa bàn phụ trách:** Huyện Diễn Châu, Quỳnh Lưu, Thị xã Hoàng Mai.
* **Dữ liệu tiềm năng giải quyết:**
  * Tiếp nhận **35 điểm bán A & B** (23 A, 12 B). Doanh số tiềm năng: **195 Triệu VNĐ/tháng**.
  * Giải quyết dứt điểm các tuyến giao vượt cự ly 37km từ TP. Vinh lên phía Bắc Nghệ An.

#### C1-HP-03: Đại Lý C1 / Cold Hub Nam Định - Thái Bình
* **Vị trí đặt kho:** Khu vực giáp ranh TP. Nam Định và Huyện Vũ Thư (Thái Bình).
* **Mục tiêu chiến lược:** Cắt đứt tuyến giao 78.3 km của NPP Hà Hải từ Hải Phòng sang. Tiếp quản hơn **400 điểm bán hiện hữu** và mở rộng hơn **150 shop A & B** tại Thái Bình/Nam Định.

---

### 📍 2. VÙNG CẦN THƠ & MIỀN TÂY (Đề xuất: 3 Đại Lý C1 / Sub-Hub)

#### C1-CT-01: Tái kích hoạt Đại Lý C1 Cà Mau (Thành phố Cà Mau)
* **Vị trí đặt kho:** Phường 8 / Phường 9, TP. Cà Mau.
* **Phương án nguồn lực:** **Tái kích hoạt từ 1 trong 6 NPP đang ngưng hoạt động tại Tỉnh Cà Mau** (đã có pháp nhân, mã thuế và mặt bằng kho cũ).
* **Dữ liệu tiềm năng giải quyết:**
  * Tiếp nhận toàn bộ các tuyến cực nam: TP. Cà Mau, Cái Nước, Trần Văn Thời, Năm Căn, Đầm Dơi.
  * Xóa bỏ hoàn toàn tình trạng NPP Hưng Lộc Phát phải giao hàng cự ly **70.6 km** từ Sóc Trăng xuống. Giảm chi phí logistics Miền Tây ước tính **35%**.

#### C1-CT-02: Đại Lý C1 Giá Rai / Bạc Liêu (Tỉnh Bạc Liêu)
* **Vị trí đặt kho:** Thị xã Giá Rai, Bạc Liêu.
* **Địa bàn phụ trách:** Thị xã Giá Rai, Huyện Phước Long, Huyện Đông Hải và tiếp giáp Cà Mau.
* **Dữ liệu tiềm năng:** Xử lý 28 điểm cự ly xa của Bạc Liêu và bảo quản chuỗi hàng khô/lạnh ổn định.

#### C1-CT-03: Đại Lý C1 Kiên Lương & Hà Tiên (Tỉnh Kiên Giang)
* **Vị trí đặt kho:** Thị trấn Kiên Lương, Huyện Kiên Lương.
* **Địa bàn phụ trách:** Kiên Lương, TP. Hà Tiên, Huyện Giang Thành.
* **Mục tiêu:** Cắt giảm cự ly giao từ Rạch Giá ra Hà Tiên (hơn 85km đường ven biển).

---

### 📍 3. VÙNG HÀ NỘI & TRUNG DU PHÍA BẮC (Đề xuất: 3 Đại Lý C1)

#### C1-HN-01: Đại Lý C1 Cửa Khẩu TP. Lào Cai (Tỉnh Lào Cai)
* **Vị trí đặt kho:** Phường Duyên Hải / Kim Tân, TP. Lào Cai.
* **Địa bàn phụ trách:** TP. Lào Cai, Huyện Bảo Thắng, Sa Pa, Bát Xát.
* **Dữ liệu tiềm năng giải quyết:**
  * Tiếp nhận **38 điểm bán Nhóm A & B** (19 A, 19 B). Doanh số tiềm năng: **498 Triệu VNĐ/tháng**.
  * Giải quyết khoảng cách cô lập **86.2 km** so với NPP Yên Bái / Phú Thọ gần nhất.

#### C1-HN-02: Đại Lý C1 Tây Bắc Phú Thọ (Huyện Cẩm Khê / Thanh Ba)
* **Vị trí đặt kho:** Thị trấn Cẩm Khê, Huyện Cẩm Khê, Phú Thọ.
* **Địa bàn phụ trách:** Cẩm Khê, Thanh Ba, Hạ Hòa, Yên Lập (bán sơn địa).
* **Dữ liệu tiềm năng giải quyết:**
  * Tiếp nhận **50 điểm bán A & B** (Thanh Ba: 18 shop; Cẩm Khê: 18 shop; Yên Lập: 14 shop). Doanh số tiềm năng: **727 Triệu VNĐ/tháng**.
  * Rút ngắn cự ly giao hàng từ 35 km xuống còn **$\le 8$ km**.

#### C1-HN-03: Đại Lý C1 Sơn Dương (Tỉnh Tuyên Quang)
* **Vị trí đặt kho:** Thị trấn Sơn Dương, Tuyên Quang.
* **Dữ liệu tiềm năng:** 15 điểm bán A & B, kết nối hành lang Vĩnh Phúc - Tuyên Quang.

---

### 📍 4. VÙNG NHA TRANG - TÂY NGUYÊN (Đề xuất: 3 Đại Lý C1)

#### C1-NT-01: Đại Lý C1 Bắc Đắk Lắk (Thị Xã Buôn Hồ / Ea H'leo)
* **Vị trí đặt kho:** Phường An Lạc, Thị xã Buôn Hồ, Đắk Lắk.
* **Phương án nguồn lực:** **Tái thẩm định và kích hoạt lại 1 trong 7 NPP đang ngưng hoạt động tại Tỉnh Đắk Lắk**.
* **Địa bàn phụ trách:** Thị xã Buôn Hồ, Huyện Krông Năng, Huyện Ea H'leo, Huyện Ea Kar.
* **Dữ liệu tiềm năng giải quyết:**
  * Tiếp nhận **54 điểm bán Nhóm A & B** (Krông Năng: 17 shop; Ea H'leo: 16 shop; Buôn Hồ: 11 shop; Ea Kar: 10 shop). Doanh số tiềm năng: **491 Triệu VNĐ/tháng**.
  * Cắt giảm cự ly giao hàng từ 46 – 61 km (từ Buôn Ma Thuột đi quốc lộ 14) xuống còn dưới **15 km**.

#### C1-NT-02: Đại Lý C1 Phước Long & Bù Gia Mập (Tỉnh Bình Phước)
* **Vị trí đặt kho:** Thị xã Phước Long, Bình Phước.
* **Địa bàn phụ trách:** TX. Phước Long, Huyện Bù Gia Mập, Bù Đăng.
* **Dữ liệu tiềm năng:** Tiếp nhận **48 điểm bán A & B** (Phước Long: 21 shop; Bù Gia Mập: 15 shop; Bù Đăng: 12 shop). Doanh số: **411 Triệu VNĐ/tháng**.

#### C1-NT-03: Đại Lý C1 Krông Pa / Ayun Pa (Tỉnh Gia Lai)
* **Vị trí đặt kho:** Thị xã Ayun Pa, Gia Lai. Tái kích hoạt 1 trong 7 NPP ngưng hoạt động tại Gia Lai.
* **Dữ liệu tiềm năng:** Giải quyết 10 shop A & B đang bị cự ly cô lập lên tới **70.4 km** từ TP. Pleiku.

---

### 📍 5. VÙNG ĐÀ NẴNG & MIỀN TRUNG (Đề xuất: 1 Đại Lý C1)

#### C1-DN-01: Đại Lý C1 Lệ Thủy & Đồng Hới (Tỉnh Quảng Bình)
* **Vị trí đặt kho:** Thị trấn Kiến Giang, Huyện Lệ Thủy, Quảng Bình.
* **Địa bàn phụ trách:** Huyện Lệ Thủy, TP. Đồng Hới, Huyện Quảng Ninh.
* **Dữ liệu tiềm năng:** Tiếp nhận **13 shop A/B** và hỗ trợ toàn diện khu vực Bắc Quảng Trị / Nam Quảng Bình, giảm cự ly từ 30.8 km xuống dưới 10 km.

---

### 📍 6. VÙNG TP. HỒ CHÍ MINH (Không Mở Mới C1 — Tối Ưu In-Fill)
* **Chiến lược:** TP.HCM đã có **35 NPP hoạt động** và cự ly bình quân cực kỳ tối ưu (6.2 km). **Khuyến nghị KHÔNG mở thêm C1** để tránh băm nhỏ thị trường và xung đột kênh.
* **Hành động:** Phân bổ **674 shop A & B tiềm năng** (doanh số **4.66 Tỷ/tháng**) trực tiếp cho 35 NPP hiện hữu theo đúng ranh giới quận/huyện để tăng sản lượng trên mỗi km đường giao.

---

## 6. LỘ TRÌNH TRIỂN KHAI VÀ KHUYẾN NGHỊ VẬN HÀNH

```
   GIAI ĐOẠN 1 (Tháng 1 - 2)      GIAI ĐOẠN 2 (Tháng 3 - 4)      GIAI ĐOẠN 3 (Tháng 5 - 6)
   [Khai Thác Quick-Wins]         [Tái Kích Hoạt NPP Cũ]         [Tuyển Mới C1 Vùng Sâu]
            │                              │                              │
 ┌──────────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
 │ Phủ ngay 6,744 shop  │       │ Khảo sát 176 NPP tắt │       │ Mở mới các C1 vùng xa│
 │ A & B (cự ly ≤ 15km) │  ──>  │ Kích hoạt 5 vị trí:  │  ──>  │ Lào Cai, Lục Ngạn,   │
 │ Tăng 74.9 Tỷ/tháng   │       │ Cà Mau, Buôn Hồ,     │       │ Phước Long, Nam Định │
 │ Thêm tuyến bán hàng  │       │ Ayun Pa, Gia Lai     │       │ Áp MOQ động          │
 └──────────────────────┘       └──────────────────────┘       └──────────────────────┘
```

### 5.1. Khuyến nghị chính sách thương mại cho Đại lý C1 mới
1. **Chính sách ký gửi kho lạnh (Cold Hub Consignment):** Công ty tài trợ tủ đông bảo quản hoặc hỗ trợ 50% chi phí điện lạnh trong 6 tháng đầu để C1 cam kết nhiệt độ bảo quản chuẩn cho nhóm hàng xúc xích, mandu, chả giò.
2. **Cơ chế MOQ linh hoạt theo bán kính (Dynamic Minimum Order Quantity):**
   * Tuyến $\le 15$ km: MOQ $500,000$ VNĐ/đơn (F2 hoặc tuần 2 lần).
   * Tuyến $15 - 30$ km: MOQ $1,200,000$ VNĐ/đơn (F2 - 2 tuần/lần).
   * Tuyến $> 30$ km (chờ C1): Tuyệt đối không giao đơn lẻ tẻ dưới 2 triệu VNĐ.
3. **Chỉ số KPI giám sát mạng lưới RTM mới:**
   * **Tỷ lệ cự ly xa (>45km):** Giảm từ 4.1% xuống **dưới 1.0%** trên toàn quốc.
   * **Tỷ lệ kết nạp Shop A & B:** Đạt tối thiểu **80%** trong bán kính 15km sau 3 tháng đầu.
   * **Chi phí logistics trên doanh thu:** Cắt giảm từ 9.8% xuống **dưới 6.5%**.

---
*Báo cáo được trích xuất và tính toán tự động dựa trên tọa độ không gian GIS, tệp dữ liệu khách hàng tiềm năng GT 12/2025 và hệ thống phân tích mạng lưới RTM.*
