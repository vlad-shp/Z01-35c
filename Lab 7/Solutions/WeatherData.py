import requests
from datetime import datetime

DAYS_SHOWS = 3
DEFAULT_CITY_NAME = 'Wroclaw'
DEFAULT_CITY_SHOW_NAME = 'Wrocław, województwo dolnośląskie, Polska'


class WeatherData:
    def __init__(self):
        self.hourly = []

    def get_weather_data(self, latitude, longitude):
        # "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,current,
        # &units=metric&lang=pl&appid=820fd123bde0f0772e98a50f46d53262"
        parameters = {"lat": latitude,
                      "lon": longitude,
                      "exclude": ["current", "hourly"],
                      "units": "metric",
                      "language": "pl",
                      "appid": "820fd123bde0f0772e98a50f46d53262"}
        response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall", params=parameters)
        response_json = response.json()

        daily = response_json["daily"]
        self.hourly = response_json["hourly"]
        days_data = list(map(self.get_day_data, daily[:DAYS_SHOWS]))
        return days_data

    def get_day_data(self, day):
        date = datetime.fromtimestamp(day["dt"])
        icon = day["weather"][0]["icon"]
        temp_min = day["temp"]["min"]
        temp_max = day["temp"]["max"]

        hours_in_day = filter(lambda hour: datetime.fromtimestamp(hour["dt"]).day == date.day, self.hourly)
        hour_data = list(map(lambda hour: (datetime.fromtimestamp(hour["dt"]).hour, hour["temp"]), hours_in_day))

        return [date.day,date.month,date.year], temp_min, temp_max, icon, hour_data