# Yahoo Finance Risk Dashboard

A concise portfolio project demonstrating data collection, metric computation, and visualization for S&P 500 equities using Python.

## Overview

This project fetches the S&P 500 constituents, computes 1-year performance and risk metrics (annualized return, volatility, Sharpe ratio) from historical price data, and visualizes the relationship between Sharpe ratio and annualized return across the index.

The repository is designed to be lightweight and reproducible — ideal for a portfolio section showcasing data engineering, financial analysis, and plotting skills.

## Highlights

- Data sources: Wikipedia (constituents list) and Yahoo Finance (`yfinance`) for historical prices.
- Metrics: annualized average return, annualized volatility, Sharpe ratio (simple annualized version).
- Output: scatter visualization showing Sharpe ratio vs. annualized return for the S&P 500 (or a subset).

## Files

- [src/top500_sharpe_vs_return.py](src/top500_sharpe_vs_return.py#L1-L300): Main script. Fetches ticker list, collects metrics (with progress logging), and generates the scatter plot.
- [requirements.txt](requirements.txt): Python dependencies required to run the project.

## Quickstart

1. Create and activate a virtual environment (recommended).

```bash
python -m venv .venv
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the analysis and plot the results:

```bash
python src/top500_sharpe_vs_return.py
```

The script prints progress to the terminal while fetching data. The final plot is saved as `sp500_sharpe_vs_return.png` (or another filename shown in the log) and displayed.

## Usage notes

- Network: The script fetches live data and may take several minutes; consider using the `limit` parameter in the script to test on a smaller subset first.
- Dependencies: `pandas.read_html` requires `lxml`; if you see an error install it with `pip install lxml` (already listed in `requirements.txt`).
- Annotation clutter: When plotting all tickers, labels can overlap. The script currently annotates points; if you prefer fewer labels, open `src/top500_sharpe_vs_return.py` and set annotation behavior to only label the top N market caps.

## Design choices

- Simplicity: Metrics are computed directly from daily closes to keep processing transparent and easy to explain.
- Reproducibility: Data fetching and processing are contained in a single script for easy review.
- Readability: Progress logs help demonstrate the pipeline when running interactively.

## License & Contact

This repository is provided for portfolio/demo purposes. For questions or collaboration, contact: [ikergom.hkim@gmail.com].

---

