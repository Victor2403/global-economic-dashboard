import requests
import pandas as pd
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

print("🐛 DEBUG MODE ACTIVATED")
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

BASE_URL = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json"

# 🌍 List of countries
COUNTRIES = [
    "USA", "CAN", "GBR", "FRA", "DEU", "JPN", "CHN", "IND", "BRA", "AUS",
    "MEX", "RUS", "ITA", "ESP", "KOR", "IDN", "ZAF", "NGA", "EGY", "ARG"
]

# 📊 Indicators for GDP, Inflation, and Unemployment
INDICATORS = {
    "GDP (USD)": "NY.GDP.MKTP.CD",
    "Inflation (%)": "FP.CPI.TOTL.ZG",
    "Unemployment (%)": "SL.UEM.TOTL.ZS"
}

# Retry logic to handle API request failures
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

def fetch_economic_data(countries=COUNTRIES, indicators=INDICATORS):
    records = []

    for country in countries:
        for metric, indicator in indicators.items():
            page = 1

            while True:
                url = f"{BASE_URL.format(country, indicator)}&page={page}"
                print(f"🌐 Fetching: {url}")
                response = session.get(url)
                print(f"🔄 Status Code for {country} ({metric}) [Page {page}]: {response.status_code}")

                if response.status_code != 200:
                    print(f"❌ Failed to fetch {metric} for {country} on page {page}")
                    break

                data = response.json()

                if len(data) < 2 or not isinstance(data[1], list):
                    print(f"⚠️ No data found on page {page} for {metric} in {country}")
                    break

                for entry in data[1]:
                    if entry.get("value") is not None:
                        year = int(entry["date"])
                        value = entry["value"]

                        records.append({
                            "Country": entry["country"]["value"],
                            "Country Code": country,
                            "Year": year,
                            metric: value
                        })

                total_pages = data[0].get("pages", 1)
                if page >= total_pages:
                    break
                page += 1

    return records

# Main
print("\n🚀 Starting data fetch...")
try:
    economic_data = fetch_economic_data()
    print(f"📊 Retrieved {len(economic_data)} raw records")

    if economic_data:
        df = pd.DataFrame(economic_data)

        # Pivot to structure data by country, year
        df = df.pivot_table(index=["Country", "Country Code", "Year"], values=list(INDICATORS.keys()), aggfunc="first").reset_index()

        # Drop duplicates (if any)
        df = df.drop_duplicates(subset=["Country", "Year"])

        # Save to CSV
        csv_path = "economic_data.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} rows to {os.path.abspath(csv_path)}")

        # Preview sample rows
        print("\n📌 Sample of final data:")
        print(df.head(10))

    else:
        print("⚠️ No data received from API")

except Exception as e:
    print(f"🔥 CRASHED: {str(e)}")