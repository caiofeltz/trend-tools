# Data Analysis Directive

**Goal**: Fetch and interpret performance data from Google Search Console (GSC), Google Analytics 4 (GA4), and Google My Business (GMB).

**Inputs**:
- `source`: One of `gsc`, `ga4`, or `gmb`.
- `site_url` (for GSC) or `property_id` (for GA4) or `location_id` (for GMB).
- `days`: Number of days to look back (default: 28).

**Process**:
1.  **Select Script**: Based on `source`, chose the correct execution script.
    -   **GSC**: `python execution/fetch_gsc_data.py --site_url "{site_url}" --days {days}`
    -   **GA4**: `python execution/fetch_ga_data.py --property_id "{property_id}" --days {days}`
    -   **GMB**: `python execution/fetch_gmb_data.py --location_id "{location_id}" --days {days}`
2.  **Execute**: Run the script. It uses `credentials.json` for authentication.
3.  **Analyze**:
    -   For **GSC**: Look for Clicks/Impressions trends and top queries.
    -   For **GA4**: Look for User and Session trends.
    -   For **GMB**: Look for Calls, Directions requests, and Reviews.

**Outputs**:
- JSON data saved to `.tmp/data_{source}.json`.
- A summary printed to stdout.

**Prerequisites**:
- `credentials.json` must be present in the root.
- User must have access to the properties.
