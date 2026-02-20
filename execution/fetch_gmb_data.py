import argparse
import json
import random
import os

# Placeholder for GMB API interaction

def fetch_gmb_data(location_id, days):
    print(f"Fetching GMB data for Location {location_id} for last {days} days...")
    
    # Simulate data
    data = {
        "location_id": location_id,
        "date_range": f"{days} days",
        "calls": random.randint(10, 200),
        "direction_requests": random.randint(20, 300),
        "website_clicks": random.randint(50, 500)
    }
    
    output_file = f".tmp/data_gmb.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"Data saved to {output_file}")
    print(f"Summary: {data['calls']} Calls, {data['direction_requests']} Direction Requests")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--location_id', required=True)
    parser.add_argument('--days', type=int, default=28)
    args = parser.parse_args()
    
    fetch_gmb_data(args.location_id, args.days)
