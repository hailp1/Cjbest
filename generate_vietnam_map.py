import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set figure size and dark executive aesthetic
fig, ax = plt.subplots(figsize=(6.2, 8.8), dpi=300, facecolor='#0F172A')
ax.set_facecolor('#0F172A')

# Hide axes ticks and spines
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Coordinate space: Longitude 101.5 to 110.5, Latitude 8.0 to 24.0
ax.set_xlim(101.8, 110.8)
ax.set_ylim(7.8, 24.2)

# Grid / Coordinate lines subtle
for lat in range(10, 24, 2):
    ax.axhline(lat, color='#1E293B', linestyle='--', linewidth=0.5, alpha=0.7)
for lon in range(102, 111, 2):
    ax.axvline(lon, color='#1E293B', linestyle='--', linewidth=0.5, alpha=0.7)

# Accurate stylized Vietnam Coastline & Border Polygon Coordinates (Lon, Lat)
vn_coords = [
    (102.15, 22.40), # Dien Bien / Lai Chau NW border
    (103.50, 22.60), # Lao Cai border
    (104.50, 23.35), # Ha Giang northern tip
    (105.30, 23.38), # Dong Van
    (106.30, 22.90), # Cao Bang
    (106.70, 21.60), # Lang Son
    (107.95, 21.50), # Mong Cai
    (107.50, 20.90), # Ha Long Bay
    (106.70, 20.85), # Hai Phong
    (106.35, 20.25), # Nam Dinh / Ninh Binh
    (105.80, 19.80), # Thanh Hoa
    (105.70, 18.70), # Nghe An - Vinh
    (106.30, 17.90), # Ha Tinh - Ky Anh
    (106.60, 17.50), # Dong Hoi
    (107.20, 16.80), # Quang Tri
    (107.60, 16.50), # Hue
    (108.20, 16.05), # Da Nang
    (108.80, 15.40), # Quang Nam / Quang Ngai
    (109.10, 14.40), # Binh Dinh - Quy Nhon
    (109.30, 13.10), # Phu Yen - Tuy Hoa
    (109.25, 12.25), # Khanh Hoa - Nha Trang
    (109.00, 11.55), # Ninh Thuan - Phan Rang
    (108.10, 10.95), # Binh Thuan - Phan Thiet
    (107.20, 10.35), # Vung Tau
    (106.70, 10.25), # Can Gio / Tien Giang
    (106.60, 9.95),  # Ben Tre coast
    (106.50, 9.50),  # Tra Vinh coast
    (105.70, 9.00),  # Bac Lieu coast
    (105.30, 8.60),  # Ca Mau southern cape (Mui Ca Mau)
    (104.80, 8.85),  # Ca Mau West coast
    (104.95, 9.80),  # Rach Gia / Kien Giang
    (104.45, 10.40), # Ha Tien border
    (105.10, 10.80), # An Giang / Chau Doc
    (105.90, 10.95), # Dong Thap / Moc Hoa
    (106.20, 11.40), # Tay Ninh border
    (106.90, 11.80), # Binh Phuoc border
    (107.50, 12.20), # Dak Nong border
    (107.60, 13.50), # Gia Lai border
    (107.50, 14.70), # Kon Tum border
    (107.40, 16.10), # A Luoi / Hue border
    (106.50, 16.80), # Quang Tri border
    (105.80, 17.80), # Quang Binh border
    (105.20, 18.40), # Ha Tinh border
    (104.20, 19.30), # Nghe An western border
    (104.80, 20.60), # Thanh Hoa / Son La border
    (103.80, 21.30), # Son La
    (102.80, 21.80), # Dien Bien
]

vn_polygon = patches.Polygon(vn_coords, closed=True, facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.8, zorder=2)
ax.add_patch(vn_polygon)

# Interior territory subtle shading
vn_inner = patches.Polygon(vn_coords, closed=True, facecolor='#0284C7', alpha=0.08, zorder=3)
ax.add_patch(vn_inner)

# Phu Quoc Island
pq_polygon = patches.Polygon([(103.90, 10.15), (104.05, 10.40), (103.95, 10.45), (103.85, 10.25)],
                             closed=True, facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.2, zorder=2)
ax.add_patch(pq_polygon)
ax.text(103.2, 10.25, 'Phú Quốc', color='#94A3B8', fontsize=6.5, style='italic', zorder=4)

# Header Title Block on Map
ax.text(102.2, 23.8, 'VIETNAM RTM NETWORK', color='#38BDF8', fontsize=11, fontweight='bold', zorder=10)
ax.text(102.2, 23.35, '215 Active Distributors • 2026 Baseline', color='#E2E8F0', fontsize=8, fontweight='medium', zorder=10)

# Regional Hubs Data
hubs = [
    {
        'name': 'HANOI & NW', 'lon': 105.85, 'lat': 21.03, 'npp': '43 Distributors', 'dist': '12.6 km',
        'color': '#38BDF8', 'bg': '#0284C7', 'align': 'right', 'offset': (-0.35, 0.25),
        'status': 'Moderate'
    },
    {
        'name': 'HAI PHONG & NE', 'lon': 106.68, 'lat': 20.85, 'npp': '38 Distributors', 'dist': '21.3 km avg',
        'color': '#F87171', 'bg': '#DC2626', 'align': 'left', 'offset': (0.35, -0.05),
        'status': 'Severe Friction (45.6% drops >45km)'
    },
    {
        'name': 'DA NANG & CENTRAL', 'lon': 108.20, 'lat': 16.05, 'npp': '16 Distributors', 'dist': '10.1 km',
        'color': '#38BDF8', 'bg': '#0284C7', 'align': 'left', 'offset': (0.35, 0.0),
        'status': 'Hai Van Pass Friction'
    },
    {
        'name': 'NHA TRANG & HIGH.', 'lon': 109.19, 'lat': 12.24, 'npp': '57 Distributors', 'dist': '11.8 km',
        'color': '#FBBF24', 'bg': '#D97706', 'align': 'left', 'offset': (0.35, -0.15),
        'status': 'Mountainous Terrain'
    },
    {
        'name': 'HO CHI MINH CITY', 'lon': 106.63, 'lat': 10.82, 'npp': '35 Distributors', 'dist': '6.2 km (Optimal)',
        'color': '#4ADE80', 'bg': '#16A34A', 'align': 'right', 'offset': (-0.35, 0.25),
        'status': 'High Outlet Density'
    },
    {
        'name': 'CAN THO & MEKONG', 'lon': 105.78, 'lat': 10.04, 'npp': '26 Distributors', 'dist': '19.4 km avg',
        'color': '#F87171', 'bg': '#DC2626', 'align': 'left', 'offset': (0.35, -0.25),
        'status': 'Severe Friction (33.9% drops >45km)'
    }
]

for h in hubs:
    # Outer glow
    ax.scatter(h['lon'], h['lat'], s=140, color=h['bg'], alpha=0.4, zorder=5)
    # Core pin
    ax.scatter(h['lon'], h['lat'], s=55, color=h['bg'], edgecolors='#FFFFFF', linewidth=1.2, zorder=6)
    
    # Text annotation box
    tx = h['lon'] + h['offset'][0]
    ty = h['lat'] + h['offset'][1]
    ha = h['align']
    
    ax.text(tx, ty + 0.18, h['name'], color='#FFFFFF', fontsize=7.8, fontweight='bold', ha=ha, zorder=7)
    ax.text(tx, ty - 0.08, f"{h['npp']} • {h['dist']}", color=h['color'], fontsize=6.8, fontweight='bold', ha=ha, zorder=7)

# Extreme Route Breakout Lines & Callouts (Severe Hotspots)
# 1. Thai Binh 78km
ax.annotate('Thai Binh (78.0km)', xy=(106.68, 20.85), xytext=(108.3, 20.1),
            arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.2, ls='--'),
            fontsize=6.8, fontweight='bold', color='#EF4444',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#450A0A', edgecolor='#EF4444', lw=0.8), zorder=8)

# 2. Ca Mau 70.6km
ax.annotate('Ca Mau (70.6km)', xy=(105.15, 9.18), xytext=(102.5, 8.8),
            arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.2, ls='--'),
            fontsize=6.8, fontweight='bold', color='#EF4444',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#450A0A', edgecolor='#EF4444', lw=0.8), zorder=8)

# 3. Lao Cai Border 86.2km
ax.annotate('Lao Cai (86.2km)', xy=(103.95, 22.48), xytext=(102.0, 21.6),
            arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.2, ls='--'),
            fontsize=6.8, fontweight='bold', color='#EF4444',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#450A0A', edgecolor='#EF4444', lw=0.8), zorder=8)

# Plot 2027 Key Tier-1 Sub-Hub Deployments (White Space Coverage)
c1_points = [
    (106.60, 21.35, 'Sub-Hub Luc Ngan'),
    (106.35, 20.45, 'Sub-Hub Thai Binh'),
    (105.60, 19.00, 'Sub-Hub Dien Chau'),
    (103.95, 22.48, 'Sub-Hub Lao Cai'),
    (108.25, 12.90, 'Sub-Hub Buon Ho'),
    (106.60, 10.05, 'Sub-Hub Ba Tri'),
    (105.15, 9.18,  'Sub-Hub Ca Mau'),
    (105.30, 9.30,  'Sub-Hub Gia Rai'),
    (104.48, 10.38, 'Sub-Hub Ha Tien')
]

for cx, cy, c_lbl in c1_points:
    ax.scatter(cx, cy, marker='D', s=24, color='#38BDF8', edgecolors='#0F172A', linewidth=0.8, zorder=9)

# Legend Box at Bottom
legend_box = patches.FancyBboxPatch((102.2, 7.95), 8.4, 0.95, boxstyle="round,pad=0.15",
                                    facecolor='#1E293B', edgecolor='#334155', linewidth=1, zorder=9)
ax.add_patch(legend_box)

ax.scatter(102.6, 8.6, s=35, color='#16A34A', edgecolors='#FFFFFF', linewidth=0.8, zorder=10)
ax.text(102.85, 8.52, 'Optimal (≤10km)', color='#E2E8F0', fontsize=6.5, zorder=10)

ax.scatter(105.1, 8.6, s=35, color='#0284C7', edgecolors='#FFFFFF', linewidth=0.8, zorder=10)
ax.text(105.35, 8.52, 'Moderate (10-15km)', color='#E2E8F0', fontsize=6.5, zorder=10)

ax.scatter(107.8, 8.6, s=35, color='#DC2626', edgecolors='#FFFFFF', linewidth=0.8, zorder=10)
ax.text(108.05, 8.52, 'Friction (>19km)', color='#E2E8F0', fontsize=6.5, zorder=10)

ax.scatter(102.6, 8.2, marker='D', s=25, color='#38BDF8', edgecolors='#0F172A', linewidth=0.8, zorder=10)
ax.text(102.85, 8.12, '2027 Tier-1 Sub-Hub Deployment (White Space Reach & Remote Drop Elimination)', color='#38BDF8', fontsize=6.2, fontweight='bold', zorder=10)

plt.tight_layout()
out_path = r'd:\SE_Project\RTM_Model\vietnam_rtm_spatial_map.png'
plt.savefig(out_path, dpi=300, facecolor='#0F172A', bbox_inches='tight', pad_inches=0.1)
print(f'Successfully rendered executive spatial map to {out_path}')
