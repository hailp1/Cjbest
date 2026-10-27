import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Starting build of RTM Model web application with Regional Filtering & Outlets Button...")

# 1. Load 391 NPPs data
json_path = 'C:/Users/IT-Backup/.gemini/antigravity-ide/brain/05b5759a-74ee-4579-a357-dad63829fe76/scratch/final_combined_391_map_data.json'
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        combined_data = json.load(f)
    npps = combined_data.get('npps', [])
else:
    with open('d:/SE_Project/RTM_Model/index.html', 'r', encoding='utf-8') as f:
        text = f.read()
    start = text.find('const ALL_NPPS = ') + len('const ALL_NPPS = ')
    end = text.find(';\n    let ALL_OUTLETS', start)
    npps = json.loads(text[start:end])

total_count = len(npps)
active_count = sum(1 for n in npps if 'Đang' in n.get('status', ''))
inactive_count = total_count - active_count
print(f"Loaded {total_count} NPPs ({active_count} active, {inactive_count} inactive).")

# 1.1 Enrich NPPs with SM and Sales Rep info from loai_npp.csv
loai_csv_path = 'd:/SE_Project/RTM_Model/loai_npp.csv'
loai_dict = {}
if os.path.exists(loai_csv_path):
    import csv
    with open(loai_csv_path, 'r', encoding='utf-8') as lf:
        reader = csv.DictReader(lf)
        for r in reader:
            raw_code = r.get('MaNPP', '').strip()
            if not raw_code:
                continue
            try:
                c = str(int(float(raw_code)))
            except:
                c = raw_code
            so_nvbh_raw = r.get('SoNVBH', '').strip()
            is_ksm = so_nvbh_raw.lower() in ['không sm', 'khong sm', '0', '', 'nan', 'none']
            top50_raw = r.get('Top50', '').strip()
            loai_dict[c] = {
                'so_nvbh': 0 if is_ksm else (int(so_nvbh_raw) if so_nvbh_raw.isdigit() else 1),
                'so_nvbh_text': 'Không SM' if is_ksm else f"{so_nvbh_raw} NVBH",
                'is_khong_sm': is_ksm,
                'sm_status': 'Không SM' if is_ksm else 'Có SM',
                'top50': 1 if top50_raw == '1' else 0,
                'gsbh': r.get('TenGSBH', '').strip(),
                'asm_rsm': r.get('ASM_RSM', '').strip(),
                'office': r.get('Office', '').strip()
            }

for n in npps:
    c = str(n.get('code', '')).strip()
    if c in loai_dict:
        info = loai_dict[c]
        n['so_nvbh'] = info['so_nvbh']
        n['so_nvbh_text'] = info['so_nvbh_text']
        n['is_khong_sm'] = info['is_khong_sm']
        n['sm_status'] = info['sm_status']
        n['top50'] = info['top50']
        n['gsbh'] = info['gsbh']
        n['asm_rsm'] = info['asm_rsm']
        n['office'] = info['office']
    else:
        is_inact = not n.get('status', '').startswith('Đang')
        n['so_nvbh'] = 0
        n['so_nvbh_text'] = 'Chưa gán SM' if not is_inact else 'Ngưng hoạt động'
        n['is_khong_sm'] = True
        n['sm_status'] = 'Không SM'
        n['top50'] = 0
        n['gsbh'] = ''
        n['asm_rsm'] = ''
        n['office'] = ''

ksm_active = sum(1 for n in npps if n.get('status', '').startswith('Đang') and n.get('is_khong_sm'))
csm_active = sum(1 for n in npps if n.get('status', '').startswith('Đang') and not n.get('is_khong_sm'))
print(f"Enriched SM status: {csm_active} Active Có SM, {ksm_active} Active Không SM.")

# 1.2 Enrich NPPs with Sales Revenue T9/2026 from doanh_so_t92026_clean.csv
sales_csv_path = 'd:/SE_Project/RTM_Model/doanh_so_t92026_clean.csv'
sales_dict = {}
if os.path.exists(sales_csv_path):
    import csv
    with open(sales_csv_path, 'r', encoding='utf-8') as sf:
        reader = csv.reader(sf)
        header = next(reader, None)
        for row in reader:
            if not row or not row[0]: continue
            raw_c = row[0].strip().replace('\ufeff', '').replace('"', '')
            try:
                c = str(int(float(raw_c)))
            except:
                c = raw_c
            try: amb = float(row[2]) if len(row) > 2 and row[2] else 0.0
            except: amb = 0.0
            try: chi = float(row[3]) if len(row) > 3 and row[3] else 0.0
            except: chi = 0.0
            try: fro = float(row[4]) if len(row) > 4 and row[4] else 0.0
            except: fro = 0.0
            tot = amb + chi + fro
            sales_dict[c] = {
                'ambient': amb,
                'chilled': chi,
                'frozen': fro,
                'total': tot
            }

sales_matched = 0
for n in npps:
    c = str(n.get('code', '')).strip()
    if c in sales_dict:
        sinfo = sales_dict[c]
        n['sales_ambient'] = sinfo['ambient']
        n['sales_chilled'] = sinfo['chilled']
        n['sales_frozen'] = sinfo['frozen']
        n['sales_total'] = sinfo['total']
        n['has_sales'] = True
        sales_matched += 1
    else:
        n['sales_ambient'] = 0.0
        n['sales_chilled'] = 0.0
        n['sales_frozen'] = 0.0
        n['sales_total'] = 0.0
        n['has_sales'] = False

print(f"Enriched Sales Revenue T9/2026: {sales_matched} NPPs matched.")


# 2. Build complete HTML
npps_json_str = json.dumps(npps, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <title>RTM Spatial Model - Bản Đồ Phân Phối Toàn Quốc & Phân Tích Cự Ly Giao Hàng</title>
  
  <!-- Google Fonts & Font Awesome -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"/>
  
  <!-- 100% Free OpenSource Leaflet GIS (NO API KEY REQUIRED) -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css"/>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>

  <!-- Load dữ liệu 59,366 điểm bán & Phân tích cự ly ở chế độ DEFER để giao diện mobile tải NGAY LẬP TỨC -->
  <script src="npp_analytics_data.js" defer></script>

  <style>
    :root {{
      --primary: #0f172a;
      --primary-light: #1e293b;
      --accent: #2563eb;
      --danger: #dc2626;
      --warning: #d97706;
      --success: #059669;
      --border: #334155;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
    html, body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #0f172a;
      color: #0f172a;
      width: 100%;
      height: 100%;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    /* Header */
    header {{
      background: #0f172a;
      color: #ffffff;
      padding: 0.5rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1e293b;
      z-index: 1000;
      flex-shrink: 0;
    }}
    .header-left {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}
    .header-badge {{
      background: rgba(37, 99, 235, 0.2);
      border: 1px solid rgba(59, 130, 246, 0.5);
      color: #60a5fa;
      padding: 2px 7px;
      border-radius: 5px;
      font-size: 0.72rem;
      font-weight: 700;
    }}
    .header-badge.outlets-badge {{
      background: rgba(245, 158, 11, 0.2);
      border-color: rgba(245, 158, 11, 0.5);
      color: #fbbf24;
    }}
    .header-badge.cold-badge {{
      background: rgba(14, 165, 233, 0.2);
      border-color: rgba(14, 165, 233, 0.5);
      color: #38bdf8;
    }}
    h1 {{
      font-size: 1rem;
      font-weight: 800;
      letter-spacing: -0.3px;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .header-right {{
      display: flex;
      gap: 0.4rem;
      align-items: center;
    }}
    .btn-nav {{
      background: #1e293b;
      color: #e2e8f0;
      border: 1px solid #334155;
      padding: 5px 9px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .btn-nav:hover {{
      background: #334155;
      color: #ffffff;
    }}

    /* ==========================================================
       UNIFIED FLOATING ISLAND TOOLBAR (THIẾT KẾ 1 HÀNG TINH GỌN)
       ========================================================== */
    .filter-bar {{
      background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
      padding: 5px 12px;
      border-bottom: 1px solid #334155;
      display: flex;
      align-items: center;
      justify-content: flex-start;
      gap: 8px;
      z-index: 999;
      flex-shrink: 0;
      flex-wrap: nowrap;
      overflow-x: auto;
      scrollbar-width: none;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
    }}
    .filter-bar::-webkit-scrollbar {{ display: none; }}

    .toolbar-cluster {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(51, 65, 85, 0.8);
      padding: 3px 6px;
      border-radius: 8px;
      backdrop-filter: blur(8px);
      flex-shrink: 0;
    }}
    .toolbar-item {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      position: relative;
    }}
    .island-select {{
      background: #0f172a;
      border: 1px solid #334155;
      color: #f1f5f9;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 4px 7px;
      border-radius: 6px;
      outline: none;
      cursor: pointer;
      transition: all 0.2s;
      max-width: 175px;
    }}
    .island-select:hover, .island-select:focus {{
      border-color: #38bdf8;
      background: #1e293b;
    }}
    .island-search {{
      background: #0f172a;
      border: 1px solid #334155;
      color: #f1f5f9;
      font-size: 0.72rem;
      font-weight: 500;
      padding: 4px 8px 4px 24px;
      border-radius: 6px;
      outline: none;
      width: 135px;
      transition: all 0.2s;
    }}
    .island-search:focus {{
      width: 185px;
      border-color: #10b981;
      background: #1e293b;
    }}
    .search-icon {{
      position: absolute;
      left: 7px;
      font-size: 0.68rem;
      color: #64748b;
      pointer-events: none;
    }}

    .island-btn {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #e2e8f0;
      padding: 4px 9px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
      white-space: nowrap;
      user-select: none;
    }}
    .island-btn:hover {{
      background: #334155;
      color: #ffffff;
    }}
    .island-btn.active-npp {{
      background: rgba(5, 150, 105, 0.25);
      border-color: #10b981;
      color: #a7f3d0;
    }}
    .island-btn.active-outlet {{
      background: rgba(245, 158, 11, 0.25) !important;
      border-color: #f59e0b !important;
      color: #fef08a !important;
    }}
    .island-btn-hero {{
      background: linear-gradient(135deg, #059669 0%, #10b981 100%);
      color: #ffffff !important;
      border: 1px solid #34d399;
      padding: 4px 11px;
      border-radius: 6px;
      font-size: 0.73rem;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.35);
      transition: all 0.2s;
      white-space: nowrap;
    }}
    .island-btn-hero:hover {{
      background: linear-gradient(135deg, #047857 0%, #059669 100%);
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(16, 185, 129, 0.5);
    }}
    .island-btn-hero.active-spatial {{
      background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%) !important;
      border-color: #f87171 !important;
      box-shadow: 0 0 14px rgba(239, 68, 68, 0.6) !important;
    }}

    /* Dropdown Menus */
    .dropdown-wrapper {{
      position: relative;
      display: inline-block;
    }}
    .island-dropdown-menu {{
      position: absolute;
      top: calc(100% + 6px);
      left: 0;
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 10px;
      box-shadow: 0 14px 36px rgba(0, 0, 0, 0.75);
      min-width: 260px;
      z-index: 10000;
      display: none;
      flex-direction: column;
      padding: 6px 0;
      backdrop-filter: blur(12px);
      animation: menuFadeIn 0.15s ease-out;
    }}
    .island-dropdown-menu.right-aligned {{
      left: auto;
      right: 0;
    }}
    .island-dropdown-menu.show {{
      display: flex;
    }}
    @keyframes menuFadeIn {{
      from {{ opacity: 0; transform: translateY(-4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .dropdown-header {{
      padding: 6px 12px;
      font-size: 0.65rem;
      font-weight: 800;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.5);
      margin-bottom: 4px;
    }}
    .dropdown-menu-item {{
      padding: 7px 12px;
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      user-select: none;
      transition: background 0.15s;
      text-decoration: none;
    }}
    .dropdown-menu-item:hover {{
      background: #1e293b;
    }}
    .item-icon-box {{
      width: 24px;
      height: 24px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      flex-shrink: 0;
    }}
    .item-text {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .item-title {{
      font-size: 0.74rem;
      font-weight: 700;
      color: #f1f5f9;
    }}
    .item-sub {{
      font-size: 0.64rem;
      color: #94a3b8;
    }}
    .badge-mini {{
      font-size: 0.65rem;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
    }}
    .dropdown-divider {{
      height: 1px;
      background: rgba(51, 65, 85, 0.6);
      margin: 4px 0;
    }}
    .zoom-mini-btn {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #e2e8f0;
      font-size: 0.65rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      cursor: pointer;
    }}
    .zoom-mini-btn:hover {{
      background: #334155;
      color: #38bdf8;
    }}
    .island-kpi-pill {{
      display: flex;
      align-items: center;
      gap: 5px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid #334155;
      padding: 4px 9px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      color: #94a3b8;
      white-space: nowrap;
      margin-left: auto;
    }}
    .kpi-tag {{ color: #38bdf8; }}
    .kpi-val {{ color: #10b981; font-weight: 800; }}
    .kpi-outlets {{ color: #fbbf24; font-weight: 800; }}
    .kpi-divider {{ color: #475569; }}

    /* Map Zoom Pill */
    .map-preset-pills {{
      position: absolute;
      top: 10px;
      left: 60px;
      z-index: 900;
      display: flex;
      gap: 4px;
      background: rgba(15, 23, 42, 0.85);
      padding: 3px 5px;
      border-radius: 6px;
      border: 1px solid #334155;
      backdrop-filter: blur(4px);
    }}
    .preset-pill {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #cbd5e1;
      padding: 3px 7px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .preset-pill:hover {{
      background: #334155;
      color: #ffffff;
    }}

    /* Layout Main */
    .main-container {{
      flex: 1;
      min-height: 0;
      display: flex;
      position: relative;
      overflow: hidden;
    }}

    #map {{
      flex: 1;
      height: 100%;
      background: #0b1120;
    }}

    /* Sidebar Drawer */
    .sidebar {{
      width: 330px;
      background: #1e293b;
      border-left: 1px solid #334155;
      display: flex;
      flex-direction: column;
      z-index: 1000;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      flex-shrink: 0;
    }}
    .sidebar-header {{
      padding: 8px 12px;
      background: #0f172a;
      border-bottom: 1px solid #334155;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .sidebar-title {{
      font-size: 0.8rem;
      font-weight: 800;
      color: #f1f5f9;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .sidebar-content {{
      flex: 1;
      overflow-y: auto;
      padding: 6px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    /* NPP Card in Sidebar */
    .npp-card {{
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 8px 10px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .npp-card:hover, .npp-card.selected {{
      border-color: #2563eb;
      background: #1e293b;
    }}
    .npp-card.selected {{
      box-shadow: 0 0 0 1px #2563eb;
    }}
    .npp-header-row {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 3px;
    }}
    .npp-code {{
      font-size: 0.75rem;
      font-weight: 800;
      color: #60a5fa;
    }}
    .badge-status {{
      font-size: 0.62rem;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 4px;
    }}
    .badge-active {{ background: rgba(5, 150, 105, 0.2); color: #34d399; border: 1px solid rgba(5, 150, 105, 0.4); }}
    .badge-inactive {{ background: rgba(220, 38, 38, 0.2); color: #f87171; border: 1px solid rgba(220, 38, 38, 0.4); }}

    .npp-title {{
      font-size: 0.75rem;
      font-weight: 700;
      color: #f8fafc;
      margin-bottom: 4px;
      line-height: 1.3;
    }}
    .npp-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      font-size: 0.68rem;
      color: #94a3b8;
    }}
    .npp-meta-item {{
      display: flex;
      align-items: center;
      gap: 3px;
    }}
    .badge-remote-danger {{
      background: rgba(220, 38, 38, 0.15);
      color: #ef4444;
      border: 1px solid rgba(220, 38, 38, 0.3);
      padding: 0 4px;
      border-radius: 3px;
      font-weight: 700;
    }}

    /* Map Controls Floating */
    .map-quick-controls {{
      position: absolute;
      top: 10px;
      left: 60px;
      z-index: 900;
      display: flex;
      gap: 5px;
      background: rgba(15, 23, 42, 0.88);
      padding: 4px 6px;
      border-radius: 8px;
      border: 1px solid #334155;
      backdrop-filter: blur(4px);
      flex-wrap: wrap;
      max-width: calc(100vw - 120px);
    }}
    .quick-btn {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #cbd5e1;
      padding: 4px 8px;
      border-radius: 5px;
      font-size: 0.7rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }}
    .quick-btn:hover {{
      background: #334155;
      color: #ffffff;
    }}
    .quick-btn.active {{
      background: rgba(37, 99, 235, 0.25);
      border-color: #2563eb;
      color: #60a5fa;
    }}
    .quick-btn.active-inactive-btn {{
      background: rgba(220, 38, 38, 0.25) !important;
      border-color: #ef4444 !important;
      color: #fca5a5 !important;
    }}
    .quick-btn.active-quick-outlet {{
      background: rgba(245, 158, 11, 0.25) !important;
      border-color: #f59e0b !important;
      color: #fef08a !important;
    }}

    /* Map Legend */
    .map-legend {{
      position: absolute;
      bottom: 18px;
      left: 12px;
      z-index: 900;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid #334155;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.68rem;
      color: #cbd5e1;
      display: flex;
      flex-direction: column;
      gap: 4px;
      pointer-events: auto;
      backdrop-filter: blur(4px);
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .legend-dot {{
      width: 9px;
      height: 9px;
      border-radius: 50%;
      flex-shrink: 0;
    }}

        /* Tooltip khi re chuot vao NPP */
    .leaflet-tooltip.npp-hover-tooltip {{
      background: rgba(15, 23, 42, 0.95) !important;
      border: 1px solid rgba(16, 185, 129, 0.6) !important;
      color: #f8fafc !important;
      font-family: inherit !important;
      font-size: 0.78rem !important;
      font-weight: 700 !important;
      padding: 5px 9px !important;
      border-radius: 6px !important;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5) !important;
      letter-spacing: 0.2px;
      white-space: nowrap;
    }}
    .leaflet-tooltip.npp-hover-tooltip::before {{
      border-top-color: rgba(15, 23, 42, 0.95) !important;
    }}
    .leaflet-tooltip.npp-hover-tooltip.tooltip-ksm {{
      border-color: rgba(239, 68, 68, 0.6) !important;
      color: #fca5a5 !important;
    }}
    .leaflet-tooltip.npp-hover-tooltip.tooltip-ksm::before {{
      border-top-color: rgba(15, 23, 42, 0.95) !important;
    }}

    
    /* ==========================================
       SPATIAL SELECTION & REVENUE ANALYTICS CSS
       ========================================== */
    .crosshair-cursor {{
      cursor: crosshair !important;
    }}

    /* Floating Toolbar on Top of Map */
    #spatialToolbar {{
      position: absolute;
      top: 15px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(16, 185, 129, 0.5);
      backdrop-filter: blur(10px);
      padding: 6px 14px;
      border-radius: 30px;
      display: none;
      align-items: center;
      gap: 8px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
      animation: fadeInDown 0.25s ease-out;
    }}
    .spatial-tool-btn {{
      background: #1e293b;
      color: #e2e8f0;
      border: 1px solid #334155;
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .spatial-tool-btn:hover {{
      background: #334155;
      color: #38bdf8;
      border-color: #38bdf8;
    }}
    .spatial-tool-btn.active {{
      background: #059669;
      color: #ffffff;
      border-color: #10b981;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }}
    .spatial-tool-btn.btn-danger-tool {{
      border-color: #ef4444;
      color: #fca5a5;
    }}
    .spatial-tool-btn.btn-danger-tool:hover {{
      background: #dc2626;
      color: #ffffff;
    }}

    /* Floating Revenue Analytics Panel */
    #spatialRevenuePanel {{
      position: absolute;
      bottom: 25px;
      left: 20px;
      width: 480px;
      max-width: calc(100vw - 40px);
      max-height: 80vh;
      background: rgba(15, 23, 42, 0.96);
      border: 1px solid rgba(16, 185, 129, 0.6);
      backdrop-filter: blur(16px);
      border-radius: 12px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7);
      z-index: 1001;
      display: none;
      flex-direction: column;
      overflow: hidden;
      animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .revenue-panel-header {{
      padding: 12px 16px;
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 95, 70, 0.2));
      border-bottom: 1px solid rgba(16, 185, 129, 0.3);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .revenue-panel-title {{
      font-size: 0.88rem;
      font-weight: 800;
      color: #34d399;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .revenue-panel-body {{
      padding: 14px 16px;
      overflow-y: auto;
      max-height: calc(80vh - 60px);
    }}
    .revenue-kpi-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-bottom: 12px;
    }}
    .revenue-kpi-card {{
      background: #1e293b;
      border-radius: 8px;
      padding: 8px 10px;
      text-align: center;
      border-left: 3px solid #10b981;
    }}
    .revenue-kpi-val {{
      font-size: 0.95rem;
      font-weight: 800;
      color: #f8fafc;
      margin-top: 2px;
    }}
    .revenue-kpi-lbl {{
      font-size: 0.68rem;
      color: #94a3b8;
      font-weight: 600;
      text-transform: uppercase;
    }}
    .revenue-progress-container {{
      background: #1e293b;
      border-radius: 8px;
      padding: 10px;
      margin-bottom: 12px;
    }}
    .revenue-stacked-bar {{
      display: flex;
      height: 12px;
      border-radius: 6px;
      overflow: hidden;
      margin: 6px 0;
      background: #334155;
    }}
    .bar-ambient {{ background: #f59e0b; }}
    .bar-chilled {{ background: #10b981; }}
    .bar-frozen  {{ background: #38bdf8; }}
    .revenue-breakdown-legend {{
      display: flex;
      justify-content: space-between;
      font-size: 0.72rem;
      margin-top: 4px;
    }}
    .revenue-table-wrapper {{
      max-height: 220px;
      overflow-y: auto;
      border: 1px solid #334155;
      border-radius: 6px;
      background: #0f172a;
      margin-bottom: 12px;
    }}
    .revenue-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.72rem;
      text-align: left;
    }}
    .revenue-table th {{
      position: sticky;
      top: 0;
      background: #1e293b;
      color: #94a3b8;
      padding: 6px 8px;
      border-bottom: 1px solid #334155;
      font-weight: 700;
      z-index: 1;
    }}
    .revenue-table td {{
      padding: 5px 8px;
      border-bottom: 1px solid #1e293b;
      color: #e2e8f0;
    }}
    .revenue-table tr:hover {{
      background: rgba(16, 185, 129, 0.1);
    }}

    /* Marker Custom */
    .custom-npp-icon {{
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      border: 2px solid white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.4);
      transition: transform 0.2s;
    }}
    .custom-npp-icon:hover {{
      transform: scale(1.25);
      z-index: 1000 !important;
    }}
    .npp-icon-active {{
      background: #059669;
    }}
    .npp-icon-inactive {{
      background: #dc2626;
      border-color: #fca5a5;
    }}
    .npp-icon-inner {{
      color: white;
      font-size: 10px;
    }}

    /* Popup Styling */
    .leaflet-popup-content-wrapper {{
      background: #0f172a;
      color: #f8fafc;
      border: 1px solid #334155;
      border-radius: 10px;
      padding: 0;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }}
    .leaflet-popup-content {{
      margin: 0;
      line-height: 1.4;
      font-family: inherit;
      width: 290px !important;
    }}
    .leaflet-popup-tip {{
      background: #0f172a;
    }}
    .popup-card {{
      padding: 10px 12px;
    }}
    .popup-header {{
      border-bottom: 1px solid #334155;
      padding-bottom: 6px;
      margin-bottom: 6px;
    }}
    .popup-tag {{
      display: inline-block;
      font-size: 0.62rem;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 3px;
      margin-bottom: 3px;
      text-transform: uppercase;
    }}
    .popup-title {{
      font-size: 0.8rem;
      font-weight: 800;
      color: #f1f5f9;
    }}
    .popup-body {{
      font-size: 0.72rem;
      color: #94a3b8;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .popup-row {{
      display: flex;
      gap: 6px;
      align-items: flex-start;
    }}
    .popup-row i {{
      margin-top: 2px;
      width: 14px;
      flex-shrink: 0;
    }}
    .popup-row span {{
      color: #cbd5e1;
    }}
    .popup-actions {{
      margin-top: 8px;
      padding-top: 6px;
      border-top: 1px solid #334155;
      display: flex;
      gap: 5px;
      flex-wrap: wrap;
    }}
    .btn-action {{
      flex: 1;
      padding: 5px;
      border-radius: 5px;
      font-size: 0.68rem;
      font-weight: 700;
      text-align: center;
      cursor: pointer;
      border: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
      transition: all 0.2s;
    }}
    .btn-action.btn-primary {{ background: #2563eb; color: white; }}
    .btn-action.btn-spider {{ background: #8b5cf6; color: white; }}
    .btn-action.btn-outlet {{ background: #f59e0b; color: #0f172a; font-weight: 800; }}
    .btn-action:hover {{ filter: brightness(1.15); }}

    /* Mobile toggle drawer button */
    .btn-mobile-drawer {{
      display: none;
      position: absolute;
      bottom: 20px;
      right: 15px;
      z-index: 950;
      background: #2563eb;
      color: white;
      border: none;
      padding: 8px 14px;
      border-radius: 25px;
      font-size: 0.75rem;
      font-weight: 700;
      box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
      cursor: pointer;
      align-items: center;
      gap: 6px;
    }}
    .btn-close-sidebar {{
      display: none;
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 1rem;
      cursor: pointer;
    }}

    /* Loading Pill */
    #loadingIndicator {{
      position: absolute;
      top: 55px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.92);
      border: 1px solid #38bdf8;
      color: #bae6fd;
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 0.74rem;
      font-weight: 700;
      z-index: 1100;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.4);
      transition: opacity 0.5s ease;
    }}

    /* Floating Outlet Banner */
    #nppOutletBanner {{
      display: none;
      position: absolute;
      top: 55px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.96);
      border: 1px solid #f59e0b;
      color: #fde68a;
      padding: 6px 14px;
      border-radius: 25px;
      font-size: 0.74rem;
      font-weight: 700;
      z-index: 1100;
      align-items: center;
      gap: 9px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.5);
      animation: bannerSlideDown 0.25s ease;
    }}
    @keyframes bannerSlideDown {{
      from {{ transform: translate(-50%, -15px); opacity: 0; }}
      to {{ transform: translate(-50%, 0); opacity: 1; }}
    }}

    /* ==========================================================================
       MODAL TABS & STRATEGIC ASSESSMENT STYLES
       ========================================================================== */
    .modal-tab-bar {{
      display: flex;
      background: #0f172a;
      border-bottom: 1px solid #334155;
      padding: 0 16px;
      gap: 8px;
      flex-shrink: 0;
      overflow-x: auto;
    }}
    .modal-tab-btn {{
      background: transparent;
      border: none;
      border-bottom: 3px solid transparent;
      color: #94a3b8;
      padding: 10px 14px;
      font-size: 0.78rem;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      transition: all 0.2s;
    }}
    .modal-tab-btn:hover {{
      color: #f1f5f9;
      background: rgba(255, 255, 255, 0.03);
    }}
    .modal-tab-btn.active {{
      color: #38bdf8;
      border-bottom-color: #38bdf8;
      background: rgba(56, 189, 248, 0.08);
    }}

    /* Tab Contents */
    .tab-content {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
    }}

    /* Strategic Tab Cards & Tables */
    .strategic-summary-banner {{
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
      border: 1px solid rgba(59, 130, 246, 0.4);
      border-radius: 10px;
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .strategic-matrix-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.72rem;
      color: #cbd5e1;
    }}
    .strategic-matrix-table th {{
      background: #0f172a;
      color: #94a3b8;
      padding: 9px 10px;
      text-align: left;
      font-weight: 800;
      border-bottom: 2px solid #334155;
      white-space: nowrap;
      position: sticky;
      top: 0;
      z-index: 5;
    }}
    .strategic-matrix-table td {{
      padding: 8px 10px;
      border-bottom: 1px solid #334155;
      vertical-align: middle;
    }}
    .strategic-matrix-table tr:hover {{
      background: rgba(37, 99, 235, 0.12);
    }}

    .regional-card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 12px;
      margin-top: 4px;
    }}
    .regional-card {{
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 10px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.2s;
    }}
    .regional-card:hover {{
      border-color: #38bdf8;
      box-shadow: 0 4px 18px rgba(0,0,0,0.4);
    }}
    .regional-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      padding-bottom: 6px;
    }}
    .regional-card-title {{
      font-size: 0.86rem;
      font-weight: 800;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .risk-badge {{
      font-size: 0.64rem;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      white-space: nowrap;
    }}
    .risk-badge-danger {{
      background: rgba(220, 38, 38, 0.2);
      border: 1px solid rgba(239, 68, 68, 0.5);
      color: #f87171;
    }}
    .risk-badge-warning {{
      background: rgba(217, 119, 6, 0.2);
      border: 1px solid rgba(245, 158, 11, 0.5);
      color: #fbbf24;
    }}
    .risk-badge-success {{
      background: rgba(5, 150, 105, 0.2);
      border: 1px solid rgba(16, 185, 129, 0.5);
      color: #34d399;
    }}

    .regional-stats-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 4px;
      background: #0f172a;
      padding: 6px 8px;
      border-radius: 6px;
      font-size: 0.68rem;
      text-align: center;
    }}
    .stat-box-title {{ color: #94a3b8; font-size: 0.62rem; font-weight: 700; }}
    .stat-box-num {{ font-weight: 800; color: #f1f5f9; font-size: 0.78rem; margin-top: 2px; }}

    .regional-bottleneck {{
      font-size: 0.7rem;
      color: #cbd5e1;
      line-height: 1.35;
    }}
    .regional-bottleneck strong {{
      color: #fca5a5;
    }}

    .regional-advice-box {{
      background: rgba(37, 99, 235, 0.12);
      border-left: 3px solid #38bdf8;
      padding: 7px 10px;
      border-radius: 0 6px 6px 0;
      font-size: 0.7rem;
      line-height: 1.45;
      color: #e2e8f0;
    }}
    .regional-advice-box strong {{
      color: #93c5fd;
    }}

    .regional-card-footer {{
      display: flex;
      gap: 6px;
      margin-top: auto;
      padding-top: 6px;
      border-top: 1px solid #334155;
    }}

    .roadmap-container {{
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 10px;
      padding: 12px 16px;
      margin-top: 4px;
    }}
    .roadmap-phase {{
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 8px 0;
      border-bottom: 1px dashed #334155;
    }}
    .roadmap-phase:last-child {{
      border-bottom: none;
      padding-bottom: 0;
    }}
    .roadmap-tag {{
      background: #2563eb;
      color: white;
      font-size: 0.68rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      white-space: nowrap;
      min-width: 145px;
      text-align: center;
    }}
    .roadmap-desc {{
      font-size: 0.72rem;
      color: #cbd5e1;
      line-height: 1.4;
    }}

    /* ==========================================================================
       ANALYTICS MODAL (TAG TỔNG THỂ PHÂN TÍCH CỰ LY & ĐỀ XUẤT TRẠM TRUNG CHUYỂN)
       ========================================================================== */
    .analytics-modal-backdrop {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(8px);
      z-index: 2000;
      align-items: center;
      justify-content: center;
      padding: 12px;
    }}
    .analytics-modal-backdrop.open {{
      display: flex;
    }}
    .analytics-modal-card {{
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 14px;
      width: 100%;
      max-width: 1220px;
      max-height: 94vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      overflow: hidden;
      animation: modalSlideIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    @keyframes modalSlideIn {{
      from {{ transform: translateY(20px) scale(0.97); opacity: 0; }}
      to {{ transform: translateY(0) scale(1); opacity: 1; }}
    }}
    .modal-head {{
      background: #1e293b;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #334155;
      flex-shrink: 0;
    }}
    .modal-head-title {{
      display: flex;
      align-items: center;
      gap: 8px;
      color: #f1f5f9;
      font-size: 0.92rem;
      font-weight: 800;
    }}
    .btn-close-modal {{
      background: #334155;
      color: #94a3b8;
      border: none;
      width: 30px;
      height: 30px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.2s;
    }}
    .btn-close-modal:hover {{
      background: #dc2626;
      color: white;
    }}
    .modal-body {{
      padding: 14px 16px;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #0f172a;
    }}
    .modal-kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
      flex-shrink: 0;
    }}
    .modal-kpi-card {{
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .modal-kpi-title {{
      font-size: 0.72rem;
      font-weight: 700;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .modal-kpi-num {{
      font-size: 1.32rem;
      font-weight: 900;
      color: #f1f5f9;
    }}
    .modal-kpi-desc {{
      font-size: 0.68rem;
      color: #64748b;
    }}
    .modal-filter-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      background: #1e293b;
      padding: 8px 12px;
      border-radius: 8px;
      border: 1px solid #334155;
    }}
    .analytics-table-wrap {{
      border: 1px solid #334155;
      border-radius: 8px;
      overflow-x: auto;
      background: #1e293b;
      flex: 1;
      max-height: 480px;
    }}
    .analytics-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.72rem;
      color: #cbd5e1;
    }}
    .analytics-table th {{
      background: #0f172a;
      color: #94a3b8;
      padding: 9px 10px;
      text-align: left;
      font-weight: 800;
      border-bottom: 2px solid #334155;
      white-space: nowrap;
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    .analytics-table td {{
      padding: 8px 10px;
      border-bottom: 1px solid #334155;
      vertical-align: middle;
    }}
    .analytics-table tr:hover {{
      background: rgba(37, 99, 235, 0.12);
    }}
    .tag-hub-cold {{
      background: rgba(14, 165, 233, 0.2);
      color: #38bdf8;
      border: 1px solid rgba(14, 165, 233, 0.5);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
      font-size: 0.65rem;
      white-space: nowrap;
    }}
    .tag-hub-dry {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.5);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
      font-size: 0.65rem;
      white-space: nowrap;
    }}
    .tag-hub-ok {{
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.4);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
      font-size: 0.65rem;
      white-space: nowrap;
    }}

    /* RESPONSIVE DESIGN CHO ĐIỆN THOẠI (Mobile <= 768px) */
    @media (max-width: 768px) {{
      header {{ padding: 0.4rem 0.6rem; }}
      h1 {{ font-size: 0.86rem; }}
      .header-badge.outlets-badge, .header-badge.cold-badge {{ display: none; }}
      .btn-nav {{ padding: 4px 7px; font-size: 0.68rem; }}
      
      .filter-bar {{
        padding: 0.35rem 0.5rem;
        gap: 0.35rem;
      }}
      .filter-row {{
        gap: 0.35rem;
      }}
      .main-container {{
        flex: 1;
        min-height: 0;
        height: auto;
      }}

      /* Drawer trượt từ dưới lên */
      .sidebar {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 60vh;
        border-radius: 16px 16px 0 0;
        border-left: none;
        border-top: 2px solid #2563eb;
        transform: translateY(105%);
        z-index: 1005;
        box-shadow: 0 -8px 25px rgba(0,0,0,0.35);
      }}
      .sidebar.open {{
        transform: translateY(0);
      }}
      .btn-close-sidebar {{
        display: block;
      }}
      .btn-mobile-drawer {{
        display: inline-flex;
      }}
      .map-quick-controls {{
        top: 8px;
        left: 50px;
        gap: 3px;
        padding: 3px;
      }}
      .quick-btn {{
        font-size: 0.65rem;
        padding: 3px 6px;
      }}
      .map-legend {{
        display: none;
      }}
      .analytics-modal-card {{
        max-height: 96vh;
      }}
    }}
  
    /* ===== PLANNED NPP FLAGS FEATURE STYLING ===== */
    @keyframes radar-pulse-flag {{
      0% {{ transform: scale(0.6); opacity: 0.9; }}
      100% {{ transform: scale(2.6); opacity: 0; }}
    }}
    @keyframes flag-bounce {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-7px); }}
    }}

    .planned-flag-container {{
      position: relative;
      width: 46px;
      height: 52px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-end;
      pointer-events: auto;
      cursor: pointer;
    }}
    .planned-flag-pulse {{
      position: absolute;
      bottom: 2px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(245, 158, 11, 0.45);
      border: 2px solid #f59e0b;
      animation: radar-pulse-flag 2.2s infinite ease-out;
      pointer-events: none;
    }}
    .planned-flag-icon {{
      position: relative;
      z-index: 2;
      font-size: 28px;
      color: #ef4444;
      filter: drop-shadow(0 2px 5px rgba(0,0,0,0.85)) drop-shadow(0 0 12px rgba(245, 158, 11, 0.9));
      animation: flag-bounce 2s infinite ease-in-out;
    }}
    .planned-flag-label {{
      position: absolute;
      top: -24px;
      white-space: nowrap;
      background: #0f172a;
      border: 1.5px solid #f59e0b;
      color: #fef08a;
      font-size: 11px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.7);
      pointer-events: none;
      z-index: 3;
    }}

    /* Pin Mode Banner */
    .pin-mode-banner {{
      position: absolute;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      background: rgba(15, 23, 42, 0.95);
      border: 2px solid #f59e0b;
      border-radius: 30px;
      padding: 6px 18px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.6), 0 0 15px rgba(245, 158, 11, 0.35);
      display: flex;
      align-items: center;
      gap: 16px;
      backdrop-filter: blur(6px);
      animation: fadeIn 0.3s ease-out;
    }}
    .banner-quick-btn {{
      border: none;
      border-radius: 20px;
      padding: 4px 12px;
      font-size: 0.7rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }}
    .banner-quick-btn:hover {{
      filter: brightness(1.15);
      transform: translateY(-1px);
    }}

    /* Planned Flags Management Widget */
    .planned-flags-widget {{
      position: absolute;
      bottom: 24px;
      right: 16px;
      z-index: 950;
      width: 320px;
      background: rgba(15, 23, 42, 0.95);
      border: 1.5px solid #f59e0b;
      border-radius: 10px;
      box-shadow: 0 12px 35px rgba(0,0,0,0.7);
      backdrop-filter: blur(8px);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: all 0.25s ease;
    }}
    .planned-widget-header {{
      background: #1e293b;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      cursor: pointer;
      user-select: none;
    }}
    .widget-badge-pulse {{
      background: #059669;
      color: #fff;
      font-size: 0.58rem;
      font-weight: 800;
      padding: 1px 5px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .planned-widget-body {{
      padding: 10px;
      max-height: 280px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .planned-flags-list {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .flag-list-item {{
      background: #1e293b;
      border: 1px solid #334155;
      border-left: 3px solid #f59e0b;
      border-radius: 6px;
      padding: 6px 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s;
    }}
    .flag-list-item:hover {{
      background: #273549;
      border-color: #64748b;
    }}
    .flag-item-info {{
      display: flex;
      flex-direction: column;
      cursor: pointer;
      flex: 1;
    }}
    .flag-item-title {{
      font-size: 0.75rem;
      font-weight: 800;
      color: #fef08a;
    }}
    .flag-item-sub {{
      font-size: 0.65rem;
      color: #94a3b8;
    }}
    .flag-item-actions {{
      display: flex;
      gap: 4px;
    }}
    .flag-btn-icon {{
      background: transparent;
      border: none;
      color: #94a3b8;
      cursor: pointer;
      padding: 4px;
      border-radius: 4px;
      font-size: 0.72rem;
      transition: all 0.15s;
    }}
    .flag-btn-icon:hover {{
      color: #f87171;
      background: rgba(239, 68, 68, 0.2);
    }}
    .planned-widget-footer {{
      display: flex;
      gap: 6px;
      padding-top: 6px;
      border-top: 1px solid #334155;
    }}
    .widget-action-btn {{
      flex: 1;
      border: none;
      border-radius: 5px;
      padding: 5px 8px;
      font-size: 0.68rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.2s;
    }}
    .widget-action-btn.btn-preset {{
      background: #0284c7;
      color: #fff;
    }}
    .widget-action-btn.btn-add {{
      background: #059669;
      color: #fff;
    }}
    .widget-action-btn.btn-clear {{
      background: #334155;
      color: #fca5a5;
    }}
    .widget-action-btn:hover {{
      filter: brightness(1.15);
    }}

    /* Crosshair cursor when in pin mode */
    .pin-mode-active #map {{
      cursor: crosshair !important;
    }}


    /* ===== PHÂN BIỆT 2 LOẠI NPP (CÓ SM VS KHÔNG SM) ===== */
    /* 1. NPP CÓ SM (Xanh Ngọc / Emerald Green) */
    .npp-icon-co-sm {{
      background: #059669 !important;
      border: 2px solid #34d399 !important;
      color: #ffffff !important;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.5) !important;
    }}
    .npp-icon-co-sm:hover {{
      transform: scale(1.25);
      z-index: 1000 !important;
    }}

    /* 2. NPP KHÔNG CÓ SM (Cam Đỏ / Amber-Red Warning) */
    .npp-icon-khong-sm {{
      background: #dc2626 !important;
      border: 2px solid #fca5a5 !important;
      color: #fef08a !important;
      box-shadow: 0 0 14px rgba(239, 68, 68, 0.75) !important;
      animation: pulse-sm-warning 2.2s infinite ease-in-out;
    }}
    .npp-icon-khong-sm:hover {{
      transform: scale(1.25);
      z-index: 1000 !important;
    }}

    @keyframes pulse-sm-warning {{
      0%, 100% {{ box-shadow: 0 0 8px rgba(239, 68, 68, 0.6); }}
      50% {{ box-shadow: 0 0 18px rgba(239, 68, 68, 0.95); }}
    }}

    /* Quick button active state for Không SM */
    .quick-btn.active-khong-sm {{
      background: rgba(239, 68, 68, 0.35) !important;
      border-color: #ef4444 !important;
      color: #fca5a5 !important;
      box-shadow: 0 0 10px rgba(239, 68, 68, 0.5) !important;
    }}

</style>
</head>
<body>

  <!-- Loading indicator -->
  <div id="loadingIndicator">
    <i class="fa-solid fa-spinner fa-spin"></i>
    <span id="loadingText">Đang tải bản đồ & 391 NPP...</span>
  </div>

  <!-- Header -->
  <header>
    <div class="header-left">
      <div class="header-badge"><i class="fa-solid fa-warehouse"></i> 391 NPP</div>
      <div class="header-badge outlets-badge"><i class="fa-solid fa-store"></i> 59.4k Điểm Bán</div>
      <h1><i class="fa-solid fa-route" style="color:#10b981;"></i> RTM Spatial Model</h1>
    </div>
    <div class="header-right">
      <!-- NÚT BẬT BÁO CÁO ĐÁNH GIÁ 6 VÙNG & CHI TIẾT CỰ LY HUB -->
      <button class="btn-nav" style="background:#0284c7; border-color:#38bdf8;" onclick="openStrategicModal()"><i class="fa-solid fa-compass-drafting"></i> Đánh Giá 6 Vùng</button>
      <a href="rtm_analytics_dashboard.html" class="btn-nav" style="background: linear-gradient(135deg, #f59e0b, #d97706); border-color: #fbbf24; text-decoration: none; color: white;" title="Xem báo cáo biểu đồ trực quan & bản đồ vùng trắng C1"><i class="fa-solid fa-chart-pie"></i> Báo Cáo Biểu Đồ & Vùng Trắng C1</a>
      <button class="btn-nav" style="background:#7c3aed; border-color:#8b5cf6;" onclick="openAnalyticsModal()"><i class="fa-solid fa-chart-pie"></i> Cự Ly & Hub</button>
      <button class="btn-nav" onclick="exportFilteredCSV()"><i class="fa-solid fa-file-excel"></i> Xuất Excel</button>
      <a href="rtm_dashboard_mien_tay.html" class="btn-nav"><i class="fa-solid fa-chart-line"></i> Dashboard</a>
    </div>
  </header>

  <!-- UNIFIED FLOATING ISLAND TOOLBAR (Giao diện 1 hàng 4 cụm tinh gọn) -->
  <div class="filter-bar">
    <!-- CỤM 1: ĐỊA BÀN & TÌM KIẾM (GEO & SEARCH) -->
    <div class="toolbar-cluster geo-cluster">
      <div class="toolbar-item" title="Lọc Miền">
        <select id="filterMien" class="island-select" onchange="onMienChange()">
          <option value="ALL">🌐 Toàn Quốc</option>
          <option value="MIỀN NAM">Miền Nam (199)</option>
          <option value="MIỀN BẮC">Miền Bắc (192)</option>
        </select>
      </div>

      <div class="toolbar-item" title="Lọc Vùng">
        <select id="filterVung" class="island-select" onchange="onVungChange()">
          <option value="ALL">Tất cả Vùng</option>
        </select>
      </div>

      <div class="toolbar-item" title="Lọc Tỉnh/Thành">
        <select id="filterTinh" class="island-select" onchange="applyFilters()">
          <option value="ALL">Tất cả Tỉnh/Thành</option>
        </select>
      </div>

      <div class="toolbar-item search-item">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input type="text" id="filterSearch" class="island-search" placeholder="Tìm NPP, điểm bán..." oninput="applyFilters()">
      </div>
    </div>

    <!-- CỤM 2: QUẢN TRỊ NPP (NPP LAYER & STATUS SELECTOR) -->
    <div class="toolbar-cluster npp-cluster">
      <button id="btnUnifiedNppToggle" class="island-btn active-npp" onclick="toggleUnifiedNppLayer()" title="Bật/Tắt hiển thị lớp Nhà Phân Phối trên bản đồ">
        <i class="fa-solid fa-warehouse" style="color:#10b981;"></i>
        <span>NPP: <strong id="chkNppCount" style="color:#a7f3d0;">391</strong></span>
      </button>

      <div class="toolbar-item">
        <select id="filterUnifiedNppStatus" class="island-select" onchange="onUnifiedNppStatusChange(this.value)" title="Lọc trạng thái hoạt động & nhân sự giám sát SM">
          <option value="ALL">🏢 Tất cả Trạng Thái (391)</option>
          <option value="ACTIVE_ALL">🟢 Đang Hoạt Động (215)</option>
          <option value="ACTIVE_SM">👤 Có SM / Nhân Viên (119)</option>
          <option value="ACTIVE_KSM">⚠️ Chưa Có SM / NV (96)</option>
          <option value="INACTIVE">🔴 Ngưng Hoạt Động (176)</option>
        </select>
      </div>
    </div>

    <!-- CỤM 3: QUẢN TRỊ ĐIỂM BÁN (OUTLET DROPDOWN MENU) -->
    <div class="toolbar-cluster outlet-cluster">
      <div class="dropdown-wrapper" id="outletDropdownWrapper">
        <button class="island-btn" id="btnOutletMasterTrigger" onclick="toggleOutletMenu(event)" title="Cấu hình lớp điểm bán lẻ & thiết bị">
          <i class="fa-solid fa-store" style="color:#f59e0b;"></i>
          <span id="outletTriggerLabel">Điểm Bán (<span id="chkOutletCount">59.4k</span>)</span>
          <i class="fa-solid fa-chevron-down" style="font-size:0.6rem; color:#94a3b8; margin-left:2px;"></i>
        </button>

        <div class="island-dropdown-menu" id="outletDropdownMenu">
          <div class="dropdown-header">
            <i class="fa-solid fa-sliders"></i> CẤU HÌNH LỚP ĐIỂM BÁN (59.4K)
          </div>

          <!-- Lớp hiển thị chính -->
          <div class="dropdown-menu-item" onclick="toggleOutletMasterFromMenu()">
            <span class="item-icon-box" style="color:#f59e0b;"><i class="fa-solid fa-store"></i></span>
            <div class="item-text">
              <div class="item-title" id="menuOutletStatusTitle">Bật Hiển Thị Điểm Bán</div>
              <div class="item-sub">Tải và hiển thị điểm bán trên bản đồ</div>
            </div>
            <span class="badge-mini" id="badgeOutletMaster">59.4k</span>
          </div>

          <div class="dropdown-divider"></div>

          <!-- Lọc có Doanh Số T9 -->
          <div class="dropdown-menu-item" onclick="toggleOnlySalesQuick()">
            <span class="item-icon-box" style="color:#10b981;"><i class="fa-solid fa-coins"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#6ee7b7;">💰 Chỉ Điểm Có DS T9</div>
              <div class="item-sub">34,171 điểm phát sinh doanh số (38.3 Tỷ)</div>
            </div>
            <span class="badge-mini" id="badgeMenuSales">34.2k</span>
          </div>

          <!-- Lọc có Tủ CJ -->
          <div class="dropdown-menu-item" onclick="toggleOnlyEquipQuick()">
            <span class="item-icon-box" style="color:#38bdf8;"><i class="fa-solid fa-snowflake"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#7dd3fc;">❄️ Chỉ Điểm Có Tủ Đông/Mát</div>
              <div class="item-sub">2,598 điểm được trang bị thiết bị CJ</div>
            </div>
            <span class="badge-mini" id="badgeMenuEquip">2.6k</span>
          </div>

          <!-- Lọc cự ly > 45km -->
          <div class="dropdown-menu-item" onclick="toggleRemoteOnlyMenu()">
            <span class="item-icon-box" style="color:#ef4444;"><i class="fa-solid fa-triangle-exclamation"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#fca5a5;" id="menuRemoteTitle">⚠️ Cự Ly Xa > 45km</div>
              <div class="item-sub">Điểm bán vượt bán kính phục vụ chuẩn</div>
            </div>
            <span class="badge-mini" style="color:#f87171;">2,456</span>
          </div>

          <div class="dropdown-divider"></div>

          <!-- Ngành hàng Đông vs Khô -->
          <div style="padding: 6px 12px; display:flex; gap:8px;">
            <label style="display:flex; align-items:center; gap:5px; font-size:0.7rem; font-weight:700; color:#38bdf8; cursor:pointer;">
              <input type="checkbox" id="chkToggleCold" checked onchange="applyFilters()">
              <span><i class="fa-solid fa-snowflake"></i> Hàng Đông</span>
            </label>
            <label style="display:flex; align-items:center; gap:5px; font-size:0.7rem; font-weight:700; color:#fbbf24; cursor:pointer;">
              <input type="checkbox" id="chkToggleDry" checked onchange="applyFilters()">
              <span><i class="fa-solid fa-box-open"></i> Hàng Khô</span>
            </label>
          </div>

          <!-- Tia nối liên kết -->
          <div class="dropdown-menu-item" onclick="toggleSpiderFromMenu()">
            <span class="item-icon-box" style="color:#a78bfa;"><i class="fa-solid fa-share-nodes"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#c4b5fd;" id="menuSpiderTitle">🕸️ Tia Nối NPP ➔ Điểm Bán</div>
              <div class="item-sub">Đường kết nối liên kết phụ trách logistics</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CỤM 4: CÔNG CỤ PHÂN TÍCH & THAO TÁC (ANALYTICS & ACTIONS) -->
    <div class="toolbar-cluster tools-cluster">
      <!-- NÚT KHOANH VÙNG DOANH SỐ NỔI BẬT NHẤT -->
      <button class="island-btn-hero" id="btnSpatialSelect" onclick="toggleSpatialSelectMode()" title="Nhấn giữ và kéo chuột trên bản đồ để khoanh vùng tính doanh số">
        <i class="fa-solid fa-draw-polygon"></i>
        <span id="btnSpatialSelectText">📐 Khoanh Vùng Doanh Số</span>
      </button>

      <!-- MENU CÔNG CỤ MỞ RỘNG -->
      <div class="dropdown-wrapper" id="toolsDropdownWrapper">
        <button class="island-btn" onclick="toggleToolsMenu(event)" title="Các công cụ phân tích và quy hoạch khác">
          <i class="fa-solid fa-compass-drafting" style="color:#818cf8;"></i>
          <span>Công Cụ ▾</span>
        </button>

        <div class="island-dropdown-menu right-aligned" id="toolsDropdownMenu">
          <div class="dropdown-header">
            <i class="fa-solid fa-wrench"></i> CÔNG CỤ PHÂN TÍCH & QUY HOẠCH
          </div>

          <div class="dropdown-menu-item" onclick="togglePinMode(); closeAllDropdowns();">
            <span class="item-icon-box" style="color:#f59e0b;"><i class="fa-solid fa-flag"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#fef08a;" id="btnPinText">🚩 Cắm Cờ Mở NPP / C1</div>
              <div class="item-sub">Định vị điểm mở mới & mô phỏng bán kính</div>
            </div>
          </div>

          <div class="dropdown-menu-item" onclick="toggleRadius(); closeAllDropdowns();">
            <span class="item-icon-box" style="color:#10b981;"><i class="fa-solid fa-circle-notch"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#6ee7b7;" id="btnToggleRadius">⭕ Bán Kính 45km NPP</div>
              <div class="item-sub">Hiển thị vòng bán kính dịch vụ logistics chuẩn</div>
            </div>
          </div>

          <div class="dropdown-divider"></div>

          <div class="dropdown-menu-item" onclick="openStrategicModal(); closeAllDropdowns();">
            <span class="item-icon-box" style="color:#38bdf8;"><i class="fa-solid fa-mountain-city"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#7dd3fc;">🧭 Đánh Giá Chiến Lược 6 Vùng</div>
              <div class="item-sub">Báo cáo hiện trạng mạng lưới & đề xuất C1</div>
            </div>
          </div>

          <div class="dropdown-menu-item" onclick="openAnalyticsModal(); closeAllDropdowns();">
            <span class="item-icon-box" style="color:#a78bfa;"><i class="fa-solid fa-chart-pie"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#c4b5fd;">📊 Báo Cáo Cự Ly & Đề Xuất Hub</div>
              <div class="item-sub">Chi tiết cự ly max, cự ly TB và điểm nóng >45km</div>
            </div>
          </div>

          <div class="dropdown-divider"></div>

          <div class="dropdown-menu-item" onclick="exportFilteredCSV(); closeAllDropdowns();">
            <span class="item-icon-box" style="color:#10b981;"><i class="fa-solid fa-file-excel"></i></span>
            <div class="item-text">
              <div class="item-title" style="color:#a7f3d0;">📥 Xuất Dữ Liệu Excel</div>
              <div class="item-sub">Tải danh sách NPP đang lọc về máy</div>
            </div>
          </div>

          <div class="dropdown-divider"></div>

          <div style="padding: 6px 12px; display:flex; gap:6px; align-items:center;">
            <span style="font-size:0.68rem; color:#94a3b8; font-weight:700;">Zoom:</span>
            <button class="zoom-mini-btn" onclick="zoomToPreset('ALL'); closeAllDropdowns();">Toàn Quốc</button>
            <button class="zoom-mini-btn" onclick="zoomToPreset('MB'); closeAllDropdowns();">Bắc</button>
            <button class="zoom-mini-btn" onclick="zoomToPreset('MN'); closeAllDropdowns();">Nam</button>
          </div>
        </div>
      </div>

      <!-- LIVE KPI PILL -->
      <div class="island-kpi-pill" title="Thống kê trực tiếp theo điều kiện lọc">
        <span class="kpi-tag"><i class="fa-solid fa-eye"></i></span>
        <span id="kpiCount" class="kpi-val">391</span> NPP
        <span class="kpi-divider">•</span>
        <span id="kpiOutlets" class="kpi-outlets">59.4k</span> Điểm
      </div>
    </div>
  </div>

  <!-- CONTAINER TƯƠNG THÍCH NGẦM (GIỮ CÁC ID CŨ KHÔNG BAO GIỜ BỊ LỖI NULL) -->
  <div style="display:none;" id="rtmBackwardCompatibilityContainer">
    <input type="checkbox" id="chkToggleNPP" checked onchange="toggleNPPVisibility()">
    <input type="checkbox" id="chkToggleOutlet" onchange="toggleOutletVisibility()">
    <input type="checkbox" id="chkHideInactive" onchange="toggleHideInactive()">
    <input type="checkbox" id="chkHideKhongSM" onchange="syncHideKhongSMFromCheckbox(this.checked)">
    <input type="checkbox" id="chkToggleRemoteOnly" onchange="applyFilters()">
    <input type="checkbox" id="chkToggleSpider" onchange="toggleSpiderVisibility()">
    <select id="filterStatus" onchange="onStatusSelectChange()">
      <option value="ALL">ALL</option>
      <option value="ACTIVE">ACTIVE</option>
      <option value="INACTIVE">INACTIVE</option>
    </select>
    <select id="filterSM" onchange="applyFilters()">
      <option value="ALL">ALL</option>
      <option value="CO_SM">CO_SM</option>
      <option value="KHONG_SM">KHONG_SM</option>
    </select>
    <span id="lblChkNpp"></span>
    <span id="lblChkHideInactive"></span>
    <span id="lblChkOutlet"></span>
    <span id="lblChkSpider"></span>
    <span id="lblChkCold"></span>
    <span id="lblChkDry"></span>
    <span id="lblChkRemoteOnly"></span>
    <span id="countInactiveNpp">176</span>
    <span id="kpiActive">215 Chạy</span>
    <span id="kpiInactive">176 Ngưng</span>
    <span id="kpiRemote">2,456</span>
    <button id="btnQuickHideKhongSM"></button>
    <span id="btnQuickHideKhongSMText"></span>
    <button id="btnQuickToggleOutlet"></button>
    <span id="btnQuickOutletText"></span>
    <button id="btnQuickOnlyEquip"></button>
    <span id="btnQuickOnlyEquipText"></span>
    <button id="btnQuickOnlySales"></button>
    <span id="btnQuickOnlySalesText"></span>
    <button id="btnQuickHideInactive"></button>
    <button id="btnTogglePinMode"></button>
  </div>

  <!-- Main Container -->
  <div class="main-container">
    <div id="map"></div>

    <!-- THANH CÔNG CỤ KHOANH VÙNG BẢN ĐỒ -->
    <div id="spatialToolbar">
      <span style="font-size:0.75rem; font-weight:800; color:#34d399; margin-right:4px;">
        <i class="fa-solid fa-draw-polygon"></i> Khoanh Vùng:
      </span>
      <button class="spatial-tool-btn active" id="btnToolBox" onclick="setSpatialTool('box')" title="Nhấn giữ và KÉO chuột để vẽ hộp khoanh vùng">
        <i class="fa-solid fa-vector-square"></i> 🖱️ Kéo Chuột (Hộp)
      </button>
      <button class="spatial-tool-btn" id="btnToolFreehand" onclick="setSpatialTool('freehand')" title="Nhấn giữ và KÉO vẽ tự do bao quanh khu vực">
        <i class="fa-solid fa-pen-nib"></i> ✏️ Vẽ Tự Do
      </button>
      <button class="spatial-tool-btn" id="btnToolCircle" onclick="setSpatialTool('circle')" title="Click 1 điểm tâm và kéo/click điểm bán kính">
        <i class="fa-solid fa-circle-dot"></i> ⭕ Bán Kính
      </button>
      <button class="spatial-tool-btn" id="btnToolPolygon" onclick="setSpatialTool('polygon')" title="Click lần lượt các đỉnh đa giác (click điểm đầu để đóng)">
        <i class="fa-solid fa-draw-polygon"></i> 📐 Đa Giác
      </button>
      <span id="spatialToolInstruction" style="font-size:0.7rem; color:#fef08a; background:rgba(0,0,0,0.35); padding:3px 8px; border-radius:12px; margin:0 4px;">
        🖱️ Nhấn giữ & KÉO chuột trên bản đồ để khoanh vùng
      </span>
      <button class="spatial-tool-btn btn-danger-tool" onclick="clearSpatialSelection()" title="Xóa vùng đã khoanh">
        <i class="fa-solid fa-trash-can"></i> Xóa
      </button>
      <button class="spatial-tool-btn" onclick="toggleSpatialSelectMode(false)" title="Thoát chế độ khoanh vùng">
        <i class="fa-solid fa-xmark"></i> Thoát
      </button>
    </div>

    <!-- BẢNG THỐNG KÊ DOANH SỐ NHÓM NPP KHOANH VÙNG -->
    <div id="spatialRevenuePanel">
      <div class="revenue-panel-header">
        <div class="revenue-panel-title">
          <i class="fa-solid fa-chart-pie"></i> Tổng Hợp Doanh Số Vùng Khoanh (T9/2026)
        </div>
        <div style="display:flex; gap:6px; align-items:center;">
          <button onclick="exportSpatialRevenueCSV()" style="background:#059669; color:#fff; border:none; padding:4px 8px; border-radius:4px; font-size:0.7rem; font-weight:700; cursor:pointer;" title="Tải file CSV">
            <i class="fa-solid fa-file-excel"></i> Xuất CSV
          </button>
          <button onclick="document.getElementById('spatialRevenuePanel').style.display='none'" style="background:transparent; color:#94a3b8; border:none; font-size:1rem; cursor:pointer; padding:2px 6px;">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
      <div class="revenue-panel-body" id="spatialRevenueBody">
        <!-- Rendered dynamically -->
      </div>
    </div>

    <!-- Floating Outlet Banner when viewing single NPP outlets -->
    <div id="nppOutletBanner">
      <i class="fa-solid fa-store" style="color:#f59e0b;"></i>
      <span id="nppOutletBannerText">Đang xem điểm bán của NPP</span>
      <button onclick="resetOutletView()" style="background:#f59e0b; color:#0f172a; border:none; padding:3px 9px; border-radius:12px; font-size:0.7rem; font-weight:800; cursor:pointer;">
        <i class="fa-solid fa-rotate-left"></i> Hiện Tất Cả
      </button>
    </div>

    <!-- Mini Map Presets (Góc trái trên) -->
    <div class="map-preset-pills">
      <button class="preset-pill" onclick="zoomToPreset('ALL')"><i class="fa-solid fa-arrows-to-eye"></i> Toàn Quốc</button>
      <button class="preset-pill" onclick="zoomToPreset('MB')">Bắc</button>
      <button class="preset-pill" onclick="zoomToPreset('MN')">Nam</button>
    </div>

    <!-- BANNER CHẾ ĐỘ CẮM CỜ -->
    <div id="pinModeBanner" class="pin-mode-banner" style="display:none;">
      <div style="display:flex; align-items:center; gap:8px;">
        <i class="fa-solid fa-crosshairs fa-spin" style="color:#f59e0b; font-size:1rem;"></i>
        <div>
          <div style="font-weight:800; font-size:0.75rem; color:#fef08a;">CHẾ ĐỘ CẮM CỜ NPP / C1 DỰ KIẾN</div>
          <div style="font-size:0.68rem; color:#cbd5e1;">Nhấp bất kỳ điểm nào trên bản đồ để cắm cờ hoặc nạp nhanh:</div>
        </div>
      </div>
      <div style="display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
        <button onclick="loadMekongPresets()" class="banner-quick-btn" style="background:#0284c7; color:#fff;">
          <i class="fa-solid fa-wand-magic-sparkles"></i> 4 Vùng Mekong
        </button>
        <button onclick="togglePinMode(false)" class="banner-quick-btn" style="background:#dc2626; color:#fff;">
          <i class="fa-solid fa-check"></i> Hoàn tất
        </button>
      </div>
    </div>

    <!-- WIDGET QUẢN LÝ CỜ NPP DỰ KIẾN (GÓC PHẢI DƯỚI) -->
    <div id="plannedFlagsWidget" class="planned-flags-widget" style="display:none;">
      <div class="planned-widget-header" onclick="toggleFlagsWidgetCollapse()">
        <div style="display:flex; align-items:center; gap:6px;">
          <i class="fa-solid fa-flag" style="color:#f59e0b;"></i>
          <span style="font-weight:800; font-size:0.75rem; color:#f8fafc;">NPP DỰ KIẾN MỞ (<span id="flagWidgetCount">0</span>)</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
          <span class="widget-badge-pulse" id="widgetLiveBadge">DỰ KIẾN</span>
          <i class="fa-solid fa-chevron-down" id="widgetChevron" style="font-size:0.7rem; color:#94a3b8; transition:transform 0.2s;"></i>
        </div>
      </div>
      <div id="plannedWidgetBody" class="planned-widget-body">
        <div id="plannedFlagsList" class="planned-flags-list">
          <!-- Dynamic Flag Items -->
        </div>
        <div class="planned-widget-footer">
          <button class="widget-action-btn btn-preset" onclick="loadMekongPresets()" title="Nạp 4 vùng trắng trọng điểm: Cai Lậy, Đức Hòa, Trà Vinh, Ba Tri">
            <i class="fa-solid fa-wand-magic-sparkles"></i> 4 Vùng Mekong
          </button>
          <button class="widget-action-btn btn-add" onclick="enablePinModeFromWidget()" title="Nhấp bản đồ để cắm thêm cờ">
            <i class="fa-solid fa-plus"></i> Cắm thêm
          </button>
          <button class="widget-action-btn btn-clear" onclick="clearAllPlannedFlags()" title="Xóa toàn bộ cờ dự kiến">
            <i class="fa-solid fa-trash-can"></i> Xóa hết
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL THIẾT LẬP CỜ NPP DỰ KIẾN -->
    <div id="modalAddFlag" class="modal-backdrop" style="display:none; z-index: 9999;">
      <div class="modal-box" style="max-width: 440px; border: 1.5px solid #f59e0b; box-shadow: 0 20px 45px rgba(0,0,0,0.8);">
        <div class="modal-header" style="background: #1e293b; border-bottom: 1px solid #334155; padding: 12px 16px;">
          <h3 style="font-size: 0.9rem; font-weight: 800; color: #fef08a; display: flex; align-items: center; gap: 8px;">
            <i class="fa-solid fa-flag" style="color: #f59e0b;"></i> THIẾT LẬP NPP / C1 DỰ KIẾN MỞ
          </h3>
          <button class="btn-close-modal" onclick="closeAddFlagModal()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div style="padding: 16px; display: flex; flex-direction: column; gap: 12px; background: #0f172a; color: #e2e8f0;">
          <div>
            <label style="font-size: 0.72rem; font-weight: 700; color: #94a3b8; display: block; margin-bottom: 4px;">TÊN NPP / C1 DỰ KIẾN</label>
            <input type="text" id="flagInputName" placeholder="VD: C1 TT. Cai Lậy / NPP Mới Đức Hòa" style="width: 100%; padding: 8px 10px; background: #1e293b; border: 1px solid #475569; border-radius: 6px; color: #fff; font-size: 0.8rem;">
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div>
              <label style="font-size: 0.72rem; font-weight: 700; color: #94a3b8; display: block; margin-bottom: 4px;">MÔ HÌNH VẬN HÀNH</label>
              <select id="flagInputType" style="width: 100%; padding: 8px 10px; background: #1e293b; border: 1px solid #475569; border-radius: 6px; color: #fff; font-size: 0.8rem;">
                <option value="C1 Partner" selected>C1 Partner (Đại lý cấp 1)</option>
                <option value="NPP Mới">NPP Mới (New Distributor)</option>
                <option value="Kho Trung Chuyển">Kho Trung Chuyển (Depot)</option>
              </select>
            </div>
            <div>
              <label style="font-size: 0.72rem; font-weight: 700; color: #94a3b8; display: block; margin-bottom: 4px;">BÁN KÍNH PHỤC VỤ</label>
              <select id="flagInputRadius" style="width: 100%; padding: 8px 10px; background: #1e293b; border: 1px solid #475569; border-radius: 6px; color: #fff; font-size: 0.8rem;">
                <option value="15">15 km (Nội ô / Cự ly ngắn)</option>
                <option value="25" selected>25 km (Cụm huyện)</option>
                <option value="35">35 km (Vùng trắng)</option>
                <option value="45">45 km (Toàn tỉnh)</option>
              </select>
            </div>
          </div>
          <div>
            <label style="font-size: 0.72rem; font-weight: 700; color: #94a3b8; display: block; margin-bottom: 4px;">GHI CHÚ / MỤC TIÊU PHỤC VỤ</label>
            <textarea id="flagInputNote" rows="2" placeholder="VD: Cắt giảm cự ly giao xa, gom 50 Golden Outlets + 233 tiệm Nhóm C..." style="width: 100%; padding: 8px 10px; background: #1e293b; border: 1px solid #475569; border-radius: 6px; color: #fff; font-size: 0.75rem;"></textarea>
          </div>
          <div style="background: rgba(30, 41, 59, 0.7); border: 1px dashed #475569; border-radius: 6px; padding: 8px 10px; font-size: 0.7rem; color: #94a3b8;">
            <i class="fa-solid fa-location-dot" style="color:#f59e0b;"></i> Tọa độ đã chọn: <b id="flagCoordsDisplay" style="color:#f1f5f9;">--</b>
          </div>
          <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 4px;">
            <button onclick="closeAddFlagModal()" style="padding: 7px 14px; background: #334155; border: none; border-radius: 6px; color: #cbd5e1; font-size: 0.75rem; cursor: pointer;">Hủy</button>
            <button onclick="confirmAddFlag()" style="padding: 7px 18px; background: #f59e0b; border: none; border-radius: 6px; color: #0f172a; font-weight: 800; font-size: 0.75rem; cursor: pointer;">
              <i class="fa-solid fa-flag"></i> Xác Nhận Cắm Cờ
            </button>
          </div>
        </div>
      </div>
    </div>

<!-- Mobile Button to Open Drawer -->
    <button class="btn-mobile-drawer" id="btnOpenMobileDrawer" onclick="toggleMobileSidebar(true)">
      <i class="fa-solid fa-list-check"></i> Danh Sách NPP (<span id="mobileCount">391</span>)
    </button>

    <!-- Legend -->
    <div class="map-legend">
      <div style="font-weight:800; font-size: 0.7rem; color: #94a3b8; margin-bottom: 3px;">CHÚ GIẢI PHÂN PHỐI & SM</div>
      <div class="legend-item"><span class="legend-dot" style="background: #059669; border:1.5px solid #34d399;"></span> <i class="fa-solid fa-user-tie" style="color:#34d399; font-size:0.65rem;"></i> NPP Có SM Giám Sát</div>
      <div class="legend-item"><span class="legend-dot" style="background: #dc2626; border:1.5px solid #f87171;"></span> <i class="fa-solid fa-user-slash" style="color:#f87171; font-size:0.65rem;"></i> ⚠️ NPP Không Có SM</div>
      <div class="legend-item"><span class="legend-dot" style="background: #475569;"></span> <i class="fa-solid fa-lock" style="color:#94a3b8; font-size:0.65rem;"></i> NPP Ngưng Hoạt Động</div>
      <div class="legend-item"><span class="legend-dot" style="background: #dc2626;"></span> NPP Ngưng Hoạt Động</div>
      <div class="legend-item"><span class="legend-dot" style="background: #0284c7; width:7px; height:7px;"></span> Điểm Hàng Đông (Cold Chain)</div>
      <div class="legend-item"><span class="legend-dot" style="background: #f59e0b; width:7px; height:7px;"></span> Điểm Hàng Khô (Dry Chain)</div>
      <div class="legend-item"><span class="legend-dot" style="background: #dc2626; width:7px; height:7px;"></span> Cự ly > 45km (Cần mở Hub)</div>
    </div>

    <!-- Sidebar Drawer -->
    <div class="sidebar" id="sidebar">
      <div class="sidebar-header" style="flex-direction:column; align-items:flex-start; gap:4px; padding:10px 12px;">
        <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
          <div class="sidebar-title">
            <i class="fa-solid fa-warehouse" style="color:#2563eb;"></i>
            <span>Danh Sách NPP (<span id="sidebarCount">391</span>)</span>
          </div>
          <button class="btn-close-sidebar" onclick="toggleMobileSidebar(false)"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div id="sidebarSalesSummary" style="font-size:0.72rem; color:#94a3b8; display:flex; justify-content:space-between; width:100%; border-top:1px dashed #334155; padding-top:4px; margin-top:2px;">
          <span>Tổng Doanh Số Vùng:</span>
          <b id="sidebarTotalSales" style="color:#10b981; font-weight:800;">0 đ</b>
        </div>
      </div>

      <div class="sidebar-content" id="sidebarList">
        <!-- Render NPP cards dynamically -->
      </div>
    </div>
  </div>

  <!-- =========================================================================
       ANALYTICS MODAL (TAG TỔNG THỂ PHÂN TÍCH CỰ LY & ĐỀ XUẤT TRẠM TRUNG CHUYỂN)
       ========================================================================= -->
  <div class="analytics-modal-backdrop" id="analyticsModal">
    <div class="analytics-modal-card">
      <div class="modal-head">
        <div class="modal-head-title">
          <i class="fa-solid fa-chart-line" style="color:#a78bfa;"></i>
          <span>Trung Tâm Phân Tích Chuỗi Cung Ứng RTM & Đề Xuất Trạm Trung Chuyển (Hubs)</span>
        </div>
        <button class="btn-close-modal" onclick="closeAnalyticsModal()"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <!-- THANH CHUYỂN TAB TRỰC QUAN -->
      <div class="modal-tab-bar">
        <button class="modal-tab-btn active" id="tabBtnStrategic" onclick="switchModalTab('strategic')">
          <i class="fa-solid fa-compass-drafting" style="color:#38bdf8;"></i> 1. Đánh Giá Hiện Trạng 6 Vùng & Lời Khuyên RTM
        </button>
        <button class="modal-tab-btn" id="tabBtnDetails" onclick="switchModalTab('details')">
          <i class="fa-solid fa-table-list" style="color:#f59e0b;"></i> 2. Bảng Dữ Liệu 388 NPP & Đề Xuất Tuyến
        </button>
      </div>

      <div class="modal-body">
        <!-- ====================================================================
             TAB 1: ĐÁNH GIÁ CHIẾN LƯỢC HIỆN TRẠNG 6 VÙNG & KHUYẾN NGHỊ RTM
             ==================================================================== -->
        <div class="tab-content" id="tabContentStrategic">
          
          <!-- Banner Tổng Quan -->
          <div class="strategic-summary-banner">
            <div>
              <div style="font-size:0.92rem; font-weight:800; color:#f8fafc;">
                <i class="fa-solid fa-chart-pie" style="color:#38bdf8;"></i> Bức Tranh Toàn Cảnh Mạng Lưới Phân Phối 6 Vùng
              </div>
              <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">
                Đo đạc thực tế <b>391 NPP</b> và <b>59.366 Điểm bán lẻ</b> &bull; Cự ly TB: <b>13.9 km</b> &bull; Điểm nóng >45km: <b>2.460 điểm (4.1%)</b>
              </div>
            </div>
            <div style="display:flex; gap:8px;">
              <span class="risk-badge risk-badge-danger"><i class="fa-solid fa-circle-exclamation"></i> 2 Vùng Điểm Nóng: Hải Phòng, Cần Thơ</span>
              <span class="risk-badge risk-badge-success"><i class="fa-solid fa-shield-check"></i> HCM: 0 điểm nóng</span>
            </div>
          </div>

          <!-- Bảng Ma Trận So Sánh 6 Vùng -->
          <div class="strategic-table-wrap">
            <table class="strategic-matrix-table">
              <thead>
                <tr>
                  <th>VÙNG PHÂN PHỐI</th>
                  <th>SỐ NPP (CHẠY/NGƯNG)</th>
                  <th>TỔNG KHÁCH HÀNG</th>
                  <th>TỶ LỆ ĐÔNG LẠNH</th>
                  <th>CỰ LY TB</th>
                  <th>CỰ LY XA NHẤT</th>
                  <th>ĐIỂM NÓNG > 45KM</th>
                  <th>MỨC ĐỘ RỦI RO</th>
                  <th>THAO TÁC</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><b style="color:#38bdf8;">Hải Phòng</b><br><span style="font-size:0.65rem; color:#64748b;">Duyên hải & Bắc Trung Bộ</span></td>
                  <td><b>78</b> (39 Chạy / 39 Ngưng)</td>
                  <td><b>13.028</b> KH</td>
                  <td><b style="color:#38bdf8;">33.4%</b> (4.3k KH)</td>
                  <td><b style="color:#ef4444;">21.3 km</b> <span style="font-size:0.65rem; color:#f87171;">(Cao nhất)</span></td>
                  <td><b style="color:#ef4444;">78.3 km</b></td>
                  <td><b style="color:#ef4444;">1.118 KH (8.6%)</b></td>
                  <td><span class="risk-badge risk-badge-danger">🔴 CỰC KỲ CAO</span></td>
                  <td>
                    <button class="btn-nav" style="padding:3px 7px; font-size:0.65rem; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Hải Phòng')">
                      <i class="fa-solid fa-filter"></i> Xem 78 NPP
                    </button>
                  </td>
                </tr>
                <tr>
                  <td><b style="color:#38bdf8;">Cần Thơ</b><br><span style="font-size:0.65rem; color:#64748b;">13 Tỉnh ĐBSCL (Miền Tây)</span></td>
                  <td><b>62</b> (34 Chạy / 28 Ngưng)</td>
                  <td><b>8.271</b> KH</td>
                  <td><b>16.6%</b> (1.4k KH)</td>
                  <td><b style="color:#ef4444;">19.4 km</b></td>
                  <td><b style="color:#ef4444;">95.2 km</b></td>
                  <td><b style="color:#ef4444;">835 KH (10.1%)</b> <span style="font-size:0.65rem; color:#f87171;">(Tỷ lệ cao nhất)</span></td>
                  <td><span class="risk-badge risk-badge-danger">🔴 CỰC KỲ CAO</span></td>
                  <td>
                    <button class="btn-nav" style="padding:3px 7px; font-size:0.65rem; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Cần Thơ')">
                      <i class="fa-solid fa-filter"></i> Xem 62 NPP
                    </button>
                  </td>
                </tr>
                <tr>
                  <td><b style="color:#38bdf8;">Hà Nội</b><br><span style="font-size:0.65rem; color:#64748b;">ĐB Sông Hồng & Tây Bắc</span></td>
                  <td><b>70</b> (35 Chạy / 35 Ngưng)</td>
                  <td><b>11.021</b> KH</td>
                  <td><b style="color:#38bdf8;">40.0%</b> <span style="font-size:0.65rem; color:#38bdf8;">(Cao nhất nước)</span></td>
                  <td><b style="color:#34d399;">10.8 km</b></td>
                  <td><b style="color:#ef4444;">120.0 km</b></td>
                  <td><b>244 KH (2.2%)</b></td>
                  <td><span class="risk-badge risk-badge-warning">🟡 TRUNG BÌNH</span></td>
                  <td>
                    <button class="btn-nav" style="padding:3px 7px; font-size:0.65rem; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Hà Nội')">
                      <i class="fa-solid fa-filter"></i> Xem 70 NPP
                    </button>
                  </td>
                </tr>
                <tr>
                  <td><b style="color:#38bdf8;">Nha Trang</b><br><span style="font-size:0.65rem; color:#64748b;">Đông Nam Bộ & Tây Nguyên</span></td>
                  <td><b>90</b> (45 Chạy / 45 Ngưng)</td>
                  <td><b>13.718</b> KH</td>
                  <td><b>22.0%</b> (3.0k KH)</td>
                  <td><b style="color:#34d399;">11.3 km</b></td>
                  <td>188.6 km</td>
                  <td><b>160 KH (1.2%)</b></td>
                  <td><span class="risk-badge risk-badge-success">🟢 AN TOÀN - THẤP</span></td>
                  <td>
                    <button class="btn-nav" style="padding:3px 7px; font-size:0.65rem; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Nha Trang')">
                      <i class="fa-solid fa-filter"></i> Xem 90 NPP
                    </button>
                  </td>
                </tr>
                <tr>
                  <td><b style="color:#38bdf8;">Đà Nẵng</b><br><span style="font-size:0.65rem; color:#64748b;">Bắc & Nam Trung Bộ</span></td>
                  <td><b>44</b> (27 Chạy / 17 Ngưng)</td>
                  <td><b>6.224</b> KH</td>
                  <td><b>33.8%</b> (2.1k KH)</td>
                  <td><b style="color:#34d399;">10.7 km</b></td>
                  <td>78.2 km</td>
                  <td><b>103 KH (1.7%)</b></td>
                  <td><span class="risk-badge risk-badge-success">🟢 AN TOÀN - THẤP</span></td>
                  <td>
                    <button class="btn-nav" style="padding:3px 7px; font-size:0.65rem; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Đà Nẵng')">
                      <i class="fa-solid fa-filter"></i> Xem 44 NPP
                    </button>
                  </td>
                </tr>
                <tr>
                  <td><b style="color:#38bdf8;">TP. Hồ Chí Minh</b><br><span style="font-size:0.65rem; color:#64748b;">Đô thị hạt nhân</span></td>
                  <td><b>47</b> (35 Chạy / 12 Ngưng)</td>
                  <td><b>7.104</b> KH</td>
                  <td><b>13.8%</b> (979 KH)</td>
                  <td><b style="color:#34d399;">6.2 km</b> <span style="font-size:0.65rem; color:#34d399;">(Tốt nhất)</span></td>
                  <td>42.9 km</td>
                  <td><b style="color:#34d399;">0 KH (0.0%)</b></td>
                  <td><span class="risk-badge risk-badge-success">🟢 TỐI ƯU CỰ LY</span></td>
                  <td>
                    <button class="btn-nav" style="padding:3px 7px; font-size:0.65rem; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('HCM')">
                      <i class="fa-solid fa-filter"></i> Xem 47 NPP
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Lời khuyên chi tiết cho từng Vùng (Deep-dive Cards) -->
          <div style="font-size:0.86rem; font-weight:800; color:#f8fafc; margin-top:6px;">
            <i class="fa-solid fa-lightbulb" style="color:#fbbf24;"></i> Đánh Giá Hiện Trạng & Khuyến Nghị Chiến Lược RTM Cho Từng Vùng:
          </div>

          <div class="regional-card-grid">
            
            <!-- VÙNG 1: HẢI PHÒNG -->
            <div class="regional-card" style="border-top: 3px solid #ef4444;">
              <div class="regional-card-header">
                <span class="regional-card-title"><i class="fa-solid fa-anchor" style="color:#38bdf8;"></i> Vùng Hải Phòng</span>
                <span class="risk-badge risk-badge-danger">🔴 RỦI RO SỐ 1</span>
              </div>
              <div class="regional-stats-row">
                <div><div class="stat-box-title">NPP Đang Chạy</div><div class="stat-box-num">39 / 78</div></div>
                <div><div class="stat-box-title">Điểm Bán</div><div class="stat-box-num">13,028</div></div>
                <div><div class="stat-box-title">Cự Ly TB</div><div class="stat-box-num" style="color:#ef4444;">21.3 km</div></div>
                <div><div class="stat-box-title">Khách >45km</div><div class="stat-box-num" style="color:#ef4444;">1,118 (8.6%)</div></div>
              </div>
              <div class="regional-bottleneck">
                <strong>Điểm nghẽn nguy cấp:</strong> NPP Thực Phẩm Hà Hải (1057559) có tới <b>438/440 khách >45km (99.5%)</b>, cự ly Max 78.3 km, trong đó <b>61.4% là HÀNG ĐÔNG</b> giao vượt ngưỡng an toàn.
              </div>
              <div class="regional-advice-box">
                💡 <strong>Khuyến nghị RTM:</strong><br>
                1. ❄️ <b>Bắt buộc mở Sub-depot Hàng Đông (Cold Hub):</b> Đặt trạm trung chuyển tủ đông đệm tại duyên hải phía Nam Hải Phòng hoặc giáp ranh Thái Bình để phục vụ 438 khách này.<br>
                2. <b>Bàn giao tuyến liên tỉnh:</b> Tách các tuyến Hải Dương, Thái Bình bàn giao lại cho NPP nội tỉnh phụ trách.
              </div>
              <div class="regional-card-footer">
                <button class="btn-nav" style="flex:1; justify-content:center; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Hải Phòng')">
                  <i class="fa-solid fa-list-check"></i> Xem 78 NPP
                </button>
                <button class="btn-nav" style="background:#0284c7; color:white; border:none;" onclick="viewRegionOnMap('Hải Phòng')">
                  <i class="fa-solid fa-map"></i> Bản Đồ
                </button>
              </div>
            </div>

            <!-- VÙNG 2: CẦN THƠ (MIỀN TÂY) -->
            <div class="regional-card" style="border-top: 3px solid #ef4444;">
              <div class="regional-card-header">
                <span class="regional-card-title"><i class="fa-solid fa-water" style="color:#38bdf8;"></i> Vùng Cần Thơ (Miền Tây)</span>
                <span class="risk-badge risk-badge-danger">🔴 TỶ LỆ XA CAO NHẤT</span>
              </div>
              <div class="regional-stats-row">
                <div><div class="stat-box-title">NPP Đang Chạy</div><div class="stat-box-num">34 / 62</div></div>
                <div><div class="stat-box-title">Điểm Bán</div><div class="stat-box-num">8,271</div></div>
                <div><div class="stat-box-title">Cự Ly TB</div><div class="stat-box-num" style="color:#ef4444;">19.4 km</div></div>
                <div><div class="stat-box-title">Khách >45km</div><div class="stat-box-num" style="color:#ef4444;">835 (10.1%)</div></div>
              </div>
              <div class="regional-bottleneck">
                <strong>Điểm nghẽn nguy cấp:</strong> Kênh rạch chia cắt kéo giãn tuyến xe máy gấp 1.5 lần. NPP Hưng Lộc Phát (350 khách >45km, Max 85.8km) & NPP Trần Điền - Cà Mau (298 khách >45km, Max 95.2km). Hàng khô chiếm tới <b>83.4%</b>.
              </div>
              <div class="regional-advice-box">
                💡 <strong>Khuyến nghị RTM:</strong><br>
                1. 🌾 <b>Mở Đại lý Chuyển tiếp Hàng Khô (Dry Hub):</b> Chọn đại lý lớn tại Thị trấn Cái Nước/Đầm Dơi (Cà Mau) và Thốt Nốt/Vĩnh Thạnh (Cần Thơ) nhận hàng xe tải lớn 1 chuyến/tuần.<br>
                2. <b>Thiết lập MOQ & Tần suất:</b> Nâng đơn hàng tối thiểu lên <b>&ge; 1.2M</b> và chuyển sang giao hàng <b>2 tuần/lần (F4)</b> cho các cụm cự ly >30km.
              </div>
              <div class="regional-card-footer">
                <button class="btn-nav" style="flex:1; justify-content:center; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Cần Thơ')">
                  <i class="fa-solid fa-list-check"></i> Xem 62 NPP
                </button>
                <button class="btn-nav" style="background:#0284c7; color:white; border:none;" onclick="viewRegionOnMap('Cần Thơ')">
                  <i class="fa-solid fa-map"></i> Bản Đồ
                </button>
              </div>
            </div>

            <!-- VÙNG 3: HÀ NỘI -->
            <div class="regional-card" style="border-top: 3px solid #f59e0b;">
              <div class="regional-card-header">
                <span class="regional-card-title"><i class="fa-solid fa-landmark" style="color:#38bdf8;"></i> Vùng Hà Nội (Miền Bắc)</span>
                <span class="risk-badge risk-badge-warning">🟡 RỦI RO VÙNG CAO</span>
              </div>
              <div class="regional-stats-row">
                <div><div class="stat-box-title">NPP Đang Chạy</div><div class="stat-box-num">35 / 70</div></div>
                <div><div class="stat-box-title">Điểm Bán</div><div class="stat-box-num">11,021</div></div>
                <div><div class="stat-box-title">Hàng Đông %</div><div class="stat-box-num" style="color:#38bdf8;">40.0%</div></div>
                <div><div class="stat-box-title">Khách >45km</div><div class="stat-box-num">244 (2.2%)</div></div>
              </div>
              <div class="regional-bottleneck">
                <strong>Điểm nghẽn vùng cao:</strong> Nội đô Hà Nội rất tốt, nhưng cụm Tuyên Quang đèo dốc hiểm trở: NPP Duy Thúy (1065021) có <b>100 khách >45km</b> (Max 111.9 km), đặc biệt có tới <b>84.8% HÀNG ĐÔNG</b>.
              </div>
              <div class="regional-advice-box">
                💡 <strong>Khuyến nghị RTM:</strong><br>
                1. ❄️ <b>Tủ đông đệm vệ tinh (Buffer Cold Storage):</b> Trang bị tủ đông đệm tại các thị trấn huyện lỵ (Chiêm Hóa, Hàm Yên) để tiếp tế cho nhân viên giao hàng vùng cao.<br>
                2. <b>Nội đô Hà Nội:</b> Chuyển dịch dần sang xe van điện / xe bán tải nhỏ tránh khung giờ cấm tải.
              </div>
              <div class="regional-card-footer">
                <button class="btn-nav" style="flex:1; justify-content:center; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Hà Nội')">
                  <i class="fa-solid fa-list-check"></i> Xem 70 NPP
                </button>
                <button class="btn-nav" style="background:#0284c7; color:white; border:none;" onclick="viewRegionOnMap('Hà Nội')">
                  <i class="fa-solid fa-map"></i> Bản Đồ
                </button>
              </div>
            </div>

            <!-- VÙNG 4: NHA TRANG -->
            <div class="regional-card" style="border-top: 3px solid #10b981;">
              <div class="regional-card-header">
                <span class="regional-card-title"><i class="fa-solid fa-mountain-sun" style="color:#38bdf8;"></i> Vùng Nha Trang (ĐNB & Tây Nguyên)</span>
                <span class="risk-badge risk-badge-success">🟢 KIỂM SOÁT TỐT</span>
              </div>
              <div class="regional-stats-row">
                <div><div class="stat-box-title">NPP Đang Chạy</div><div class="stat-box-num">45 / 90</div></div>
                <div><div class="stat-box-title">Điểm Bán</div><div class="stat-box-num">13,718</div></div>
                <div><div class="stat-box-title">Cự Ly TB</div><div class="stat-box-num" style="color:#34d399;">11.3 km</div></div>
                <div><div class="stat-box-title">Khách >45km</div><div class="stat-box-num">160 (1.2%)</div></div>
              </div>
              <div class="regional-bottleneck">
                <strong>Điểm nghẽn ranh giới:</strong> NPP Tiến An Nhiên (Đồng Nai) có 55 khách giáp Bình Phước/Lâm Đồng (Max 65.9km). NPP Đăng Khoa BD có 29 khách cự ly 50km.
              </div>
              <div class="regional-advice-box">
                💡 <strong>Khuyến nghị RTM:</strong><br>
                1. 🔄 <b>Tái cấu trúc ranh giới (Re-zoning):</b> Cắt chuyển các điểm bán vùng giáp ranh của Đồng Nai và Bình Dương giao cho NPP Bình Phước và Tây Ninh quản lý.<br>
                2. <b>Tây Nguyên (Đắk Lắk, Lâm Đồng):</b> Gom chuyến theo lịch thứ cố định trong tuần (Route-day schedule).
              </div>
              <div class="regional-card-footer">
                <button class="btn-nav" style="flex:1; justify-content:center; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Nha Trang')">
                  <i class="fa-solid fa-list-check"></i> Xem 90 NPP
                </button>
                <button class="btn-nav" style="background:#0284c7; color:white; border:none;" onclick="viewRegionOnMap('Nha Trang')">
                  <i class="fa-solid fa-map"></i> Bản Đồ
                </button>
              </div>
            </div>

            <!-- VÙNG 5: ĐÀ NẴNG -->
            <div class="regional-card" style="border-top: 3px solid #10b981;">
              <div class="regional-card-header">
                <span class="regional-card-title"><i class="fa-solid fa-bridge-water" style="color:#38bdf8;"></i> Vùng Đà Nẵng (Miền Trung)</span>
                <span class="risk-badge risk-badge-success">🟢 DỌC TRỤC QL1A</span>
              </div>
              <div class="regional-stats-row">
                <div><div class="stat-box-title">NPP Đang Chạy</div><div class="stat-box-num">27 / 44</div></div>
                <div><div class="stat-box-title">Điểm Bán</div><div class="stat-box-num">6,224</div></div>
                <div><div class="stat-box-title">Cự Ly TB</div><div class="stat-box-num" style="color:#34d399;">10.7 km</div></div>
                <div><div class="stat-box-title">Khách >45km</div><div class="stat-box-num">103 (1.7%)</div></div>
              </div>
              <div class="regional-bottleneck">
                <strong>Điểm nghẽn ranh giới:</strong> NPP Hoàng Mai Foods (Huế) giao ra Chân Mây - Lăng Cô mất 60km qua đèo; NPP Cao Hồng Ánh (Quảng Trị) giao 15 khách Lao Bảo (75.7% hàng đông).
              </div>
              <div class="regional-advice-box">
                💡 <strong>Khuyến nghị RTM:</strong><br>
                1. <b>Bàn giao cụm Lăng Cô cho NPP Đà Nẵng:</b> Rút ngắn cự ly từ 60.4km xuống còn 25km (qua hầm Hải Vân).<br>
                2. <b>Tuyến Lao Bảo:</b> Chạy xe tải lạnh chuyên dụng 2 chuyến/tuần từ Đông Hà thay vì chạy xe máy thùng xốp.
              </div>
              <div class="regional-card-footer">
                <button class="btn-nav" style="flex:1; justify-content:center; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('Đà Nẵng')">
                  <i class="fa-solid fa-list-check"></i> Xem 44 NPP
                </button>
                <button class="btn-nav" style="background:#0284c7; color:white; border:none;" onclick="viewRegionOnMap('Đà Nẵng')">
                  <i class="fa-solid fa-map"></i> Bản Đồ
                </button>
              </div>
            </div>

            <!-- VÙNG 6: TP. HỒ CHÍ MINH -->
            <div class="regional-card" style="border-top: 3px solid #10b981;">
              <div class="regional-card-header">
                <span class="regional-card-title"><i class="fa-solid fa-city" style="color:#38bdf8;"></i> Vùng TP. Hồ Chí Minh</span>
                <span class="risk-badge risk-badge-success">🟢 HOÀN HẢO CỰ LY</span>
              </div>
              <div class="regional-stats-row">
                <div><div class="stat-box-title">NPP Đang Chạy</div><div class="stat-box-num">35 / 47</div></div>
                <div><div class="stat-box-title">Điểm Bán</div><div class="stat-box-num">7,104</div></div>
                <div><div class="stat-box-title">Cự Ly TB</div><div class="stat-box-num" style="color:#34d399;">6.2 km</div></div>
                <div><div class="stat-box-title">Khách >45km</div><div class="stat-box-num" style="color:#34d399;">0 (0.0%)</div></div>
              </div>
              <div class="regional-bottleneck">
                <strong>Thách thức đô thị:</strong> 100% khách hàng trong cự ly an toàn <43km. Rủi ro chính là <b>xung đột chồng chéo địa bàn (overlap)</b> giữa 35 NPP và chi phí kẹt xe/dừng đỗ đô thị.
              </div>
              <div class="regional-advice-box">
                💡 <strong>Khuyến nghị RTM:</strong><br>
                1. 🗺️ <b>Siết chặt ranh giới địa bàn:</b> Rà soát triệt để hiện tượng 2 NPP cùng chào hàng vào 1 phường/tuyến phố.<br>
                2. <b>Tăng Dropsize & Tần suất:</b> Đẩy mạnh tần suất lên F4 hoặc F8 cho Key Outlets và tăng giá trị đơn hàng bình quân.
              </div>
              <div class="regional-card-footer">
                <button class="btn-nav" style="flex:1; justify-content:center; background:#2563eb; color:white; border:none;" onclick="filterByRegionFromStrategic('HCM')">
                  <i class="fa-solid fa-list-check"></i> Xem 47 NPP
                </button>
                <button class="btn-nav" style="background:#0284c7; color:white; border:none;" onclick="viewRegionOnMap('HCM')">
                  <i class="fa-solid fa-map"></i> Bản Đồ
                </button>
              </div>
            </div>

          </div>

          <!-- Lộ trình Ưu Tiên Triển Khai -->
          <div class="roadmap-container">
            <div style="font-size:0.86rem; font-weight:800; color:#f8fafc; margin-bottom:8px;">
              <i class="fa-solid fa-route" style="color:#10b981;"></i> Lộ Trình 3 Giai Đoạn Tái Cấu Trúc Toàn Quốc:
            </div>
            
            <div class="roadmap-phase">
              <span class="roadmap-tag" style="background:#dc2626;">GIAI ĐOẠN 1 (Tháng 1 - 2)</span>
              <div class="roadmap-desc">
                <b>Cấp bách chuỗi lạnh:</b> Mở Cold Sub-depot giải cứu 438 khách hàng >45km của NPP Hà Hải (Hải Phòng) & Đặt tủ đông đệm (Buffer Cold Storage) cho NPP Duy Thúy (Tuyên Quang).
              </div>
            </div>

            <div class="roadmap-phase">
              <span class="roadmap-tag" style="background:#d97706;">GIAI ĐOẠN 2 (Tháng 3 - 4)</span>
              <div class="roadmap-desc">
                <b>Tái cấu trúc cước Miền Tây:</b> Mở 2 Đại lý chuyển tiếp Hàng Khô (Dry Hubs) tại Cà Mau & Cần Thơ; ban hành chính sách MOQ &ge; 1.2M và giãn tần suất F4 cho các cụm cự ly >30km.
              </div>
            </div>

            <div class="roadmap-phase">
              <span class="roadmap-tag" style="background:#059669;">GIAI ĐOẠN 3 (Tháng 5 - 6)</span>
              <div class="roadmap-desc">
                <b>Tối ưu hóa & Chống chồng lấn:</b> Bàn giao tuyến giáp ranh (Lăng Cô sang Đà Nẵng; Định Quán sang Bình Phước); Siết chặt ranh giới địa bàn phường/quận giữa 35 NPP tại TP.HCM.
              </div>
            </div>
          </div>

        </div>

        <!-- ====================================================================
             TAB 2: BẢNG DỮ LIỆU CHI TIẾT 388 NPP & ĐỀ XUẤT TRẠM HUB (HIỆN CÓ)
             ==================================================================== -->
        <div class="tab-content" id="tabContentDetails" style="display:none;">
          <!-- KPI Summary Cards (Cập nhật động theo Vùng / Bộ lọc) -->
        <div class="modal-kpi-grid">
          <div class="modal-kpi-card">
            <span class="modal-kpi-title"><i class="fa-solid fa-arrows-left-right" style="color:#38bdf8;"></i> Cự Ly Trung Bình</span>
            <span class="modal-kpi-num" id="modalKpiAvgDist">13.9 <span style="font-size:0.85rem; font-weight:600; color:#94a3b8;">km</span></span>
            <span class="modal-kpi-desc" id="modalKpiAvgDesc">Bình quân cự ly phục vụ theo vùng được chọn</span>
          </div>

          <div class="modal-kpi-card">
            <span class="modal-kpi-title"><i class="fa-solid fa-triangle-exclamation" style="color:#ef4444;"></i> Điểm Nóng > 45km</span>
            <span class="modal-kpi-num" id="modalKpiRemote" style="color:#f87171;">2,454 <span style="font-size:0.85rem; font-weight:600; color:#94a3b8;">điểm bán</span></span>
            <span class="modal-kpi-desc" id="modalKpiRemoteDesc">Cần mở trạm trung chuyển để giảm cước</span>
          </div>

          <div class="modal-kpi-card">
            <span class="modal-kpi-title"><i class="fa-solid fa-snowflake" style="color:#38bdf8;"></i> Hàng Đông Cự Ly Xa</span>
            <span class="modal-kpi-num" id="modalKpiCold" style="color:#38bdf8;">854 <span style="font-size:0.85rem; font-weight:600; color:#94a3b8;">điểm</span></span>
            <span class="modal-kpi-desc" id="modalKpiColdDesc">Rủi ro rã đông & hư hỏng nhiệt độ cao nhất</span>
          </div>

          <div class="modal-kpi-card">
            <span class="modal-kpi-title"><i class="fa-solid fa-box-open" style="color:#f59e0b;"></i> Hàng Khô Cự Ly Xa</span>
            <span class="modal-kpi-num" id="modalKpiDry" style="color:#fbbf24;">1,600 <span style="font-size:0.85rem; font-weight:600; color:#94a3b8;">điểm</span></span>
            <span class="modal-kpi-desc" id="modalKpiDryDesc">Có thể gom tuyến hoặc chuyển tải linh hoạt</span>
          </div>
        </div>

        <!-- Filter & Search Controls in Modal (Đầy đủ lọc Miền, Vùng, Trạng thái, Sắp xếp) -->
        <div class="modal-filter-row">
          <span style="color:#94a3b8; font-size:0.72rem; font-weight:700;"><i class="fa-solid fa-filter"></i> Lọc:</span>
          
          <!-- LỌC MIỀN TRONG MODAL -->
          <select id="modalFilterMien" class="filter-select" onchange="onModalMienChange()">
            <option value="ALL">Tất cả Miền</option>
            <option value="MIỀN NAM">MIỀN NAM (199 NPP)</option>
            <option value="MIỀN BẮC">MIỀN BẮC (192 NPP)</option>
          </select>

          <!-- LỌC THEO VÙNG (AREA) TRONG MODAL -->
          <select id="modalFilterVung" class="filter-select" onchange="filterAnalyticsTable()">
            <option value="ALL">Tất cả Vùng (6 Vùng)</option>
          </select>

          <select id="modalFilterStatus" class="filter-select" onchange="filterAnalyticsTable()">
            <option value="ACTIVE" selected>🟢 Chỉ NPP Đang Hoạt Động</option>
            <option value="REMOTE_ONLY">⚠️ Chỉ NPP có khách >45km</option>
            <option value="ALL">Tất cả NPP</option>
          </select>

          <select id="modalSortCriteria" class="filter-select" onchange="filterAnalyticsTable()">
            <option value="REMOTE_COUNT" selected>Sắp xếp: Số khách >45km giảm dần</option>
            <option value="MAX_DIST">Sắp xếp: Cự ly Max giảm dần</option>
            <option value="AVG_DIST">Sắp xếp: Cự ly TB giảm dần</option>
            <option value="TOTAL_OUTLETS">Sắp xếp: Tổng khách giảm dần</option>
          </select>

          <input type="text" id="modalSearch" class="filter-search" placeholder="🔍 Tìm NPP, Tỉnh, Khách xa nhất..." oninput="filterAnalyticsTable()" style="flex:1; min-width:140px;">
          
          <span style="font-size:0.7rem; color:#94a3b8; margin-left:auto;">Hiển thị: <b id="modalTableCount" style="color:#38bdf8;">0</b> NPP</span>
        </div>

        <!-- Table displaying NPP Average & Max distances -->
        <div class="analytics-table-wrap">
          <table class="analytics-table">
            <thead>
              <tr>
                <th>MÃ & TÊN NPP</th>
                <th>TRẠNG THÁI</th>
                <th>VÙNG / TỈNH</th>
                <th>TỔNG KH</th>
                <th>CỰ LY TB</th>
                <th>CỰ LY XA NHẤT</th>
                <th>KHÁCH HÀNG XA NHẤT (TÊN, CỰ LY & LOẠI HÀNG)</th>
                <th>KH > 45KM</th>
                <th>ĐỀ XUẤT TRẠM HUB</th>
                <th>THAO TÁC</th>
              </tr>
            </thead>
            <tbody id="analyticsTableBody">
              <!-- Dynamically rendered -->
            </tbody>
          </table>
        </div>
        </div> <!-- End Tab 2 Details -->
      </div>
    </div>
  </div>

  <script>
    // Dữ liệu 391 NPP
    const ALL_NPPS = {npps_json_str};
    let ALL_OUTLETS = [];
    let NPP_ANALYTICS = [];

    let filteredNPPs = [...ALL_NPPS];
    let filteredOutlets = [];
    let selectedNPP = null;

    let showNPP = true;
    let showOutlets = false;
    let showOnlyEquip = false;
    let showOnlyWithSales = false;
    let showSpiderLines = false;
    let showRadius = false;

    // Khởi tạo Leaflet Map
    const map = L.map('map', {{
      center: [14.0583, 108.2772],
      zoom: 6,
      zoomControl: false,
      preferCanvas: true
    }});

    L.control.zoom({{ position: 'topleft' }}).addTo(map);

    // Tile Layer OpenStreetMap
    const osmLayer = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap'
    }}).addTo(map);

    // Layer Groups
    const markersLayer = L.layerGroup().addTo(map);
    const radiusLayer = L.layerGroup();
    const outletsLayer = L.layerGroup().addTo(map);
    const spiderLayer = L.layerGroup().addTo(map);

    // Poll data loaded from deferred script
    let checkTimer = setInterval(() => {{
      let hasUpdate = false;
      if (window.ALL_OUTLETS && ALL_OUTLETS.length === 0) {{
        ALL_OUTLETS = window.ALL_OUTLETS;
        hasUpdate = true;
      }}
      if (window.NPP_ANALYTICS && NPP_ANALYTICS.length === 0) {{
        NPP_ANALYTICS = window.NPP_ANALYTICS;
        hasUpdate = true;
      }}

      if (hasUpdate) {{
        document.getElementById('loadingIndicator').style.opacity = '0';
        setTimeout(() => {{
          const el = document.getElementById('loadingIndicator');
          if (el) el.style.display = 'none';
        }}, 500);
        applyFilters();
      }}
      if (ALL_OUTLETS.length > 0 && NPP_ANALYTICS.length > 0) {{
        clearInterval(checkTimer);
      }}
    }}, 200);

    // Initial Setup
    document.addEventListener('DOMContentLoaded', () => {{
      populateVungOptions();
      populateTinhOptions();
      loadPlannedFlagsFromStorage();

      applyFilters();

      // Check mobile size to auto-adjust
      if (window.innerWidth <= 768) {{
        map.setZoom(5);
      }}

      // Tải ngầm 59.4k điểm bán sau 2.5 giây khi giao diện chính đã sẵn sàng
      setTimeout(() => {{
        ensureOutletsLoaded();
      }}, 2500);
    }});

    function populateVungOptions() {{
      const mienVal = document.getElementById('filterMien').value;
      const vungSelect = document.getElementById('filterVung');
      vungSelect.innerHTML = '<option value="ALL">Tất cả Vùng</option>';

      let areas = new Set();
      ALL_NPPS.forEach(n => {{
        if (mienVal === 'ALL' || n.region === mienVal) {{
          if (n.area) areas.add(n.area);
        }}
      }});

      Array.from(areas).sort().forEach(a => {{
        const opt = document.createElement('option');
        opt.value = a;
        const count = ALL_NPPS.filter(n => (mienVal === 'ALL' || n.region === mienVal) && n.area === a).length;
        opt.textContent = `${{a}} (${{count}} NPP)`;
        vungSelect.appendChild(opt);
      }});
    }}

    function populateTinhOptions() {{
      const mienVal = document.getElementById('filterMien').value;
      const vungVal = document.getElementById('filterVung').value;
      const tinhSelect = document.getElementById('filterTinh');
      tinhSelect.innerHTML = '<option value="ALL">Tất cả Tỉnh/Thành</option>';

      let provinces = new Set();
      ALL_NPPS.forEach(n => {{
        const matchMien = (mienVal === 'ALL' || n.region === mienVal);
        const matchVung = (vungVal === 'ALL' || n.area === vungVal);
        if (matchMien && matchVung && n.province) {{
          provinces.add(n.province);
        }}
      }});

      Array.from(provinces).sort().forEach(p => {{
        const opt = document.createElement('option');
        opt.value = p;
        const count = ALL_NPPS.filter(n => 
          (mienVal === 'ALL' || n.region === mienVal) && 
          (vungVal === 'ALL' || n.area === vungVal) && 
          n.province === p
        ).length;
        opt.textContent = `${{p}} (${{count}} NPP)`;
        tinhSelect.appendChild(opt);
      }});
    }}

    function onMienChange() {{
      populateVungOptions();
      populateTinhOptions();
      applyFilters();
    }}

    function onVungChange() {{
      populateTinhOptions();
      applyFilters();
    }}

    function toggleNPPVisibility() {{
      const chk = document.getElementById('chkToggleNPP');
      const lbl = document.getElementById('lblChkNpp');
      showNPP = chk.checked;
      if (showNPP) {{
        lbl.classList.add('active-npp');
        markersLayer.addTo(map);
      }} else {{
        lbl.classList.remove('active-npp');
        map.removeLayer(markersLayer);
      }}
    }}

    function toggleHideInactive() {{
      const chk = document.getElementById('chkHideInactive');
      const statusSelect = document.getElementById('filterStatus');
      if (statusSelect) {{
        if (chk.checked) {{
          statusSelect.value = 'ACTIVE';
        }} else {{
          statusSelect.value = 'ALL';
        }}
      }}
      applyFilters();
    }}

    function toggleHideInactiveQuick() {{
      const chk = document.getElementById('chkHideInactive');
      if (chk) {{
        chk.checked = !chk.checked;
        toggleHideInactive();
      }}
    }}

    function onStatusSelectChange() {{
      const statusSelect = document.getElementById('filterStatus');
      const chk = document.getElementById('chkHideInactive');
      if (chk && statusSelect) {{
        chk.checked = (statusSelect.value === 'ACTIVE');
      }}
      applyFilters();
    }}

    
    // ==========================================
    // DYNAMIC LAZY LOADER FOR 59.4K OUTLETS (11.8MB)
    // ==========================================
    let outletsLoaded = (typeof ALL_OUTLETS !== 'undefined' && ALL_OUTLETS && ALL_OUTLETS.length > 0);
    let outletsLoading = false;

    function showToastNotification(msg) {{
      let t = document.getElementById('rtmToast');
      if (!t) {{
        t = document.createElement('div');
        t.id = 'rtmToast';
        t.style.cssText = 'position:fixed; bottom:20px; right:20px; background:rgba(15,23,42,0.95); border:1px solid #10b981; color:#fff; font-size:0.75rem; font-weight:700; padding:8px 14px; border-radius:8px; z-index:99999; box-shadow:0 8px 24px rgba(0,0,0,0.5); backdrop-filter:blur(6px); transition:all 0.3s;';
        document.body.appendChild(t);
      }}
      t.innerHTML = msg;
      t.style.display = 'block';
      setTimeout(() => {{ if (t) t.style.display = 'none'; }}, 3000);
      return t;
    }}

    function ensureOutletsLoaded(callback) {{
      if (typeof ALL_OUTLETS !== 'undefined' && ALL_OUTLETS && ALL_OUTLETS.length > 0 && ALL_OUTLETS[0].length > 12) {{
        outletsLoaded = true;
        if (callback) callback();
        return;
      }}
      if (outletsLoading) {{
        const checkTimer = setInterval(() => {{
          if (typeof ALL_OUTLETS !== 'undefined' && ALL_OUTLETS && ALL_OUTLETS.length > 0 && ALL_OUTLETS[0].length > 12) {{
            clearInterval(checkTimer);
            outletsLoaded = true;
            if (callback) callback();
          }}
        }}, 100);
        return;
      }}
      outletsLoading = true;
      showToastNotification('⏳ Đang tải dữ liệu 59.4k điểm bán & Doanh số T9...');

      const s = document.createElement('script');
      s.src = 'outlets_data.js?v=20261027_t9_mtd_v2';
      s.onload = () => {{
        outletsLoaded = true;
        outletsLoading = false;
        showToastNotification('✅ Đã nạp 59.4k điểm bán (34.2k có DS T9 - 38.3 Tỷ | 2.6k có Tủ)!');
        console.log('Loaded ALL_OUTLETS:', ALL_OUTLETS.length);
        applyFilters();
        if (callback) callback();
      }};
      s.onerror = () => {{
        outletsLoading = false;
        showToastNotification('⚠️ Không thể tải file outlets_data.js');
      }};
      document.body.appendChild(s);
    }}

    function toggleOutletVisibility() {{
      setTimeout(updateOutletTriggerLabel, 50);
      const chk = document.getElementById('chkToggleOutlet');
      const lbl = document.getElementById('lblChkOutlet');
      const quickBtn = document.getElementById('btnQuickToggleOutlet');
      const quickText = document.getElementById('btnQuickOutletText');
      showOutlets = chk.checked;
      if (showOutlets) {{
        if (lbl) lbl.classList.add('active-outlet');
        if (quickBtn) quickBtn.classList.add('active-quick-outlet');
        if (quickText) quickText.textContent = 'Ẩn Điểm Bán';
        ensureOutletsLoaded(() => {{
          renderOutlets();
          outletsLayer.addTo(map);
        }});
      }} else {{
        if (lbl) lbl.classList.remove('active-outlet');
        if (quickBtn) quickBtn.classList.remove('active-quick-outlet');
        if (quickText) quickText.textContent = 'Hiện Điểm Bán';
        map.removeLayer(outletsLayer);
      }}
    }}

    function toggleOnlySalesQuick() {{
      setTimeout(updateOutletTriggerLabel, 50);
      showOnlyWithSales = !showOnlyWithSales;
      const btn = document.getElementById('btnQuickOnlySales');
      if (btn) {{
        btn.classList.toggle('active-inactive-btn', showOnlyWithSales);
      }}
      if (showOnlyWithSales) {{
        showOutlets = true;
        const chk = document.getElementById('chkToggleOutlet');
        if (chk) chk.checked = true;
        const quickText = document.getElementById('btnQuickOutletText');
        if (quickText) quickText.textContent = 'Ẩn Điểm Bán';
        ensureOutletsLoaded(() => {{
          renderOutlets();
          outletsLayer.addTo(map);
          showToastNotification('💰 Đang lọc 34,171 điểm bán có Doanh số T9 (38.3 Tỷ)!');
        }});
      }} else {{
        renderOutlets();
      }}
    }}

    function toggleOnlyEquipQuick() {{
      setTimeout(updateOutletTriggerLabel, 50);
      showOnlyEquip = !showOnlyEquip;
      const btn = document.getElementById('btnQuickOnlyEquip');
      if (btn) {{
        btn.classList.toggle('active-inactive-btn', showOnlyEquip);
      }}
      if (showOnlyEquip) {{
        showOutlets = true;
        const chk = document.getElementById('chkToggleOutlet');
        if (chk) chk.checked = true;
        const quickText = document.getElementById('btnQuickOutletText');
        if (quickText) quickText.textContent = 'Ẩn Điểm Bán';
        ensureOutletsLoaded(() => {{
          renderOutlets();
          outletsLayer.addTo(map);
          showToastNotification('❄️ Đang hiển thị 2,598 điểm bán có Tủ đông/Tủ mát!');
        }});
      }} else {{
        renderOutlets();
      }}
    }}


    function toggleOutletQuick() {{
      const chk = document.getElementById('chkToggleOutlet');
      if (chk) {{
        chk.checked = !chk.checked;
        toggleOutletVisibility();
      }}
    }}

    function toggleSpiderVisibility() {{
      const chk = document.getElementById('chkToggleSpider');
      const lbl = document.getElementById('lblChkSpider');
      showSpiderLines = chk.checked;
      if (showSpiderLines) {{
        lbl.classList.add('active-spider');
        renderSpiderLines();
      }} else {{
        lbl.classList.remove('active-spider');
        spiderLayer.clearLayers();
      }}
    }}

    // ==========================================
    // UNIFIED TOOLBAR EVENT HANDLERS & HELPERS
    // ==========================================
    function toggleUnifiedNppLayer() {{
      const chk = document.getElementById('chkToggleNPP');
      if (chk) {{
        chk.checked = !chk.checked;
        toggleNPPVisibility();
        const btn = document.getElementById('btnUnifiedNppToggle');
        if (btn) btn.classList.toggle('active-npp', chk.checked);
      }}
    }}

    function onUnifiedNppStatusChange(val) {{
      const filterStatus = document.getElementById('filterStatus');
      const filterSM = document.getElementById('filterSM');
      const chkHideInactive = document.getElementById('chkHideInactive');
      const chkHideKhongSM = document.getElementById('chkHideKhongSM');

      if (val === 'ALL') {{
        if (filterStatus) filterStatus.value = 'ALL';
        if (chkHideInactive) chkHideInactive.checked = false;
        if (filterSM) filterSM.value = 'ALL';
        if (chkHideKhongSM) chkHideKhongSM.checked = false;
      }} else if (val === 'ACTIVE_ALL') {{
        if (filterStatus) filterStatus.value = 'ACTIVE';
        if (chkHideInactive) chkHideInactive.checked = true;
        if (filterSM) filterSM.value = 'ALL';
        if (chkHideKhongSM) chkHideKhongSM.checked = false;
      }} else if (val === 'ACTIVE_SM') {{
        if (filterStatus) filterStatus.value = 'ACTIVE';
        if (chkHideInactive) chkHideInactive.checked = true;
        if (filterSM) filterSM.value = 'CO_SM';
        if (chkHideKhongSM) chkHideKhongSM.checked = true;
      }} else if (val === 'ACTIVE_KSM') {{
        if (filterStatus) filterStatus.value = 'ACTIVE';
        if (chkHideInactive) chkHideInactive.checked = true;
        if (filterSM) filterSM.value = 'KHONG_SM';
        if (chkHideKhongSM) chkHideKhongSM.checked = false;
      }} else if (val === 'INACTIVE') {{
        if (filterStatus) filterStatus.value = 'INACTIVE';
        if (chkHideInactive) chkHideInactive.checked = false;
        if (filterSM) filterSM.value = 'ALL';
        if (chkHideKhongSM) chkHideKhongSM.checked = false;
      }}

      applyFilters();
    }}

    function toggleOutletMenu(e) {{
      if (e) e.stopPropagation();
      const menu = document.getElementById('outletDropdownMenu');
      const isShown = menu.classList.contains('show');
      closeAllDropdowns();
      if (!isShown) menu.classList.add('show');
    }}

    function toggleToolsMenu(e) {{
      if (e) e.stopPropagation();
      const menu = document.getElementById('toolsDropdownMenu');
      const isShown = menu.classList.contains('show');
      closeAllDropdowns();
      if (!isShown) menu.classList.add('show');
    }}

    function closeAllDropdowns() {{
      document.querySelectorAll('.island-dropdown-menu').forEach(el => el.classList.remove('show'));
    }}
    document.addEventListener('click', (e) => {{
      if (e.target && e.target.closest('#outletDropdownMenu')) return;
      closeAllDropdowns();
    }});

    function updateOutletTriggerLabel() {{
      const lbl = document.getElementById('outletTriggerLabel');
      const btn = document.getElementById('btnOutletMasterTrigger');
      const countSpan = document.getElementById('chkOutletCount');
      const cnt = countSpan ? countSpan.textContent : '59.4k';

      if (showOnlyWithSales) {{
        if (lbl) lbl.innerHTML = `💰 Có DS T9 (${{cnt}})`;
        if (btn) btn.classList.add('active-outlet');
      }} else if (showOnlyEquip) {{
        if (lbl) lbl.innerHTML = `❄️ Có Tủ CJ (${{cnt}})`;
        if (btn) btn.classList.add('active-outlet');
      }} else if (showOutlets) {{
        if (lbl) lbl.innerHTML = `🏪 Điểm Bán (${{cnt}})`;
        if (btn) btn.classList.add('active-outlet');
      }} else {{
        if (lbl) lbl.innerHTML = `Điểm Bán (${{cnt}})`;
        if (btn) btn.classList.remove('active-outlet');
      }}

      // Cập nhật text & badge trong menu
      const menuTitle = document.getElementById('menuOutletStatusTitle');
      if (menuTitle) {{
        menuTitle.textContent = showOutlets ? 'Ẩn Lớp Điểm Bán' : 'Bật Hiển Thị Điểm Bán';
      }}
      const bSales = document.getElementById('badgeMenuSales');
      if (bSales) {{
        bSales.style.background = showOnlyWithSales ? '#059669' : 'rgba(255,255,255,0.08)';
        bSales.style.color = showOnlyWithSales ? '#ffffff' : '#cbd5e1';
      }}
      const bEquip = document.getElementById('badgeMenuEquip');
      if (bEquip) {{
        bEquip.style.background = showOnlyEquip ? '#0284c7' : 'rgba(255,255,255,0.08)';
        bEquip.style.color = showOnlyEquip ? '#ffffff' : '#cbd5e1';
      }}
      const bMaster = document.getElementById('badgeOutletMaster');
      if (bMaster) {{
        bMaster.style.background = showOutlets ? '#d97706' : 'rgba(255,255,255,0.08)';
        bMaster.style.color = showOutlets ? '#ffffff' : '#cbd5e1';
      }}
    }}

    function toggleOutletMasterFromMenu() {{
      const chk = document.getElementById('chkToggleOutlet');
      if (chk) {{
        chk.checked = !chk.checked;
        toggleOutletVisibility();
        updateOutletTriggerLabel();
      }}
    }}

    function toggleRemoteOnlyMenu() {{
      const chk = document.getElementById('chkToggleRemoteOnly');
      if (chk) {{
        chk.checked = !chk.checked;
        applyFilters();
      }}
    }}

    function toggleSpiderFromMenu() {{
      const chk = document.getElementById('chkToggleSpider');
      if (chk) {{
        chk.checked = !chk.checked;
        toggleSpiderVisibility();
      }}
    }}

    function applyFilters() {{
      const mienVal = document.getElementById('filterMien').value;
      const vungVal = document.getElementById('filterVung').value;
      const tinhVal = document.getElementById('filterTinh').value;
      const statusVal = document.getElementById('filterStatus') ? document.getElementById('filterStatus').value : 'ALL';
      const hideInactive = document.getElementById('chkHideInactive') ? document.getElementById('chkHideInactive').checked : false;
      const hideKhongSM = document.getElementById('chkHideKhongSM') ? document.getElementById('chkHideKhongSM').checked : false;
      const smVal = document.getElementById('filterSM') ? document.getElementById('filterSM').value : 'ALL';
      const searchVal = document.getElementById('filterSearch').value.toLowerCase().trim();

      // Đồng bộ trạng thái visual nút Bỏ NPP Không SM trên bản đồ
      const btnQuickKSM = document.getElementById('btnQuickHideKhongSM');
      const textQuickKSM = document.getElementById('btnQuickHideKhongSMText');
      if (btnQuickKSM) {{
        btnQuickKSM.classList.toggle('active-inactive-btn', hideKhongSM || smVal === 'CO_SM');
        if (textQuickKSM) {{
          textQuickKSM.textContent = (hideKhongSM || smVal === 'CO_SM') ? 'Đã Ẩn NPP Không SM' : 'Bỏ NPP Không SM';
        }}
      }}

      const allowCold = document.getElementById('chkToggleCold').checked;
      const allowDry = document.getElementById('chkToggleDry').checked;
      const remoteOnly = document.getElementById('chkToggleRemoteOnly').checked;

      // Update toggle visual active states
      document.getElementById('lblChkCold').classList.toggle('active-cold', allowCold);
      document.getElementById('lblChkDry').classList.toggle('active-dry', allowDry);
      document.getElementById('lblChkRemoteOnly').classList.toggle('active-remote', remoteOnly);

      const lblInactive = document.getElementById('lblChkHideInactive');
      if (lblInactive) lblInactive.classList.toggle('active-hide-inactive', hideInactive);

      const btnQuickInactive = document.getElementById('btnQuickHideInactive');
      if (btnQuickInactive) {{
        btnQuickInactive.classList.toggle('active-inactive-btn', hideInactive);
      }}

      // 1. Filter NPPs
      filteredNPPs = ALL_NPPS.filter(n => {{
        const matchMien = (mienVal === 'ALL' || n.region === mienVal);
        const matchVung = (vungVal === 'ALL' || n.area === vungVal);
        const matchTinh = (tinhVal === 'ALL' || n.province === tinhVal);

        // Bỏ NPP ngưng hoạt động khi nút tích Bỏ NPP Ngưng được chọn
        if (hideInactive && !n.status.includes('Đang')) return false;

        // Ẩn hoàn toàn NPP không có SM nếu chọn Bỏ NPP Không SM hoặc lọc Chỉ Có SM
        if (hideKhongSM && n.is_khong_sm) return false;
        if (smVal === 'CO_SM' && n.is_khong_sm) return false;
        if (smVal === 'KHONG_SM' && !n.is_khong_sm) return false;

        const matchStatus = (statusVal === 'ALL') || 
                            (statusVal === 'ACTIVE' && n.status.includes('Đang')) || 
                            (statusVal === 'INACTIVE' && !n.status.includes('Đang'));
        const matchSearch = !searchVal || 
          n.name.toLowerCase().includes(searchVal) ||
          n.code.toLowerCase().includes(searchVal) ||
          n.short_name.toLowerCase().includes(searchVal) ||
          n.address.toLowerCase().includes(searchVal) ||
          n.province.toLowerCase().includes(searchVal);

        return matchMien && matchVung && matchTinh && matchStatus && matchSearch;
      }});

      const matchingNppCodeSet = new Set(filteredNPPs.map(n => String(n.code)));

      // 2. Filter Outlets
      filteredOutlets = ALL_OUTLETS.filter(o => {{
        if (mienVal !== 'ALL' && o[7] !== mienVal) return false;
        if (vungVal !== 'ALL' && o[6] !== vungVal) return false;
        if (tinhVal !== 'ALL' && o[5] !== tinhVal) return false;

        // Tự động ẩn toàn bộ điểm bán nếu NPP của điểm bán đó bị ẩn (do lọc vùng, ngưng hoạt động, hoặc không có SM)
        if (!matchingNppCodeSet.has(String(o[4]))) return false;
        if (remoteOnly && o[10] < 45) return false;

        const ptype = o[11];
        const isCold = (ptype === 'DONG' || ptype === 'BOTH');
        const isDry = (ptype === 'KHO' || ptype === 'BOTH' || ptype === 'OTHER');

        if (!allowCold && isCold && !allowDry) return false;
        if (!allowDry && !isCold) return false;
        if (!allowCold && !allowDry) return false;

        if (searchVal) {{
          const matchO = o[2].toLowerCase().includes(searchVal) ||
                         o[3].toLowerCase().includes(searchVal) ||
                         o[4].toLowerCase().includes(searchVal) ||
                         o[9].toLowerCase().includes(searchVal);
          if (!matchO) return false;
        }}
        return true;
      }});

      renderMapMarkers();
      renderOutlets();
      if (showSpiderLines) renderSpiderLines();
      renderSidebarList();
      updateKPIs();
    }}

    function updateKPIs() {{
      const totalNpp = filteredNPPs.length;
      const activeNpp = filteredNPPs.filter(n => n.status.includes('Đang')).length;
      const inactiveNpp = totalNpp - activeNpp;
      const totalOutlets = filteredOutlets.length;
      const remoteCount = filteredOutlets.filter(o => o[10] >= 45).length;

      document.getElementById('kpiCount').textContent = totalNpp;
      if (document.getElementById('kpiActive')) document.getElementById('kpiActive').textContent = `${{activeNpp}} Chạy`;
      if (document.getElementById('kpiInactive')) document.getElementById('kpiInactive').textContent = `${{inactiveNpp}} Ngưng`;
      document.getElementById('kpiOutlets').textContent = totalOutlets.toLocaleString('vi-VN');
      document.getElementById('kpiRemote').textContent = remoteCount.toLocaleString('vi-VN');
      document.getElementById('sidebarCount').textContent = totalNpp;
      if (document.getElementById('mobileCount')) document.getElementById('mobileCount').textContent = totalNpp;

      const totalFilteredSales = filteredNPPs.reduce((acc, n) => acc + (n.sales_total || 0), 0);
      const salesElem = document.getElementById('sidebarTotalSales');
      if (salesElem) {{
        salesElem.textContent = formatMoneyVND(totalFilteredSales);
      }}

      document.getElementById('chkNppCount').textContent = totalNpp;
      document.getElementById('chkOutletCount').textContent = totalOutlets >= 1000 ? (totalOutlets/1000).toFixed(1) + 'k' : totalOutlets;
      updateOutletTriggerLabel();
    }}

    // Render Markers on Map
    function renderMapMarkers() {{
      markersLayer.clearLayers();
      radiusLayer.clearLayers();

      const bounds = [];

      filteredNPPs.forEach(n => {{
        if (!n.lat || !n.lng) return;

        const isActive = n.status.includes('Đang');
        let iconClass = 'npp-icon-inactive';
        let iconInner = 'fa-solid fa-lock';
        let iconTitle = 'NPP Ngưng Hoạt Động';

        if (isActive) {{
          if (n.is_khong_sm) {{
            iconClass = 'npp-icon-khong-sm';
            iconInner = 'fa-solid fa-user-slash';
            iconTitle = '⚠️ NPP Không Có SM (Cần giám sát)';
          }} else {{
            iconClass = 'npp-icon-co-sm';
            iconInner = 'fa-solid fa-user-tie';

            // Định dạng hover: "NPP [Tên] ( X SM)" vd: "NPP Trần Điền ( 2SM)"
            const rawName = n.short_name || n.name || '';
            const prefixRegex = /^(CÔNG TY TNHH (MỘT THÀNH VIÊN|MTV|SX TM DV|SX TM|TM DV|THƯƠNG MẠI DỊCH VỤ|DỊCH VỤ VỆ SINH|THỰC PHẨM|DV PHÂN PHỐI|DV|TM|SX)?|CÔNG TY CP|CÔNG TY CỔ PHẦN|DOANH NGHIỆP TƯ NHÂN|DNTN|HỢP TÁC XÃ THƯƠNG MẠI- DỊCH VỤ PHƯỜNG 1- TP|HỢP TÁC XÃ|CTY TNHH|CTY CP)\\s*/i;
            let cleanName = rawName.replace(prefixRegex, '').trim();
            if (!cleanName.toUpperCase().startsWith('NPP')) {{
              cleanName = 'NPP ' + cleanName;
            }}
            const soSM = n.so_nvbh || 1;
            iconTitle = `${{cleanName}} ( ${{soSM}}SM)`;
          }}
        }}

        const iconHtml = `
          <div class="custom-npp-icon ${{iconClass}}" style="width: 26px; height: 26px;" title="${{iconTitle}}">
            <i class="${{iconInner}} npp-icon-inner"></i>
          </div>
        `;

        const customIcon = L.divIcon({{
          html: iconHtml,
          className: 'custom-leaflet-marker',
          iconSize: [24, 24],
          iconAnchor: [12, 12],
          popupAnchor: [0, -12]
        }});

        const marker = L.marker([n.lat, n.lng], {{ icon: customIcon, title: iconTitle }});
        marker.bindTooltip(iconTitle, {{
          direction: 'top',
          offset: [0, -14],
          opacity: 0.96,
          className: 'npp-hover-tooltip ' + (n.is_khong_sm ? 'tooltip-ksm' : '')
        }});

        const outletCnt = n.outlet_count || 0;
        const remoteCnt = n.remote_count || 0;
        const dongCnt = n.dong_count || 0;
        const maxDist = n.max_dist || 0;

        const popupContent = `
          <div class="popup-card">
            <div class="popup-header">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:3px;">
                <span class="popup-tag ${{isActive ? 'badge-active' : 'badge-inactive'}}">${{n.status}}</span>
                <div style="display:flex; gap:3px;">
                  <span class="popup-tag" style="background:${{n.is_khong_sm ? '#fee2e2' : '#d1fae5'}}; color:${{n.is_khong_sm ? '#991b1b' : '#065f46'}}; font-weight:800;">
                    ${{n.is_khong_sm ? '⚠️ Không có nhân viên' : `👤 Có ${{n.so_nvbh}} nhân viên`}}
                  </span>
                  ${{n.top50 ? '<span class="popup-tag" style="background:#fef3c7; color:#92400e; font-weight:800;">⭐ Top 50</span>' : ''}}
                </div>
              </div>
              <div class="popup-title">${{n.name}}</div>
              <div style="font-size:0.68rem; color:#94a3b8; margin-top:2px;">Mã: <b>${{n.code}}</b> &bull; ${{n.region}} &bull; ${{n.province}}</div>
            </div>

            <div class="popup-body">
              <!-- THÔNG TIN NHÂN SỰ BÁN HÀNG GỌN GÀNG -->
              <div class="popup-row" style="margin: 4px 0; padding: 5px 8px; background: #1e293b; border-radius: 5px; border-left: 3px solid ${{n.is_khong_sm ? '#ef4444' : '#10b981'}};">
                <i class="fa-solid fa-users" style="color:${{n.is_khong_sm ? '#ef4444' : '#34d399'}};"></i>
                <div>
                  Nhân sự bán hàng: <b style="color:${{n.is_khong_sm ? '#f87171' : '#34d399'}}; font-size: 0.78rem;">
                    ${{n.is_khong_sm ? 'Không có nhân viên (0 NV)' : `Có ${{n.so_nvbh}} nhân viên`}}
                  </b>
                  ${{n.gsbh ? `<span style="color:#94a3b8; font-size:0.68rem; margin-left:4px;">(GS: ${{n.gsbh}})</span>` : ''}}
                </div>
              </div>

              
              <!-- THÔNG TIN DOANH SỐ T9/2026 THEO NHÓM SẢN PHẨM -->
              ${{n.sales_total > 0 ? `
              <div class="popup-row" style="margin: 5px 0; padding: 7px 10px; background: rgba(16, 185, 129, 0.1); border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.35); flex-direction:column; align-items:flex-start;">
                <div style="display:flex; justify-content:space-between; width:100%; align-items:center; margin-bottom:4px;">
                  <span style="color:#6ee7b7; font-weight:800; font-size:0.75rem;"><i class="fa-solid fa-chart-line"></i> Doanh số T9/2026:</span>
                  <b style="color:#10b981; font-size:0.85rem;">${{formatMoneyVND(n.sales_total)}}</b>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; width:100%; text-align:center; font-size:0.68rem;">
                  <div style="background:#1e293b; padding:3px 2px; border-radius:4px; border-left:2px solid #f59e0b;">
                    <div style="color:#94a3b8;">Ambient</div>
                    <b style="color:#fbbf24;">${{formatMoneyShort(n.sales_ambient)}}</b>
                  </div>
                  <div style="background:#1e293b; padding:3px 2px; border-radius:4px; border-left:2px solid #10b981;">
                    <div style="color:#94a3b8;">Chilled</div>
                    <b style="color:#34d399;">${{formatMoneyShort(n.sales_chilled)}}</b>
                  </div>
                  <div style="background:#1e293b; padding:3px 2px; border-radius:4px; border-left:2px solid #38bdf8;">
                    <div style="color:#94a3b8;">Frozen</div>
                    <b style="color:#38bdf8;">${{formatMoneyShort(n.sales_frozen)}}</b>
                  </div>
                </div>
              </div>` : ''}}

              <!-- THÔNG TIN VẬN HÀNH & ĐIỂM BÁN -->
              <div class="popup-row"><i class="fa-solid fa-location-dot" style="color:#60a5fa;"></i><span>${{n.address || 'Đang cập nhật'}}</span></div>
              ${{n.phone && n.phone !== '0000000000' && n.phone !== '123456' ? `<div class="popup-row"><i class="fa-solid fa-phone" style="color:#34d399;"></i><span>Liên hệ: <b style="color:#e2e8f0;">${{n.phone}}</b></span></div>` : ''}}
              <div class="popup-row"><i class="fa-solid fa-store" style="color:#f59e0b;"></i><span><b>${{outletCnt}}</b> Điểm bán (${{dongCnt}} hàng đông)</span></div>
              <div class="popup-row"><i class="fa-solid fa-arrows-left-right" style="color:#38bdf8;"></i><span>Cự ly Max: <b>${{maxDist}} km</b> &bull; Cự ly TB: <b>${{n.avg_dist || 0}} km</b></span></div>
              ${{remoteCnt > 0 ? `<div class="popup-row"><i class="fa-solid fa-triangle-exclamation" style="color:#ef4444;"></i><span style="color:#ef4444; font-weight:700;">${{remoteCnt}} điểm cự ly > 45km</span></div>` : ''}}
            </div>

            <div class="popup-actions">
              <button class="btn-action btn-spider" onclick="focusNPPAndSpider('${{n.code}}')"><i class="fa-solid fa-share-nodes"></i> Tia nối</button>
              <button class="btn-action btn-primary" onclick="zoomToNPP('${{n.code}}')"><i class="fa-solid fa-crosshairs"></i> Phóng to</button>
              <button class="btn-action btn-outlet" onclick="showNPPOutlets('${{n.code}}')">
                <i class="fa-solid fa-store"></i> Hiện Điểm Bán (${{outletCnt}})
              </button>
            </div>
          </div>
        `

        marker.bindPopup(popupContent);
        marker.on('click', () => selectNPP(n.code, false));
        markersLayer.addLayer(marker);
        bounds.push([n.lat, n.lng]);

        // Radius 45km
        const circle = L.circle([n.lat, n.lng], {{
          radius: 45000,
          color: isActive ? '#059669' : '#dc2626',
          weight: 1,
          opacity: 0.6,
          fillColor: isActive ? '#10b981' : '#ef4444',
          fillOpacity: 0.05
        }});
        radiusLayer.addLayer(circle);
      }});

      if (bounds.length > 0 && bounds.length <= 15) {{
        map.fitBounds(bounds, {{ padding: [30, 30], maxZoom: 12 }});
      }}
    }}

    // Render Outlets as Lightweight Circle Markers
    function renderOutlets() {{
      outletsLayer.clearLayers();
      if (!showOutlets && !showOnlyEquip) return;

      // Tra cứu nhanh Tên NPP theo Mã NPP
      const nppNameMap = new Map();
      ALL_NPPS.forEach(n => {{
        nppNameMap.set(String(n.code), n.short_name || n.name);
      }});

      const maxRender = 15000;
      let toRender = filteredOutlets;
      if (showOnlyEquip) {{
        toRender = toRender.filter(o => o[13] && o[13].length > 0);
      }}
      if (showOnlyWithSales) {{
        toRender = toRender.filter(o => o[12] && o[12] > 0);
      }}
      toRender = toRender.slice(0, maxRender);

      toRender.forEach(o => {{
        const lat = o[0];
        const lng = o[1];
        if (!lat || !lng) return;

        const storeName = o[2];
        const storeCode = o[3];
        const nppCode = String(o[4]);
        const nppName = nppNameMap.get(nppCode) || ('NPP ' + nppCode);
        const address = o[9] || '';
        const dist = o[10];
        const ptype = o[11];
        const isRemote = dist >= 45;

        // Dữ liệu Doanh số & Thiết bị đầu tư T9/2026
        const salesMtd = o[12] || 0;
        const equip = o[13] || '';
        const vpo = o[14] || '';
        const action = o[15] || '';
        const salesRep = o[16] || '';
        const salesM1 = o[17] || 0;
        const route = o[18] || '';

        const hasEquip = equip && equip.length > 0;

        let color = '#f59e0b';
        if (ptype === 'DONG') color = '#0284c7';
        else if (ptype === 'BOTH') color = '#8b5cf6';
        if (isRemote) color = '#dc2626';

        // Điểm có tủ: bán kính 5, viền vàng kim (#eab308) nổi bật
        const circleMarker = L.circleMarker([lat, lng], {{
          radius: hasEquip ? 5 : (isRemote ? 4 : 3),
          fillColor: hasEquip ? '#0284c7' : color,
          color: hasEquip ? '#eab308' : '#ffffff',
          weight: hasEquip ? 2.2 : 0.8,
          opacity: 0.95,
          fillOpacity: 0.85
        }});

        circleMarker.bindPopup(`
          <div style="font-size:0.75rem; padding:4px 6px; min-width:260px; color:#0f172a;">
            <div style="font-weight:800; font-size:0.85rem; color:#0f172a; border-bottom:1px solid #cbd5e1; padding-bottom:4px; margin-bottom:5px; display:flex; justify-content:space-between; align-items:center;">
              <span>${{storeName}}</span>
              <span style="font-weight:600; color:#64748b; font-size:0.7rem;">#${{storeCode}}</span>
            </div>

            ${{hasEquip ? `
              <div style="margin-bottom:6px; padding:4px 7px; background:#eff6ff; border:1px solid #93c5fd; border-radius:5px; color:#1e40af; font-size:0.73rem; font-weight:700; display:flex; align-items:center; gap:5px;">
                <i class="fa-solid fa-snowflake" style="color:#0284c7;"></i>
                <span>Thiết bị: <b>${{equip}}</b></span>
              </div>
            ` : `
              <div style="margin-bottom:4px; font-size:0.7rem; color:#64748b;">
                <i class="fa-solid fa-box" style="color:#94a3b8;"></i> Thiết bị: <i>Chưa đầu tư tủ</i>
              </div>
            `}}

            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:5px; padding:4px 6px; margin-bottom:5px;">
              <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
                <span style="color:#64748b;">Doanh số T9 (MTD):</span>
                <b style="color:${{salesMtd > 0 ? '#10b981' : '#64748b'}};">${{salesMtd > 0 ? formatMoneyVND(salesMtd) : '0 đ (Chưa có đơn)'}}</b>
              </div>
              ${{salesM1 > 0 ? `
                <div style="display:flex; justify-content:space-between; font-size:0.68rem;">
                  <span style="color:#94a3b8;">Doanh số T8 (M-1):</span>
                  <span style="color:#475569; font-weight:600;">${{formatMoneyVND(salesM1)}}</span>
                </div>
              ` : ''}}
              ${{vpo ? `
                <div style="display:flex; justify-content:space-between; font-size:0.68rem; margin-top:2px; border-top:1px dashed #cbd5e1; padding-top:2px;">
                  <span style="color:#64748b;">Phân khúc VPO:</span>
                  <span style="color:#0f172a; font-weight:600;">${{vpo}} ${{action ? `<b style="margin-left:4px;">${{action}}</b>` : ''}}</span>
                </div>
              ` : ''}}
            </div>

            ${{salesRep ? `
              <div style="margin-bottom:3px; font-size:0.7rem;">
                <i class="fa-solid fa-user-tie" style="color:#64748b;"></i> NVBH: <b style="color:#0f172a;">${{salesRep}}</b>
                ${{route ? `<span style="color:#64748b; font-size:0.66rem;"> (${{route}})</span>` : ''}}
              </div>
            ` : ''}}

            <div style="margin-bottom:3px;">
              <span style="color:#64748b;">NPP Quản lý:</span> <b style="color:#0284c7;">${{nppName}}</b> <span style="color:#64748b; font-size:0.68rem;">(#${{nppCode}})</span>
            </div>

            <div style="margin-bottom:3px;">
              <span style="color:#64748b;">Khoảng cách đến NPP:</span> <b style="color:${{isRemote ? '#dc2626':'#059669'}};">${{dist}} km</b>
              ${{isRemote ? '<span style="color:#dc2626; font-size:0.65rem; font-weight:700; margin-left:3px;">(⚠️ Giao xa >45km)</span>' : ''}}
            </div>

            <div style="margin-bottom:3px;">
              <span style="color:#64748b;">Phân loại hàng:</span> <b>${{ptype === 'DONG' ? '❄️ Hàng Đông' : (ptype === 'BOTH' ? '❄️🌾 Cả 2' : '🌾 Hàng Khô')}}</b>
            </div>

            <div style="color:#475569; font-size:0.7rem; line-height:1.3; margin-top:3px; padding-top:3px; border-top:1px dashed #e2e8f0;">
              <i class="fa-solid fa-location-dot" style="color:#94a3b8;"></i> ${{address}}
            </div>
          </div>
        `);

        outletsLayer.addLayer(circleMarker);
      }});
    }}

    // Render Spider Lines
    function renderSpiderLines() {{
      spiderLayer.clearLayers();
      if (!showSpiderLines) return;

      const nppMap = new Map();
      ALL_NPPS.forEach(n => {{
        if (n.lat && n.lng) nppMap.set(String(n.code), [n.lat, n.lng]);
      }});

      filteredOutlets.slice(0, 1500).forEach(o => {{
        const nppPos = nppMap.get(String(o[4]));
        if (nppPos && o[0] && o[1]) {{
          const isRemote = o[10] >= 45;
          const polyline = L.polyline([nppPos, [o[0], o[1]]], {{
            color: isRemote ? '#ef4444' : '#8b5cf6',
            weight: isRemote ? 1.5 : 0.8,
            opacity: isRemote ? 0.8 : 0.4
          }});
          spiderLayer.addLayer(polyline);
        }}
      }});
    }}

    // Render Sidebar List
    function renderSidebarList() {{
      const container = document.getElementById('sidebarList');
      container.innerHTML = '';

      const toShow = filteredNPPs.slice(0, 150);
      toShow.forEach(n => {{
        const isActive = n.status.includes('Đang');
        const card = document.createElement('div');
        card.className = `npp-card ${{selectedNPP === n.code ? 'selected' : ''}}`;
        card.onclick = () => selectNPP(n.code, true);

        card.innerHTML = `
          <div class="npp-header-row">
            <span class="npp-code">${{n.code}}</span>
            <div style="display:flex; gap:4px; align-items:center;">
              <span class="badge-status ${{isActive ? 'badge-active' : 'badge-inactive'}}">${{n.status}}</span>
              ${{isActive ? `<span class="badge-status" style="background:${{n.is_khong_sm ? 'rgba(239,68,68,0.2)' : 'rgba(16,185,129,0.2)'}}; color:${{n.is_khong_sm ? '#fca5a5' : '#6ee7b7'}}; border:1px solid ${{n.is_khong_sm ? '#ef4444' : '#10b981'}};">${{n.is_khong_sm ? '⚠️ Không SM' : '👤 ' + n.so_nvbh_text}}</span>` : ''}}
            </div>
          </div>
          <div class="npp-title">${{n.name}}</div>
          <div class="npp-meta">
            <span class="npp-meta-item"><i class="fa-solid fa-city"></i> ${{n.province}}</span>
            <span class="npp-meta-item"><i class="fa-solid fa-store"></i> ${{n.outlet_count || 0}} KH</span>
            <span class="npp-meta-item"><i class="fa-solid fa-arrows-left-right"></i> Max: ${{n.max_dist || 0}}km</span>
            ${{n.remote_count > 0 ? `<span class="badge-remote-danger"><i class="fa-solid fa-triangle-exclamation"></i> ${{n.remote_count}} >45km</span>` : ''}}
          </div>

          <!-- KHỐI DOANH SỐ T9/2026 KÈM 3 NHÓM SP (AMBIENT / CHILLED / FROZEN) -->
          ${{n.sales_total ? `
            <div style="background:rgba(15,23,42,0.9); border:1px solid rgba(16,185,129,0.35); border-radius:6px; padding:6px 8px; margin-top:6px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="color:#6ee7b7; font-weight:800; font-size:0.7rem;">
                  <i class="fa-solid fa-chart-line" style="color:#10b981;"></i> Doanh số T9:
                </span>
                <b style="color:#10b981; font-size:0.82rem; font-weight:800;">
                  ${{formatMoneyVND(n.sales_total)}}
                </b>
              </div>
              <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; text-align:center; font-size:0.65rem;">
                <div style="background:#1e293b; padding:3px 2px; border-radius:4px; border-left:2px solid #f59e0b;">
                  <div style="color:#94a3b8; font-size:0.62rem;">Ambient</div>
                  <b style="color:#fbbf24;">${{formatMoneyShort(n.sales_ambient || 0)}}</b>
                </div>
                <div style="background:#1e293b; padding:3px 2px; border-radius:4px; border-left:2px solid #10b981;">
                  <div style="color:#94a3b8; font-size:0.62rem;">Chilled</div>
                  <b style="color:#34d399;">${{formatMoneyShort(n.sales_chilled || 0)}}</b>
                </div>
                <div style="background:#1e293b; padding:3px 2px; border-radius:4px; border-left:2px solid #38bdf8;">
                  <div style="color:#94a3b8; font-size:0.62rem;">Frozen</div>
                  <b style="color:#38bdf8;">${{formatMoneyShort(n.sales_frozen || 0)}}</b>
                </div>
              </div>
            </div>
          ` : `
            <div style="font-size:0.65rem; color:#64748b; margin-top:4px;">
              <i class="fa-solid fa-circle-info"></i> Doanh số T9: <i>Chưa có dữ liệu</i>
            </div>
          `}}

          <div style="margin-top:6px; display:flex; gap:5px;">
            <button class="btn-nav" style="padding:2px 6px; font-size:0.65rem; background:#2563eb; color:white; border:none; border-radius:4px;" onclick="event.stopPropagation(); focusNPPAndSpider('${{n.code}}')">
              <i class="fa-solid fa-share-nodes"></i> Tia Nối
            </button>
            <button class="btn-nav" style="padding:2px 6px; font-size:0.65rem; background:#d97706; color:white; border:none; border-radius:4px;" onclick="event.stopPropagation(); showNPPOutlets('${{n.code}}')">
              <i class="fa-solid fa-store"></i> Hiện Điểm Bán (${{n.outlet_count || 0}})
            </button>
          </div>
        `;
        container.appendChild(card);
      }});

      if (filteredNPPs.length > 150) {{
        const moreNotice = document.createElement('div');
        moreNotice.style.textAlign = 'center';
        moreNotice.style.padding = '8px';
        moreNotice.style.fontSize = '0.7rem';
        moreNotice.style.color = '#94a3b8';
        moreNotice.textContent = `Và ${{filteredNPPs.length - 150}} NPP khác... (Dùng ô tìm kiếm để lọc)`;
        container.appendChild(moreNotice);
      }}
    }}

    function selectNPP(code, zoom = false) {{
      selectedNPP = code;
      const npp = ALL_NPPS.find(n => n.code === code);
      if (npp && zoom && npp.lat && npp.lng) {{
        map.setView([npp.lat, npp.lng], 11);
      }}
      document.querySelectorAll('.npp-card').forEach(el => {{
        el.classList.toggle('selected', el.querySelector('.npp-code').textContent === code);
      }});
      if (window.innerWidth <= 768 && zoom) {{
        toggleMobileSidebar(false);
      }}
    }}

    function zoomToNPP(code) {{
      const npp = ALL_NPPS.find(n => n.code === code);
      if (npp && npp.lat && npp.lng) {{
        map.setView([npp.lat, npp.lng], 12);
      }}
      if (window.innerWidth <= 768) {{
        toggleMobileSidebar(false);
      }}
    }}

    function focusNPPAndSpider(code) {{
      const npp = ALL_NPPS.find(n => n.code === code);
      if (!npp || !npp.lat || !npp.lng) return;

      map.setView([npp.lat, npp.lng], 11);
      spiderLayer.clearLayers();

      const nppPos = [npp.lat, npp.lng];
      const outletsOfNpp = ALL_OUTLETS.filter(o => String(o[4]) === String(code));

      outletsOfNpp.forEach(o => {{
        if (o[0] && o[1]) {{
          const isRemote = o[10] >= 45;
          const polyline = L.polyline([nppPos, [o[0], o[1]]], {{
            color: isRemote ? '#ef4444' : '#8b5cf6',
            weight: isRemote ? 2 : 1,
            opacity: 0.8
          }});
          spiderLayer.addLayer(polyline);
        }}
      }});
    }}

    // NÚT HIỆN TOÀN BỘ ĐIỂM BÁN CỦA MỘT NPP
    function showNPPOutlets(nppCode) {{
      // 1. Đảm bảo bật layer Outlets
      showOutlets = true;
      const chk = document.getElementById('chkToggleOutlet');
      if (chk) chk.checked = true;
      const lbl = document.getElementById('lblChkOutlet');
      if (lbl) lbl.classList.add('active-outlet');
      const quickBtn = document.getElementById('btnQuickToggleOutlet');
      if (quickBtn) quickBtn.classList.add('active-quick-outlet');
      const quickText = document.getElementById('btnQuickOutletText');
      if (quickText) quickText.textContent = 'Ẩn Điểm Bán';
      if (!map.hasLayer(outletsLayer)) outletsLayer.addTo(map);

      // 2. Điền mã NPP vào ô tìm kiếm để chỉ hiển thị NPP và Điểm bán của NPP đó
      const searchInput = document.getElementById('filterSearch');
      if (searchInput) searchInput.value = nppCode;
      applyFilters();

      // 3. Vẽ tia nối liên kết
      focusNPPAndSpider(nppCode);

      // 4. Zoom vừa vặn bao quát NPP và tất cả outlets trực thuộc
      const npp = ALL_NPPS.find(n => String(n.code) === String(nppCode));
      const outlets = ALL_OUTLETS.filter(o => String(o[4]) === String(nppCode));
      const latlngs = [];
      if (npp && npp.lat && npp.lng) latlngs.push([npp.lat, npp.lng]);
      outlets.forEach(o => {{
        if (o[0] && o[1]) latlngs.push([o[0], o[1]]);
      }});
      if (latlngs.length > 0) {{
        map.fitBounds(latlngs, {{ padding: [50, 50], maxZoom: 13 }});
      }}

      // 5. Hiển thị banner thông báo nổi
      const banner = document.getElementById('nppOutletBanner');
      const bannerText = document.getElementById('nppOutletBannerText');
      if (banner && bannerText) {{
        const nppName = npp ? npp.name : nppCode;
        bannerText.innerHTML = `Đang xem <b>${{outlets.length}} Điểm bán</b> của NPP <b>${{nppCode}}</b> (${{nppName}})`;
        banner.style.display = 'flex';
      }}

      if (window.innerWidth <= 768) {{
        toggleMobileSidebar(false);
      }}
    }}

    function resetOutletView() {{
      const banner = document.getElementById('nppOutletBanner');
      if (banner) banner.style.display = 'none';

      const searchInput = document.getElementById('filterSearch');
      if (searchInput) searchInput.value = '';
      spiderLayer.clearLayers();
      applyFilters();
      zoomToPreset('ALL');
    }}

    function showNPPOutletsFromModal(nppCode) {{
      closeAnalyticsModal();
      showNPPOutlets(nppCode);
    }}

    function toggleRadius() {{
      const btn = document.getElementById('btnToggleRadius');
      showRadius = !showRadius;
      btn.classList.toggle('active', showRadius);
      if (showRadius) radiusLayer.addTo(map);
      else map.removeLayer(radiusLayer);
    }}

    function zoomToPreset(preset) {{
      if (preset === 'ALL') {{
        map.setView([14.0583, 108.2772], window.innerWidth <= 768 ? 5 : 6);
      }} else if (preset === 'MB') {{
        map.setView([21.0285, 105.8542], 7);
      }} else if (preset === 'MN') {{
        map.setView([10.8231, 106.6297], 7);
      }}
    }}

    function toggleMobileSidebar(open) {{
      const sidebar = document.getElementById('sidebar');
      if (open) {{
        sidebar.classList.add('open');
      }} else {{
        sidebar.classList.remove('open');
      }}
    }}

    function exportFilteredCSV() {{
      let csv = 'Mã NPP,Tên NPP,Trạng thái,Miền,Vùng,Tỉnh/Thành,Địa chỉ,Lat,Lng,Tổng KH,Cự ly Max (km),KH >45km,KH Hàng Đông\\n';
      filteredNPPs.forEach(n => {{
        csv += `"${{n.code}}","${{n.name}}","${{n.status}}","${{n.region}}","${{n.area}}","${{n.province}}","${{n.address || ''}}",${{n.lat}},${{n.lng}},${{n.outlet_count||0}},${{n.max_dist||0}},${{n.remote_count||0}},${{n.dong_count||0}}\\n`;
      }});
      const blob = new Blob(["\\uFEFF" + csv], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `RTM_NPP_Spatial_Export_${{new Date().toISOString().slice(0,10)}}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }}

    // =========================================================================
    // ANALYTICS MODAL FUNCTIONS (BÁO CÁO CỰ LY & ĐỀ XUẤT TRẠM TRUNG CHUYỂN)
    // =========================================================================
    function populateModalVungOptions() {{
      const mienVal = document.getElementById('modalFilterMien') ? document.getElementById('modalFilterMien').value : 'ALL';
      const vungSelect = document.getElementById('modalFilterVung');
      if (!vungSelect) return;

      const currentVal = vungSelect.value;
      vungSelect.innerHTML = '<option value="ALL">Tất cả Vùng (6 Vùng)</option>';

      const areas = ['Cần Thơ', 'HCM', 'Nha Trang', 'Hà Nội', 'Hải Phòng', 'Đà Nẵng'];
      areas.forEach(a => {{
        const sample = NPP_ANALYTICS.find(d => d.area === a);
        if (sample && (mienVal === 'ALL' || sample.region === mienVal)) {{
          const count = NPP_ANALYTICS.filter(d => (mienVal === 'ALL' || d.region === mienVal) && d.area === a).length;
          const opt = document.createElement('option');
          opt.value = a;
          opt.textContent = `${{a}} (${{count}} NPP)`;
          vungSelect.appendChild(opt);
        }}
      }});

      if (currentVal && Array.from(vungSelect.options).some(o => o.value === currentVal)) {{
        vungSelect.value = currentVal;
      }} else {{
        vungSelect.value = 'ALL';
      }}
    }}

    function onModalMienChange() {{
      populateModalVungOptions();
      filterAnalyticsTable();
    }}

    function switchModalTab(tab) {{
      const btnStrategic = document.getElementById('tabBtnStrategic');
      const btnDetails = document.getElementById('tabBtnDetails');
      const contentStrategic = document.getElementById('tabContentStrategic');
      const contentDetails = document.getElementById('tabContentDetails');

      if (tab === 'strategic') {{
        if (btnStrategic) btnStrategic.classList.add('active');
        if (btnDetails) btnDetails.classList.remove('active');
        if (contentStrategic) contentStrategic.style.display = 'flex';
        if (contentDetails) contentDetails.style.display = 'none';
      }} else {{
        if (btnStrategic) btnStrategic.classList.remove('active');
        if (btnDetails) btnDetails.classList.add('active');
        if (contentStrategic) contentStrategic.style.display = 'none';
        if (contentDetails) contentDetails.style.display = 'flex';
        filterAnalyticsTable();
      }}
    }}

    function openStrategicModal() {{
      document.getElementById('analyticsModal').classList.add('open');
      switchModalTab('strategic');
    }}

    function filterByRegionFromStrategic(areaName) {{
      const modalVung = document.getElementById('modalFilterVung');
      if (modalVung) modalVung.value = areaName;

      const mainVung = document.getElementById('filterVung');
      if (mainVung) {{
        mainVung.value = areaName;
        onVungChange();
      }}

      switchModalTab('details');
    }}

    function viewRegionOnMap(areaName) {{
      closeAnalyticsModal();
      const mainVung = document.getElementById('filterVung');
      if (mainVung) {{
        mainVung.value = areaName;
        onVungChange();
      }}
    }}

    function openAnalyticsModal() {{
      // Đồng bộ theo bộ lọc Miền & Vùng hiện tại trên thanh công cụ bản đồ
      const mainMien = document.getElementById('filterMien') ? document.getElementById('filterMien').value : 'ALL';
      const mainVung = document.getElementById('filterVung') ? document.getElementById('filterVung').value : 'ALL';

      const modalMien = document.getElementById('modalFilterMien');
      if (modalMien && mainMien) modalMien.value = mainMien;

      populateModalVungOptions();

      const modalVung = document.getElementById('modalFilterVung');
      if (modalVung && mainVung && mainVung !== 'ALL') {{
        modalVung.value = mainVung;
      }}

      document.getElementById('analyticsModal').classList.add('open');
      switchModalTab('details');
    }}

    function closeAnalyticsModal() {{
      document.getElementById('analyticsModal').classList.remove('open');
    }}

    function updateModalKPIs(list) {{
      let totalOutlets = 0;
      let weightedDistSum = 0;
      let totalRemote = 0;

      list.forEach(d => {{
        const outCnt = (d.total_outlets || 0);
        totalOutlets += outCnt;
        weightedDistSum += (d.avg_dist || 0) * outCnt;
        totalRemote += (d.remote_outlets_45km || 0);
      }});

      const avgDist = totalOutlets > 0 ? (weightedDistSum / totalOutlets).toFixed(1) : '0.0';
      const remotePct = totalOutlets > 0 ? (totalRemote / totalOutlets * 100).toFixed(1) : 0;

      let estimatedColdRemote = 0;
      let estimatedDryRemote = 0;
      list.forEach(d => {{
        if (d.remote_outlets_45km > 0) {{
          const coldRem = Math.round(d.remote_outlets_45km * (d.cold_pct / 100));
          estimatedColdRemote += coldRem;
          estimatedDryRemote += (d.remote_outlets_45km - coldRem);
        }}
      }});

      const kpiAvg = document.getElementById('modalKpiAvgDist');
      if (kpiAvg) kpiAvg.innerHTML = `${{avgDist}} <span style="font-size:0.85rem; font-weight:600; color:#94a3b8;">km</span>`;

      const kpiRemote = document.getElementById('modalKpiRemote');
      if (kpiRemote) kpiRemote.innerHTML = `${{totalRemote.toLocaleString('vi-VN')}} <span style="font-size:0.85rem; font-weight:600; color:#94a3b8;">điểm (${{remotePct}}%)</span>`;

      const kpiCold = document.getElementById('modalKpiCold');
      if (kpiCold) kpiCold.innerHTML = `${{estimatedColdRemote.toLocaleString('vi-VN')}} <span style="font-size:0.85rem; font-weight:600; color:#94a3b8;">điểm</span>`;

      const kpiDry = document.getElementById('modalKpiDry');
      if (kpiDry) kpiDry.innerHTML = `${{estimatedDryRemote.toLocaleString('vi-VN')}} <span style="font-size:0.85rem; font-weight:600; color:#94a3b8;">điểm</span>`;
    }}

    function filterAnalyticsTable() {{
      if (!NPP_ANALYTICS || NPP_ANALYTICS.length === 0) return;

      const mienFilter = document.getElementById('modalFilterMien') ? document.getElementById('modalFilterMien').value : 'ALL';
      const vungFilter = document.getElementById('modalFilterVung') ? document.getElementById('modalFilterVung').value : 'ALL';
      const statusFilter = document.getElementById('modalFilterStatus').value;
      const sortCriteria = document.getElementById('modalSortCriteria').value;
      const searchVal = document.getElementById('modalSearch').value.toLowerCase().trim();

      let list = [...NPP_ANALYTICS];

      // 1. Lọc theo Miền
      if (mienFilter !== 'ALL') {{
        list = list.filter(d => d.region === mienFilter);
      }}

      // 2. Lọc theo Vùng (Area)
      if (vungFilter !== 'ALL') {{
        list = list.filter(d => d.area === vungFilter);
      }}

      // 3. Lọc theo Trạng thái
      if (statusFilter === 'ACTIVE') {{
        list = list.filter(d => d.is_active);
      }} else if (statusFilter === 'REMOTE_ONLY') {{
        list = list.filter(d => d.remote_outlets_45km > 0);
      }}

      // 4. Tìm kiếm từ khóa
      if (searchVal) {{
        list = list.filter(d => 
          d.npp_name.toLowerCase().includes(searchVal) ||
          d.npp_code.toLowerCase().includes(searchVal) ||
          d.province.toLowerCase().includes(searchVal) ||
          (d.area && d.area.toLowerCase().includes(searchVal)) ||
          (d.farthest_outlet && d.farthest_outlet.name.toLowerCase().includes(searchVal))
        );
      }}

      // 5. Sắp xếp
      if (sortCriteria === 'MAX_DIST') {{
        list.sort((a, b) => b.max_dist - a.max_dist);
      }} else if (sortCriteria === 'AVG_DIST') {{
        list.sort((a, b) => b.avg_dist - a.avg_dist);
      }} else if (sortCriteria === 'REMOTE_COUNT') {{
        list.sort((a, b) => b.remote_outlets_45km - a.remote_outlets_45km);
      }} else if (sortCriteria === 'TOTAL_OUTLETS') {{
        list.sort((a, b) => b.total_outlets - a.total_outlets);
      }}

      document.getElementById('modalTableCount').textContent = list.length;
      updateModalKPIs(list);
      renderAnalyticsTable(list);
    }}

    function renderAnalyticsTable(list) {{
      const tbody = document.getElementById('analyticsTableBody');
      tbody.innerHTML = '';

      if (list.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding:20px; color:#94a3b8;">Không tìm thấy NPP nào phù hợp điều kiện lọc vùng / trạng thái này.</td></tr>';
        return;
      }}

      list.forEach(item => {{
        const tr = document.createElement('tr');
        const fo = item.farthest_outlet;
        const hasRemote = item.remote_outlets_45km > 0;
        const remotePct = item.total_outlets > 0 ? (item.remote_outlets_45km / item.total_outlets * 100).toFixed(1) : 0;
        
        let hubTag = '<span class="tag-hub-ok"><i class="fa-solid fa-check"></i> Ổn định (<45km)</span>';
        if (hasRemote) {{
          if (item.cold_pct >= 25) {{
            hubTag = '<span class="tag-hub-cold"><i class="fa-solid fa-snowflake"></i> Cần Hub ĐÔNG LẠNH</span>';
          }} else {{
            hubTag = '<span class="tag-hub-dry"><i class="fa-solid fa-box-open"></i> Cần Hub HÀNG KHÔ</span>';
          }}
        }}

        tr.innerHTML = `
          <td>
            <b style="color:#60a5fa;">${{item.npp_code}}</b><br>
            <span style="font-weight:700; color:#f1f5f9;">${{item.npp_name}}</span>
          </td>
          <td>
            <span class="badge-status ${{item.is_active ? 'badge-active' : 'badge-inactive'}}">${{item.status}}</span>
          </td>
          <td>
            <b style="color:#e2e8f0;">${{item.province}}</b><br>
            <span style="color:#60a5fa; font-weight:700; font-size:0.68rem;"><i class="fa-solid fa-network-wired"></i> ${{item.area || item.region}}</span>
          </td>
          <td>
            <b style="color:#f1f5f9;">${{item.total_outlets.toLocaleString('vi-VN')}}</b> KH<br>
            <span style="color:#38bdf8; font-size:0.65rem;">❄️ ${{item.cold_pct}}% Đông</span>
          </td>
          <td>
            <b style="color:${{item.avg_dist > 30 ? '#f87171' : '#34d399'}};">${{item.avg_dist}} km</b>
          </td>
          <td>
            <b style="color:${{item.max_dist > 45 ? '#ef4444' : '#f59e0b'}};">${{item.max_dist}} km</b>
          </td>
          <td>
            ${{fo ? `
              <b style="color:#f1f5f9;">${{fo.name}}</b> (<span style="color:#ef4444; font-weight:700;">${{fo.dist}} km</span>)<br>
              <span style="color:#94a3b8; font-size:0.65rem;">Loại hàng: <b>${{fo.ptype === 'DONG' ? '❄️ Hàng Đông' : (fo.ptype === 'BOTH' ? '❄️🌾 Cả 2' : '🌾 Hàng Khô')}}</b> | ${{fo.addr || ''}}</span>
            ` : '<span style="color:#64748b;">Chưa có điểm bán</span>'}}
          </td>
          <td>
            ${{hasRemote ? `<b style="color:#ef4444;">${{item.remote_outlets_45km}} KH</b> (${{remotePct}}%)` : '<span style="color:#10b981;">0 KH</span>'}}
          </td>
          <td>${{hubTag}}</td>
          <td>
            <div style="display:flex; gap:4px; flex-wrap:nowrap;">
              <button class="btn-nav" style="padding:4px 7px; font-size:0.65rem; background:#2563eb; color:white; border:none;" onclick="zoomToNPPAndFarthest('${{item.npp_code}}')" title="Xem vị trí NPP và khách xa nhất">
                <i class="fa-solid fa-crosshairs"></i> Xem
              </button>
              <button class="btn-nav" style="padding:4px 7px; font-size:0.65rem; background:#d97706; color:white; border:none;" onclick="showNPPOutletsFromModal('${{item.npp_code}}')" title="Hiện toàn bộ điểm bán của NPP này">
                <i class="fa-solid fa-store"></i> Hiện Outlet
              </button>
            </div>
          </td>
        `;

        tbody.appendChild(tr);
      }});
    }}

    function zoomToNPPAndFarthest(code) {{
      closeAnalyticsModal();
      focusNPPAndSpider(code);
    }}
  
    // ==========================================
    // PLANNED NPP FLAGS ENGINE (CẮM CỜ DỰ KIẾN MỞ)
    // ==========================================
    let plannedFlags = [];
    let isPinMode = false;
    let pendingFlagCoords = null;
    let isWidgetCollapsed = false;

    const plannedFlagsLayer = L.layerGroup().addTo(map);

    // Bật / Tắt chế độ cắm cờ
    function togglePinMode(forceState) {{
      if (typeof forceState === 'boolean') {{
        isPinMode = forceState;
      }} else {{
        isPinMode = !isPinMode;
      }}

      const btn = document.getElementById('btnTogglePinMode');
      const text = document.getElementById('btnPinText');
      const banner = document.getElementById('pinModeBanner');

      if (isPinMode) {{
        document.body.classList.add('pin-mode-active');
        if (btn) {{
          btn.style.background = 'rgba(245, 158, 11, 0.4)';
          btn.style.borderColor = '#fbbf24';
          btn.style.boxShadow = '0 0 12px rgba(245, 158, 11, 0.5)';
        }}
        if (text) text.textContent = 'Đang Cắm Cờ...';
        if (banner) banner.style.display = 'flex';
      }} else {{
        document.body.classList.remove('pin-mode-active');
        if (btn) {{
          btn.style.background = 'rgba(245, 158, 11, 0.15)';
          btn.style.borderColor = '#f59e0b';
          btn.style.boxShadow = 'none';
        }}
        if (text) text.textContent = 'Cắm Cờ Mở NPP';
        if (banner) banner.style.display = 'none';
      }}
    }}

    function enablePinModeFromWidget() {{
      togglePinMode(true);
    }}

    // Lắng nghe click trên map để cắm cờ
    map.on('click', function(e) {{
      if (!isPinMode) return;
      openAddFlagModal(e.latlng.lat, e.latlng.lng);
    }});

    function openAddFlagModal(lat, lng, defName, defType, defRadius, defNote) {{
      pendingFlagCoords = {{ lat: lat, lng: lng }};
      document.getElementById('flagCoordsDisplay').textContent = `${{lat.toFixed(5)}}, ${{lng.toFixed(5)}}`;
      document.getElementById('flagInputName').value = defName || `NPP Mới (${{lat.toFixed(3)}}, ${{lng.toFixed(3)}})`;
      document.getElementById('flagInputType').value = defType || 'C1 Partner';
      document.getElementById('flagInputRadius').value = defRadius || '25';
      document.getElementById('flagInputNote').value = defNote || '';

      document.getElementById('modalAddFlag').style.display = 'flex';
      setTimeout(() => {{
        document.getElementById('flagInputName').focus();
        document.getElementById('flagInputName').select();
      }}, 100);
    }}

    function closeAddFlagModal() {{
      document.getElementById('modalAddFlag').style.display = 'none';
      pendingFlagCoords = null;
    }}

    function confirmAddFlag() {{
      if (!pendingFlagCoords) return;
      const name = document.getElementById('flagInputName').value.trim() || 'NPP Dự Kiến Mới';
      const type = document.getElementById('flagInputType').value;
      const radiusKm = parseFloat(document.getElementById('flagInputRadius').value) || 25;
      const note = document.getElementById('flagInputNote').value.trim();

      addPlannedFlag({{
        id: 'flag_' + Date.now() + '_' + Math.floor(Math.random()*1000),
        name: name,
        type: type,
        lat: pendingFlagCoords.lat,
        lng: pendingFlagCoords.lng,
        radiusKm: radiusKm,
        note: note
      }}, true, true);

      closeAddFlagModal();
    }}

    // Hàm tạo và hiển thị cờ trên bản đồ
    function addPlannedFlag(flagData, autoOpen, shouldSave) {{
      // 1. Phân tích không gian: Tìm NPP active gần nhất
      let closestNPP = null;
      let minDistanceKm = 99999;
      ALL_NPPS.filter(n => n.status === 'Đang Sử Dụng').forEach(n => {{
        const d = map.distance([flagData.lat, flagData.lng], [n.lat, n.lng]) / 1000;
        if (d < minDistanceKm) {{
          minDistanceKm = d;
          closestNPP = n;
        }}
      }});

      // 2. Đếm số outlet hiện hữu nằm trong bán kính
      let coveredOutlets = 0;
      let coldOutlets = 0;
      if (ALL_OUTLETS && ALL_OUTLETS.length > 0) {{
        const radMeters = flagData.radiusKm * 1000;
        for (let i = 0; i < ALL_OUTLETS.length; i++) {{
          const o = ALL_OUTLETS[i];
          const dist = map.distance([flagData.lat, flagData.lng], [o[0], o[1]]);
          if (dist <= radMeters) {{
            coveredOutlets++;
            if (o[11] === 'DONG' || o[11] === 'BOTH') coldOutlets++;
          }}
        }}
      }}

      flagData.closestNPP = closestNPP;
      flagData.minDistanceKm = minDistanceKm.toFixed(1);
      flagData.coveredOutlets = coveredOutlets;
      flagData.coldOutlets = coldOutlets;

      // 3. Tạo DivIcon cờ siêu nổi bật với radar phát sóng
      const flagIcon = L.divIcon({{
        className: 'custom-planned-flag-wrapper',
        html: `
          <div class="planned-flag-container">
            <div class="planned-flag-pulse"></div>
            <i class="fa-solid fa-flag planned-flag-icon"></i>
            <div class="planned-flag-label">🚩 ${{flagData.name}}</div>
          </div>
        `,
        iconSize: [46, 52],
        iconAnchor: [23, 50],
        popupAnchor: [0, -48]
      }});

      const marker = L.marker([flagData.lat, flagData.lng], {{ icon: flagIcon, zIndexOffset: 3000 }});

      // 4. Vòng tròn bán kính phục vụ dự kiến (Dashed Gold)
      const circle = L.circle([flagData.lat, flagData.lng], {{
        radius: flagData.radiusKm * 1000,
        color: '#f59e0b',
        weight: 2,
        dashArray: '6, 6',
        fillColor: '#f59e0b',
        fillOpacity: 0.12,
        interactive: false
      }});

      // 5. Popup hiển thị đầy đủ thông số
      const popupHtml = `
        <div class="popup-card" style="border-top: 3px solid #f59e0b; width: 300px;">
          <div class="popup-header">
            <span class="popup-tag" style="background:#fef3c7; color:#92400e; font-weight:800;">🚩 NPP / C1 DỰ KIẾN MỞ 2027</span>
            <div class="popup-title" style="font-size:0.9rem; color:#fef08a;">${{flagData.name}}</div>
            <div style="font-size:0.68rem; color:#94a3b8; margin-top:2px;">Mô hình: <b style="color:#38bdf8;">${{flagData.type}}</b></div>
          </div>
          <div class="popup-body">
            <div class="popup-row">
              <i class="fa-solid fa-circle-notch" style="color:#f59e0b;"></i>
              <div>Bán kính phục vụ: <b style="color:#f1f5f9;">${{flagData.radiusKm}} km</b></div>
            </div>
            <div class="popup-row">
              <i class="fa-solid fa-store" style="color:#34d399;"></i>
              <div>Điểm bán CJ trong vùng: <b style="color:#34d399;">${{flagData.coveredOutlets}} điểm</b> (${{flagData.coldOutlets}} điểm đông lạnh)</div>
            </div>
            <div class="popup-row">
              <i class="fa-solid fa-route" style="color:#60a5fa;"></i>
              <div>NPP Active gần nhất: <b style="color:#e2e8f0;">${{closestNPP ? closestNPP.short_name : 'Không'}}</b> (<span style="color:#f87171; font-weight:800;">${{flagData.minDistanceKm}} km</span>)</div>
            </div>
            ${{flagData.note ? `
            <div style="background:#1e293b; border-left:2px solid #f59e0b; padding:4px 6px; border-radius:3px; margin-top:4px; font-size:0.68rem; color:#cbd5e1;">
              <b>Mục tiêu:</b> ${{flagData.note}}
            </div>` : ''}}
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; padding-top:6px; border-top:1px solid #334155;">
            <button onclick="changeFlagRadius('${{flagData.id}}')" style="background:#0284c7; color:#fff; border:none; padding:3px 8px; border-radius:4px; font-size:0.65rem; font-weight:700; cursor:pointer;">
              <i class="fa-solid fa-arrows-up-down-left-right"></i> Đổi bán kính
            </button>
            <button onclick="removePlannedFlag('${{flagData.id}}')" style="background:#dc2626; color:#fff; border:none; padding:3px 8px; border-radius:4px; font-size:0.65rem; font-weight:700; cursor:pointer;">
              <i class="fa-solid fa-trash-can"></i> Xóa cờ
            </button>
          </div>
        </div>
      `;

      marker.bindPopup(popupHtml, {{ maxWidth: 320 }});

      // Lưu tham chiếu marker & circle
      flagData.marker = marker;
      flagData.circle = circle;

      plannedFlagsLayer.addLayer(circle);
      plannedFlagsLayer.addLayer(marker);

      plannedFlags.push(flagData);

      if (autoOpen) {{
        marker.openPopup();
      }}

      if (shouldSave) {{
        savePlannedFlagsToStorage();
      }}

      updatePlannedFlagsUI();
    }}

    // Đổi bán kính phục vụ của cờ
    function changeFlagRadius(flagId) {{
      const flag = plannedFlags.find(f => f.id === flagId);
      if (!flag) return;
      const current = flag.radiusKm;
      const nextRadii = [15, 25, 35, 45];
      const idx = nextRadii.indexOf(current);
      const nextR = nextRadii[(idx + 1) % nextRadii.length];

      flag.radiusKm = nextR;
      flag.circle.setRadius(nextR * 1000);

      // Recalculate outlets count
      let coveredOutlets = 0;
      let coldOutlets = 0;
      if (ALL_OUTLETS && ALL_OUTLETS.length > 0) {{
        const radMeters = nextR * 1000;
        for (let i = 0; i < ALL_OUTLETS.length; i++) {{
          const o = ALL_OUTLETS[i];
          const dist = map.distance([flag.lat, flag.lng], [o[0], o[1]]);
          if (dist <= radMeters) {{
            coveredOutlets++;
            if (o[11] === 'DONG' || o[11] === 'BOTH') coldOutlets++;
          }}
        }}
      }}
      flag.coveredOutlets = coveredOutlets;
      flag.coldOutlets = coldOutlets;

      // Re-bind popup
      removePlannedFlag(flagId, false);
      addPlannedFlag(flag, true, true);
    }}

    // Xóa 1 cờ
    function removePlannedFlag(flagId, shouldSave = true) {{
      const idx = plannedFlags.findIndex(f => f.id === flagId);
      if (idx !== -1) {{
        const flag = plannedFlags[idx];
        if (flag.marker) plannedFlagsLayer.removeLayer(flag.marker);
        if (flag.circle) plannedFlagsLayer.removeLayer(flag.circle);
        plannedFlags.splice(idx, 1);
        if (shouldSave) savePlannedFlagsToStorage();
        updatePlannedFlagsUI();
      }}
    }}

    // Xóa tất cả cờ
    function clearAllPlannedFlags() {{
      if (plannedFlags.length === 0) return;
      if (confirm('Bạn có chắc chắn muốn xóa tất cả các cờ NPP dự kiến trên bản đồ?')) {{
        plannedFlags.forEach(f => {{
          if (f.marker) plannedFlagsLayer.removeLayer(f.marker);
          if (f.circle) plannedFlagsLayer.removeLayer(f.circle);
        }});
        plannedFlags = [];
        savePlannedFlagsToStorage();
        updatePlannedFlagsUI();
      }}
    }}

    // Bay tới vị trí cờ
    function flyToPlannedFlag(flagId) {{
      const flag = plannedFlags.find(f => f.id === flagId);
      if (flag && flag.marker) {{
        map.flyTo([flag.lat, flag.lng], 12, {{ animate: true, duration: 1.2 }});
        setTimeout(() => {{
          flag.marker.openPopup();
        }}, 1200);
      }}
    }}

    // Cập nhật giao diện Widget
    function updatePlannedFlagsUI() {{
      const widget = document.getElementById('plannedFlagsWidget');
      const countEl = document.getElementById('flagWidgetCount');
      const listEl = document.getElementById('plannedFlagsList');

      if (!widget || !countEl || !listEl) return;

      countEl.textContent = plannedFlags.length;

      if (plannedFlags.length === 0) {{
        widget.style.display = 'none';
        listEl.innerHTML = '';
        return;
      }}

      widget.style.display = 'flex';
      listEl.innerHTML = '';

      plannedFlags.forEach(f => {{
        const div = document.createElement('div');
        div.className = 'flag-list-item';
        div.innerHTML = `
          <div class="flag-item-info" onclick="flyToPlannedFlag('${{f.id}}')" title="Nhấp để xem trên bản đồ">
            <span class="flag-item-title">🚩 ${{f.name}}</span>
            <span class="flag-item-sub">Bán kính: <b style="color:#e2e8f0;">${{f.radiusKm}}km</b> | Phủ: <b style="color:#34d399;">${{f.coveredOutlets}} KH</b></span>
          </div>
          <div class="flag-item-actions">
            <button class="flag-btn-icon" onclick="flyToPlannedFlag('${{f.id}}')" title="Xem trên bản đồ"><i class="fa-solid fa-crosshairs"></i></button>
            <button class="flag-btn-icon" onclick="removePlannedFlag('${{f.id}}')" title="Xóa cờ này"><i class="fa-solid fa-xmark"></i></button>
          </div>
        `;
        listEl.appendChild(div);
      }});
    }}

    function toggleFlagsWidgetCollapse() {{
      const body = document.getElementById('plannedWidgetBody');
      const chev = document.getElementById('widgetChevron');
      if (!body) return;
      isWidgetCollapsed = !isWidgetCollapsed;
      if (isWidgetCollapsed) {{
        body.style.display = 'none';
        if (chev) chev.style.transform = 'rotate(-90deg)';
      }} else {{
        body.style.display = 'flex';
        if (chev) chev.style.transform = 'rotate(0deg)';
      }}
    }}

    // Lưu vào LocalStorage
    function savePlannedFlagsToStorage() {{
      try {{
        const dataToSave = plannedFlags.map(f => ({{
          id: f.id,
          name: f.name,
          type: f.type,
          lat: f.lat,
          lng: f.lng,
          radiusKm: f.radiusKm,
          note: f.note
        }}));
        localStorage.setItem('RTM_PLANNED_FLAGS_2027', JSON.stringify(dataToSave));
      }} catch (e) {{
        console.warn('Cannot save planned flags to storage:', e);
      }}
    }}

    // Nạp lại từ LocalStorage khi khởi động
    function loadPlannedFlagsFromStorage() {{
      try {{
        const saved = localStorage.getItem('RTM_PLANNED_FLAGS_2027');
        if (saved) {{
          const list = JSON.parse(saved);
          if (Array.isArray(list) && list.length > 0) {{
            list.forEach(f => addPlannedFlag(f, false, false));
          }}
        }}
      }} catch (e) {{
        console.warn('Cannot load planned flags from storage:', e);
      }}
    }}

    // Nạp nhanh 4 Vùng Trắng Trọng Điểm Mekong (Cai Lậy, Đức Hòa, Trà Vinh, Ba Tri)
    function loadMekongPresets() {{
      const mekongPresets = [
        {{
          id: 'preset_cailay',
          name: 'C1 TT. Cai Lậy (Tiền Giang)',
          type: 'C1 Partner',
          lat: 10.4087,
          lng: 106.1158,
          radiusKm: 25,
          note: 'Cắt giảm 60km từ TP. Mỹ Tho sang Cái Bè/Cai Lậy. Tiếp quản 50 Golden Outlets + 233 tiệm Nhóm C.'
        }},
        {{
          id: 'preset_duchoa',
          name: 'C1 TT. Hậu Nghĩa / Đức Hòa (Long An)',
          type: 'C1 Partner',
          lat: 10.8872,
          lng: 106.4485,
          radiusKm: 25,
          note: 'Cắt giảm 40km từ TP. Tân An lên Bắc Long An. Tiếp quản 17 Golden Outlets + 266 tiệm Nhóm C.'
        }},
        {{
          id: 'preset_travinh',
          name: 'C1 TP. Trà Vinh (Trà Vinh)',
          type: 'C1 Partner',
          lat: 9.9348,
          lng: 106.3456,
          radiusKm: 30,
          note: 'Cắt giảm 42km vượt sông Cổ Chiên từ NPP Vĩnh Long. Tiếp quản 87-453 Golden Outlets + 400 tiệm Nhóm C.'
        }},
        {{
          id: 'preset_batri',
          name: 'C1 TT. Ba Tri (Bến Tre)',
          type: 'C1 Partner',
          lat: 10.0381,
          lng: 106.5986,
          radiusKm: 25,
          note: 'Cắt giảm 42km-65km vượt đảo từ TP. Bến Tre. Tiếp quản 80 Golden Outlets Ba Tri & Bình Đại.'
        }}
      ];

      let addedCount = 0;
      mekongPresets.forEach(preset => {{
        if (!plannedFlags.some(f => f.id === preset.id || f.name === preset.name)) {{
          addPlannedFlag(preset, false, false);
          addedCount++;
        }}
      }});

      savePlannedFlagsToStorage();
      updatePlannedFlagsUI();

      // Zoom tới vùng Mekong
      map.flyTo([10.25, 106.25], 9, {{ animate: true, duration: 1.2 }});

      alert(`Đã nạp thành công 4 cờ C1 trọng điểm vùng trắng Mekong:\n1. C1 Cai Lậy (Tiền Giang)\n2. C1 Đức Hòa (Long An)\n3. C1 TP. Trà Vinh\n4. C1 Ba Tri (Bến Tre)\n\nCác cờ được hiển thị nổi bật với hiệu ứng radar phát sóng và vòng tròn bán kính.`);
    }}


    // ==========================================
        // ==========================================
    // BỘ LỌC ẨN / HIỆN NPP KHÔNG CÓ SM
    // ==========================================
    function toggleHideKhongSMQuick() {{
      const chk = document.getElementById('chkHideKhongSM');
      const smSelect = document.getElementById('filterSM');

      if (chk) {{
        chk.checked = !chk.checked;
        if (chk.checked) {{
          if (smSelect) smSelect.value = 'CO_SM';
        }} else {{
          if (smSelect && smSelect.value === 'CO_SM') smSelect.value = 'ALL';
        }}
      }}
      applyFilters();
    }}

    function syncHideKhongSMFromCheckbox(isChecked) {{
      const smSelect = document.getElementById('filterSM');
      if (smSelect) {{
        if (isChecked) {{
          smSelect.value = 'CO_SM';
        }} else {{
          if (smSelect.value === 'CO_SM') smSelect.value = 'ALL';
        }}
      }}
      applyFilters();
    }}

    
    // ==========================================
    // SPATIAL SELECTION & REVENUE ANALYTICS MODULE (KÉO CHUỘT KHOANH VÙNG)
    // ==========================================
    let isSpatialMode = false;
    let spatialTool = 'box'; // 'box', 'freehand', 'circle', 'polygon'
    let spatialPoints = [];
    let spatialActivePolygon = null;
    let spatialActiveCircle = null;
    let spatialActiveRect = null;
    let spatialTempMarkers = [];
    let spatialLayerGroup = L.layerGroup();
    let currentSpatialResult = null;
    let activeSpatialTab = 'npp'; // 'npp' or 'outlet'

    // Mouse drag state variables
    let isSpatialMouseDown = false;
    let spatialDragStartLatLng = null;
    let spatialDragRectPreview = null;
    let spatialFreehandPolyline = null;
    let spatialFreehandPoints = [];

    function formatMoneyVND(num) {{
      if (!num || isNaN(num)) return '0 đ';
      if (num >= 1000000000) {{
        return (num / 1000000000).toFixed(2) + ' Tỷ đ';
      }}
      if (num >= 1000000) {{
        return (num / 1000000).toFixed(1) + ' Tr đ';
      }}
      return Math.round(num).toLocaleString('vi-VN') + ' đ';
    }}

    function formatMoneyShort(num) {{
      if (!num || isNaN(num)) return '0';
      if (num >= 1000000000) {{
        return (num / 1000000000).toFixed(2) + ' Tỷ';
      }}
      if (num >= 1000000) {{
        return (num / 1000000).toFixed(1) + ' Tr';
      }}
      if (num >= 1000) {{
        return (num / 1000).toFixed(0) + ' k';
      }}
      return Math.round(num).toLocaleString('vi-VN');
    }}

    function toggleSpatialSelectMode(forceState) {{
      isSpatialMode = (forceState !== undefined) ? forceState : !isSpatialMode;
      const btn = document.getElementById('btnSpatialSelect');
      const toolbar = document.getElementById('spatialToolbar');
      const mapElem = document.getElementById('map');

      if (isSpatialMode) {{
        if (btn) {{ btn.classList.add('active-spatial'); const t = document.getElementById('btnSpatialSelectText'); if (t) t.textContent = '❌ Đóng Khoanh Vùng'; }}
        if (toolbar) toolbar.style.display = 'flex';
        if (mapElem) mapElem.classList.add('crosshair-cursor');
        
        // Tự động nạp sẵn dữ liệu điểm bán trong nền
        ensureOutletsLoaded();
        
        // Mặc định công cụ kéo chuột tạo hộp
        setSpatialTool('box');
        showToastNotification('🖱️ Nhấn giữ chuột và KÉO trên bản đồ để khoanh vùng tính doanh số!');
      }} else {{
        if (btn) {{ btn.classList.remove('active-spatial'); const t = document.getElementById('btnSpatialSelectText'); if (t) t.textContent = '📐 Khoanh Vùng Doanh Số'; }}
        if (toolbar) toolbar.style.display = 'none';
        if (mapElem) mapElem.classList.remove('crosshair-cursor');
        clearSpatialSelection();
        map.dragging.enable();
        document.getElementById('spatialRevenuePanel').style.display = 'none';
      }}
    }}

    function setSpatialTool(toolName) {{
      spatialTool = toolName;
      if (document.getElementById('btnToolBox')) document.getElementById('btnToolBox').classList.toggle('active', toolName === 'box');
      if (document.getElementById('btnToolFreehand')) document.getElementById('btnToolFreehand').classList.toggle('active', toolName === 'freehand');
      if (document.getElementById('btnToolCircle')) document.getElementById('btnToolCircle').classList.toggle('active', toolName === 'circle');
      if (document.getElementById('btnToolPolygon')) document.getElementById('btnToolPolygon').classList.toggle('active', toolName === 'polygon');

      const instr = document.getElementById('spatialToolInstruction');
      if (instr) {{
        if (toolName === 'box') instr.textContent = '🖱️ Nhấn giữ & KÉO chuột trên bản đồ để tạo hộp khoanh vùng';
        else if (toolName === 'freehand') instr.textContent = '✏️ Nhấn giữ & KÉO vẽ tự do bao quanh khu vực';
        else if (toolName === 'circle') instr.textContent = '⭕ Click 1 điểm tâm rồi click/kéo điểm bán kính';
        else if (toolName === 'polygon') instr.textContent = '📐 Click các đỉnh đa giác (click điểm đầu để chốt)';
      }}
      clearSpatialSelection();
    }}

    function clearSpatialSelection() {{
      spatialPoints = [];
      spatialLayerGroup.clearLayers();
      spatialTempMarkers = [];
      spatialActivePolygon = null;
      spatialActiveCircle = null;
      spatialActiveRect = null;
      spatialDragRectPreview = null;
      spatialFreehandPolyline = null;
      spatialFreehandPoints = [];
      currentSpatialResult = null;
      isSpatialMouseDown = false;
      map.dragging.enable();
      document.getElementById('spatialRevenuePanel').style.display = 'none';
    }}

    // Point in polygon math (Ray-casting)
    function isPointInsidePolygon(lat, lng, polyCoords) {{
      let inside = false;
      for (let i = 0, j = polyCoords.length - 1; i < polyCoords.length; j = i++) {{
        const xi = polyCoords[i][0], yi = polyCoords[i][1];
        const xj = polyCoords[j][0], yj = polyCoords[j][1];
        const intersect = ((yi > lng) !== (yj > lng)) &&
                          (lat < (xj - xi) * (lng - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
      }}
      return inside;
    }}

    function getDistanceKm(lat1, lon1, lat2, lon2) {{
      const R = 6371;
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLon/2) * Math.sin(dLon/2);
      return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    }}

    // ==========================================
    // MOUSE DRAG EVENT HANDLERS (KÉO CHUỘT KHOANH VÙNG)
    // ==========================================
    map.on('mousedown', function(e) {{
      // Hỗ trợ cả khi bật Spatial Mode HOẶC giữ phím Shift khi kéo chuột
      if (!isSpatialMode && (!e.originalEvent || !e.originalEvent.shiftKey)) return;

      if (!isSpatialMode && e.originalEvent && e.originalEvent.shiftKey) {{
        toggleSpatialSelectMode(true);
        setSpatialTool('box');
      }}

      if (spatialTool === 'box') {{
        isSpatialMouseDown = true;
        spatialDragStartLatLng = e.latlng;
        map.dragging.disable();

        if (spatialActiveRect) spatialLayerGroup.removeLayer(spatialActiveRect);
        if (spatialDragRectPreview) spatialLayerGroup.removeLayer(spatialDragRectPreview);

        spatialDragRectPreview = L.rectangle([spatialDragStartLatLng, spatialDragStartLatLng], {{
          color: '#10b981',
          weight: 2,
          fillColor: '#059669',
          fillOpacity: 0.25,
          dashArray: '5, 5'
        }});
        spatialLayerGroup.addLayer(spatialDragRectPreview);
      }} else if (spatialTool === 'freehand') {{
        isSpatialMouseDown = true;
        map.dragging.disable();
        spatialFreehandPoints = [[e.latlng.lat, e.latlng.lng]];

        if (spatialActivePolygon) spatialLayerGroup.removeLayer(spatialActivePolygon);
        if (spatialFreehandPolyline) spatialLayerGroup.removeLayer(spatialFreehandPolyline);

        spatialFreehandPolyline = L.polyline(spatialFreehandPoints, {{
          color: '#10b981',
          weight: 3
        }});
        spatialLayerGroup.addLayer(spatialFreehandPolyline);
      }}
    }});

    map.on('mousemove', function(e) {{
      if (!isSpatialMode || !isSpatialMouseDown) return;

      if (spatialTool === 'box' && spatialDragStartLatLng && spatialDragRectPreview) {{
        spatialDragRectPreview.setBounds(L.latLngBounds(spatialDragStartLatLng, e.latlng));
      }} else if (spatialTool === 'freehand' && spatialFreehandPolyline) {{
        spatialFreehandPoints.push([e.latlng.lat, e.latlng.lng]);
        spatialFreehandPolyline.setLatLngs(spatialFreehandPoints);
      }}
    }});

    map.on('mouseup', function(e) {{
      if (!isSpatialMode || !isSpatialMouseDown) return;
      isSpatialMouseDown = false;
      map.dragging.enable();

      if (spatialTool === 'box' && spatialDragStartLatLng && spatialDragRectPreview) {{
        const bounds = L.latLngBounds(spatialDragStartLatLng, e.latlng);
        const d = getDistanceKm(spatialDragStartLatLng.lat, spatialDragStartLatLng.lng, e.latlng.lat, e.latlng.lng);
        if (d >= 0.15) {{
          spatialDragRectPreview.setStyle({{ dashArray: null, weight: 3, fillOpacity: 0.2 }});
          spatialActiveRect = spatialDragRectPreview;
          finishSpatialBox(bounds);
        }} else {{
          spatialLayerGroup.removeLayer(spatialDragRectPreview);
          spatialDragRectPreview = null;
        }}
      }} else if (spatialTool === 'freehand' && spatialFreehandPoints.length >= 4) {{
        spatialLayerGroup.removeLayer(spatialFreehandPolyline);
        spatialPoints = spatialFreehandPoints;
        spatialActivePolygon = L.polygon(spatialPoints, {{
          color: '#10b981',
          weight: 3,
          fillColor: '#059669',
          fillOpacity: 0.25
        }});
        spatialLayerGroup.addLayer(spatialActivePolygon);
        finishSpatialPolygon();
      }}
    }});

    // Click handler for polygon / circle tools
    function onMapClickSpatial(e) {{
      if (!isSpatialMode) return;
      if (spatialTool === 'box' || spatialTool === 'freehand') return; // Handled by mousedown/mouseup

      const lat = e.latlng.lat;
      const lng = e.latlng.lng;

      if (spatialTool === 'polygon') {{
        spatialPoints.push([lat, lng]);

        const ptMarker = L.circleMarker([lat, lng], {{
          radius: 5,
          color: '#10b981',
          fillColor: '#34d399',
          fillOpacity: 0.9,
          weight: 2
        }});
        ptMarker.on('click', () => {{
          if (spatialPoints.length >= 3) finishSpatialPolygon();
        }});
        spatialLayerGroup.addLayer(ptMarker);
        spatialTempMarkers.push(ptMarker);

        if (spatialActivePolygon) {{
          spatialLayerGroup.removeLayer(spatialActivePolygon);
        }}
        if (spatialPoints.length >= 2) {{
          spatialActivePolygon = L.polygon(spatialPoints, {{
            color: '#10b981',
            weight: 2,
            dashArray: '5, 5',
            fillColor: '#059669',
            fillOpacity: 0.2
          }});
          spatialLayerGroup.addLayer(spatialActivePolygon);
        }}

        if (spatialPoints.length >= 3) {{
          const dStart = getDistanceKm(lat, lng, spatialPoints[0][0], spatialPoints[0][1]);
          if (dStart < 2.0 && spatialPoints.length > 3) {{
            finishSpatialPolygon();
          }}
        }}
      }} else if (spatialTool === 'circle') {{
        if (spatialPoints.length === 0) {{
          spatialPoints.push([lat, lng]);
          const centerMarker = L.circleMarker([lat, lng], {{
            radius: 6,
            color: '#38bdf8',
            fillColor: '#60a5fa',
            fillOpacity: 1,
            weight: 2
          }});
          spatialLayerGroup.addLayer(centerMarker);
          spatialTempMarkers.push(centerMarker);
        }} else {{
          const center = spatialPoints[0];
          const distKm = getDistanceKm(center[0], center[1], lat, lng);
          const radiusMeters = distKm * 1000;

          if (spatialActiveCircle) {{
            spatialLayerGroup.removeLayer(spatialActiveCircle);
          }}
          spatialActiveCircle = L.circle(center, {{
            radius: radiusMeters,
            color: '#38bdf8',
            weight: 2,
            dashArray: '6, 6',
            fillColor: '#0284c7',
            fillOpacity: 0.2
          }});
          spatialLayerGroup.addLayer(spatialActiveCircle);
          finishSpatialCircle(center, distKm);
        }}
      }}
    }}

    function finishSpatialBox(bounds) {{
      // Lọc NPP trong bounds
      const selectedNpps = ALL_NPPS.filter(n => {{
        if (!n.lat || !n.lng) return false;
        return bounds.contains([n.lat, n.lng]);
      }});

      const sw = bounds.getSouthWest();
      const ne = bounds.getNorthEast();
      const boxPolygon = [
        [sw.lat, sw.lng],
        [ne.lat, sw.lng],
        [ne.lat, ne.lng],
        [sw.lat, ne.lng]
      ];

      processSpatialSelection(selectedNpps, 'Hộp chữ nhật kéo chuột', null, null, boxPolygon, bounds);
    }}

    function finishSpatialPolygon() {{
      if (spatialPoints.length < 3) return;
      if (spatialActivePolygon) {{
        spatialActivePolygon.setStyle({{ dashArray: null, fillOpacity: 0.25, weight: 3 }});
      }}

      const selected = ALL_NPPS.filter(n => {{
        if (!n.lat || !n.lng) return false;
        return isPointInsidePolygon(n.lat, n.lng, spatialPoints);
      }});

      processSpatialSelection(selected, 'Đa giác tự do', null, null, spatialPoints, null);
    }}

    function finishSpatialCircle(center, radiusKm) {{
      const selected = ALL_NPPS.filter(n => {{
        if (!n.lat || !n.lng) return false;
        const d = getDistanceKm(center[0], center[1], n.lat, n.lng);
        return d <= radiusKm;
      }});

      processSpatialSelection(selected, `Vòng tròn bán kính ${{radiusKm.toFixed(1)}} km`, radiusKm, center, null, null);
      spatialPoints = [];
    }}

    function processSpatialSelection(nppList, zoneTitle, radiusKm, circleCenter, polyPoints, bounds) {{
      let totAmb = 0, totChi = 0, totFro = 0, totRev = 0;
      let activeCnt = 0, coSmCnt = 0;

      nppList.forEach(n => {{
        totAmb += (n.sales_ambient || 0);
        totChi += (n.sales_chilled || 0);
        totFro += (n.sales_frozen || 0);
        totRev += (n.sales_total || 0);
        if (n.status && n.status.includes('Đang')) activeCnt++;
        if (!n.is_khong_sm && n.status && n.status.includes('Đang')) coSmCnt++;
      }});

      const ambPct = totRev > 0 ? (totAmb / totRev * 100).toFixed(1) : '0';
      const chiPct = totRev > 0 ? (totChi / totRev * 100).toFixed(1) : '0';
      const froPct = totRev > 0 ? (totFro / totRev * 100).toFixed(1) : '0';
      const avgNpp = nppList.length > 0 ? (totRev / nppList.length) : 0;

      // Thống kê Điểm Bán (Outlets) trong vùng khoanh
      let selOutlets = [];
      let totOutletRev = 0;
      let equipOutletCnt = 0;
      let activeOutletCnt = 0;

      if (typeof ALL_OUTLETS !== 'undefined' && ALL_OUTLETS && ALL_OUTLETS.length > 0) {{
        if (bounds) {{
          selOutlets = ALL_OUTLETS.filter(o => o[0] && o[1] && bounds.contains([o[0], o[1]]));
        }} else if (circleCenter && radiusKm) {{
          selOutlets = ALL_OUTLETS.filter(o => o[0] && o[1] && getDistanceKm(circleCenter[0], circleCenter[1], o[0], o[1]) <= radiusKm);
        }} else if (polyPoints && polyPoints.length >= 3) {{
          selOutlets = ALL_OUTLETS.filter(o => o[0] && o[1] && isPointInsidePolygon(o[0], o[1], polyPoints));
        }}
        selOutlets.forEach(o => {{
          const s = o[12] || 0;
          totOutletRev += s;
          if (s > 0) activeOutletCnt++;
          if (o[13] && o[13].length > 0) equipOutletCnt++;
        }});
      }}

      const totalZoneSales = totRev + totOutletRev;

      currentSpatialResult = {{
        zoneTitle,
        nppList,
        totAmb, totChi, totFro, totRev,
        activeCnt, coSmCnt, ambPct, chiPct, froPct, avgNpp,
        totOutlets: selOutlets.length,
        totOutletRev,
        equipOutletCnt,
        activeOutletCnt,
        totalZoneSales,
        selOutlets,
        bounds,
        polyPoints,
        circleCenter,
        radiusKm
      }};

      renderSpatialRevenuePanel();
    }}

    function switchSpatialTab(tabName) {{
      activeSpatialTab = tabName;
      renderSpatialRevenuePanel();
    }}

    function renderSpatialRevenuePanel() {{
      const r = currentSpatialResult;
      if (!r) return;

      const body = document.getElementById('spatialRevenueBody');
      const panel = document.getElementById('spatialRevenuePanel');

      // Tạo bảng NPP
      let rowsNppHtml = '';
      r.nppList.forEach(n => {{
        const rev = n.sales_total || 0;
        rowsNppHtml += `
          <tr>
            <td style="font-weight:700; color:#38bdf8;">${{n.code}}</td>
            <td style="max-width:140px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:#ffffff !important; font-weight:700;" title="${{n.name}}">
              ${{n.short_name || n.name}}
            </td>
            <td>${{n.province || ''}}</td>
            <td style="text-align:right; color:#fbbf24;">${{formatMoneyShort(n.sales_ambient || 0)}}</td>
            <td style="text-align:right; color:#34d399;">${{formatMoneyShort(n.sales_chilled || 0)}}</td>
            <td style="text-align:right; color:#38bdf8;">${{formatMoneyShort(n.sales_frozen || 0)}}</td>
            <td style="text-align:right; font-weight:800; color:#10b981;">${{formatMoneyShort(rev)}}</td>
          </tr>
        `;
      }});

      if (r.nppList.length === 0) {{
        rowsNppHtml = '<tr><td colspan="7" style="text-align:center; padding:12px; color:#94a3b8;">Không có trụ sở NPP trong vùng khoanh này (vùng chỉ có Điểm Bán Lẻ).</td></tr>';
      }}

      // Tạo bảng Điểm Bán (Hiển thị Top 40 điểm có doanh số cao nhất hoặc có tủ)
      let rowsOutletHtml = '';
      const topOutlets = (r.selOutlets || [])
        .slice()
        .sort((a, b) => (b[12] || 0) - (a[12] || 0))
        .slice(0, 50);

      topOutlets.forEach(o => {{
        const sMtd = o[12] || 0;
        const equip = o[13] || '';
        const vpo = o[14] || '';
        rowsOutletHtml += `
          <tr>
            <td style="font-weight:700; color:#38bdf8; font-size:0.72rem;">${{o[3]}}</td>
            <td style="max-width:150px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:#ffffff !important; font-weight:700; font-size:0.75rem;" title="${{o[2]}}">
              ${{o[2]}}
            </td>
            <td>
              ${{equip ? `<span style="color:#38bdf8; font-weight:700; font-size:0.68rem; background:rgba(2,132,199,0.25); padding:1px 5px; border-radius:3px; border:1px solid rgba(56,189,248,0.4);"><i class="fa-solid fa-snowflake"></i> ${{equip}}</span>` : '<span style="color:#64748b; font-size:0.68rem;">Chưa có</span>'}}
            </td>
            <td style="color:#cbd5e1; font-size:0.68rem;">${{vpo || '-'}}</td>
            <td style="text-align:right; font-weight:800; color:${{sMtd > 0 ? '#10b981':'#94a3b8'}};">${{formatMoneyVND(sMtd)}}</td>
          </tr>
        `;
      }});

      if (!r.selOutlets || r.selOutlets.length === 0) {{
        rowsOutletHtml = `
          <tr>
            <td colspan="5" style="text-align:center; padding:12px; color:#94a3b8;">
              ${{outletsLoaded ? 'Không có điểm bán nào trong vùng khoanh này.' : '⏳ Đang tải dữ liệu điểm bán... <a href="#" onclick="ensureOutletsLoaded(function(){{processSpatialSelection(currentSpatialResult.nppList, currentSpatialResult.zoneTitle, currentSpatialResult.radiusKm, currentSpatialResult.circleCenter, currentSpatialResult.polyPoints, currentSpatialResult.bounds);}}); return false;" style="color:#38bdf8; text-decoration:underline;">Bấm để tính lại ngay</a>'}}
            </td>
          </tr>
        `;
      }}

      body.innerHTML = `
        <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
          <span>Vùng chọn: <b style="color:#e2e8f0;">${{r.zoneTitle}}</b></span>
          <span style="color:#34d399; font-size:0.7rem;"><i class="fa-solid fa-check-circle"></i> Đã tính toán xong</span>
        </div>

        <!-- HERO TỔNG DOANH SỐ TOÀN BỘ VÙNG KHOANH -->
        <div style="background: linear-gradient(135deg, rgba(16,185,129,0.22), rgba(6,182,212,0.15)); border: 1px solid #10b981; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-size:0.68rem; color:#94a3b8; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
              TỔNG DOANH SỐ VÙNG KHOANH (T9/2026)
            </div>
            <div style="font-size:1.4rem; font-weight:900; color:#34d399; text-shadow:0 0 12px rgba(16,185,129,0.4);">
              ${{formatMoneyVND(r.totRev > 0 ? r.totRev : r.totOutletRev)}}
            </div>
            <div style="font-size:0.68rem; color:#cbd5e1; margin-top:2px;">
              ${{r.totRev > 0 ? `Bao gồm <b>${{formatMoneyShort(r.totRev)}} đ</b> NPP Sell-in + <b>${{formatMoneyShort(r.totOutletRev)}} đ</b> Điểm Bán Sell-out` : `Tổng Sell-out từ <b>${{r.totOutlets}}</b> Điểm Bán Lẻ trong vùng`}}
            </div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:0.75rem; color:#cbd5e1;">NPP Sell-in: <b style="color:#10b981;">${{formatMoneyVND(r.totRev)}}</b></div>
            <div style="font-size:0.75rem; color:#cbd5e1; margin-top:3px;">Điểm bán Sell-out: <b style="color:#38bdf8;">${{formatMoneyVND(r.totOutletRev)}}</b></div>
          </div>
        </div>

        <!-- LƯỚI 4 THẺ KPI CHI TIẾT -->
        <div class="revenue-kpi-grid" style="grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));">
          <div class="revenue-kpi-card" style="border-left-color:#38bdf8;">
            <div class="revenue-kpi-lbl">Số NPP Trong Vùng</div>
            <div class="revenue-kpi-val" style="color:#38bdf8;">${{r.nppList.length}} <span style="font-size:0.7rem; font-weight:400; color:#94a3b8;">(${{r.coSmCnt}} Có SM)</span></div>
          </div>
          <div class="revenue-kpi-card" style="border-left-color:#10b981;">
            <div class="revenue-kpi-lbl">Doanh Số NPP T9</div>
            <div class="revenue-kpi-val" style="color:#10b981;">${{formatMoneyVND(r.totRev)}}</div>
          </div>
          <div class="revenue-kpi-card" style="border-left-color:#06b6d4;">
            <div class="revenue-kpi-lbl">Số Điểm Bán (Outlets)</div>
            <div class="revenue-kpi-val" style="color:#06b6d4;">
              ${{r.totOutlets.toLocaleString('vi-VN')}} <span style="font-size:0.7rem; color:#94a3b8;">(${{r.activeOutletCnt}} có DS)</span>
            </div>
          </div>
          <div class="revenue-kpi-card" style="border-left-color:#f59e0b;">
            <div class="revenue-kpi-lbl">Tủ Đông/Mát Đầu Tư</div>
            <div class="revenue-kpi-val" style="color:#fbbf24;">
              ${{r.equipOutletCnt}} <span style="font-size:0.7rem; color:#67e8f9;">Tủ CJ</span>
            </div>
          </div>
        </div>

        <!-- STACKED PROGRESS BAR THEO NHÓM SP (NẾU CÓ NPP) -->
        ${{r.totRev > 0 ? `
          <div class="revenue-progress-container">
            <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#cbd5e1; margin-bottom:3px;">
              <span><b>Cơ cấu ngành hàng NPP:</b></span>
              <span>${{r.ambPct}}% Khô &bull; ${{r.chiPct}}% Mát &bull; ${{r.froPct}}% Đông</span>
            </div>
            <div class="revenue-stacked-bar">
              <div class="bar-ambient" style="width: ${{r.ambPct}}%;" title="Ambient: ${{formatMoneyVND(r.totAmb)}} (${{r.ambPct}}%)"></div>
              <div class="bar-chilled" style="width: ${{r.chiPct}}%;" title="Chilled: ${{formatMoneyVND(r.totChi)}} (${{r.chiPct}}%)"></div>
              <div class="bar-frozen"  style="width: ${{r.froPct}}%;" title="Frozen: ${{formatMoneyVND(r.totFro)}} (${{r.froPct}}%)"></div>
            </div>
            <div class="revenue-breakdown-legend">
              <span style="color:#fbbf24;"><i class="fa-solid fa-square" style="color:#f59e0b;"></i> Ambient: <b>${{formatMoneyShort(r.totAmb)}} đ</b> (${{r.ambPct}}%)</span>
              <span style="color:#34d399;"><i class="fa-solid fa-square" style="color:#10b981;"></i> Chilled: <b>${{formatMoneyShort(r.totChi)}} đ</b> (${{r.chiPct}}%)</span>
              <span style="color:#38bdf8;"><i class="fa-solid fa-square" style="color:#38bdf8;"></i> Frozen: <b>${{formatMoneyShort(r.totFro)}} đ</b> (${{r.froPct}}%)</span>
            </div>
          </div>
        ` : ''}}

        <!-- TABS CHUYỂN ĐỔI BẢNG NPP VÀ BẢNG ĐIỂM BÁN -->
        <div style="display:flex; gap:6px; margin: 10px 0 6px 0; border-bottom:1px solid #334155; padding-bottom:6px;">
          <button onclick="switchSpatialTab('npp')" style="background:${{activeSpatialTab==='npp'?'#059669':'#1e293b'}}; color:#fff; border:1px solid ${{activeSpatialTab==='npp'?'#10b981':'#475569'}}; border-radius:15px; padding:3px 12px; font-size:0.72rem; font-weight:700; cursor:pointer;">
            🏢 Nhà Phân Phối (${{r.nppList.length}})
          </button>
          <button onclick="switchSpatialTab('outlet')" style="background:${{activeSpatialTab==='outlet'?'#0284c7':'#1e293b'}}; color:#fff; border:1px solid ${{activeSpatialTab==='outlet'?'#38bdf8':'#475569'}}; border-radius:15px; padding:3px 12px; font-size:0.72rem; font-weight:700; cursor:pointer;">
            🏪 Điểm Bán Lẻ (${{r.totOutlets}})
          </button>
        </div>

        <!-- BẢNG DANH SÁCH THEO TAB -->
        ${{activeSpatialTab === 'npp' ? `
          <div class="revenue-table-wrapper">
            <table class="revenue-table">
              <thead>
                <tr>
                  <th>Mã</th>
                  <th>Tên NPP</th>
                  <th>Tỉnh</th>
                  <th style="text-align:right;">Ambient</th>
                  <th style="text-align:right;">Chilled</th>
                  <th style="text-align:right;">Frozen</th>
                  <th style="text-align:right;">Tổng NPP</th>
                </tr>
              </thead>
              <tbody>
                ${{rowsNppHtml}}
              </tbody>
            </table>
          </div>
        ` : `
          <div class="revenue-table-wrapper">
            <table class="revenue-table">
              <thead>
                <tr>
                  <th>Mã Cửa Hàng</th>
                  <th>Tên Điểm Bán</th>
                  <th>Thiết Bị</th>
                  <th>Phân Khúc</th>
                  <th style="text-align:right;">DS T9 (MTD)</th>
                </tr>
              </thead>
              <tbody>
                ${{rowsOutletHtml}}
              </tbody>
            </table>
          </div>
          ${{r.selOutlets && r.selOutlets.length > 50 ? `<div style="font-size:0.68rem; color:#94a3b8; text-align:center; margin-top:4px;">(Đang hiển thị 50 điểm có doanh số cao nhất. Bấm "Xuất CSV" để tải đủ ${{r.selOutlets.length}} điểm)</div>` : ''}}
        `}}
      `;

      panel.style.display = 'flex';
    }}

    function exportSpatialRevenueCSV() {{
      const r = currentSpatialResult;
      if (!r) {{
        alert('Chưa có vùng khoanh nào được chọn.');
        return;
      }}

      const lines = [];
      let filename = 'Bao_Cao_Doanh_So_Vung_Khoanh_T9_2026.csv';

      // Nếu đang ở Tab Điểm Bán hoặc vùng khoanh chỉ có Điểm Bán
      if (activeSpatialTab === 'outlet' || (r.nppList.length === 0 && r.selOutlets && r.selOutlets.length > 0)) {{
        filename = 'Danh_Sach_Diem_Ban_Vung_Khoanh_T9_2026.csv';
        lines.push('"Mã Cửa Hàng","Tên Điểm Bán","Mã NPP","Tỉnh Thành","Địa Chỉ","Cự Ly (km)","Phân Loại","Doanh Số T9 MTD (VNĐ)","Doanh Số T8 M-1 (VNĐ)","Thiết Bị Đầu Tư","Phân Khúc VPO","Hành Động Đề Xuất","NVBH Phụ Trách","Tuyến Bán Hàng"');
        
        r.selOutlets.forEach(o => {{
          const row = [
            o[3] || '',
            (o[2] || '').replace(/"/g, '""'),
            o[4] || '',
            o[5] || '',
            (o[9] || '').replace(/"/g, '""'),
            o[10] || 0,
            o[11] || '',
            Math.round(o[12] || 0),
            Math.round(o[17] || 0),
            (o[13] || 'Chưa có').replace(/"/g, '""'),
            o[14] || '',
            (o[15] || '').replace(/"/g, '""'),
            (o[16] || '').replace(/"/g, '""'),
            (o[18] || '').replace(/"/g, '""')
          ];
          lines.push(row.map(v => `"${{v}}"`).join(','));
        }});
      }} else {{
        // Xuất báo cáo NPP
        filename = 'Doanh_So_Nhom_NPP_Khoanh_Vung_T9_2026.csv';
        lines.push('"Mã NPP","Tên NPP","Tỉnh","Miền","Trạng Thái","Giám Sát","Ambient (VNĐ)","Chilled (VNĐ)","Frozen (VNĐ)","Tổng Doanh Số (VNĐ)"');
        
        r.nppList.forEach(n => {{
          const row = [
            n.code,
            (n.name || '').replace(/"/g, '""'),
            n.province || '',
            n.region || '',
            n.status || '',
            n.is_khong_sm ? 'Không SM' : `Có SM (${{n.so_nvbh}} NV)`,
            Math.round(n.sales_ambient || 0),
            Math.round(n.sales_chilled || 0),
            Math.round(n.sales_frozen || 0),
            Math.round(n.sales_total || 0)
          ];
          lines.push(row.map(v => `"${{v}}"`).join(','));
        }});
      }}

      const csvContent = '\uFEFF' + lines.join(String.fromCharCode(10));
      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

</script>
</body>
</html>
'''

# 3. Write to both files
with open('d:/SE_Project/RTM_Model/ban_do_khong_gian_rtm_mekong.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("Successfully written to ban_do_khong_gian_rtm_mekong.html")

with open('d:/SE_Project/RTM_Model/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("Successfully written to index.html")
