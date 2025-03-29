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