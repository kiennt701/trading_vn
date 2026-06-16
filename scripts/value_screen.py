#!/usr/bin/env python3
"""
VN Value Screener — Script Lọc Cổ Phiếu Giá Trị
Companion script cho vn-value-screener skill

Sử dụng: python value_screen.py [--sector SECTOR] [--cap large|mid|small] [--top N]
Ví dụ:  python value_screen.py --sector BNK --top 10
         python value_screen.py --cap large --top 15
         python value_screen.py --top 10  (toàn thị trường)
"""

import sys
import json
import argparse
from datetime import datetime, timedelta

try:
    import pandas as pd
    import numpy as np
    from vnstock3 import Vnstock
except ImportError:
    print("⚠️  Cài thư viện cần thiết:")
    print("    pip install vnstock3 pandas numpy --break-system-packages")
    sys.exit(1)

# ============================================================
# CẤU HÌNH
# ============================================================
WACC_DEFAULT = 0.11           # 11% — WACC mặc định thị trường VN
TERMINAL_GROWTH = 0.04        # 4% — Tăng trưởng terminal (≈ GDP dài hạn VN)
MIN_MARKETCAP_BILLION = 200   # 200 tỷ VNĐ — Loại shell/micro-cap
MIN_LIQUIDITY_BILLION = 5     # 5 tỷ VNĐ/ngày — Thanh khoản tối thiểu

# Ngưỡng vốn hóa (tỷ VNĐ)
CAP_THRESHOLDS = {
    "large": 10_000,   # > 10,000 tỷ
    "mid":   1_000,    # 1,000 – 10,000 tỷ
    "small": 0         # < 1,000 tỷ
}

# Danh sách ngành và mã đại diện
SECTOR_MAP = {
    "BNK": ["VCB", "BID", "CTG", "TCB", "MBB", "ACB", "VPB", "HDB", "SHB", "MSB", "STB"],
    "BDS": ["VHM", "VIC", "NLG", "KDH", "DXG", "PDR", "HDG", "CEO", "DIG"],
    "THP": ["HPG", "HSG", "NKG", "VIS", "TIS", "SMC"],
    "CNT": ["FPT", "CMG", "VGI", "ELC"],
    "TDG": ["VNM", "MSN", "SAB", "QNS", "MCH"],
    "BLE": ["MWG", "PNJ", "FRT", "DGW"],
    "YT":  ["DHG", "IMP", "DMC", "TNH", "DBD"],
    "DKH": ["GAS", "PLX", "PVS", "PVD", "BSR"],
    "XD":  ["HBC", "CTD", "VCG", "BMP", "PHC"],
    "LSX": ["GMD", "HAH", "VTP", "STG"],
    "CK":  ["SSI", "VCI", "HCM", "MBS", "SHS", "VND"],
    "NN":  ["VHC", "ANV", "IDI", "HAG", "HVN"],
    "CN":  ["REE", "GEG", "PPC", "NT2", "BCG"],
    "KCN": ["BCM", "KBC", "SZC", "PHR", "D2D"],
}

def get_all_tickers():
    """Lấy danh sách tất cả mã chứng khoán"""
    try:
        stock = Vnstock().stock(symbol="VCB", source="VCI")
        listing = stock.listing.all_symbols()
        return listing["ticker"].tolist() if "ticker" in listing.columns else []
    except Exception as e:
        print(f"⚠️  Không lấy được danh sách mã: {e}")
        # Fallback: dùng danh sách mã trong SECTOR_MAP
        all_tickers = []
        for tickers in SECTOR_MAP.values():
            all_tickers.extend(tickers)
        return list(set(all_tickers))

def get_financial_data(ticker: str) -> dict:
    """Lấy dữ liệu tài chính cơ bản của một mã"""
    try:
        stock = Vnstock().stock(symbol=ticker, source="TCBS")
        
        # Lấy dữ liệu định giá
        result = {"ticker": ticker, "error": None}
        
        # Income statement (4 quý gần nhất)
        try:
            income = stock.finance.income_statement(period="quarter", lang="en")
            if income is not None and len(income) >= 4:
                # Tổng hợp TTM (trailing 12 months)
                ttm_revenue = income["revenue"].iloc[:4].sum()
                ttm_net_income = income["post_tax_profit"].iloc[:4].sum()
                result["ttm_revenue"] = float(ttm_revenue) if ttm_revenue else None
                result["ttm_net_income"] = float(ttm_net_income) if ttm_net_income else None
                
                # Kiểm tra lợi nhuận âm
                if result["ttm_net_income"] and result["ttm_net_income"] < 0:
                    result["excluded"] = "LNST âm"
                    return result
        except:
            result["ttm_revenue"] = None
            result["ttm_net_income"] = None
        
        # Balance sheet
        try:
            balance = stock.finance.balance_sheet(period="quarter", lang="en")
            if balance is not None and len(balance) >= 1:
                latest = balance.iloc[0]
                result["total_assets"] = float(latest.get("total_assets", 0) or 0)
                result["total_equity"] = float(latest.get("owner_equity", 0) or 0)
                result["total_debt"] = float(latest.get("short_term_borrowing", 0) or 0) + \
                                       float(latest.get("long_term_borrowing", 0) or 0)
                result["cash"] = float(latest.get("cash", 0) or 0)
        except:
            result["total_assets"] = None
            result["total_equity"] = None
            result["total_debt"] = None
            result["cash"] = None
        
        # Cash flow
        try:
            cashflow = stock.finance.cash_flow(period="annual", lang="en")
            if cashflow is not None and len(cashflow) >= 1:
                result["cfo"] = float(cashflow["from_operating"].iloc[0] or 0)
                result["capex"] = abs(float(cashflow["purchase_fixed_assets"].iloc[0] or 0))
                result["fcf"] = result["cfo"] - result["capex"]
                
                # FCF 3 năm gần nhất
                if len(cashflow) >= 3:
                    fcf_3y = []
                    for i in range(3):
                        cfo = float(cashflow["from_operating"].iloc[i] or 0)
                        capex = abs(float(cashflow["purchase_fixed_assets"].iloc[i] or 0))
                        fcf_3y.append(cfo - capex)
                    result["fcf_positive_years"] = sum(1 for f in fcf_3y if f > 0)
                else:
                    result["fcf_positive_years"] = 1 if result.get("fcf", 0) > 0 else 0
        except:
            result["fcf"] = None
            result["fcf_positive_years"] = None
        
        # Ratio / Market data
        try:
            ratio = stock.finance.ratio(period="quarter", lang="en")
            if ratio is not None and len(ratio) >= 1:
                latest_ratio = ratio.iloc[0]
                result["pe"] = float(latest_ratio.get("price_to_earning", 0) or 0)
                result["pb"] = float(latest_ratio.get("price_to_book", 0) or 0)
                result["roe"] = float(latest_ratio.get("roe", 0) or 0)
                result["roa"] = float(latest_ratio.get("roa", 0) or 0)
                result["eps"] = float(latest_ratio.get("earning_per_share", 0) or 0)
                
                # Lọc PE/PB vô lý
                if result["pe"] and result["pe"] < 0:
                    result["excluded"] = "PE âm"
                    return result
        except:
            result["pe"] = None
            result["pb"] = None
            result["roe"] = None
        
        # Market cap & price
        try:
            overview = stock.trading.price_board()
            if overview is not None and len(overview) > 0:
                row = overview.iloc[0]
                result["price"] = float(row.get("close", 0) or 0) * 1000  # Giá VNĐ đầy đủ
                result["shares"] = float(row.get("listed_share", 0) or 0)
                result["market_cap"] = result["price"] * result["shares"] / 1e9  # Tỷ VNĐ
                
                # Loại vốn hóa quá nhỏ
                if result["market_cap"] < MIN_MARKETCAP_BILLION:
                    result["excluded"] = f"Vốn hóa < {MIN_MARKETCAP_BILLION}B"
                    return result
        except:
            result["price"] = None
            result["shares"] = None
            result["market_cap"] = None
        
        return result
        
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

def compute_value_score(data: dict) -> float:
    """Tính điểm Value Composite (0-100)"""
    score = 0
    
    # 1. Định giá tương đối (30đ) — Dùng PE < 15 làm ngưỡng reference
    pe = data.get("pe")
    if pe and pe > 0:
        if pe < 8:   score += 30
        elif pe < 12: score += 22
        elif pe < 16: score += 15
        elif pe < 20: score += 8
        else:         score += 3
    
    # 2. Chất lượng FCF (25đ)
    fcf_years = data.get("fcf_positive_years")
    if fcf_years is not None:
        if fcf_years >= 3: score += 25
        elif fcf_years == 2: score += 18
        elif fcf_years == 1: score += 10
        else: score += 0
    
    # 3. ROE (20đ)
    roe = data.get("roe")
    if roe:
        if roe > 20:   score += 20
        elif roe > 15: score += 15
        elif roe > 10: score += 10
        elif roe > 5:  score += 5
        else:          score += 0
    
    # 4. PB (15đ)
    pb = data.get("pb")
    if pb and pb > 0:
        if pb < 1.0:   score += 15
        elif pb < 1.5: score += 11
        elif pb < 2.5: score += 7
        elif pb < 4.0: score += 3
        else:          score += 0
    
    # 5. Đòn bẩy (10đ)
    debt = data.get("total_debt", 0) or 0
    equity = data.get("total_equity", 1) or 1
    leverage = debt / equity if equity > 0 else 999
    if leverage < 0.3:   score += 10
    elif leverage < 0.8: score += 7
    elif leverage < 1.5: score += 4
    elif leverage < 3.0: score += 2
    else:                score += 0
    
    return round(score, 1)

def filter_stocks(tickers: list, cap_filter: str = None, top_n: int = 10) -> list:
    """Lọc và xếp hạng cổ phiếu theo tiêu chí value"""
    
    print(f"\n🔍 Đang quét {len(tickers)} mã cổ phiếu...")
    print("   Vui lòng chờ (mỗi mã ~2-3 giây)...\n")
    
    results = []
    excluded = {"pe_am": 0, "lnst_am": 0, "von_hoa_nho": 0, "loi": 0}
    
    for i, ticker in enumerate(tickers):
        if i % 10 == 0:
            print(f"   [{i+1}/{len(tickers)}] Đang xử lý {ticker}...")
        
        data = get_financial_data(ticker)
        
        if data.get("error"):
            excluded["loi"] += 1
            continue
        
        if data.get("excluded"):
            reason = data["excluded"]
            if "PE âm" in reason or "LNST âm" in reason:
                excluded["lnst_am"] += 1
            elif "Vốn hóa" in reason:
                excluded["von_hoa_nho"] += 1
            continue
        
        # Lọc theo vốn hóa
        market_cap = data.get("market_cap", 0) or 0
        if cap_filter == "large" and market_cap < CAP_THRESHOLDS["large"]:
            continue
        elif cap_filter == "mid" and (market_cap < CAP_THRESHOLDS["mid"] or 
                                       market_cap >= CAP_THRESHOLDS["large"]):
            continue
        elif cap_filter == "small" and market_cap >= CAP_THRESHOLDS["mid"]:
            continue
        
        # Tính điểm
        data["value_score"] = compute_value_score(data)
        results.append(data)
    
    # Sắp xếp theo điểm value
    results.sort(key=lambda x: x.get("value_score", 0), reverse=True)
    
    print(f"\n✅ Quét xong!")
    print(f"   Tổng quét: {len(tickers)} mã")
    print(f"   Loại trừ (LNST âm/PE âm): {excluded['lnst_am']} mã")
    print(f"   Loại trừ (vốn hóa nhỏ): {excluded['von_hoa_nho']} mã")
    print(f"   Lỗi dữ liệu: {excluded['loi']} mã")
    print(f"   Đạt tiêu chí: {len(results)} mã")
    print(f"   Trình bày top {min(top_n, len(results))} mã\n")
    
    return results[:top_n]

def print_report(results: list, sector: str = None, cap_filter: str = None):
    """In báo cáo dạng Markdown"""
    
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    print(f"\n{'='*80}")
    print(f"🔍 BÁO CÁO SÀNG LỌC CỔ PHIẾU GIÁ TRỊ — {now}")
    print(f"{'='*80}")
    
    scope = SECTOR_MAP.get(sector, {}) if sector else "Toàn thị trường"
    print(f"Phạm vi: {sector if sector else 'Toàn thị trường'}")
    print(f"Vốn hóa: {cap_filter if cap_filter else 'Không giới hạn'}")
    print()
    
    # Bảng tổng hợp
    print("| # | Mã | Giá (VNĐ) | Vốn hóa (tỷ) | P/E | P/B | ROE% | FCF+ | Điểm |")
    print("|:--:|:--:|--:|--:|:--:|:--:|:--:|:--:|:--:|")
    
    for i, d in enumerate(results, 1):
        ticker = d.get("ticker", "???")
        price = d.get("price")
        price_str = f"{price:,.0f}" if price else "N/A"
        
        market_cap = d.get("market_cap")
        cap_str = f"{market_cap:,.0f}" if market_cap else "N/A"
        
        pe = d.get("pe")
        pe_str = f"{pe:.1f}x" if pe and pe > 0 else "N/A"
        
        pb = d.get("pb")
        pb_str = f"{pb:.2f}x" if pb and pb > 0 else "N/A"
        
        roe = d.get("roe")
        roe_str = f"{roe:.1f}%" if roe else "N/A"
        
        fcf_years = d.get("fcf_positive_years")
        fcf_str = f"{fcf_years}/3" if fcf_years is not None else "N/A"
        
        score = d.get("value_score", 0)
        verdict = "✅" if score >= 70 else ("👀" if score >= 55 else "📌")
        
        print(f"| {i} | **{ticker}** | {price_str} | {cap_str} | {pe_str} | {pb_str} | {roe_str} | {fcf_str} | {score} {verdict} |")
    
    print()
    print("**Ghi chú**: Điểm ≥70 = ✅ Theo dõi mua; 55-69 = 👀 Theo dõi; <55 = 📌 Giám sát")
    print()
    print("---")
    print("⚠️ **Tuyên bố miễn trách nhiệm**: Kết quả chỉ mang tính tham khảo, KHÔNG phải khuyến nghị đầu tư.")
    
    return results

def save_results(results: list, filename: str = None):
    """Lưu kết quả ra file JSON"""
    if not filename:
        filename = f"value_screen_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    output = {
        "generated_at": datetime.now().isoformat(),
        "results": results
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n💾 Kết quả đã lưu: {filename}")

def main():
    parser = argparse.ArgumentParser(
        description="VN Value Screener — Lọc cổ phiếu giá trị thị trường Việt Nam"
    )
    parser.add_argument("--sector", type=str, default=None,
                       choices=list(SECTOR_MAP.keys()),
                       help=f"Lọc theo ngành: {', '.join(SECTOR_MAP.keys())}")
    parser.add_argument("--cap", type=str, default=None,
                       choices=["large", "mid", "small"],
                       help="Lọc theo vốn hóa: large (>10,000B), mid (1,000-10,000B), small (<1,000B)")
    parser.add_argument("--top", type=int, default=10,
                       help="Số mã trình bày (mặc định: 10)")
    parser.add_argument("--save", action="store_true",
                       help="Lưu kết quả ra file JSON")
    
    args = parser.parse_args()
    
    # Lấy danh sách mã cần quét
    if args.sector:
        tickers = SECTOR_MAP.get(args.sector, [])
        print(f"\n📋 Quét ngành {args.sector}: {len(tickers)} mã")
    else:
        tickers = get_all_tickers()
        if not tickers:
            # Fallback nếu không lấy được danh sách toàn thị trường
            tickers = []
            for t in SECTOR_MAP.values():
                tickers.extend(t)
            tickers = list(set(tickers))
            print(f"\n⚠️  Dùng danh sách mã tích hợp: {len(tickers)} mã")
        else:
            print(f"\n📋 Quét toàn thị trường: {len(tickers)} mã")
    
    # Lọc và xếp hạng
    results = filter_stocks(tickers, cap_filter=args.cap, top_n=args.top)
    
    # In báo cáo
    print_report(results, sector=args.sector, cap_filter=args.cap)
    
    # Lưu nếu cần
    if args.save:
        save_results(results)

if __name__ == "__main__":
    main()
