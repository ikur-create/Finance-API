import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def fetch_commodity_prices(period="1y"):
    """Fetch historical prices for gold, silver, and WTI crude oil."""
    tickers = {
        'Gold': 'GC=F',
        'Silver': 'SI=F',
        'WTI Crude Oil': 'CL=F'
    }

    print(f"Fetching {period} of historical data...")
    data = {}

    for name, ticker in tickers.items():
        print(f"  Downloading {name} ({ticker})...")
        df = yf.download(ticker, period=period, progress=False)
        data[name] = df['Close']

    prices_df = pd.DataFrame(data)
    return prices_df

def calculate_correlation(prices_df):
    """Calculate correlation matrix between commodities."""
    correlation = prices_df.corr()
    return correlation

def visualize_results(prices_df, correlation):
    """Create visualizations for prices and correlation."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Gold, Silver, and WTI Crude Oil - Correlation Analysis', fontsize=16, fontweight='bold')

    # Normalize prices for comparison
    normalized_prices = (prices_df - prices_df.min()) / (prices_df.max() - prices_df.min())

    # Plot 1: Normalized price trends
    ax1 = axes[0, 0]
    for column in normalized_prices.columns:
        ax1.plot(normalized_prices.index, normalized_prices[column], label=column, linewidth=2)
    ax1.set_title('Normalized Price Trends (0-1 scale)')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Normalized Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Actual prices
    ax2 = axes[0, 1]
    for column in prices_df.columns:
        ax2.plot(prices_df.index, prices_df[column], label=column, linewidth=2)
    ax2.set_title('Actual Prices Over Time')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Price (USD)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: Correlation heatmap
    ax3 = axes[1, 0]
    sns.heatmap(correlation, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax3, vmin=-1, vmax=1)
    ax3.set_title('Correlation Matrix')

    # Plot 4: Correlation statistics
    ax4 = axes[1, 1]
    ax4.axis('off')

    # Create text summary
    summary_text = "Correlation Summary:\n\n"
    corr_pairs = []
    for i in range(len(correlation.columns)):
        for j in range(i+1, len(correlation.columns)):
            col1 = correlation.columns[i]
            col2 = correlation.columns[j]
            corr_value = correlation.iloc[i, j]
            corr_pairs.append((col1, col2, corr_value))
            summary_text += f"{col1} vs {col2}:\n  {corr_value:.4f}\n\n"

    # Interpret correlations
    summary_text += "Interpretation:\n"
    for col1, col2, corr_value in corr_pairs:
        if corr_value > 0.5:
            strength = "Strong positive"
        elif corr_value > 0.2:
            strength = "Moderate positive"
        elif corr_value > -0.2:
            strength = "Weak"
        elif corr_value > -0.5:
            strength = "Moderate negative"
        else:
            strength = "Strong negative"
        summary_text += f"• {strength} correlation\n"

    ax4.text(0.1, 0.95, summary_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
    print("\n✓ Visualization saved as 'correlation_analysis.png'")
    plt.show()

def main():
    print("=" * 60)
    print("Commodity Correlation Analysis (Gold, Silver, Oil WTI)")
    print("=" * 60)

    # Fetch data
    prices_df = fetch_commodity_prices(period="1y")

    # Calculate correlation
    correlation = calculate_correlation(prices_df)

    # Display results
    print("\n" + "=" * 60)
    print("CORRELATION MATRIX")
    print("=" * 60)
    print(correlation.round(4))

    print("\n" + "=" * 60)
    print("PRICE STATISTICS")
    print("=" * 60)
    print(prices_df.describe().round(2))

    # Visualize
    print("\n" + "=" * 60)
    print("Generating visualizations...")
    print("=" * 60)
    visualize_results(prices_df, correlation)

if __name__ == "__main__":
    main()
