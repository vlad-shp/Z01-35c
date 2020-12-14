import tkinter as tk
from datetime import datetime
from tkinter.font import Font
from WeatherData import WeatherData,DAYS_SHOWS,DEFAULT_CITY_SHOW_NAME,DEFAULT_CITY_NAME
from OtherTools import get_icon_image,get_city_data


def draw_weather_hourly(day_hourly, title):
    root = tk.Tk()
    root.title(f"Weather 3 Days (Hourly: {title})")
    root.configure(bg='white')
    canvas = tk.Canvas(root, width=800, height=300)
    canvas.pack()
    # 40°-70
    # 300-70/70
    # -10°-300
    # 4.2
    padding_left = 10
    for hour in day_hourly:
        temp = hour[1]
        if 10 > temp > 1:
            color = "#FFD733"
        elif 10 <= temp < 17:
            color = "#FFE333"
        elif 17 <= temp < 28:
            color = "#FF9633"
        elif temp >= 28:
            color = "#FF5533"
        elif 1 >= temp > -10:
            color = "#33DAFF"
        else:
            color = "#3349FF"

        canvas.create_rectangle(padding_left + 33 * hour[0], 200, padding_left + 33 * hour[0] + 30, 200 - 3.2 * temp,
                                outline=color,
                                fill=color)
        canvas.create_text(padding_left + 33 * hour[0] + 20, 190, text=f"{int(temp)}°", font="Times 12")
        canvas.create_line(padding_left + 0, 200, 800 - padding_left, 200)

    for i in range(0, 24):
        canvas.create_text(padding_left + 33 * i + 20, 20, text=i, font="Times 16")

    canvas.create_line(padding_left, 28, 800 - padding_left, 28)

    for i in range(1, 24):
        canvas.create_line(padding_left + i * 33, 0, padding_left + i * 33, 300)


class GUI:

    def __init__(self):
        self.weather_data = WeatherData()
        self.weather_data_upd: WeatherData = None
        self.root = tk.Tk()
        self.root.title("Weather 3 Days")
        self.root.configure(bg='white')
        self.canvas1 = tk.Canvas(self.root, width=600, height=300)
        self.canvas1.pack()
        self.canvas1.configure(bg='white')
        self.city_display_name = tk.StringVar()
        self.city_display_name.set(DEFAULT_CITY_SHOW_NAME)
        label_city = tk.Label(self.root, textvariable=self.city_display_name, bg='white')
        self.canvas1.create_window(300, 50, window=label_city)
        label1 = tk.Label(self.root, text='City:', bg='white')
        self.canvas1.create_window(150, 20, window=label1)
        self.entry_city = tk.Entry(self.root, width=40, bg='white')
        self.canvas1.create_window(300, 20, window=self.entry_city)
        search_button = tk.Button(text="Search", command=self.search_weather_for_city)
        self.canvas1.create_window(450, 20, window=search_button)

        self.label_icons = [tk.Label(self.root, image=get_icon_image("10d"), bg='white'),
                            tk.Label(self.root, image=get_icon_image("10d"), bg='white'),
                            tk.Label(self.root, image=get_icon_image("10d"), bg='white')]

        position_x = 100

        for label in self.label_icons:
            self.canvas1.create_window(position_x, 200, window=label)
            position_x += 200


        city_data = get_city_data(DEFAULT_CITY_NAME)
        weather_data = self.weather_data.get_weather_data(city_data[0], city_data[1])

        my_font = Font(family="Times New Roman", size=14)
        max_temp_font = Font(family="Times New Roman", size=16)
        min_temp_font = Font(family="Times New Roman", size=10)
        label = tk.Label(self.root, font=my_font, text="Today", bg='white')
        self.canvas1.create_window(100, 90, window=label)
        position_x = 300
        for i in range(1, DAYS_SHOWS):
            day_name = datetime(weather_data[i][0][2], weather_data[i][0][1], weather_data[i][0][0]).strftime("%a")
            label = tk.Label(self.root, font=my_font, text=f'{day_name} {weather_data[i][0][0]}', bg='white')
            self.canvas1.create_window(position_x, 90, window=label)
            position_x += 200

        self.max_temperatures = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        position_x = 120
        for i in range(0, DAYS_SHOWS):
            label = tk.Label(self.root, font=max_temp_font, textvariable=self.max_temperatures[i], bg='white')
            self.canvas1.create_window(position_x, 130, window=label)
            position_x += 200

        self.min_temperatures = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        position_x = 110
        for i in range(0, DAYS_SHOWS):
            label = tk.Label(self.root, font=min_temp_font, textvariable=self.min_temperatures[i], bg='white')
            self.canvas1.create_window(position_x, 150, window=label)
            position_x += 200

        self.canvas1.create_line(200, 90, 200, 280)
        self.canvas1.create_line(400, 90, 400, 280)
        self.canvas1.create_line(50, 110, 550, 110)

        button_first_day = tk.Button(text="Hourly", command=self.show_first_day_hourly)
        self.canvas1.create_window(100, 270, window=button_first_day)

        button_second_day = tk.Button(text="Hourly", command=self.show_second_day_hourly)
        self.canvas1.create_window(300, 270, window=button_second_day)

        button_third_day = tk.Button(text="Hourly", command=self.show_third_day_hourly)
        self.canvas1.create_window(500, 270, window=button_third_day)

        self.update_weather_data(weather_data)

        self.root.mainloop()

    def show_first_day_hourly(self):
        draw_weather_hourly(self.weather_data_upd[0][4], f"{self.weather_data_upd[0][0][0]}.{self.weather_data_upd[0][0][1]}.{self.weather_data_upd[0][0][2]}")

    def show_second_day_hourly(self):
        draw_weather_hourly(self.weather_data_upd[1][4], f"{self.weather_data_upd[1][0][0]}.{self.weather_data_upd[1][0][1]}.{self.weather_data_upd[1][0][2]}")

    def show_third_day_hourly(self):
        draw_weather_hourly(self.weather_data_upd[2][4], f"{self.weather_data_upd[2][0][0]}.{self.weather_data_upd[2][0][1]}.{self.weather_data_upd[2][0][2]}")

    def search_weather_for_city(self):
        city_data = get_city_data(self.entry_city.get())
        self.city_display_name.set(city_data[2])
        if city_data[2].find('t find city') == -1:
            weather_data = self.weather_data.get_weather_data(city_data[0], city_data[1])
            self.update_weather_data(weather_data)

    def update_weather_data(self, weather_data):
        self.weather_data_upd = weather_data
        for i in range(len(self.label_icons)):
            icon_image = get_icon_image(weather_data[i][3])
            self.label_icons[i].configure(image=icon_image)
            self.label_icons[i].image = icon_image
            self.max_temperatures[i].set(f"{round(weather_data[i][2])}°")
            self.min_temperatures[i].set(f"{round(weather_data[i][1])}°")

