import yfinance as yf
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import numpy as np

# ── Theme ──────────────────────────────────────────────────────────────────────
BG        = '#0d0d0d'
PANEL     = '#141414'
GRID      = '#1e1e1e'
TEXT      = '#e8e8e8'
SUBTEXT   = '#808080'
GOLD      = '#D4A843'
SILVER    = '#9BAAB5'
OIL       = '#4A90D9'
OIL_INV   = '#6EC6E6'
ZERO_LINE = '#3a3a3a'

plt.rcParams.update({
    'font.family':       'Comfortaa',
    'text.color':        TEXT,
    'axes.labelcolor':   SUBTEXT,
    'xtick.color':       SUBTEXT,
    'ytick.color':       SUBTEXT,
    'axes.edgecolor':    GRID,
    'figure.facecolor':  BG,
    'axes.facecolor':    PANEL,
    'axes.grid':         True,
    'grid.color':        GRID,
    'grid.linewidth':    0.6,
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.spines.left':  False,
    'axes.spines.bottom':False,
    'xtick.major.size':  0,
    'ytick.major.size':  0,
    'legend.facecolor':  PANEL,
    'legend.edgecolor':  GRID,
    'legend.framealpha': 0.9,
})

# ── Data ───────────────────────────────────────────────────────────────────────
tickers = ['GC=F', 'SI=F', 'CL=F']
data = yf.download(tickers, start='2019-01-01', end='2026-05-01')['Close']
normalized = data / data.iloc[-1]
inverse_wti = 2 - normalized['CL=F']

monthly_corr_wti = (
    data.groupby(pd.Grouper(freq='ME'))
        .apply(lambda x: x['GC=F'].corr(x['CL=F']))
        .dropna()
)
monthly_corr_gs = (
    data.groupby(pd.Grouper(freq='ME'))
        .apply(lambda x: x['GC=F'].corr(x['SI=F']))
        .dropna()
)

# ── Layout ─────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 24))
fig.patch.set_facecolor(BG)

gs = GridSpec(
    4, 1,
    figure=fig,
    top=0.935, bottom=0.045,
    left=0.07, right=0.96,
    hspace=0.55,
)
axes = [fig.add_subplot(gs[i]) for i in range(4)]


# ── Shared x-axis formatter ────────────────────────────────────────────────────
def style_xaxis(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.tick_params(axis='x', rotation=0, labelsize=8, colors=SUBTEXT, pad=4)
    ax.tick_params(axis='y', labelsize=8, colors=SUBTEXT)

def add_legend(ax, **kw):
    leg = ax.legend(
        frameon=True, fontsize=8, loc='upper left',
        labelcolor=TEXT, handlelength=1.6, handletextpad=0.5, **kw
    )
    leg.get_frame().set_linewidth(0.4)

def shade_fill(ax, x, y1, y2, color, alpha=0.07):
    ax.fill_between(x, y1, y2, color=color, alpha=alpha)

# ── Subplot 0: All three normalized ────────────────────────────────────────────
ax = axes[0]
ax.plot(normalized.index, normalized['GC=F'], color=GOLD,   lw=1.8, label='Gold')
ax.plot(normalized.index, normalized['SI=F'], color=SILVER, lw=1.8, label='Silver')
ax.plot(normalized.index, normalized['CL=F'], color=OIL,    lw=1.8, label='WTI Crude')
shade_fill(ax, normalized.index, normalized['GC=F'], 0, GOLD)
ax.set_title('All Three Assets — Normalized to Latest Close', fontsize=10, fontweight='bold',
             color=TEXT, loc='left', pad=8)
ax.set_ylabel('Norm. Price', fontsize=8)
add_legend(ax)
style_xaxis(ax)

# ── Subplot 1: Gold vs Silver ──────────────────────────────────────────────────
ax = axes[1]
ax.plot(normalized.index, normalized['GC=F'], color=GOLD,   lw=1.8, label='Gold')
ax.plot(normalized.index, normalized['SI=F'], color=SILVER, lw=1.8, label='Silver', linestyle='--')
shade_fill(ax, normalized.index, normalized['GC=F'], normalized['SI=F'], GOLD, alpha=0.05)
ax.set_title('Gold vs Silver — Co-movement', fontsize=10, fontweight='bold',
             color=TEXT, loc='left', pad=8)
ax.set_ylabel('Norm. Price', fontsize=8)
add_legend(ax)
style_xaxis(ax)

# ── Subplot 2: Gold vs Inverse WTI ────────────────────────────────────────────
ax = axes[2]
ax.plot(normalized.index, normalized['GC=F'], color=GOLD,    lw=1.8, label='Gold')
ax.plot(normalized.index, inverse_wti,        color=OIL_INV, lw=1.8, label='Inverse WTI', linestyle=':')
shade_fill(ax, normalized.index, normalized['GC=F'], inverse_wti, GOLD, alpha=0.04)
ax.set_title('Gold vs Inverse WTI Crude — Divergence Signal', fontsize=10, fontweight='bold',
             color=TEXT, loc='left', pad=8)
ax.set_ylabel('Norm. Price', fontsize=8)
add_legend(ax)
style_xaxis(ax)

# ── Subplot 3: Monthly correlations ───────────────────────────────────────────
ax = axes[3]

# Positive/negative coloring for WTI correlation
x_wti = monthly_corr_wti.index
y_wti = monthly_corr_wti.values
ax.fill_between(x_wti, 0, y_wti, where=(y_wti >= 0), color=OIL,    alpha=0.15, interpolate=True)
ax.fill_between(x_wti, 0, y_wti, where=(y_wti < 0),  color='#c0392b', alpha=0.12, interpolate=True)
ax.plot(x_wti, y_wti, color=OIL, lw=1.5, label='Gold vs WTI Crude')

ax.plot(monthly_corr_gs.index, monthly_corr_gs.values,
        color=SILVER, lw=1.5, linestyle='--', label='Gold vs Silver')

ax.axhline(0, color=ZERO_LINE, lw=0.9, linestyle='-')
ax.axhline( 0.5, color=GRID, lw=0.6, linestyle=':')
ax.axhline(-0.5, color=GRID, lw=0.6, linestyle=':')
ax.set_ylim(-1.05, 1.05)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
ax.set_title('Monthly Rolling Correlation', fontsize=10, fontweight='bold',
             color=TEXT, loc='left', pad=8)
ax.set_ylabel('Correlation', fontsize=8)
ax.set_xlabel('Date', fontsize=8)
add_legend(ax)
style_xaxis(ax)

# ── Watermark ──────────────────────────────────────────────────────────────────
fig.text(
    0.96, 0.03, 'source: yfinance',
    fontsize=7, color='#333333', ha='right', va='bottom', fontfamily='Comfortaa',
)

plt.show()

# ── Correlation matrix ─────────────────────────────────────────────────────────
correlation = data.corr()
print("\nCorrelation Matrix:")
print(correlation.rename(columns={'GC=F': 'Gold', 'SI=F': 'Silver', 'CL=F': 'WTI'})
                 .rename(index={'GC=F': 'Gold', 'SI=F': 'Silver', 'CL=F': 'WTI'})
                 .round(4))