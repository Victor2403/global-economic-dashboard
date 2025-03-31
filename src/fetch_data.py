print("🚀 Script started!")  # Add this at the very top

import requests
import pandas as pd
import os  # Added for path checking

print("🐛 DEBUG MODE ACTIVATED")
print("Current directory:", os.getcwd())  # Shows where Python thinks you are
print("Files in directory:", os.listdir())  # Lists all files in current folder


BASE_URL = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json"  # Fixed to use .format()

def fetch_gdp_data(country="USA", indicator="NY.GDP.MKTP.CD"):
    url = BASE_URL.format(country, indicator)
    print(f"🌐 Fetching URL: {url}")  # Debug
    response = requests.get(url)
    print(f"🔄 Status Code: {response.status_code}")  # Debug

    if response.status_code == 200:
        data = response.json()
        records = []
        
        # Check if data[1] exists (API returns metadata in data[0])
        if len(data) > 1:  
            for entry in data[1]:
                if entry.get("value") is not None:  # Safer than direct access
                    records.append({
                        "Country": entry["country"]["value"],
                        "Year": entry["date"],
                        "GDP (USD)": entry["value"]
                    })
            print(f"📊 Found {len(records)} records")  # Debug
        else:
            print("⚠️ No data found in API response")
        return records
    else:
        print(f"❌ Failed to fetch data (HTTP {response.status_code})")
        return []

# Main execution
print("\n🚀 Starting data fetch...")
try:
    gdp_data = fetch_gdp_data()
    print(f"📊 Received {len(gdp_data)} records")
    
    if gdp_data:
        df = pd.DataFrame(gdp_data)
        csv_path = "gdp_data.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} rows to {os.path.abspath(csv_path)}")
    else:
        print("⚠️ No data received from API")
        
except Exception as e:
    print(f"🔥 CRASHED: {str(e)}")