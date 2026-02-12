import requests

API_KEY = "HAHAZULS4PFNLX3952HYVH42D"   
LOCATION = "Coimbatore,India"     # city, lat/long also works

url = (
    f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
    f"timeline/{LOCATION}"
)

params = {
    "unitGroup": "metric",      # metric units (Celsius)
    "key": API_KEY,
    "contentType": "json"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("Error fetching weather data:", response.text)
    exit()

data = response.json()

print(f"\n14-Day Weather Forecast for {data['resolvedAddress']}\n")

# Get first 16 days
for day in data["days"][:16]:
    print(
        f"Date: {day['datetime']} | "
        f"Min: {day['tempmin']}°C | "
        f"Max: {day['tempmax']}°C | "
        f"Condition: {day['conditions']}"
    )
