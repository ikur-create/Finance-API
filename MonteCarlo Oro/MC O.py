"""
Monte Carlo - Simulación de Regímenes del Oro
Requiere: pip install yfinance pandas numpy matplotlib scipy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────
# 1. DESCARGA DE DATOS REALES
# ──────────────────────────────────────────────

def descargar_datos(ticker="GC=F", start="2010-01-01", end=None):
    """
    Descarga precios históricos del oro.
    Tickers útiles:
      GC=F  → Futuros del oro (COMEX) - recomendado
      GLD   → ETF SPDR Gold Shares
      IAU   → ETF iShares Gold Trust
    """
    print(f"📥 Descargando datos de {ticker}...")
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    df = df["Close"].squeeze().dropna()  # squeeze() colapsa cualquier dimensión extra
    df.name = "Precio"
    print(f"   ✅ {len(df)} sesiones descargadas ({df.index[0].date()} → {df.index[-1].date()})")
    return df


# ──────────────────────────────────────────────
# 2. CÁLCULO DE RETORNOS Y ESTADÍSTICAS
# ──────────────────────────────────────────────

def calcular_retornos(precios):
    """Retornos diarios logarítmicos (más estables que aritméticos)."""
    retornos = np.log(precios / precios.shift(1)).dropna()
    return retornos


def estadisticas(retornos):
    """Estadísticas descriptivas completas."""
    r = retornos.values.flatten()
    media       = np.mean(r)
    std         = np.std(r, ddof=1)
    skewness    = float(stats.skew(r))
    kurt        = float(stats.kurtosis(r))   # curtosis en exceso (normal=0)
    var_95      = np.percentile(r, 5)
    cvar_95     = r[r <= var_95].mean()
    sharpe_ann  = (media / std) * np.sqrt(252)

    print("\n📊 ESTADÍSTICAS DE RETORNOS DIARIOS")
    print("─" * 42)
    print(f"  Observaciones  : {len(r):>10,}")
    print(f"  Media diaria   : {media*100:>10.4f}%")
    print(f"  Vol. diaria    : {std*100:>10.4f}%")
    print(f"  Vol. anual     : {std*np.sqrt(252)*100:>10.2f}%")
    print(f"  Skewness       : {skewness:>10.4f}")
    print(f"  Curtosis exc.  : {kurt:>10.4f}  {'⚠ fat tails' if kurt > 1 else ''}")
    print(f"  VaR 95% diario : {var_95*100:>10.4f}%")
    print(f"  CVaR 95%       : {cvar_95*100:>10.4f}%")
    print(f"  Sharpe anual.  : {sharpe_ann:>10.4f}")
    return {"media": media, "std": std, "skewness": skewness, "kurtosis": kurt,
            "var95": var_95, "cvar95": cvar_95}


def analizar_umbrales(retornos):
    """Cuenta subidas/caídas para cada umbral de magnitud."""
    umbrales = [0.01, 0.02, 0.05, 0.10, 0.15, 0.20]
    r = retornos.values
    n = len(r)

    print("\n📈 FRECUENCIA DE MOVIMIENTOS POR UMBRAL")
    print(f"{'Umbral':>8} │ {'Subidas':>8} {'%Días':>7} │ {'Caídas':>8} {'%Días':>7}")
    print("─" * 50)
    rows = []
    for t in umbrales:
        ups   = np.sum(r >=  t)
        downs = np.sum(r <= -t)
        rows.append({"umbral": t, "subidas": ups, "pct_sub": ups/n*100,
                     "caidas": downs, "pct_cai": downs/n*100})
        print(f"  {t*100:>4.0f}%  │ {ups:>8,} {ups/n*100:>6.2f}% │ {downs:>8,} {downs/n*100:>6.2f}%")
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────
# 3. SIMULACIÓN MONTE CARLO (BOOTSTRAP)
# ──────────────────────────────────────────────

def simular_monte_carlo(retornos, precio_inicial, n_paths=1000, horizonte=252, seed=42):
    """
    Bootstrap no paramétrico: resamplea retornos históricos reales.
    Preserva fat tails, asimetría y distribución empírica real.
    """
    rng = np.random.default_rng(seed)
    r   = retornos.values.flatten()
    # Matriz de índices aleatorios: shape (horizonte, n_paths)
    idx     = rng.integers(0, len(r), size=(horizonte, n_paths))
    ret_sim = r[idx]                              # retornos sorteados
    # Precio acumulado: price_0 * exp(sum de log-retornos)
    log_cum = np.vstack([np.zeros(n_paths), np.cumsum(ret_sim, axis=0)])
    precios = precio_inicial * np.exp(log_cum)    # shape (horizonte+1, n_paths)
    return precios


def calcular_percentiles(matriz_precios):
    """Percentiles día a día sobre todas las trayectorias."""
    pcts = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    df = pd.DataFrame(
        np.percentile(matriz_precios, pcts, axis=1).T,
        columns=[f"P{p}" for p in pcts]
    )
    df.index.name = "dia"
    return df


def resumen_final(matriz_precios, precio_inicial):
    """Estadísticas del precio final simulado."""
    precios_finales = matriz_precios[-1, :]
    retorno_total   = precios_finales / precio_inicial - 1

    print("\n🎯 DISTRIBUCIÓN DEL PRECIO FINAL SIMULADO")
    print("─" * 42)
    for p, label in [(1,"P1 (extremo bajista)"), (5,"P5"), (10,"P10"),
                     (25,"P25"), (50,"Mediana"), (75,"P75"),
                     (90,"P90"), (95,"P95"), (99,"P99 (extremo alcista)")]:
        v = np.percentile(precios_finales, p)
        r = v / precio_inicial - 1
        print(f"  {label:<22}: ${v:>9.2f}  ({r*100:>+.1f}%)")
    prob_ganancia = np.mean(precios_finales > precio_inicial) * 100
    print(f"\n  Prob. de ganancia  : {prob_ganancia:.1f}%")
    print(f"  Prob. pérdida >20% : {np.mean(retorno_total < -0.20)*100:.1f}%")
    print(f"  Prob. ganancia >20%: {np.mean(retorno_total >  0.20)*100:.1f}%")


# ──────────────────────────────────────────────
# 4. VISUALIZACIÓN
# ──────────────────────────────────────────────

def plot_todo(precios_hist, retornos, df_umbrales, matriz_mc, df_pct, horizonte):
    fig = plt.figure(figsize=(18, 14), facecolor="#0f172a")
    fig.suptitle("🥇 Monte Carlo — Simulación de Regímenes del Oro",
                 fontsize=17, color="white", fontweight="bold", y=0.98)

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)
    DARK  = "#0f172a"
    PANEL = "#1e293b"
    GRID  = "#334155"
    TEXT  = "#94a3b8"

    def style_ax(ax, title):
        ax.set_facecolor(PANEL)
        ax.spines[:].set_color(GRID)
        ax.tick_params(colors=TEXT, labelsize=9)
        ax.set_title(title, color="white", fontsize=10, fontweight="bold", pad=8)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.grid(color=GRID, linewidth=0.5, alpha=0.7)

    # ── Plot 1: Precio histórico ──
    ax1 = fig.add_subplot(gs[0, :2])
    ph = precios_hist.values.flatten()
    ax1.plot(precios_hist.index, ph, color="#6366f1", linewidth=1.2)
    ax1.fill_between(precios_hist.index, ph, ph.min(), alpha=0.15, color="#6366f1")
    style_ax(ax1, "Precio Histórico del Oro (USD)")

    # ── Plot 2: Histograma retornos ──
    ax2 = fig.add_subplot(gs[0, 2])
    r = retornos.values.flatten() * 100
    ax2.hist(r, bins=80, color="#6366f1", alpha=0.8, density=True, edgecolor="none")
    xr = np.linspace(r.min(), r.max(), 300)
    ax2.plot(xr, stats.norm.pdf(xr, r.mean(), r.std()), color="#f59e0b",
             linewidth=1.5, label="Normal teórica")
    ax2.legend(fontsize=8, labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID)
    style_ax(ax2, "Distribución de Retornos Diarios (%)")

    # ── Plot 3: Frecuencia por umbral ──
    ax3 = fig.add_subplot(gs[1, 0])
    x   = np.arange(len(df_umbrales))
    w   = 0.35
    ax3.bar(x - w/2, df_umbrales["pct_sub"], w, label="Subidas", color="#10b981", alpha=0.85)
    ax3.bar(x + w/2, df_umbrales["pct_cai"], w, label="Caídas",  color="#ef4444", alpha=0.85)
    ax3.set_xticks(x)
    ax3.set_xticklabels([f"{int(t*100)}%" for t in df_umbrales["umbral"]])
    ax3.set_ylabel("% de días")
    ax3.legend(fontsize=8, labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID)
    style_ax(ax3, "Frecuencia de Movimientos")

    # ── Plot 4: QQ-plot ──
    ax4 = fig.add_subplot(gs[1, 1])
    (osm, osr), (slope, intercept, _) = stats.probplot(retornos.values.flatten(), dist="norm")
    ax4.scatter(osm, osr, color="#6366f1", s=3, alpha=0.5)
    ax4.plot(osm, slope * np.array(osm) + intercept, color="#f59e0b", linewidth=1.5)
    ax4.set_xlabel("Cuantiles teóricos (Normal)")
    ax4.set_ylabel("Cuantiles observados")
    style_ax(ax4, "QQ-Plot (fat tails visibles en extremos)")

    # ── Plot 5: Rolling volatility ──
    ax5 = fig.add_subplot(gs[1, 2])
    vol_roll = retornos.rolling(21).std() * np.sqrt(252) * 100
    ax5.plot(vol_roll.index, vol_roll.values.flatten(), color="#f59e0b", linewidth=1)
    ax5.fill_between(vol_roll.index, vol_roll.values.flatten(), alpha=0.2, color="#f59e0b")
    ax5.set_ylabel("Vol. anualizada (%)")
    style_ax(ax5, "Volatilidad Rodante 21 días (Anualizada)")

    # ── Plot 6: Trayectorias MC ──
    ax6 = fig.add_subplot(gs[2, :2])
    dias = np.arange(horizonte + 1)
    n_show = min(200, matriz_mc.shape[1])
    colors = ["#ef4444","#f59e0b","#6366f1","#10b981","#8b5cf6","#ec4899","#14b8a6"]
    for i in range(n_show):
        ax6.plot(dias, matriz_mc[:, i], linewidth=0.4, alpha=0.25,
                 color=colors[i % len(colors)])
    ax6.plot(dias, df_pct["P50"].values,  color="white",   linewidth=2,   label="Mediana")
    ax6.plot(dias, df_pct["P95"].values,  color="#10b981", linewidth=1.8, label="P95", linestyle="--")
    ax6.plot(dias, df_pct["P5"].values,   color="#ef4444", linewidth=1.8, label="P5",  linestyle="--")
    ax6.legend(fontsize=9, labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID)
    ax6.set_xlabel(f"Días (horizonte = {horizonte})")
    ax6.set_ylabel("Precio (USD)")
    style_ax(ax6, f"Trayectorias Monte Carlo ({matriz_mc.shape[1]:,} simulaciones)")

    # ── Plot 7: Distribución precio final ──
    ax7 = fig.add_subplot(gs[2, 2])
    pf = matriz_mc[-1, :]
    ax7.hist(pf, bins=80, color="#6366f1", alpha=0.85, orientation="horizontal",
             edgecolor="none", density=True)
    for p, c, lbl in [(5,"#ef4444","P5"), (50,"white","P50"), (95,"#10b981","P95")]:
        v = np.percentile(pf, p)
        ax7.axhline(v, color=c, linewidth=1.5, linestyle="--")
        ax7.text(ax7.get_xlim()[1]*0.05 if ax7.get_xlim()[1] > 0 else 0.001,
                 v, f" {lbl}: ${v:.0f}", color=c, va="bottom", fontsize=8)
    ax7.set_xlabel("Densidad")
    ax7.set_ylabel("Precio final (USD)")
    style_ax(ax7, "Distribución del Precio Final")

    plt.savefig("monte_carlo_oro.png", dpi=150, bbox_inches="tight",
                facecolor=DARK, edgecolor="none")
    print("\n💾 Gráfico guardado como 'monte_carlo_oro.png'")
    plt.show()


# ──────────────────────────────────────────────
# 5. MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":

    # ── Parámetros configurables ──────────────
    TICKER          = "GC=F"       # Futuros oro. Alternativa: "GLD"
    FECHA_INICIO    = "2010-01-01"
    N_SIMULACIONES  = 1000         # Número de trayectorias
    HORIZONTE_DIAS  = 252          # 252 ≈ 1 año bursátil
    SEED            = 42
    # ─────────────────────────────────────────

    # 1. Datos
    precios  = descargar_datos(TICKER, start=FECHA_INICIO)
    retornos = calcular_retornos(precios)

    # 2. Análisis estadístico
    stats_dict  = estadisticas(retornos)
    df_umbrales = analizar_umbrales(retornos)

    # 3. Simulación
    precio_hoy = float(precios.iloc[-1].item() if hasattr(precios.iloc[-1], 'item') else precios.iloc[-1])
    print(f"\n🚀 Simulando {N_SIMULACIONES:,} trayectorias × {HORIZONTE_DIAS} días "
          f"desde ${precio_hoy:,.2f}...")

    matriz_mc  = simular_monte_carlo(retornos, precio_hoy,
                                     n_paths=N_SIMULACIONES,
                                     horizonte=HORIZONTE_DIAS,
                                     seed=SEED)
    df_pct = calcular_percentiles(matriz_mc)

    # 4. Resumen en consola
    resumen_final(matriz_mc, precio_hoy)

    # 5. Gráficos
    plot_todo(precios, retornos, df_umbrales, matriz_mc, df_pct, HORIZONTE_DIAS)
