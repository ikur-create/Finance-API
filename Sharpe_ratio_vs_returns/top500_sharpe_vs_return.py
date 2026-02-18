import requests
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def fetch_and_save_sp500():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        # 1. Leemos la tabla completa
        table = pd.read_html(resp.text)[0]

        # 2. Limpiamos los símbolos para yfinance (opcional, pero útil)
        table['Symbol'] = table['Symbol'].astype(str).str.replace('.', '-', regex=False)

        # 3. GUARDAR EN ARCHIVO DE TEXTO
        with open('sp500_info.txt', 'w', encoding='utf-8') as f:
            f.write("LISTADO COMPLETO S&P 500 - WIKIPEDIA\n")
            f.write("=" * 50 + "\n\n")
            f.write(table.to_string(index=False))

        print("¡Hecho! Se ha creado el archivo 'sp500_info.txt' con toda la información.")

        # Retornamos la lista de símbolos por si la necesitas luego
        return table['Symbol'].tolist()

    except Exception as e:
        print(f"Error: {e}")
        return []

from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_ticker_metrics(sym):
    """Fetch metrics for a single ticker. Returns dict or None."""
    try:
        tk = yf.Ticker(sym)
        info = tk.info if hasattr(tk, 'info') else {}
        market_cap = info.get('marketCap', 0) or 0

        hist = tk.history(period='1y')
        if hist is None or hist.empty:
            print(f"  - No historical data for {sym}, skipping.")
            return None

        returns = hist['Close'].pct_change().dropna()
        avg_return = returns.mean() * 252
        vol = returns.std() * np.sqrt(252)
        sharpe = avg_return / vol if vol != 0 else 0

        print(f"  ✓ {sym}: market_cap={market_cap:,}  return={avg_return:.2%}  sharpe={sharpe:.2f}")

        return {
            'symbol': sym,
            'market_cap': market_cap,
            'average_return': avg_return,
            'sharpe_ratio': sharpe,
        }
    except Exception as e:
        print(f"  - Error fetching {sym}: {e}")
        return None


def compute_metrics_and_plot(tickers, limit=None, out_path='sp500_sharpe_vs_return.png', max_workers=20):
    tickers = tickers[:limit] if limit else tickers
    total = len(tickers)
    print(f"Collecting metrics for {total} tickers with {max_workers} workers...")

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_ticker_metrics, sym): sym for sym in tickers}
        for i, future in enumerate(as_completed(futures), 1):
            print(f"[{i}/{total}] completed")
            result = future.result()
            if result:
                results.append(result)

    if not results:
        print("No valid ticker data collected, aborting plot.")
        return

    df = pd.DataFrame(results).sort_values('market_cap', ascending=False)

    # --- GRÁFICO ---
    sns.set(style='whitegrid')
    fig, ax = plt.subplots(figsize=(14, 8))

    # Tamaño del punto proporcional al market cap
    sizes = (df['market_cap'] / df['market_cap'].max() * 800).clip(lower=30)

    scatter = ax.scatter(
        df['average_return'],
        df['sharpe_ratio'],
        s=sizes,
        c=df['sharpe_ratio'],
        cmap='RdYlGn',
        alpha=0.7,
        edgecolors='grey',
        linewidths=0.5
    )

    # Etiquetas solo para el top 20 por market cap
    for _, row in df.head(20).iterrows():
        ax.annotate(
            row['symbol'],
            (row['average_return'], row['sharpe_ratio']),
            textcoords='offset points',
            xytext=(6, 6),
            fontsize=7,
            ha='left'
        )

    # Líneas de referencia
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)

    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Sharpe Ratio', fontsize=10)

    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
    ax.set_xlabel('Annualized Average Return (1Y)', fontsize=12)
    ax.set_ylabel('Sharpe Ratio', fontsize=12)
    ax.set_title('S&P 500: Sharpe Ratio vs Annualized Return\n Size = market cap', fontsize=14)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    print(f"Plot saved to {out_path} ({len(df)} points)")
    plt.show()



if __name__ == '__main__':
    tickers = fetch_and_save_sp500()
    # For quick testing set a small limit, e.g., limit=100
    compute_metrics_and_plot(tickers, limit=None)