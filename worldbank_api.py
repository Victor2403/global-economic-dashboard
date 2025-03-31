import requests

def fetch_worldbank_data(country_code="USA", indicator_code="NY.GDP.MKTP.CD"):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises error for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    data = fetch_worldbank_data("USA", "NY.GDP.MKTP.CD")  # Change args as needed
    if data:
        print(data[1][:5])  # Print first 5 entries of the actual data (not metadata)

# Print scripts
import requests

def fetch_worldbank_data(country_code="USA", indicator_code="NY.GDP.MKTP.CD"):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json"
    print(f"\n🔍 Attempting to fetch: {url}")  # Debug line
    
    try:
        response = requests.get(url)
        print(f"🔄 Response status: {response.status_code}")  # Debug line
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")  # Modified to show error details
        return None

if __name__ == "__main__":
    print("🚀 Script started")  # Debug line
    data = fetch_worldbank_data()
    print(f"📦 Data received: {bool(data)}")  # Debug line
    if data:
        print(data[1][:5])  # Show first 5 entries