# ============================================================
#   Task 3: Data Visualization
#   Tools: Matplotlib & Seaborn
#   Run:   python dashboard.py
# ============================================================

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd
import numpy as np

# ── Dark Theme ──────────────────────────────────────────────
plt.style.use('dark_background')
sns.set_theme(style="darkgrid", palette="muted")

ACCENT  = '#4f8ef7'
GREEN   = '#36d97b'
ORANGE  = '#f7934f'
PURPLE  = '#a78bfa'
PINK    = '#f472b6'
COLORS  = [ACCENT, GREEN, ORANGE, PURPLE, PINK, '#38bdf8']
BG      = '#0d0f14'
CARD    = '#1c2130'

# ── Dataset ─────────────────────────────────────────────────

# 1. Monthly Sales
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']
sales  = [42, 48, 55, 51, 62, 70, 65, 74, 80, 76, 84, 91]
df_sales = pd.DataFrame({'Month': months, 'Revenue': sales})

# 2. Category Sales
categories = ['Electronics','Fashion','Books','Sports','Home','Beauty']
units      = [320, 275, 180, 240, 195, 310]
df_cat = pd.DataFrame({'Category': categories, 'Units': units})

# 3. Traffic Sources
sources = ['Organic\nSearch','Social\nMedia','Direct','Email','Paid\nAds']
traffic = [35, 25, 18, 12, 10]

# 4. Region Data
regions = ['North America','Europe','Asia Pacific','South America','Others']
share   = [42, 28, 18, 8, 4]
df_region = pd.DataFrame({'Region': regions, 'Share': share})

# 5. Transactions
transactions = pd.DataFrame({
    'Product':  ['iPhone 15 Pro','Nike Air Max','Python Book','Smart Watch','Headphones'],
    'Customer': ['Ali Hassan','Sara Khan','Ahmed Raza','Fatima Malik','Usman Ali'],
    'Amount':   [1199, 189, 45, 349, 129],
    'Month':    ['Jun','Jun','Jun','Jun','Jun'],
    'Status':   ['Paid','Paid','Pending','Paid','Paid']
})

# ── Figure Layout ────────────────────────────────────────────
fig = plt.figure(figsize=(18, 14), facecolor=BG)
fig.suptitle('Data Visualization Dashboard',
             fontsize=22, fontweight='bold', color='white', y=0.98)

gs = gridspec.GridSpec(3, 3, figure=fig,
                       hspace=0.45, wspace=0.35,
                       top=0.93, bottom=0.05,
                       left=0.06, right=0.97)

def style_ax(ax, title):
    ax.set_facecolor(CARD)
    ax.set_title(title, color='white', fontsize=12, fontweight='bold', pad=10)
    ax.tick_params(colors='#64748b')
    for spine in ax.spines.values():
        spine.set_edgecolor('#252d3d')

# ── Plot 1: Line Chart – Monthly Sales ──────────────────────
ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, 'Monthly Sales Trend (Revenue in $K)')

ax1.plot(df_sales['Month'], df_sales['Revenue'],
         color=ACCENT, linewidth=2.5, marker='o',
         markersize=6, markerfacecolor=ACCENT)
ax1.fill_between(df_sales['Month'], df_sales['Revenue'],
                 alpha=0.12, color=ACCENT)
ax1.set_ylabel('Revenue ($K)', color='#64748b')
ax1.set_xlabel('')

# Annotate max
max_idx = df_sales['Revenue'].idxmax()
ax1.annotate(f"Peak: ${df_sales['Revenue'][max_idx]}K",
             xy=(max_idx, df_sales['Revenue'][max_idx]),
             xytext=(max_idx - 1.5, df_sales['Revenue'][max_idx] + 4),
             color=GREEN, fontsize=9,
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))

# ── Plot 2: Pie Chart – Traffic Sources ─────────────────────
ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2, 'Traffic Sources')

wedges, texts, autotexts = ax2.pie(
    traffic, labels=sources, colors=COLORS,
    autopct='%1.0f%%', startangle=90,
    wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
    pctdistance=0.75
)
for t in texts:      t.set_color('#94a3b8'); t.set_fontsize(8)
for t in autotexts:  t.set_color('white');   t.set_fontsize(8); t.set_fontweight('bold')

# ── Plot 3: Bar Chart – Sales by Category ───────────────────
ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, 'Sales by Category (Units Sold)')

bars = ax3.bar(df_cat['Category'], df_cat['Units'],
               color=COLORS, edgecolor=BG, linewidth=1.5,
               width=0.6)
ax3.set_ylabel('Units Sold', color='#64748b')

for bar in bars:
    ax3.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 4,
             f'{int(bar.get_height())}',
             ha='center', va='bottom',
             color='white', fontsize=9, fontweight='bold')

ax3.set_ylim(0, max(units) + 50)

# ── Plot 4: Horizontal Bar – Regions ────────────────────────
ax4 = fig.add_subplot(gs[1, 2])
style_ax(ax4, 'Top Regions (%)')

bars_h = ax4.barh(df_region['Region'], df_region['Share'],
                  color=COLORS, edgecolor=BG, linewidth=1, height=0.55)
ax4.set_xlabel('Sales Share (%)', color='#64748b')
ax4.invert_yaxis()

for bar in bars_h:
    ax4.text(bar.get_width() + 0.5,
             bar.get_y() + bar.get_height()/2,
             f'{int(bar.get_width())}%',
             va='center', color='white', fontsize=9, fontweight='bold')

ax4.set_xlim(0, 55)

# ── Plot 5: Seaborn Heatmap – Correlation ───────────────────
ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, 'Seaborn - Sales Heatmap by Month & Category')

np.random.seed(42)
heatmap_data = pd.DataFrame(
    np.random.randint(50, 400, size=(6, 6)),
    index=categories,
    columns=['Jan','Mar','May','Jul','Sep','Nov']
)

sns.heatmap(heatmap_data, ax=ax5, cmap='Blues',
            annot=True, fmt='d', linewidths=0.5,
            linecolor='#0d0f14', cbar_kws={'shrink': 0.8},
            annot_kws={'size': 8, 'color': 'white'})

ax5.set_xlabel('')
ax5.tick_params(axis='x', colors='#94a3b8', labelsize=9)
ax5.tick_params(axis='y', colors='#94a3b8', labelsize=9)

# ── Plot 6: Seaborn Violin – Amount Distribution ─────────────
ax6 = fig.add_subplot(gs[2, 2])
style_ax(ax6, 'Seaborn - Order Amount Distribution')

np.random.seed(0)
order_data = pd.DataFrame({
    'Status': np.random.choice(['Paid','Pending'], 80, p=[0.75, 0.25]),
    'Amount': np.concatenate([
        np.random.normal(300, 120, 60),
        np.random.normal(100, 50, 20)
    ])
})

sns.violinplot(data=order_data, x='Status', y='Amount', hue='Status',
               palette={'Paid': GREEN, 'Pending': ORANGE}, legend=False,
               ax=ax6, inner='quartile', linewidth=1.2)

ax6.set_ylabel('Order Amount ($)', color='#64748b')
ax6.set_xlabel('')

# ── Save & Show ──────────────────────────────────────────────
plt.savefig('dashboard_output.png', dpi=150,
            bbox_inches='tight', facecolor=BG)
print("Dashboard saved as 'dashboard_output.png'")
plt.show()
