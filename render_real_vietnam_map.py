import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon
import numpy as np

# Load Real Vietnam 63 Provinces GeoJSON (WGS84 GPS Coordinates)
with open(r'd:\SE_Project\RTM_Model\vietnam_wgs84.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Regional classification by province
REGION_MAP = {
    # 1. Hai Phong & North-East
    'Hải Phòng': 'HP', 'Quảng Ninh': 'HP', 'Bắc Giang': 'HP', 'Bắc Ninh': 'HP',
    'Hải Dương': 'HP', 'Hưng Yên': 'HP', 'Thái Bình': 'HP', 'Nam Định': 'HP',
    'Ninh Bình': 'HP', 'Hà Nam': 'HP', 'Thanh Hóa': 'HP', 'Nghệ An': 'HP',
    'Ha Tinh': 'HP', 'Lạng Sơn': 'HP', 'Cao Bằng': 'HP', 'Đông Bắc': 'HP',
    'Đồng Bằng Sông Hồng': 'HP',

    # 2. Hanoi & North-West
    'Ha Noi': 'HN', 'Vĩnh Phúc': 'HN', 'Phú Thọ': 'HN', 'Yên Bái': 'HN',
    'Lào Cai': 'HN', 'Tuyên Quang': 'HN', 'Thái Nguyên': 'HN', 'Bắc Kạn': 'HN',
    'Hà Giang': 'HN', 'Son La': 'HN', 'Hòa Bình': 'HN', 'Điện Biên': 'HN', 'Lai Chau': 'HN',

    # 3. Da Nang & Central
    'Đà Nẵng': 'DN', 'Thừa Thiên - Huế': 'DN', 'Quảng Trị': 'DN',
    'Quảng Bình': 'DN', 'Quàng Nam': 'DN', 'Quảng Ngãi': 'DN',

    # 4. Nha Trang & Highlands
    'Khánh Hòa': 'NT', 'Bình Định': 'NT', 'Phú Yên': 'NT', 'Ninh Thuận': 'NT',
    'Bình Thuận': 'NT', 'Kon Tum': 'NT', 'Gia Lai': 'NT', 'Đắk Lắk': 'NT',
    'Đắk Nông': 'NT', 'Lâm Đồng': 'NT', 'Bình Phước': 'NT',

    # 5. Ho Chi Minh City & South-East
    'Hồ Chí Minh city': 'HCM', 'Bình Dương': 'HCM', 'Đồng Nai': 'HCM',
    'Bà Rịa - Vũng Tàu': 'HCM', 'Tây Ninh': 'HCM', 'Đông Nam Bộ': 'HCM',

    # 6. Can Tho & Mekong Delta
    'Can Tho': 'CT', 'Long An': 'CT', 'Tiền Giang': 'CT', 'Bến Tre': 'CT',
    'Trà Vinh': 'CT', 'Vĩnh Long': 'CT', 'Ðong Tháp': 'CT', 'An Giang': 'CT',
    'Kiên Giang': 'CT', 'Hau Giang': 'CT', 'Sóc Trăng': 'CT', 'Bạc Liêu': 'CT', 'Cà Mau': 'CT'
}

# Regional styling palette
REGION_STYLES = {
    'HP': {'face': '#141E33', 'edge': '#F87171', 'lw': 0.85},
    'CT': {'face': '#141E33', 'edge': '#F87171', 'lw': 0.85},
    'HCM': {'face': '#141E33', 'edge': '#4ADE80', 'lw': 0.95},
    'HN': {'face': '#141E33', 'edge': '#38BDF8', 'lw': 0.8},
    'NT': {'face': '#141E33', 'edge': '#FBBF24', 'lw': 0.8},
    'DN': {'face': '#141E33', 'edge': '#38BDF8', 'lw': 0.8},
    'DEFAULT': {'face': '#141E33', 'edge': '#475569', 'lw': 0.7}
}

fig, ax = plt.subplots(figsize=(6.4, 9.0), dpi=300, facecolor='#0B132B')
ax.set_facecolor('#0B132B')

ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

# Spatial Bounds for Vietnam
ax.set_xlim(101.2, 111.0)
ax.set_ylim(8.0, 23.8)

# Cartographic grid
for lat in range(10, 24, 2):
    ax.axhline(lat, color='#1E293B', linestyle=':', linewidth=0.5, alpha=0.5)
for lon in range(102, 111, 2):
    ax.axvline(lon, color='#1E293B', linestyle=':', linewidth=0.5, alpha=0.5)

# Render real province polygons
for feature in geojson_data['features']:
    props = feature['properties']
    name = props.get('name', '')
    reg_code = REGION_MAP.get(name, 'DEFAULT')
    style = REGION_STYLES.get(reg_code, REGION_STYLES['DEFAULT'])
    
    geom = feature['geometry']
    g_type = geom['type']
    coords = geom['coordinates']
    
    polys = [coords] if g_type == 'Polygon' else coords
    
    for poly in polys:
        ext = np.array(poly[0])
        p_base = Polygon(ext, closed=True,
                         facecolor=style['face'],
                         edgecolor=style['edge'],
                         linewidth=style['lw'],
                         zorder=2)
        ax.add_patch(p_base)

# Title & Context Block
ax.text(101.6, 23.4, 'VIETNAM RTM SPATIAL NETWORK', color='#38BDF8', fontsize=11.5, fontweight='bold', zorder=10)
ax.text(101.6, 22.95, '215 Active Distributors • 2026 Nationwide Baseline', color='#E2E8F0', fontsize=8.2, zorder=10)

# Regional Commercial Headquarters (6 Pins) with clean label boxes
hubs = [
    {
        'name': 'HANOI & NW', 'lon': 105.85, 'lat': 21.03, 'npp': '43 Distributors', 'dist': '12.6 km',
        'color': '#38BDF8', 'bg': '#0284C7', 'align': 'right', 'offset': (-0.45, 0.35)
    },
    {
        'name': 'HAI PHONG & NE', 'lon': 106.68, 'lat': 20.85, 'npp': '38 Distributors', 'dist': '21.3 km (High Friction)',
        'color': '#F87171', 'bg': '#DC2626', 'align': 'left', 'offset': (0.45, 0.25)
    },
    {
        'name': 'DA NANG & CENTRAL', 'lon': 108.20, 'lat': 16.05, 'npp': '16 Distributors', 'dist': '10.1 km',
        'color': '#38BDF8', 'bg': '#0284C7', 'align': 'left', 'offset': (0.45, 0.0)
    },
    {
        'name': 'NHA TRANG & HIGH.', 'lon': 109.19, 'lat': 12.24, 'npp': '57 Distributors', 'dist': '11.8 km',
        'color': '#FBBF24', 'bg': '#D97706', 'align': 'left', 'offset': (0.45, 0.0)
    },
    {
        'name': 'HO CHI MINH CITY', 'lon': 106.63, 'lat': 10.82, 'npp': '35 Distributors', 'dist': '6.2 km (Optimal)',
        'color': '#4ADE80', 'bg': '#16A34A', 'align': 'right', 'offset': (-0.45, 0.20)
    },
    {
        'name': 'CAN THO & MEKONG', 'lon': 105.78, 'lat': 10.04, 'npp': '26 Distributors', 'dist': '19.4 km (High Friction)',
        'color': '#F87171', 'bg': '#DC2626', 'align': 'left', 'offset': (0.45, -0.15)
    }
]

for h in hubs:
    # Outer glowing aura
    ax.scatter(h['lon'], h['lat'], s=180, color=h['bg'], alpha=0.35, zorder=5)
    # White ring
    ax.scatter(h['lon'], h['lat'], s=65, color=h['bg'], edgecolors='#FFFFFF', linewidth=1.4, zorder=6)
    
    tx = h['lon'] + h['offset'][0]
    ty = h['lat'] + h['offset'][1]
    ha = h['align']
    
    # Combined label in a clean background pill
    label_text = f"{h['name']}\n{h['npp']} • {h['dist']}"
    ax.text(tx, ty, label_text, color='#FFFFFF', fontsize=7.2, fontweight='bold', ha=ha, va='center',
            bbox=dict(boxstyle="round,pad=0.25", facecolor='#0B132B', edgecolor='#1E293B', lw=0.7),
            zorder=8)

# Extreme Delivery Bottlenecks (Callout arrows)
# 1. Thai Binh 78.0km (pointed to Thai Binh coordinates 106.35, 20.45)
ax.annotate('Thai Binh (78.0km Haul)', xy=(106.35, 20.45), xytext=(107.5, 19.3),
            arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.2, ls='--'),
            fontsize=6.8, fontweight='bold', color='#EF4444',
            bbox=dict(boxstyle="round,pad=0.25", facecolor='#450A0A', edgecolor='#EF4444', lw=0.8), zorder=9)

# 2. Ca Mau 70.6km (pointed to Dam Doi coordinates 105.15, 9.18)
ax.annotate('Ca Mau (70.6km Haul)', xy=(105.15, 9.18), xytext=(102.1, 9.4),
            arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.2, ls='--'),
            fontsize=6.8, fontweight='bold', color='#EF4444',
            bbox=dict(boxstyle="round,pad=0.25", facecolor='#450A0A', edgecolor='#EF4444', lw=0.8), zorder=9)

# 3. Lao Cai Border 86.2km (pointed to Lao Cai coordinates 103.95, 22.48)
ax.annotate('Lao Cai (86.2km Haul)', xy=(103.95, 22.48), xytext=(101.6, 22.1),
            arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.2, ls='--'),
            fontsize=6.8, fontweight='bold', color='#EF4444',
            bbox=dict(boxstyle="round,pad=0.25", facecolor='#450A0A', edgecolor='#EF4444', lw=0.8), zorder=9)

# Proposed 2027 C1 Deployment Diamonds
c1_points = [
    (106.60, 21.35, 'C1 Luc Ngan'),
    (106.35, 20.45, 'C1 Thai Binh'),
    (105.60, 19.00, 'C1 Dien Chau'),
    (103.95, 22.48, 'C1 Lao Cai'),
    (105.18, 21.62, 'C1 Doan Hung'),
    (108.25, 12.90, 'C1 Buon Ho'),
    (106.90, 11.85, 'C1 Phuoc Long'),
    (108.70, 13.20, 'C1 Krong Pa'),
    (106.80, 17.20, 'C1 Le Thuy'),
    (106.60, 10.05, 'C1 Ba Tri - Ben Tre'),
    (105.15, 9.18,  'C1 Ca Mau City'),
    (105.30, 9.30,  'C1 Gia Rai'),
    (104.48, 10.38, 'C1 Ha Tien')
]

for cx, cy, c_lbl in c1_points:
    ax.scatter(cx, cy, marker='D', s=26, color='#38BDF8', edgecolors='#0B132B', linewidth=1.0, zorder=7)

# Legend Card at Bottom
legend_box = FancyBboxPatch((101.6, 8.05), 8.8, 0.95, boxstyle="round,pad=0.15",
                            facecolor='#141E33', edgecolor='#334155', linewidth=1, zorder=10)
ax.add_patch(legend_box)

ax.scatter(102.0, 8.7, s=35, color='#16A34A', edgecolors='#FFFFFF', linewidth=0.8, zorder=11)
ax.text(102.25, 8.62, 'Optimal Density (≤10km)', color='#E2E8F0', fontsize=6.5, zorder=11)

ax.scatter(104.9, 8.7, s=35, color='#0284C7', edgecolors='#FFFFFF', linewidth=0.8, zorder=11)
ax.text(105.15, 8.62, 'Moderate Distance (10-15km)', color='#E2E8F0', fontsize=6.5, zorder=11)

ax.scatter(108.0, 8.7, s=35, color='#DC2626', edgecolors='#FFFFFF', linewidth=0.8, zorder=11)
ax.text(108.25, 8.62, 'Friction (>19km)', color='#E2E8F0', fontsize=6.5, zorder=11)

ax.scatter(102.0, 8.3, marker='D', s=25, color='#38BDF8', edgecolors='#0B132B', linewidth=0.8, zorder=11)
ax.text(102.25, 8.22, '2027 C1 Deployment (White Space Reach & FCL Drop)', color='#38BDF8', fontsize=6.2, fontweight='bold', zorder=11)

plt.tight_layout()
out_path = r'd:\SE_Project\RTM_Model\vietnam_rtm_spatial_map.png'
plt.savefig(out_path, dpi=300, facecolor='#0B132B', bbox_inches='tight', pad_inches=0.1)
print(f'Successfully re-rendered polished Vietnam WGS84 map to {out_path}')
