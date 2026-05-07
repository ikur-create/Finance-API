# Resource Correlation Dashboard

This repository contains a simple Python script that fetches futures price data for gold, silver, and WTI crude oil, then displays:

- normalized price movements for all three instruments
- gold vs silver directional comparison
- gold vs inverse WTI crude
- weekly correlation between gold and oil
- weekly correlation between gold and silver

## Files

- `Gold_vs_Silver_vs_oil.py`: Main analysis script
- `README.md`: Project overview and usage instructions

## Requirements

- Python 3.8+
- `pandas`
- `matplotlib`
- `yfinance`

## Installation

```bash
pip install pandas matplotlib yfinance
```

## Usage

Run the script from the repository root:

```bash
python Gold_vs_Silver_vs_oil.py
```

The script will download historical futures data from Yahoo Finance and render a polished chart dashboard with weekly correlation.

## Notes

- The script normalizes prices relative to the most recent closing value.
- Correlation is computed weekly and plotted as a separate chart.
- The chart uses a clean seaborn-style theme for readability.

## License

This repository is provided as-is for analysis and visualization purposes.
