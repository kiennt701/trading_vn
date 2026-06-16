# Phương Pháp Sàng Lọc Chi Tiết — Thị Trường VN

## NGƯỠNG ĐỊNH GIÁ THEO NGÀNH (Dựa trên dữ liệu lịch sử VNIndex)

### Mức trung vị P/E và P/B theo ngành (cập nhật tham chiếu):

| Ngành | P/E Trung vị | P/B Trung vị | ROE TB | Ghi chú |
|:---|:---:|:---:|:---:|:---|
| Ngân hàng | 8–12x | 1.2–2.0x | 15–20% | Dùng P/B là chính |
| BĐS nhà ở | 12–20x | 2.0–3.5x | 12–18% | Biến động mạnh theo chu kỳ |
| BĐS KCN | 18–28x | 2.5–4.0x | 15–25% | Premium vì tăng trưởng FDI |
| Thép | 6–12x | 1.0–2.0x | 10–18% | Rất chu kỳ, dùng P/B chu kỳ thấp |
| Công nghệ | 18–30x | 3.0–6.0x | 20–35% | FPT làm méo trung bình ngành |
| Tiêu dùng thiết yếu | 15–22x | 3.0–5.0x | 20–30% | Defensive, định giá cao ổn định |
| Bán lẻ | 12–20x | 2.0–4.0x | 15–25% | MWG làm méo, cần tách |
| Dược phẩm | 16–25x | 2.5–4.5x | 18–28% | Ổn định, ít biến động |
| Dầu khí | 8–15x | 1.5–2.5x | 12–18% | Theo giá dầu |
| Xây dựng | 8–14x | 1.0–2.0x | 8–15% | Rủi ro đòn bẩy |
| Logistics | 12–18x | 1.5–3.0x | 12–20% | Tăng trưởng theo thương mại |
| Chứng khoán | 10–18x | 1.5–3.0x | 12–20% | Rất biến động theo margin |
| Thủy sản | 8–15x | 1.2–2.5x | 10–18% | Biến động theo xuất khẩu |
| Năng lượng/Điện | 10–16x | 1.2–2.2x | 10–16% | Ổn định, cổ tức tốt |

*Nguồn tham chiếu: VNDirect, SSI Research, VCSC (cập nhật theo mỗi chu kỳ thị trường)*
*Lưu ý: Ngưỡng thay đổi theo giai đoạn lãi suất — thị trường lãi suất cao = định giá thấp hơn*

---

## CÔNG THỨC TÍNH CÁC CHỈ SỐ ĐẶC THÙ

### LNST Điều Chỉnh (Adjusted Net Profit):

```
LNST_ĐC = LNST báo cáo
         - Thu nhập bất thường (thanh lý TS, bán công ty con)
         - Trợ cấp/miễn thuế một lần
         - Lãi/lỗ đầu tư tài chính ngắn hạn
         + Chi phí bất thường (nếu không tái diễn)
```

### FCF (Free Cash Flow) đơn giản:

```
FCF = Dòng tiền hoạt động (CFO) - Capex
    = LNST + Khấu hao + ΔVốn lưu động - Đầu tư TSCĐ
```

### ROIC (Return on Invested Capital):

```
ROIC = EBIT × (1 - Thuế suất thực)
       ÷ (Tổng tài sản - Tiền mặt - Nợ ngắn hạn không lãi)
```

### PEG Ratio (điều chỉnh cho VN):

```
PEG = P/E (trailing 12 tháng, dùng LNST ĐC)
      ÷ CAGR LNST 3 năm gần nhất (%)
```
*PEG < 1.0 = tiềm năng; PEG 1.0–1.5 = hợp lý; PEG > 2.0 = đắt*

### Chỉ Số Ngân Hàng Đặc Thù:

```
NIM = Thu nhập lãi thuần / Tài sản sinh lãi bình quân
CAR = Vốn tự có / Tài sản có rủi ro (Basel II: ≥ 8%)
NPL = Nợ xấu / Tổng dư nợ (tốt: < 2%, xấu: > 3%)
LDR = Dư nợ tín dụng / Huy động vốn (giới hạn SBV: ≤ 85%)
```

---

## THANG ĐIỂM VALUE COMPOSITE (0–100)

Dùng để xếp hạng các cổ phiếu sau khi lọc:

| Thành phần | Trọng số | Cách tính điểm |
|:---|:---:|:---|
| **Định giá tương đối** | 30% | Discount so với trung vị ngành: >30% = 30đ; 20–30% = 22đ; 10–20% = 15đ; <10% = 8đ |
| **Chất lượng lợi nhuận** | 25% | FCF/LNST > 80% = 25đ; 60–80% = 18đ; 40–60% = 12đ; < 40% = 5đ |
| **Tăng trưởng** | 20% | CAGR LNST 3 năm: >20% = 20đ; 10–20% = 15đ; 5–10% = 10đ; 0–5% = 5đ; <0 = 0đ |
| **ROIC vs WACC** | 15% | ROIC - WACC: >8% = 15đ; 4–8% = 11đ; 0–4% = 7đ; < 0 = 0đ |
| **Catalyst rõ ràng** | 10% | Có catalyst ngắn hạn xác định = 10đ; trung hạn = 7đ; chỉ dài hạn = 4đ; không rõ = 0đ |

**Kết quả:**
- 80–100: Value xuất sắc → ✅ MUA
- 60–79: Value tốt → 👀 THEO DÕI (chờ điểm vào kỹ thuật)
- 40–59: Trung bình → 📌 Danh mục giám sát
- < 40: Không đạt → ❌ Loại

---

## PHƯƠNG PHÁP DCF ĐƠN GIẢN CHO THỊ TRƯỜNG VN

### Tham số mặc định:

| Tham số | Giá trị | Ghi chú |
|:---|:---:|:---|
| WACC | 11% | Lãi suất phi rủi ro VN 10Y (~5%) + ERP (~6%) |
| WACC ngành ngân hàng | 12% | Rủi ro hệ thống cao hơn |
| WACC ngành công nghệ | 13% | Beta cao hơn |
| WACC ngành tiện ích/điện | 10% | Beta thấp, ổn định |
| Terminal Growth Rate | 4% | ≈ GDP VN dài hạn |
| Chiết khấu thanh khoản | -10% đến -20% | Với small-cap, mid-cap VN |
| Discount FOL premium | -5% đến -15% | Khi room ngoại đã đầy |

### Template DCF (5 năm):

```
FCF năm 1 = FCF gần nhất × (1 + g1)
FCF năm 2 = FCF năm 1 × (1 + g2)
...
Terminal Value = FCF năm 5 × (1 + g_terminal) / (WACC - g_terminal)

Intrinsic Value = Σ FCF_t / (1+WACC)^t + TV / (1+WACC)^5
                  - Nợ vay ròng
                  ÷ Số cổ phiếu lưu hành
```

*Khuyến nghị: Chạy 3 kịch bản (Base, Bull +20% g, Bear -20% g) và lấy kết quả xác suất trọng số 25%-50%-25%*

---

## ĐIỀU CHỈNH ĐẶC BIỆT CHO CÁC LOẠI HÌNH DOANH NGHIỆP VN

### Doanh nghiệp Nhà nước (DNNN):

Áp dụng thêm điều chỉnh:
- **Chiết khấu quản trị**: -10% đến -20% so với định giá thuần
- **Tuy nhiên tìm kiếm**: Tiến trình cổ phần hóa, cam kết cải thiện ROE, bổ nhiệm lãnh đạo từ khu vực tư nhân
- DNNN "tốt" để lọc: Có lộ trình rõ ràng về: tăng tỷ lệ cổ tức, thoái vốn SCIC, bổ sung độc lập vào HĐQT

### Doanh nghiệp gia đình (Family Business):

- Xem cấu trúc sở hữu: Người sáng lập nắm > 51% + nhiều vị trí quản lý = rủi ro
- Điểm cộng: Gia đình đang mua thêm (insider buying) là tín hiệu tích cực
- Điểm trừ: Giao dịch với bên liên quan chiếm > 20% doanh thu

### Công ty có Room Ngoại Đã Đầy:

- Giá thị trường có thể cao hơn giá "fair value" thuần do khan hiếm nguồn cung
- Khi phân tích định giá, chú ý: Nếu room vừa được nới → áp lực bán từ nhà đầu tư ngoại đang "mắc kẹt"
- Nếu room đầy + uptrend → tín hiệu demand mạnh từ khối ngoại

### Cổ Phiếu "Thị Giá Cao" nhưng Giá Trị Thực Thấp:

- KHÔNG nhầm giá cổ phiếu tuyệt đối với định giá (VCB giá 90,000đ không "đắt" hơn một cổ phiếu 5,000đ)
- So sánh luôn bằng các bội số (P/E, P/B, EV/EBITDA)
