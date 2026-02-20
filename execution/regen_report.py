import pandas as pd
import os

def generate_report(keyword, geo, timeframe, time_df, region_df, plot_filename, report_filename):
    """Generates a Markdown report."""
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(f"# Google Trends Report: {keyword}\n\n")
        f.write(f"**Date:** {pd.Timestamp.now()}\n\n")
        f.write(f"**Parameters:**\n")
        f.write(f"- Keyword: `{keyword}`\n")
        f.write(f"- Region: `{geo}`\n")
        f.write(f"- Timeframe: `{timeframe}`\n\n")
        
        f.write("## Interest Over Time\n\n")
        if not time_df.empty:
            f.write(f"![Interest Over Time]({os.path.basename(plot_filename)})\n\n")
            f.write("### Summary Statistics\n")
            try:
                f.write(time_df.describe().to_markdown())
            except ImportError:
                 f.write("Error: tabulate not installed.\n")
                 print("Error: tabulate not installed.")
            f.write("\n\n")
            f.write("### Data Preview (Top 5 rows)\n")
            try:
                f.write(time_df.head().to_markdown())
            except ImportError:
                 pass
            f.write("\n\n")
        else:
            f.write("No interest over time data found.\n\n")

        f.write("## Interest by Region\n\n")
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
    # Hardcoded parameters matching the test case
    keyword = "dengue"
    geo = "BR"
    timeframe = "2025-01-01 2025-12-31"
    
    output_dir = "output"
    base_name = f"{keyword}_{geo}"
    time_csv = os.path.join(output_dir, f"{base_name}_time.csv")
    region_csv = os.path.join(output_dir, f"{base_name}_region.csv")
    plot_png = os.path.join(output_dir, f"{base_name}_plot.png")
    report_md = os.path.join(output_dir, f"{base_name}_report.md")
    
    print(f"Loading data from {time_csv} and {region_csv}")
    
    if os.path.exists(time_csv):
        time_df = pd.read_csv(time_csv, index_col=0, parse_dates=True)
    else:
        time_df = pd.DataFrame()
        
    if os.path.exists(region_csv):
        region_df = pd.read_csv(region_csv, index_col=0)
    else:
        region_df = pd.DataFrame()

    generate_report(keyword, geo, timeframe, time_df, region_df, plot_png, report_md)

if __name__ == '__main__':
    main()
