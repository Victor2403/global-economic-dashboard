import requests
import pandas as pd
import os  

print("🐛 DEBUG MODE ACTIVATED")
print("Current directory:", os.getcwd())  
print("Files in directory:", os.listdir())  

BASE_URL = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json"

# 🌍 List of countries (Add more as needed)
COUNTRIES = ["USA", "CAN", "GBR", "FRA", "DEU", "JPN", "CHN", "IND", "BRA", "AUS"]

# 📊 Indicators for GDP, Inflation, and Unemployment
INDICATORS = {
    "GDP (USD)": "NY.GDP.MKTP.CD",
    "Inflation (%)": "FP.CPI.TOTL.ZG",
    "Unemployment (%)": "SL.UEM.TOTL.ZS"
}

def fetch_economic_data(countries=COUNTRIES, indicators=INDICATORS):
    records = []

    for country in countries:
        country_data = {"Country": country}

        for metric, indicator in indicators.items():
            url = BASE_URL.format(country, indicator)
            print(f"🌐 Fetching URL: {url}")  
            response = requests.get(url)
            print(f"🔄 Status Code for {country} ({metric}): {response.status_code}")  

            if response.status_code == 200:
                data = response.json()
                
                if len(data) > 1 and isinstance(data[1], list):
                    for entry in data[1]:
                        if entry.get("value") is not None:
                            year = int(entry["date"])
                            value = entry["value"]

                            # Store data per year
                            records.append({
                                "Country": entry["country"]["value"],
                                "Country Code": country,
                                "Year": year,
                                metric: value
                            })
            else:
                print(f"❌ Failed to fetch {metric} for {country} (HTTP {response.status_code})")

    return records

# Main execution
print("\n🚀 Starting data fetch...")
try:
    economic_data = fetch_economic_data()
    print(f"📊 Received {len(economic_data)} records")

    if economic_data:
        df = pd.DataFrame(economic_data)

        # 🛠 Pivot to structure data properly
        df = df.pivot_table(index=["Country", "Country Code", "Year"], values=list(INDICATORS.keys()), aggfunc="first").reset_index()

        csv_path = "economic_data.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} rows to {os.path.abspath(csv_path)}")
    else:
        print("⚠️ No data received from API")

except Exception as e:
    print(f"🔥 CRASHED: {str(e)}")
