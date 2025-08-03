import requests
import geocoder
from colorama import init, Fore
from config import API_KEY

init(autoreset=True)

def get_location():
    g = geocoder.ip('me')
    return g.city or "Unknown"

def get_weather(city):
    print(Fore.MAGENTA + f"🔍 Fetching weather for {city}...")
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            print(Fore.RED + f"Error: {data.get('message', 'Unknown error')}")
            return

        print(Fore.CYAN + f"📍 3-Day Forecast for {city.title()}")
        days = {}
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in days:
                days[date] = item
            if len(days) >= 3:
                break

        for date, forecast in days.items():
            desc = forecast["weather"][0]["description"].title()
            temp = forecast["main"]["temp"]
            feels = forecast["main"]["feels_like"]
            print(Fore.YELLOW + f"📅 {date}")
            print(Fore.GREEN + f"   {desc} | 🌡️ {temp}°C (Feels like {feels}°C)")

    except Exception as e:
        print(Fore.RED + f"Failed to fetch weather: {e}")

if __name__ == "__main__":
    use_auto = input("Use your current location? (y/n): ").strip().lower()
    if use_auto == 'y':
        city = get_location()
    else:
        city = input("Enter city name: ")
    get_weather(city)
