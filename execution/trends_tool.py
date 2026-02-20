import argparse
import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import os
import requests
import datetime

def fetch_trends_data(keywords, geo, timeframe):
    """
    Fetches Interest Over Time and Interest by Region from Google Trends.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [keywords] # pytrends expects a list
    
    print(f"Fetching Google Trends data for: {kw_list}, geo={geo}, timeframe={timeframe}")
    
    # Build payload
    try:
        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo, gprop='')
        
        # Interest Over Time
        interest_over_time_df = pytrends.interest_over_time()
        if not interest_over_time_df.empty:
            interest_over_time_df = interest_over_time_df.drop(labels=['isPartial'], axis='columns')

        # Interest By Region (States/Provinces)
        interest_by_region_df = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
        
        return interest_over_time_df, interest_by_region_df
    except Exception as e:
        print(f"Google Trends Error: {e}")
        return pd.DataFrame(), pd.DataFrame()

def fetch_wikipedia_data(keyword, lang='pt', days=365, start_date_str=None, end_date_str=None):
    """
    Fetches daily pageviews for a Wikipedia article.
    If start_date_str/end_date_str (YYYY-MM-DD) are provided, uses them.
    Otherwise uses the last 'days' from today.
    """
    print(f"Fetching Wikipedia data for: {keyword} ({lang})")
    
    if start_date_str and end_date_str:
        # Convert YYYY-MM-DD to YYYYMMDD
        start_str = start_date_str.replace('-', '')
        end_str = end_date_str.replace('-', '')
    else:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")
    
    # Wikipedia API format: project / access / agent / article / granularity / start / end
    # Note: Keyword must match the article title exactly (case sensitive, underscores)
    article_title = keyword.replace(' ', '_')
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{lang}.wikipedia/all-access/all-agents/{article_title}/daily/{start_str}/{end_str}"
    
    headers = {
        'User-Agent': 'TrendTool/1.0 (renan.reis_enext@example.com)' # Good practice to identify script
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            if not items:
                return pd.DataFrame()
            
            dates = [datetime.datetime.strptime(item['timestamp'], "%Y%m%d00") for item in items]
            views = [item['views'] for item in items]
            
            df = pd.DataFrame({'views': views}, index=dates)
            return df
        else:
            print(f"Wikipedia API Error: {response.status_code} - {response.text}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Wikipedia Request Error: {e}")
        return pd.DataFrame()

def save_to_csv(df, filename):
    """Saves DataFrame to CSV."""
    if df is not None and not df.empty:
        df.to_csv(filename)
        print(f"Data saved to {filename}")
    else:
        print(f"No data to save for {filename}")

def plot_trends(google_df, wiki_df, keyword, filename):
    """Plots Interest Over Time (Google) and Pageviews (Wikipedia)."""
    
    if (google_df is None or google_df.empty) and (wiki_df is None or wiki_df.empty):
        print("No data to plot.")
        return

    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot Google Trends on primary y-axis
    if google_df is not None and not google_df.empty:
        ax1.plot(google_df.index, google_df[keyword], color='tab:blue', label='Google Search Interest')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Google Interest (0-100)', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    # Plot Wikipedia Views on secondary y-axis
    if wiki_df is not None and not wiki_df.empty:
        ax2 = ax1.twinx()
        ax2.plot(wiki_df.index, wiki_df['views'], color='tab:orange', linestyle='--', label='Wikipedia Pageviews')
        ax2.set_ylabel('Wikipedia Pageviews', color='tab:orange')
        ax2.tick_params(axis='y', labelcolor='tab:orange')

    plt.title(f'Interest & Pageviews Over Time: {keyword}')
    fig.tight_layout()
    plt.grid(True, axis='x')
    
    # Manual Legend
    lines1, labels1 = ax1.get_legend_handles_labels() if google_df is not None else ([], [])
    if wiki_df is not None and not wiki_df.empty:
        lines2, labels2 = ax2.get_legend_handles_labels()
    else:
        lines2, labels2 = [], []
        
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.savefig(filename)
    plt.close()
    print(f"Plot saved to {filename}")

def generate_report(keyword, geo, timeframe, time_df, region_df, wiki_df, plot_filename, report_filename):
    """Generates a Markdown report."""
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(f"# Trends Report: {keyword}\n\n")
        f.write(f"**Date:** {pd.Timestamp.now()}\n\n")
        f.write(f"**Parameters:**\n")
        f.write(f"- Keyword: `{keyword}`\n")
        f.write(f"- Region: `{geo}`\n")
        f.write(f"- Timeframe: `{timeframe}`\n\n")
        
        f.write("## Trends Visualization\n\n")
        f.write(f"![Trends Plot]({os.path.basename(plot_filename)})\n\n")

        f.write("## Google Trends Stats\n\n")
        if not time_df.empty:
            f.write("### Interest Over Time - Summary\n")
            try:
                f.write(time_df.describe().to_markdown())
            except ImportError:
                 f.write("pip install tabulate for table\n")
            f.write("\n\n")
        else:
            f.write("No Google Trends data found.\n\n")

        f.write("## Wikipedia Stats\n\n")
        if not wiki_df.empty:
            f.write("### Pageviews - Summary\n")
            try:
                f.write(wiki_df.describe().to_markdown())
            except ImportError:
                 f.write("pip install tabulate for table\n")
            f.write("\n\n")
        else:
            f.write("No Wikipedia data found (Article title might not match exactly).\n\n")

        f.write("## Interest by Region (Google)\n\n")
        if not region_df.empty:
            # Sort by interest
            if keyword in region_df.columns:
                region_sorted = region_df.sort_values(by=keyword, ascending=False)
                try:
                    f.write(region_sorted.head(10).to_markdown())
                except ImportError:
                     pass
                f.write("\n\n(Showing top 10 regions)\n")
            else:
                 f.write("Keyword column not found in region data.\n")
        else:
            f.write("No region data found.\n\n")
            
    print(f"Report generated: {report_filename}")

def main():
    parser = argparse.ArgumentParser(description='Google & Wikipedia Trends Tool')
    parser.add_argument('keyword', type=str, help='Keyword to search')
    parser.add_argument('--geo', type=str, default='', help='Region code (e.g., US, BR)')
    parser.add_argument('--timeframe', type=str, default='today 12-m', help='Timeframe (e.g., "today 12-m", "2024-01-01 2024-12-31")')
    parser.add_argument('--lang', type=str, default='pt', help='Wikipedia Language code (default: pt)')
    
    args = parser.parse_args()
    
    # Create output directory if not exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Filenames
    base_name = f"{args.keyword.replace(' ', '_')}_{args.geo if args.geo else 'global'}"
    time_csv = os.path.join(output_dir, f"{base_name}_google_time.csv")
    region_csv = os.path.join(output_dir, f"{base_name}_google_region.csv")
    wiki_csv = os.path.join(output_dir, f"{base_name}_wiki_views.csv")
    plot_png = os.path.join(output_dir, f"{base_name}_combined_plot.png")
    report_md = os.path.join(output_dir, f"{base_name}_report.md")
    
    # Fetch Data
    time_df = pd.DataFrame()
    region_df = pd.DataFrame()
    wiki_df = pd.DataFrame()

    try:
        # Google Trends
        time_df, region_df = fetch_trends_data(args.keyword, args.geo, args.timeframe)
        save_to_csv(time_df, time_csv)
        save_to_csv(region_df, region_csv)
        
        # Wikipedia Trends
        # Attempt to parse specific date range from timeframe
        wiki_start = None
        wiki_end = None
        
        try:
            # Check for "YYYY-MM-DD YYYY-MM-DD" format
            parts = args.timeframe.split()
            if len(parts) == 2:
                # Simple check if they look like dates
                datetime.datetime.strptime(parts[0], "%Y-%m-%d")
                datetime.datetime.strptime(parts[1], "%Y-%m-%d")
                wiki_start = parts[0]
                wiki_end = parts[1]
        except ValueError:
            pass
            
        # Capitalize keyword for Wikipedia (Dengue vs dengue)
        wiki_keyword = args.keyword.capitalize() if args.keyword.islower() else args.keyword
        
        wiki_df = fetch_wikipedia_data(wiki_keyword, lang=args.lang, days=365, start_date_str=wiki_start, end_date_str=wiki_end)
        save_to_csv(wiki_df, wiki_csv)

        # Plot Combined
        plot_trends(time_df, wiki_df, args.keyword, plot_png)
        
        # Report
        generate_report(args.keyword, args.geo, args.timeframe, time_df, region_df, wiki_df, plot_png, report_md)
        
    except Exception as e:
        print(f"Critical Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
