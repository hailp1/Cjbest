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

# 2. Build complete HTML
npps_json_str = json.dumps(npps, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
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
  <script src="outlets_data.js" defer></script>
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

    /* Filter Bar - Được chia làm 2 dòng trực quan, dễ bấm, tiện lọc */
    .filter-bar {{
      background: #1e293b;
      padding: 0.4rem 0.75rem;
      border-bottom: 1px solid #334155;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
      z-index: 999;
      flex-shrink: 0;
    }}
    .filter-row {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      overflow-x: auto;
      white-space: nowrap;
      scrollbar-width: none;
    }}
    .filter-row::-webkit-scrollbar {{ display: none; }}
    .filter-row-primary {{
      padding-bottom: 3px;
    }}
    .filter-row-secondary {{
      padding-top: 3px;
      border-top: 1px dashed rgba(51, 65, 85, 0.75);
    }}

    .filter-group {{
      display: flex;
      align-items: center;
      gap: 0.3rem;
      flex-shrink: 0;
    }}
    .filter-label {{
      color: #94a3b8;
      font-size: 0.72rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 3px;
      white-space: nowrap;
    }}
    .filter-select, .filter-search {{
      background: #0f172a;
      border: 1px solid #334155;
      color: #f1f5f9;
      font-size: 0.74rem;
      font-weight: 600;
      padding: 4px 7px;
      border-radius: 6px;
      outline: none;
    }}
    .filter-search {{
      min-width: 140px;
    }}

    /* Checkbox Toggles */
    .layer-toggle-container {{
      display: flex;
      align-items: center;
      gap: 0.35rem;
      background: #0f172a;
      padding: 2px 5px;
      border-radius: 7px;
      border: 1px solid #334155;
      flex-shrink: 0;
    }}
    .toggle-checkbox-label {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      cursor: pointer;
      user-select: none;
      padding: 3px 6px;
      border-radius: 5px;
      font-size: 0.71rem;
      font-weight: 700;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid transparent;
      white-space: nowrap;
      transition: all 0.2s;
    }}
    .toggle-checkbox-label input[type="checkbox"] {{
      appearance: none;
      -webkit-appearance: none;
      width: 13px;
      height: 13px;
      border-radius: 3px;
      outline: none;
      cursor: pointer;
      position: relative;
      border: 1.5px solid #64748b;
      background: #1e293b;
    }}
    .toggle-checkbox-label.npp-label input[type="checkbox"]:checked {{ background: #059669; border-color: #10b981; }}
    .toggle-checkbox-label.inactive-label input[type="checkbox"]:checked {{ background: #dc2626; border-color: #ef4444; }}
    .toggle-checkbox-label.outlet-label input[type="checkbox"]:checked {{ background: #f59e0b; border-color: #fbbf24; }}
    .toggle-checkbox-label.cold-label input[type="checkbox"]:checked {{ background: #0284c7; border-color: #38bdf8; }}
    .toggle-checkbox-label.dry-label input[type="checkbox"]:checked {{ background: #d97706; border-color: #f59e0b; }}
    .toggle-checkbox-label.remote-label input[type="checkbox"]:checked {{ background: #dc2626; border-color: #ef4444; }}
    .toggle-checkbox-label.spider-label input[type="checkbox"]:checked {{ background: #8b5cf6; border-color: #a78bfa; }}
    
    .toggle-checkbox-label input[type="checkbox"]:checked::after {{
      content: '\\f00c';
      font-family: 'Font Awesome 6 Free';
      font-weight: 900;
      font-size: 8px;
      color: white;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }}
    .active-npp {{ background: rgba(5, 150, 105, 0.18); border-color: rgba(16, 185, 129, 0.4); color: #a7f3d0; }}
    .active-hide-inactive {{ background: rgba(220, 38, 38, 0.25) !important; border-color: rgba(239, 68, 68, 0.6) !important; color: #fecaca !important; }}
    .active-outlet {{ background: rgba(245, 158, 11, 0.18); border-color: rgba(245, 158, 11, 0.4); color: #fde68a; }}
    .active-cold {{ background: rgba(14, 165, 233, 0.18); border-color: rgba(14, 165, 233, 0.4); color: #bae6fd; }}
    .active-dry {{ background: rgba(217, 119, 6, 0.18); border-color: rgba(217, 119, 6, 0.4); color: #fed7aa; }}
    .active-remote {{ background: rgba(220, 38, 38, 0.2); border-color: rgba(239, 68, 68, 0.5); color: #fecaca; }}
    .active-spider {{ background: rgba(139, 92, 246, 0.2); border-color: rgba(167, 139, 250, 0.5); color: #ddd6fe; }}

    .kpi-pill {{
      margin-left: auto;
      background: #0f172a;
      border: 1px solid #334155;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.7rem;
      font-weight: 600;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .kpi-val {{ color: #f8fafc; font-weight: 800; }}
    .kpi-active {{ color: #10b981; }}
    .kpi-inactive {{ color: #ef4444; }}
    .kpi-outlets {{ color: #f59e0b; font-weight: 800; }}
    .kpi-remote {{ color: #ef4444; font-weight: 800; }}

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
      <!-- NÚT BẬT BẢNG TỔNG THỂ PHÂN TÍCH CỰ LY & HUB -->
      <button class="btn-nav" style="background:#7c3aed; border-color:#8b5cf6;" onclick="openAnalyticsModal()"><i class="fa-solid fa-chart-pie"></i> Cự Ly & Hub</button>
      <button class="btn-nav" onclick="exportFilteredCSV()"><i class="fa-solid fa-file-excel"></i> Xuất Excel</button>
      <a href="rtm_dashboard_mien_tay.html" class="btn-nav"><i class="fa-solid fa-chart-line"></i> Dashboard</a>
    </div>
  </header>

  <!-- Cascading Filter Bar (Được chia làm 2 dòng rõ ràng, dễ chọn & không bị che khuất) -->
  <div class="filter-bar">
    <!-- DÒNG 1: BỘ LỌC ĐỊA BÀN (MIỀN, VÙNG, TỈNH), TRẠNG THÁI NPP & TÌM KIẾM -->
    <div class="filter-row filter-row-primary">
      <div class="filter-group">
        <span class="filter-label"><i class="fa-solid fa-globe"></i> Miền:</span>
        <select id="filterMien" class="filter-select" onchange="onMienChange()">
          <option value="ALL">Tất cả Miền</option>
          <option value="MIỀN NAM">MIỀN NAM (199 NPP)</option>
          <option value="MIỀN BẮC">MIỀN BẮC (192 NPP)</option>
        </select>
      </div>

      <div class="filter-group">
        <span class="filter-label"><i class="fa-solid fa-network-wired"></i> Vùng:</span>
        <select id="filterVung" class="filter-select" onchange="onVungChange()">
          <option value="ALL">Tất cả Vùng</option>
        </select>
      </div>

      <div class="filter-group">
        <span class="filter-label"><i class="fa-solid fa-city"></i> Tỉnh/Thành:</span>
        <select id="filterTinh" class="filter-select" onchange="applyFilters()">
          <option value="ALL">Tất cả Tỉnh/Thành</option>
        </select>
      </div>

      <!-- BỘ LỌC TRẠNG THÁI NPP: ĐANG HOẠT ĐỘNG / NGƯNG / TẤT CẢ -->
      <div class="filter-group">
        <span class="filter-label"><i class="fa-solid fa-toggle-on"></i> Trạng thái NPP:</span>
        <select id="filterStatus" class="filter-select" onchange="onStatusSelectChange()">
          <option value="ALL">Tất cả Trạng thái (391 NPP)</option>
          <option value="ACTIVE">🟢 Đang Hoạt Động (215 NPP)</option>
          <option value="INACTIVE">🔴 Ngưng Hoạt Động (176 NPP)</option>
        </select>
      </div>

      <div class="filter-group" style="flex: 1; min-width: 160px;">
        <input type="text" id="filterSearch" class="filter-search" placeholder="🔍 Tìm NPP, Điểm bán, Tỉnh..." oninput="applyFilters()" style="width: 100%;">
      </div>
    </div>

    <!-- DÒNG 2: BỘ BẬT/TẮT LỚP HIỂN THỊ (TOGGLES) & THÔNG SỐ KPI TỔNG QUAN -->
    <div class="filter-row filter-row-secondary">
      <!-- DẤU TICK HIỂN THỊ LỚP (LAYER TOGGLES) -->
      <div class="layer-toggle-container">
        <label class="toggle-checkbox-label npp-label active-npp" id="lblChkNpp" title="Bật/Tắt hiển thị Nhà Phân Phối">
          <input type="checkbox" id="chkToggleNPP" checked onchange="toggleNPPVisibility()">
          <i class="fa-solid fa-warehouse" style="color:#10b981;"></i>
          <span>NPP (<span id="chkNppCount">391</span>)</span>
        </label>

        <!-- DẤU TICK BỎ CÁC NPP NGƯNG HOẠT ĐỘNG -->
        <label class="toggle-checkbox-label inactive-label" id="lblChkHideInactive" title="Tích chọn để BỎ TOÀN BỘ các NPP đã ngưng hoạt động">
          <input type="checkbox" id="chkHideInactive" onchange="toggleHideInactive()">
          <i class="fa-solid fa-ban" style="color:#ef4444;"></i>
          <span>Bỏ NPP Ngưng (<span id="countInactiveNpp">176</span>)</span>
        </label>

        <label class="toggle-checkbox-label outlet-label active-outlet" id="lblChkOutlet" title="Bật/Tắt hiển thị Điểm Bán">
          <input type="checkbox" id="chkToggleOutlet" checked onchange="toggleOutletVisibility()">
          <i class="fa-solid fa-store" style="color:#f59e0b;"></i>
          <span>Điểm Bán (<span id="chkOutletCount">59.4k</span>)</span>
        </label>

        <label class="toggle-checkbox-label spider-label" id="lblChkSpider" title="Vẽ tia nối liên kết từ NPP đến Điểm Bán">
          <input type="checkbox" id="chkToggleSpider" onchange="toggleSpiderVisibility()">
          <i class="fa-solid fa-share-nodes" style="color:#a78bfa;"></i>
          <span>Tia Nối</span>
        </label>
      </div>

      <!-- DẤU TICK PHÂN LOẠI HÀNG ĐÔNG / HÀNG KHÔ -->
      <div class="layer-toggle-container">
        <label class="toggle-checkbox-label cold-label active-cold" id="lblChkCold" title="Điểm bán có mua Hàng Đông">
          <input type="checkbox" id="chkToggleCold" checked onchange="applyFilters()">
          <i class="fa-solid fa-snowflake" style="color:#38bdf8;"></i>
          <span>Hàng Đông</span>
        </label>

        <label class="toggle-checkbox-label dry-label active-dry" id="lblChkDry" title="Điểm bán mua Hàng Khô">
          <input type="checkbox" id="chkToggleDry" checked onchange="applyFilters()">
          <i class="fa-solid fa-box-open" style="color:#f59e0b;"></i>
          <span>Hàng Khô</span>
        </label>
      </div>

      <!-- DẤU TICK CỰ LY > 45KM (MỞ ĐẠI LÝ CHUYỂN TIẾP) -->
      <div class="layer-toggle-container">
        <label class="toggle-checkbox-label remote-label" id="lblChkRemoteOnly" title="Chỉ xem điểm bán cự ly > 45km">
          <input type="checkbox" id="chkToggleRemoteOnly" onchange="applyFilters()">
          <i class="fa-solid fa-triangle-exclamation" style="color:#ef4444;"></i>
          <span>Cự ly > 45km</span>
        </label>
      </div>

      <div class="kpi-pill">
        <span>Xem:</span>
        <span id="kpiCount" class="kpi-val">391</span> NPP
        (<span id="kpiActive" class="kpi-active">215 Chạy</span>/<span id="kpiInactive" class="kpi-inactive">176 Ngưng</span>)
        &bull; <span id="kpiOutlets" class="kpi-outlets">59.4k</span> Điểm Bán
        (<span id="kpiRemote" class="kpi-remote">2,456</span> >45km)
      </div>
    </div>
  </div>

  <!-- Main Container -->
  <div class="main-container">
    <div id="map"></div>

    <!-- Floating Outlet Banner when viewing single NPP outlets -->
    <div id="nppOutletBanner">
      <i class="fa-solid fa-store" style="color:#f59e0b;"></i>
      <span id="nppOutletBannerText">Đang xem điểm bán của NPP</span>
      <button onclick="resetOutletView()" style="background:#f59e0b; color:#0f172a; border:none; padding:3px 9px; border-radius:12px; font-size:0.7rem; font-weight:800; cursor:pointer;">
        <i class="fa-solid fa-rotate-left"></i> Hiện Tất Cả
      </button>
    </div>

    <!-- Quick Buttons (Bản đồ) -->
    <div class="map-quick-controls">
      <button class="quick-btn" onclick="zoomToPreset('ALL')"><i class="fa-solid fa-arrows-to-eye"></i> Toàn Quốc</button>
      <button class="quick-btn" onclick="zoomToPreset('MB')"><i class="fa-solid fa-location-dot"></i> Bắc</button>
      <button class="quick-btn" onclick="zoomToPreset('MN')"><i class="fa-solid fa-location-dot"></i> Nam</button>
      
      <!-- NÚT HIỆN / ẨN OUTLET TRỰC TIẾP TRÊN BẢN ĐỒ -->
      <button class="quick-btn active-quick-outlet" id="btnQuickToggleOutlet" onclick="toggleOutletQuick()" style="border-color: rgba(245, 158, 11, 0.6);">
        <i class="fa-solid fa-store" style="color:#f59e0b;"></i> <span id="btnQuickOutletText">Ẩn Điểm Bán</span>
      </button>

      <button class="quick-btn" id="btnQuickHideInactive" onclick="toggleHideInactiveQuick()" style="border-color: rgba(239, 68, 68, 0.6);"><i class="fa-solid fa-ban" style="color:#ef4444;"></i> Bỏ NPP Ngưng</button>
      <button class="quick-btn" onclick="openAnalyticsModal()" style="border-color:#a78bfa; color:#c4b5fd;"><i class="fa-solid fa-chart-pie"></i> Báo Cáo Cự Ly</button>
      <button class="quick-btn" id="btnToggleRadius" onclick="toggleRadius()"><i class="fa-solid fa-circle-notch"></i> Bán kính 45km</button>
    </div>

    <!-- Mobile Button to Open Drawer -->
    <button class="btn-mobile-drawer" id="btnOpenMobileDrawer" onclick="toggleMobileSidebar(true)">
      <i class="fa-solid fa-list-check"></i> Danh Sách NPP (<span id="mobileCount">391</span>)
    </button>

    <!-- Legend -->
    <div class="map-legend">
      <div style="font-weight:800; font-size: 0.7rem; color: #94a3b8; margin-bottom: 2px;">CHÚ GIẢI GIAO HÀNG</div>
      <div class="legend-item"><span class="legend-dot" style="background: #059669;"></span> NPP Đang Hoạt Động</div>
      <div class="legend-item"><span class="legend-dot" style="background: #dc2626;"></span> NPP Ngưng Hoạt Động</div>
      <div class="legend-item"><span class="legend-dot" style="background: #0284c7; width:7px; height:7px;"></span> Điểm Hàng Đông (Cold Chain)</div>
      <div class="legend-item"><span class="legend-dot" style="background: #f59e0b; width:7px; height:7px;"></span> Điểm Hàng Khô (Dry Chain)</div>
      <div class="legend-item"><span class="legend-dot" style="background: #dc2626; width:7px; height:7px;"></span> Cự ly > 45km (Cần mở Hub)</div>
    </div>

    <!-- Sidebar Drawer -->
    <div class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-title">
          <i class="fa-solid fa-warehouse" style="color:#2563eb;"></i>
          <span>Danh Sách NPP (<span id="sidebarCount">391</span>)</span>
        </div>
        <button class="btn-close-sidebar" onclick="toggleMobileSidebar(false)"><i class="fa-solid fa-xmark"></i></button>
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
          <span>Báo Cáo Tổng Thể Cự Ly Giao Hàng & Đề Xuất Trạm Trung Chuyển (Hubs)</span>
        </div>
        <button class="btn-close-modal" onclick="closeAnalyticsModal()"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <div class="modal-body">
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
    let showOutlets = true;
    let showSpiderLines = false;
    let showRadius = false;

    // Khởi tạo Leaflet Map
    const map = L.map('map', {{
      center: [14.0583, 108.2772],
      zoom: 6,
      zoomControl: false
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
      applyFilters();

      // Check mobile size to auto-adjust
      if (window.innerWidth <= 768) {{
        map.setZoom(5);
      }}
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

    function toggleOutletVisibility() {{
      const chk = document.getElementById('chkToggleOutlet');
      const lbl = document.getElementById('lblChkOutlet');
      const quickBtn = document.getElementById('btnQuickToggleOutlet');
      const quickText = document.getElementById('btnQuickOutletText');
      showOutlets = chk.checked;
      if (showOutlets) {{
        if (lbl) lbl.classList.add('active-outlet');
        if (quickBtn) quickBtn.classList.add('active-quick-outlet');
        if (quickText) quickText.textContent = 'Ẩn Điểm Bán';
        renderOutlets();
        outletsLayer.addTo(map);
      }} else {{
        if (lbl) lbl.classList.remove('active-outlet');
        if (quickBtn) quickBtn.classList.remove('active-quick-outlet');
        if (quickText) quickText.textContent = 'Hiện Điểm Bán';
        map.removeLayer(outletsLayer);
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

    function applyFilters() {{
      const mienVal = document.getElementById('filterMien').value;
      const vungVal = document.getElementById('filterVung').value;
      const tinhVal = document.getElementById('filterTinh').value;
      const statusVal = document.getElementById('filterStatus') ? document.getElementById('filterStatus').value : 'ALL';
      const hideInactive = document.getElementById('chkHideInactive') ? document.getElementById('chkHideInactive').checked : false;
      const searchVal = document.getElementById('filterSearch').value.toLowerCase().trim();

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

        // Nếu bỏ NPP ngưng hoặc lọc theo trạng thái, ẩn luôn các outlet thuộc NPP bị loại bỏ
        if ((hideInactive || statusVal !== 'ALL') && !matchingNppCodeSet.has(String(o[4]))) return false;
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

      document.getElementById('chkNppCount').textContent = totalNpp;
      document.getElementById('chkOutletCount').textContent = totalOutlets >= 1000 ? (totalOutlets/1000).toFixed(1) + 'k' : totalOutlets;
    }}

    // Render Markers on Map
    function renderMapMarkers() {{
      markersLayer.clearLayers();
      radiusLayer.clearLayers();

      const bounds = [];

      filteredNPPs.forEach(n => {{
        if (!n.lat || !n.lng) return;

        const isActive = n.status.includes('Đang');
        const iconClass = isActive ? 'npp-icon-active' : 'npp-icon-inactive';
        const iconHtml = `
          <div class="custom-npp-icon ${{iconClass}}" style="width: 24px; height: 24px;">
            <i class="fa-solid fa-warehouse npp-icon-inner"></i>
          </div>
        `;

        const customIcon = L.divIcon({{
          html: iconHtml,
          className: 'custom-leaflet-marker',
          iconSize: [24, 24],
          iconAnchor: [12, 12],
          popupAnchor: [0, -12]
        }});

        const marker = L.marker([n.lat, n.lng], {{ icon: customIcon }});

        const outletCnt = n.outlet_count || 0;
        const remoteCnt = n.remote_count || 0;
        const dongCnt = n.dong_count || 0;
        const maxDist = n.max_dist || 0;

        const popupContent = `
          <div class="popup-card">
            <div class="popup-header">
              <span class="popup-tag ${{isActive ? 'badge-active' : 'badge-inactive'}}">${{n.status}}</span>
              <div class="popup-title">${{n.name}}</div>
              <div style="font-size:0.68rem; color:#94a3b8; margin-top:2px;">Mã: ${{n.code}} &bull; ${{n.region}} &bull; ${{n.province}}</div>
            </div>
            <div class="popup-body">
              <div class="popup-row"><i class="fa-solid fa-location-dot"></i><span>${{n.address || 'Đang cập nhật'}}</span></div>
              <div class="popup-row"><i class="fa-solid fa-store" style="color:#f59e0b;"></i><span><b>${{outletCnt}}</b> Điểm bán (${{dongCnt}} hàng đông)</span></div>
              <div class="popup-row"><i class="fa-solid fa-arrows-left-right" style="color:#38bdf8;"></i><span>Cự ly Max: <b>${{maxDist}} km</b></span></div>
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
        `;

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
      if (!showOutlets) return;

      const maxRender = 12000;
      const toRender = filteredOutlets.slice(0, maxRender);

      toRender.forEach(o => {{
        const lat = o[0];
        const lng = o[1];
        if (!lat || !lng) return;

        const dist = o[10];
        const ptype = o[11];
        const isRemote = dist >= 45;

        let color = '#f59e0b';
        if (ptype === 'DONG') color = '#0284c7';
        else if (ptype === 'BOTH') color = '#8b5cf6';
        if (isRemote) color = '#dc2626';

        const circleMarker = L.circleMarker([lat, lng], {{
          radius: isRemote ? 4 : 3,
          fillColor: color,
          color: '#ffffff',
          weight: 0.8,
          opacity: 0.9,
          fillOpacity: 0.85
        }});

        circleMarker.bindPopup(`
          <div style="font-size:0.75rem; padding:4px;">
            <b style="color:#0f172a;">${{o[2]}}</b> (Mã: ${{o[3]}})<br>
            <span style="color:#64748b;">NPP Quản lý:</span> <b>${{o[4]}}</b><br>
            <span style="color:#64748b;">Khoảng cách đến NPP:</span> <b style="color:${{isRemote ? '#dc2626':'#059669'}};">${{dist}} km</b><br>
            <span style="color:#64748b;">Phân loại hàng:</span> <b>${{ptype === 'DONG' ? '❄️ Hàng Đông' : (ptype === 'BOTH' ? '❄️🌾 Cả 2' : '🌾 Hàng Khô')}}</b><br>
            <span style="color:#64748b;">Địa chỉ:</span> ${{o[9]}}
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
            <span class="badge-status ${{isActive ? 'badge-active' : 'badge-inactive'}}">${{n.status}}</span>
          </div>
          <div class="npp-title">${{n.name}}</div>
          <div class="npp-meta">
            <span class="npp-meta-item"><i class="fa-solid fa-city"></i> ${{n.province}}</span>
            <span class="npp-meta-item"><i class="fa-solid fa-store"></i> ${{n.outlet_count || 0}} KH</span>
            <span class="npp-meta-item"><i class="fa-solid fa-arrows-left-right"></i> Max: ${{n.max_dist || 0}}km</span>
            ${{n.remote_count > 0 ? `<span class="badge-remote-danger"><i class="fa-solid fa-triangle-exclamation"></i> ${{n.remote_count}} >45km</span>` : ''}}
          </div>
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
      filterAnalyticsTable();
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
