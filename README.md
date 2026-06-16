# VN Value Screener — Bộ Lọc Cổ Phiếu Giá Trị Việt Nam

## Tổng quan

Skill này biến Claude thành **Chuyên gia Phân tích Nghiên cứu Vốn Cổ Phần (Equity Research Analyst)**, chuyên tìm cổ phiếu niêm yết tại Việt Nam (HOSE, HNX, UPCOM) có nền tảng cơ bản vững nhưng đang bị định giá thấp hơn giá trị thực.

**Nguồn gốc**: Điều chỉnh từ hệ thống lọc cổ phiếu A-share Trung Quốc, tối ưu hóa toàn diện cho đặc thù TTCK Việt Nam.

## Cấu trúc thư mục

```
vn-value-screener/
├── SKILL.md                          ← File skill chính (đọc vào context Claude)
├── README.md                         ← File này
├── references/
│   ├── bao_cao_value_screening.md   ← Mẫu báo cáo hoàn chỉnh (ví dụ MWG)
│   ├── screening_methodology.md     ← Phương pháp lọc, ngưỡng theo ngành, công thức
│   └── luu_y_thi_truong_vn_value.md ← Cảnh báo value trap, red flag, green flag
└── scripts/
    └── value_screen.py               ← Script Python tự động lọc qua vnstock3
```

## Cách kích hoạt

Skill được kích hoạt khi người dùng hỏi về:
- "Tìm cổ phiếu đang bị định giá thấp"
- "Cổ phiếu nào PE/PB thấp ngành ngân hàng?"
- "Lọc cổ phiếu giá trị trong VN30"
- "Screening cổ phiếu theo ROE và FCF"
- "Tìm hidden gem thị trường VN"

## Quy trình 4 bước

1. **Xác nhận tham số** (phạm vi, vốn hóa, số lượng, trọng tâm)
2. **Áp dụng bộ lọc** (loại trừ tự động + tiêu chí theo trọng tâm)
3. **Phân tích chuyên sâu** (moat, lý do định giá thấp, rủi ro, định giá 3 phương pháp)
4. **Xuất báo cáo** (bảng xếp hạng + phân tích từng mã + verdict)

## Điểm khác biệt so với bộ lọc A-share gốc

| Chiều | A-share (Trung Quốc) | VN (Skill này) |
|:---|:---|:---|
| So sánh ngành | Theo phân loại Shenwan L1 | Theo GICS điều chỉnh cho VN (14 ngành) |
| Ngưỡng loại trừ | ST/*ST công ty | Cổ phiếu cảnh báo/kiểm soát UBCK |
| Lợi nhuận | Loại phi tái diễn (非经常性损益) | LNST điều chỉnh (loại trợ cấp, miễn thuế) |
| Ngân hàng | Phân tích riêng | Bổ sung NIM, NPL, LDR, CAR đặc thù |
| BĐS | Phân tích riêng | Bổ sung NAV discount, backlog, KCN vs nhà ở |
| DCF | WACC A-share | WACC VN = 11% (lãi suất VN + ERP VN) |
| Piotroski | F-Score chuẩn | Điều chỉnh F7 cho phát hành thưởng VN |
| Thanh khoản | Giới hạn A-share | ≥5 tỷ VNĐ/ngày, chú ý T+2 và ATC |
| Room ngoại | Không có | Tích hợp phân tích FOL premium |
| Cảnh báo | Chú ý shell value | Chú ý margin call, thời vụ Tết |

## Chạy Script Tự động

```bash
# Cài thư viện
pip install vnstock3 pandas numpy --break-system-packages

# Quét toàn thị trường, top 10
python scripts/value_screen.py --top 10

# Quét ngành ngân hàng
python scripts/value_screen.py --sector BNK --top 5

# Quét large-cap, lưu kết quả
python scripts/value_screen.py --cap large --top 15 --save
```

## Companion Skill

Sau khi xác định được mã cổ phiếu đáng quan tâm, kết hợp với **`vietnam-stock-analysis`** để:
- Lấy dữ liệu OHLCV 200 phiên và phân tích kỹ thuật đầy đủ
- Xác định điểm mua tối ưu (entry point) theo MA, RSI, MACD
- Tích hợp phân tích cơ bản (value) + kỹ thuật trong một báo cáo hoàn chỉnh

## Tuyên bố miễn trách nhiệm

Toàn bộ phân tích chỉ mang tính tham khảo, **KHÔNG** phải khuyến nghị đầu tư theo Luật Chứng khoán Việt Nam. "Rẻ" ≠ "đáng mua". Thị trường cổ phiếu có rủi ro — nhà đầu tư phải tự nghiên cứu và chịu trách nhiệm.
