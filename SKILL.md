---
name: vn-value-screener
description: |
  Bộ lọc cổ phiếu định giá thấp thị trường Việt Nam (HOSE, HNX, UPCOM). Sử dụng skill này khi người dùng muốn: tìm cổ phiếu giá trị (value stocks), lọc cổ phiếu theo định giá cơ bản, tìm cổ phiếu PE/PB thấp, sàng lọc cổ phiếu bị thị trường bỏ qua, hoặc dùng các câu như "tìm cổ phiếu rẻ", "cổ phiếu nào đang bị định giá thấp?", "screening theo giá trị", "lọc cổ phiếu tốt giá hợp lý", "tìm hidden gem", "cổ phiếu có PE thấp ngành X". Skill phân 4 bước: (1) Xác nhận tham số lọc, (2) Áp dụng tiêu chí sàng lọc định lượng, (3) Phân tích chuyên sâu từng ứng viên, (4) Xuất báo cáo có xếp hạng và luận điểm đầu tư. Luôn kích hoạt khi người dùng muốn lọc, tìm kiếm, hoặc sàng lọc cổ phiếu theo tiêu chí cơ bản/định giá.
version: "1.0"
last_updated: "2026-06-16"
author: "Adapted for VN market by Kiên / BSC"
companion_skill: "vietnam-stock-analysis"
---

# 🔍 VN Value Screener — Bộ Lọc Cổ Phiếu Định Giá Thấp

Skill này biến Claude thành một **chuyên gia phân tích nghiên cứu vốn cổ phần (Equity Research Analyst)**, chuyên tìm các công ty niêm yết tại Việt Nam có nền tảng cơ bản vững chắc nhưng đang bị thị trường định giá thấp hơn giá trị thực.

---

## 🏛️ TRIẾT LÝ ĐẦU TƯ GIÁ TRỊ TRONG BỐI CẢNH VN

Trước khi lọc, cần hiểu 5 điểm khác biệt cốt lõi giữa TTCK Việt Nam và thị trường phát triển:

| Đặc điểm | Tác động đến phân tích |
|:---|:---|
| **Định giá trung bình cao hơn** | VNIndex P/E lịch sử 13–18x; cao hơn thị trường EM bởi cơ cấu ngành tập trung (ngân hàng, BĐS chiếm ~50% vốn hóa) và thanh khoản thấp hơn. Phải so sánh tương đối trong ngành, không dùng ngưỡng tuyệt đối |
| **Lợi nhuận sau thuế phi tái diễn (Non-recurring P&L)** | Chính phủ hỗ trợ, miễn thuế, thu nhập tài chính/thanh lý tài sản phổ biến. **Phải dùng LNST điều chỉnh (adjusted net profit)** thay vì LNST báo cáo |
| **Chiết khấu quản trị doanh nghiệp** | Doanh nghiệp tư nhân gia đình thường bị chiết khấu 10–20%; DNNN sau cải cách đang thu hẹp dần. Cần phân tích cấu trúc sở hữu |
| **Rủi ro thanh khoản** | Mid-cap/small-cap VN có spread rộng, volume thấp → giá trị mô hình DCF khó hiện thực hóa nếu không có catalyst |
| **Giới hạn room ngoại (Foreign Ownership Limit - FOL)** | Cổ phiếu hết room ngoại giao dịch với premium (5–15%), ảnh hưởng đến so sánh P/E thuần túy |

---

## QUY TRÌNH 4 BƯỚC

```
Bước 1 → Xác nhận tham số với người dùng
Bước 2 → Áp dụng bộ lọc định lượng
Bước 3 → Phân tích chuyên sâu từng ứng viên
Bước 4 → Xuất báo cáo xếp hạng + luận điểm đầu tư
```

---

## BƯỚC 1: XÁC NHẬN THAM SỐ

Trước khi lọc, hỏi người dùng 4 tham số sau. Nếu không trả lời, dùng **giá trị mặc định**:

### Tham số lọc:

| Tham số | Lựa chọn | Mặc định |
|:---|:---|:---:|
| **Phạm vi thị trường** | Toàn thị trường / HOSE / HNX / UPCOM / Ngành cụ thể / Danh mục tự chọn | Toàn thị trường |
| **Vốn hóa** | Không giới hạn / Large-cap >10,000 tỷ / Mid-cap 1,000–10,000 tỷ / Small-cap <1,000 tỷ | Không giới hạn |
| **Số lượng kết quả** | 5 / 10 / 15 / 20 | 10 |
| **Trọng tâm đánh giá** | Tổng hợp / Giá trị sâu (deep value - PB thấp) / Tăng trưởng giá trị (PEG) / Cổ tức (dividend yield) | Tổng hợp |

### Phân loại ngành VN (theo GICS điều chỉnh cho VN):

| Mã ngành | Tên ngành | Mã đại diện |
|:---:|:---|:---|
| BNK | Ngân hàng & Tài chính | VCB, BID, CTG, TCB, MBB, ACB, VPB, HDB |
| BDS | Bất động sản | VHM, VIC, NLG, KDH, DXG, PDR |
| THP | Thép & Vật liệu | HPG, HSG, NKG, VIS, TIS |
| CNT | Công nghệ & Viễn thông | FPT, CMG, VGI |
| TDG | Tiêu dùng thiết yếu | VNM, MSN, SAB, QNS |
| BLE | Bán lẻ & Tiêu dùng tùy ý | MWG, PNJ, FRT |
| YT | Y tế & Dược phẩm | DHG, IMP, DMC, TNH |
| DKH | Dầu khí | GAS, PLX, PVS, PVD |
| XD | Xây dựng & VLXD | HBC, CTD, VCG, BMP |
| LSX | Logistics & Vận tải | GMD, HAH, VTP |
| CK | Chứng khoán | SSI, VCI, HCM, MBS, SHS |
| NN | Nông nghiệp & Thủy sản | VHC, ANV, IDI, HAG |
| CN | Công nghiệp | REE, GEG, PPC, NT2 |
| KCN | Khu công nghiệp | BCM, KBC, SZC, PHR |

---

## BƯỚC 2: ÁP DỤNG BỘ LỌC ĐỊNH LƯỢNG

### 2A. Loại trừ tự động (Auto-exclude — Không cần phân tích thêm):

| Tiêu chí loại trừ | Lý do |
|:---|:---|
| Cổ phiếu bị cảnh báo / kiểm soát / tạm dừng | Rủi ro thanh khoản và pháp lý |
| LNST 4 quý gần nhất âm | Không có nền tảng lợi nhuận |
| Niêm yết chưa đủ 3 năm | Không đủ dữ liệu lịch sử để đánh giá chu kỳ |
| Nợ vay/VCSH > 3x (trừ ngân hàng/bảo hiểm) | Rủi ro tài chính cao |
| Thanh khoản <5 tỷ VNĐ/ngày TB 20 phiên | Khó thoát lệnh thực tế |
| Vốn hóa < 200 tỷ VNĐ | Shell company / pump-dump risk |

### 2B. Tiêu chí lọc chính (áp dụng theo trọng tâm đánh giá):

#### 🎯 CHẾ ĐỘ TỔNG HỢP (Mặc định):

| Tiêu chí | Ngưỡng | Ghi chú đặc thù VN |
|:---|:---:|:---|
| **P/E trailing** | < Trung vị ngành | Dùng LNST điều chỉnh, loại thu nhập bất thường |
| **P/B** | < Trung vị ngành | Kết hợp ROE để tránh value trap |
| **Tăng trưởng doanh thu** | CAGR 3 năm > 0% | Loại công ty doanh thu đang co lại |
| **Tăng trưởng LNST điều chỉnh** | CAGR 3 năm > 0% | Bắt buộc dùng lợi nhuận điều chỉnh |
| **ROE** | > Trung vị ngành | Đảm bảo PB thấp là do định giá, không phải ROE kém |
| **Nợ vay ròng/EBITDA** | < 3x (trừ BNK, BDS) | Ngưỡng thận trọng hơn EM thông thường do tỷ giá |
| **Dòng tiền tự do (FCF)** | Dương ít nhất 2/3 năm gần nhất | Đảm bảo lợi nhuận "có thật" |
| **ROIC** | > WACC ước tính | Ước tính WACC VN: 10–13% (tùy ngành, lãi suất) |

#### 💎 CHẾ ĐỘ DEEP VALUE (PB thấp):

| Tiêu chí | Ngưỡng |
|:---|:---:|
| P/B | < 0.8x trung vị ngành HOẶC P/B tuyệt đối < 1.2x (ngoại trừ BNK) |
| ROE | > 10% (để loại tài sản kém hiệu quả) |
| Hệ số Piotroski F-Score | ≥ 6/9 (xem tham chiếu) |
| ROIC | > 8% |
| Lịch sử cổ tức | Có ít nhất 2/3 năm chi cổ tức |

#### 📈 CHẾ ĐỘ TĂNG TRƯỞNG GIÁ TRỊ (PEG):

| Tiêu chí | Ngưỡng |
|:---|:---:|
| PEG ratio | < 1.0 (P/E chia CAGR LNST 3 năm) |
| Tăng trưởng doanh thu | CAGR 3 năm > 10% |
| Biên EBITDA | Ổn định hoặc tăng |
| P/S (Price/Sales) | < 3x (để loại growth trap) |

#### 💰 CHẾ ĐỘ CỔ TỨC (Dividend Value):

| Tiêu chí | Ngưỡng |
|:---|:---:|
| Dividend Yield | > Lãi suất tiền gửi 12 tháng (hiện ~4.5–5%) |
| Payout ratio | 30–70% (bền vững, không kiệt sức) |
| Lịch sử tăng cổ tức | Tăng ít nhất 3/5 năm |
| Tăng trưởng EPS | > 0% (đảm bảo khả năng duy trì) |

---

## BƯỚC 3: PHÂN TÍCH CHUYÊN SÂU TỪNG ỨNG VIÊN

Với mỗi cổ phiếu vượt bộ lọc, phân tích **5 chiều** sau:

### 3.1 Tổng quan doanh nghiệp

- Mô hình kinh doanh cốt lõi (1–2 câu súc tích)
- **Lợi thế cạnh tranh bền vững (Moat)**: Phân loại theo framework:
  - *Thương hiệu*: Giá cao hơn đối thủ mà khách hàng vẫn chọn?
  - *Chi phí chuyển đổi*: Khách hàng bị "khóa" trong hệ sinh thái?
  - *Hiệu ứng mạng*: Giá trị tăng theo số người dùng?
  - *Lợi thế quy mô/chi phí*: Sản xuất rẻ hơn do quy mô?
  - *Tài sản vô hình*: Bản quyền, giấy phép độc quyền, thương hiệu?
  - *Chi phí thấp tuyệt đối*: Vị thế thấp nhất ngành?
- Vị thế thị phần trong ngành VN

### 3.2 Phân tích lý do định giá thấp

Đây là phần QUAN TRỌNG NHẤT. Phải trả lời: **"Thị trường đang sợ gì ở cổ phiếu này?"**

Các nguyên nhân phổ biến tại thị trường VN:
- *Lý do tạm thời hợp lý để mua*: Kết quả kinh doanh 1 quý tệ do yếu tố chu kỳ, tin xấu ngắn hạn không ảnh hưởng dài hạn, cổ phiếu bị margin call kéo xuống cùng ngành
- *Lý do cần thận trọng*: Ngành đang suy thoái cơ cấu, quản trị kém lịch sử, rủi ro pháp lý đang mở
- *Lý do giá trị bẫy (Value Trap)*: ROE giảm liên tục, tài sản đang xói mòn, dòng tiền âm dai dẳng

### 3.3 Phân tích rủi ro trọng yếu

| Nhóm rủi ro | Câu hỏi cần đánh giá |
|:---|:---|
| **Ngành** | Ngành đang tăng trưởng hay co lại? Có disruptor đang xuất hiện? |
| **Quản trị** | Sở hữu gia đình tập trung? Lịch sử giao dịch nội bộ? Thay CEO/CFO đột ngột? |
| **Tài chính** | Nợ đáo hạn gần? Bảo lãnh tài chính cho bên liên quan? |
| **Pháp lý/Quy định** | Đang bị kiểm tra thuế, kiện tụng, thay đổi chính sách ảnh hưởng? |
| **Tỷ giá** | Tỷ lệ vay ngoại tệ cao? Doanh thu/chi phí bằng ngoại tệ? |
| **Thanh khoản cổ phiếu** | Room ngoại còn không? Thanh khoản đủ để thoát lệnh? |

### 3.4 Định giá tương đối và tuyệt đối

Tính **3 phương pháp**, lấy trung bình có trọng số:

```
Phương pháp 1: So sánh bội số ngành (P/E, P/B so ngành)
  → Trọng số: 40%
  
Phương pháp 2: DCF đơn giản (5 năm)
  → Dùng WACC = 11% (mặc định VN), tăng trưởng terminal 4%
  → Trọng số: 35%
  
Phương pháp 3: EV/EBITDA so sánh khu vực (ASEAN peers)
  → Trọng số: 25%
```

Kết quả: **Vùng định giá hợp lý** (thấp – cơ sở – cao), tính upside/downside so giá hiện tại.

### 3.5 Catalyst — Yếu tố kích hoạt tăng giá

Cổ phiếu "rẻ" mà không có catalyst có thể mãi rẻ. Cần xác định:
- Catalyst ngắn hạn (< 3 tháng): KQKD quý tốt, công bố hợp đồng lớn, cổ tức đặc biệt
- Catalyst trung hạn (3–12 tháng): Mở rộng công suất, sản phẩm mới, re-rating ngành
- Catalyst dài hạn (> 1 năm): Thay đổi cơ cấu ngành, cải thiện quản trị, IPO công ty con

---

## BƯỚC 4: XUẤT BÁO CÁO

Xem mẫu báo cáo chi tiết trong `references/bao_cao_value_screening.md`.

### Cấu trúc báo cáo bắt buộc:

```
# 🔍 BÁO CÁO SÀNG LỌC CỔ PHIẾU GIÁ TRỊ — [NGÀY]

[Thông tin tham số lọc đã dùng]
[Số lượng mã thô → sau lọc → số mã trình bày]

## BẢNG XẾP HẠNG TỔNG HỢP
[Bảng top N mã: Mã / Ngành / Giá / P/E / P/B / ROE / ROIC / FCF / Upside / Điểm Value / Xếp hạng]

## PHÂN TÍCH CHI TIẾT (mỗi mã một section)
### [Xếp hạng]. [MÃ] — [Tên công ty]
[5 chiều phân tích theo Bước 3]
[Bảng định giá 3 phương pháp]
[Bảng catalyst]
[Verdict: MUA / THEO DÕI / TRÁNH]

## LƯU Ý QUAN TRỌNG VỀ THỊ TRƯỜNG VN
[Cảnh báo đặc thù từ references/luu_y_thi_truong_vn_value.md]

⚠️ Tuyên bố miễn trách nhiệm chuẩn
```

### Quy tắc Verdict:

| Verdict | Điều kiện |
|:---:|:---|
| ✅ **MUA** | Upside > 20%, moat rõ ràng, catalyst xác định, rủi ro quản lý được |
| 👀 **THEO DÕI** | Upside 10–20% HOẶC còn 1 yếu tố cần xác nhận thêm |
| ❌ **TRÁNH** | Rủi ro quản trị cao, value trap có dấu hiệu, thanh khoản kém |

### Quy tắc định dạng:
- Giá tính bằng **VNĐ** (ví dụ: 45,200 VNĐ)
- Vốn hóa tính bằng **tỷ VNĐ**
- Dùng bảng Markdown, tránh ASCII art
- Emoji: ✅ tốt, ⚠️ cần chú ý, ❌ xấu, 💰 định giá, 🏛️ moat, 🎯 catalyst
- Ghi rõ nguồn dữ liệu và thời điểm cập nhật

---

## NGUỒN DỮ LIỆU ĐỀ XUẤT

### Dữ liệu tài chính cơ bản:
| Nguồn | Loại dữ liệu | Cách truy cập |
|:---|:---|:---|
| **CafeF.vn** | BCTC, P/E, P/B, EPS, ROE | Web search / trực tiếp |
| **VietStock.vn** | So sánh bội số ngành, screener | Web search |
| **FireAnt.vn** | Dữ liệu thực, phân tích cộng đồng | Web search |
| **TCBS / MBS** | Báo cáo phân tích CTCK | Web search tên mã + "báo cáo phân tích" |
| **SSI Research** | Báo cáo ngành và công ty | Web search |
| **vnstock (Python)** | Dữ liệu lịch sử giá, tài chính API miễn phí | Script (xem companion skill) |

### Sử dụng companion skill:
Sau khi sàng lọc xong, với các mã được chọn, **kích hoạt `vietnam-stock-analysis` skill** để:
- Lấy dữ liệu OHLCV 200 phiên và phân tích kỹ thuật
- Xác định điểm mua tối ưu (entry point) dựa trên kỹ thuật
- Tích hợp phân tích cơ bản + kỹ thuật trong một báo cáo duy nhất

---

## ĐẶC THÙ THEO NGÀNH TẠI VN

### 🏦 Ngân hàng (BNK):
- **KHÔNG dùng** P/E và D/E thông thường
- Dùng: P/B, ROE, NIM (Net Interest Margin), NPL ratio, LDR (Loan-to-Deposit)
- P/B < 1x KHÔNG tự động là rẻ — có thể phản ánh NPL cao và rủi ro vốn
- Ngưỡng ROE tốt cho ngân hàng VN: > 15%
- NIM tốt: > 3.5%; NPL an toàn: < 2%

### 🏘️ Bất động sản (BDS):
- Dùng NAV (Net Asset Value) discount thay vì P/E
- Phân biệt: BDS nhà ở (phụ thuộc chính sách), BDS khu công nghiệp (theo FDI), BDS thương mại (REIT-like)
- KHÔNG dùng P/E cho BDS nếu lợi nhuận đến từ bàn giao dự án (lumpy revenue)
- Xem backlog (giá trị ký kết chưa ghi nhận) quan trọng hơn EPS hiện tại

### ⚙️ Thép & Vật liệu (THP):
- P/E rất biến động theo chu kỳ thép → dùng P/B và EV/EBITDA normalization
- Giá thép HRC thế giới là biến ngoại sinh quan trọng nhất
- FCF thường âm trong giai đoạn đầu tư mở rộng → không loại ngay nếu EBITDA tốt

### 💊 Y tế & Dược phẩm (YT):
- Định giá cao hơn mặt bằng chung (premium) là bình thường do tăng trưởng ổn định
- Phân biệt: Dược phẩm (ổn định, margin cao), Bệnh viện (capital intensive), Thiết bị y tế
- Chú ý: Phụ thuộc nhập khẩu nguyên liệu → rủi ro tỷ giá và chuỗi cung ứng

### 🏭 Khu công nghiệp (KCN):
- Định giá theo tỷ lệ lấp đầy và giá cho thuê trên mét vuông
- FDI vào Việt Nam là driver chính → theo dõi dữ liệu FDI hàng quý
- Quỹ đất KCN là tài sản chiến lược, P/B discount thường không hợp lý ở đây

---

## PIOTROSKI F-SCORE ĐẶC THÙ VN (Tham chiếu cho chế độ Deep Value)

Hệ thống 9 điểm nhị phân (0 hoặc 1):

**Nhóm lợi nhuận (4 điểm):**
| # | Tiêu chí | Điểm 1 nếu... |
|:---:|:---|:---|
| F1 | ROA | ROA > 0 |
| F2 | CFO | Dòng tiền hoạt động > 0 |
| F3 | ΔROA | ROA năm nay > ROA năm trước |
| F4 | Accruals | CFO > LNST (lợi nhuận "thật" hơn ghi nhận kế toán) |

**Nhóm đòn bẩy & thanh khoản (3 điểm):**
| # | Tiêu chí | Điểm 1 nếu... |
|:---:|:---|:---|
| F5 | Δ Leverage | Tỷ lệ nợ dài hạn/tổng tài sản giảm YoY |
| F6 | Δ Liquidity | Hệ số thanh toán hiện hành tăng YoY |
| F7 | Dilution | Không phát hành thêm cổ phiếu trong năm vừa qua |

**Nhóm hiệu quả hoạt động (2 điểm):**
| # | Tiêu chí | Điểm 1 nếu... |
|:---:|:---|:---|
| F8 | Δ Gross Margin | Biên lợi nhuận gộp tăng YoY |
| F9 | Δ Asset Turnover | Vòng quay tài sản tăng YoY |

**Phiên giải VN:**
- F-Score 0–2: Nguy hiểm (tránh)
- F-Score 3–5: Trung bình (cần phân tích thêm)
- F-Score 6–7: Tốt (ứng viên deep value)
- F-Score 8–9: Xuất sắc (strong candidate)

*Lưu ý VN: F7 (dilution) cần điều chỉnh — nhiều DNVN phát hành cổ phiếu thưởng từ thặng dư vốn, không pha loãng thực sự. Cần phân biệt phát hành thưởng vs phát hành huy động vốn.*

---

## QUY TẮC CỨNG (KHÔNG ĐƯỢC VI PHẠM)

1. **Không bao giờ** kết luận "MUA" chỉ vì P/E hoặc P/B thấp mà không phân tích nguyên nhân
2. **Bắt buộc** dùng LNST điều chỉnh (loại thu nhập bất thường) khi tính P/E
3. **Bắt buộc** tính FCF — nếu LNST tốt nhưng FCF âm liên tục → nghi ngờ chất lượng lợi nhuận
4. **Bắt buộc** xác định ít nhất 1 catalyst cụ thể cho mỗi mã khuyến nghị MUA
5. **Không bao giờ** bỏ qua phân tích rủi ro quản trị doanh nghiệp
6. Với cổ phiếu **thanh khoản < 5 tỷ VNĐ/ngày**: đưa vào "Theo dõi", không khuyến nghị MUA
7. **Mọi con số** phải ghi rõ nguồn và thời điểm dữ liệu
8. Kết quả sàng lọc chỉ là **tham khảo phân tích**, KHÔNG phải khuyến nghị đầu tư pháp lý

---

## TÀI LIỆU THAM KHẢO

- `references/bao_cao_value_screening.md` — Mẫu báo cáo hoàn chỉnh (ví dụ thực tế)
- `references/screening_methodology.md` — Chi tiết phương pháp lọc và ngưỡng theo từng ngành
- `references/luu_y_thi_truong_vn_value.md` — Cảnh báo đặc thù TTCK VN cho nhà đầu tư giá trị
- `references/piotroski_vn.md` — Hướng dẫn tính F-Score điều chỉnh cho VN
- Companion skill: `vietnam-stock-analysis/SKILL.md` — Phân tích kỹ thuật sau khi lọc xong

---

> ⚠️ **Tuyên bố miễn trách nhiệm**: Toàn bộ phân tích và kết quả sàng lọc trong skill này chỉ mang tính chất thông tin tham khảo, **KHÔNG** cấu thành lời khuyên đầu tư tài chính theo quy định của Luật Chứng khoán Việt Nam. "Rẻ" không đồng nghĩa với "đáng mua". Thị trường cổ phiếu có rủi ro — nhà đầu tư phải tự nghiên cứu và chịu trách nhiệm với mọi quyết định của mình.
