import requests
import pandas as pd
import os  

print("🐛 DEBUG MODE ACTIVATED")
print("Current directory:", os.getcwd())  
print("Files in directory:", os.listdir())  

BASE_URL = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json"

# 🌍 List of countries (Add more as needed)
COUNTRIES = ["USA", "CAN", "GBR", "FRA", "DEU", "JPN", "CHN", "IND", "BRA", "AUS"]

def fetch_gdp_data(countries=COUNTRIES, indicator="NY.GDP.MKTP.CD"):
    records = []

    for country in countries:
        url = BASE_URL.format(country, indicator)
        print(f"🌐 Fetching URL: {url}")  
        response = requests.get(url)
        print(f"🔄 Status Code for {country}: {response.status_code}")  

        if response.status_code == 200:
            data = response.json()
            
            if len(data) > 1:
                for entry in data[1]:
                    if entry.get("value") is not None:
                        records.append({
                            "Country": entry["country"]["value"],
                            "Country Code": country,
                            "Year": int(entry["date"]),
                            "GDP (USD)": entry["value"]
                        })
            else:
                print(f"⚠️ No data found for {country}")
        else:
            print(f"❌ Failed to fetch data for {country} (HTTP {response.status_code})")

    return records

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