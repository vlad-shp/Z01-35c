import io
from geopy.geocoders import Nominatim
from PIL import Image, ImageTk
import urllib.request as ur



def get_icon_image(icon_name):
    icon_url = f"http://openweathermap.org/img/wn/{icon_name}@2x.png"
    icon_request = ur.urlopen(icon_url)
    icon = Image.open(io.BytesIO(icon_request.read()))
    icon_request.close()
    return ImageTk.PhotoImage(icon)


def get_city_data(city_name="Wroclaw"):
    app = Nominatim(user_agent="City")
    lat = 0
    lon = 0
    display_name = f"Can't find city:{city_name}"
    try:
        city_raw = app.geocode(city_name).raw
        lat = city_raw['lat']
        lon = city_raw['lon']
        display_name = city_raw['display_name']
    except:
        print("get_city_data err")

    return lat, lon, display_name
