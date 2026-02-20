# Trends Tool 📈

A free, open-source command-line tool to analyze and visualize search trends using **Google Trends** and **Wikipedia Pageviews**.

## ✨ Features

*   **Google Trends**: Fetches "Interest Over Time" and "Interest by Region" (via `pytrends`).
*   **Wikipedia Trends**: Fetches daily article pageviews (via Wikimedia REST API).
*   **Dual-Axis Visualization**: Plots Google Search Interest vs. Wikipedia Pageviews on the same graph.
*   **Batch Processing**: Process multiple keywords from a spreadsheet at once (NEW!)
*   **Excel Reports**: Generate professional Excel reports with embedded charts (NEW!)
*   **Automated Reporting**: Generates reports with summary statistics and top regions.
*   **CSV Export**: Saves all raw data to CSV files for further analysis.
*   **100% Free**: Uses only free public APIs.

## 🚀 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/YOUR_USERNAME/trends_tool.git
    cd trends_tool
    ```

2.  Create virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 📋 Usage

### Mode 1: Single Keyword Analysis
```bash
python3 execution/trends_tool.py "keyword" [options]
```

**Arguments:**
*   `keyword`: The search term (e.g., "AI", "Dengue").
*   `--geo`: (Optional) Region code (e.g., `US`, `BR`). Default: Global.
*   `--timeframe`: (Optional) Timeframe (e.g., `today 12-m`, `2024-01-01 2024-12-31`). Default: `today 12-m`.
*   `--lang`: (Optional) Wikipedia language code (e.g., `en`, `pt`). Default: `pt`.

**Examples:**
```bash
python3 execution/trends_tool.py "Python" --lang "en"
python3 execution/trends_tool.py "dengue" --geo "BR" --timeframe "2025-01-01 2025-12-31" --lang "pt"
```

### Mode 2: Batch Processing with Spreadsheet (NEW!)
```bash
python3 execution/trends_tool_batch.py input.xlsx [options]
```

**Arguments:**
*   `input_file`: Excel or CSV file with keywords and optional parameters
*   `-o, --output`: Output file name (default: `output/trends_report.xlsx`)

**Examples:**
```bash
# Process keywords from spreadsheet
python3 execution/trends_tool_batch.py keywords.xlsx

# Specify custom output
python3 execution/trends_tool_batch.py keywords.csv -o my_report.xlsx
```

### Input Spreadsheet Format

**Required column:** `keyword`  
**Optional columns:** `geo`, `timeframe`, `language`

**Default values** (used if column missing or cell empty):
- `geo`: `BR` (Brazil)
- `timeframe`: `today 12-m` (last 12 months)
- `language`: `pt` (Portuguese)

For detailed examples and documentation, see [BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md)

## 📊 Output

### Single Mode Output
Results are saved in the `output/` directory:
*   `*_google_time.csv`: Daily search interest.
*   `*_google_region.csv`: Interest by state/region.
*   `*_wiki_views.csv`: Daily Wikipedia pageviews.
*   `*_combined_plot.png`: Visualization graph.
*   `*_report.md`: Summary report.

### Batch Mode Output
Single Excel file with one sheet per keyword:
*   **Each sheet contains:**
  - Keyword parameters (region, timeframe, language)
  - Dual-axis chart (Google Trends + Wikipedia Pageviews)
  - Google Trends data table
  - Interest by region table
  - Wikipedia pageviews table
*   **File:** `output/trends_report.xlsx` (customizable)

## 🌍 Supported Parameters

### Region Codes (geo)
BR, US, MX, GB, DE, FR, IT, ES, JP, CN, IN, AU, CA, AR, PT

### Timeframe Formats
`today 1-m`, `today 3-m`, `today 12-m`, `today 5-y`, `YYYY-MM-DD YYYY-MM-DD`

### Language Codes
pt, en, es, fr, de, it, ja, zh, ru, ar, hi

## 📚 Requirements

*   Python 3.7+
*   See `requirements.txt` for library dependencies.

## ✅ Validation & Error Handling

- ✓ Automatic validation of input data
- ✓ Default values for missing parameters
- ✓ Continues processing even if one keyword fails
- ✓ Summary of errors at the end
- ✓ No API credentials needed (uses free APIs)

## 📄 License

MIT
