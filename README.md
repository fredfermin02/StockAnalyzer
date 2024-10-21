# Financial Data Extraction and Analysis Tool

This project is a Python-based tool designed to fetch and analyze financial data for NYSE and Nasdaq. It retrieves key financial metrics from various external APIs and websites, such as Yahoo Finance, CNBC, Wallmine, YCharts, and AlphaVantage. The tool provides insights into key metrics like sales growth, market capitalization, debt-to-capital ratio, profit margins, operating expenses, and the average P/E ratio over the past six months. Additionally, the program calculates potential future returns for the company based on this data.

## Key Features:

- **Sales Growth Calculation**: Fetches and formats Alphabet Inc.'s estimated sales growth from Yahoo Finance.
- **200-Day Moving Average**: Retrieves the company's 200-day moving average from AlphaVantage.
- **Market Capitalization**: Obtains Alphabet Inc.'s current market capitalization from AlphaVantage.
- **Cash and Debt Information**: Extracts total cash and debt-to-capital ratio from Yahoo Finance and CNBC.
- **Operating Expenses**: Fetches operating expense data from Wallmine to analyze the company's solvency.
- **Average Profit Margin**: Calculates the average profit margin for the past four years using Wallmine income statements.
- **P/E Ratio Over Time**: Averages the P/E ratio over the past six months using YCharts data.
- **Future Market Capitalization and Return**: Computes potential future market capitalization and stock return based on historical and forecasted data.

## Data Sources:
- [Yahoo Finance](https://finance.yahoo.com/)
- [CNBC](https://www.cnbc.com/)
- [Wallmine](https://wallmine.com/)
- [YCharts](https://ycharts.com/)
- [AlphaVantage](https://www.alphavantage.co/)

## How to Use

### 1. Install Dependencies:

You need to install the required Python packages before running the script. Use the following command:

```bash
pip install beautifulsoup4 requests statistics

Error handling is incorporated into each function to manage potential issues such as:

