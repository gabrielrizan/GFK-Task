import os
import requests
from dotenv import load_dotenv

load_dotenv()

weather_api_key = os.getenv('WEATHER_API_KEY')

def fetch_weather_data(city):
    url = f'http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={city}&days=4&aqi=no&alerts=no'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("API Response:", data)  # test
            return data
        elif response.status_code == 400:
            print(f"Error: Received {response.status_code} (Bad Request) from WeatherAPI")
            return None
        else:
            print(f"Error: Received {response.status_code} from WeatherAPI")
            return "error"
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "error"
