# Resource Correlation — Gold, Silver & WTI Crude

> Price normalization and rolling correlation analysis across three major commodity markets, with a focus on the structural relationship between gold and oil.

---

## 📈 What does this project do?

This script downloads historical price data for Gold (`GC=F`), Silver (`SI=F`), and WTI Crude Oil (`CL=F`) via `yfinance`, normalizes each series to its most recent closing price, and visualizes their co-movement and monthly rolling correlations across four subplots.

The central question is whether gold behaves as an inverse hedge against oil — and whether the gold/silver relationship is more stable over time than the gold/oil one.



##  📊 Output

| Metric | Description |
|---|---|
| Normalized price chart | All three assets on a common scale |
| Gold/Silver co-movement | Paired chart with fill between series |
| Gold vs Inverse WTI | Divergence signal visualization |
| Monthly correlation | Rolling Pearson correlation with signed fill |
| Correlation matrix | Printed to terminal at script end |



## 🚀 Quickstart

1. Install dependencies:

```bash
pip install yfinance pandas matplotlib numpy
```

2. Run the script:

```bash
python Gold_vs_Silver_vs_oil.py
```

The chart opens interactively. To save it, add before `plt.show()`:

```python
plt.savefig('commodity_correlation.png', dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
```



## ⚙️ Configuration

Edit these variables at the top of the script to adjust the analysis window or assets:

```python
tickers = ['GC=F', 'SI=F', 'CL=F']   # Gold, Silver, WTI Crude futures
start   = '2019-01-01'
end     = '2026-05-01'
```

## 🎨 Design notes

The chart uses a dark editorial theme — monospace fonts, a restrained color palette (amber gold, steel silver, blue oil), and signed fill on the correlation panel — to produce a figure that reads clearly both on screen and in a portfolio PDF. Thanks to AI the design was enhanced for a better understanding.



## ⚠️ Disclaimer

This project is for educational and research purposes only. It does not constitute financial advice or investment recommendations.



## 📬 Contact

For questions or collaboration: **ikergom.hkim@gmail.com**