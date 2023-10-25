import os
import sys
from datetime import datetime
from dotenv import load_dotenv

import requests
import json
import pytz
import geopy.exc
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from PIL import Image
from twilio.rest import Client

# Custom Modules
import customtkinter
from CTkMessagebox import CTkMessagebox

# Constants
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
MAX_HOURS = 12

# Load Environment Variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')

# GUI Components
main_window = None
time_label = None
latitude = None
longitude = None
city = None
country = None
town_label = None
country_label = None
phone_number = None
hours, minutes, seconds = None, None, None
weather_list = []
weather_images = []
weather_labels = []
temp_list = []

# Current Time
current_time = datetime.now().time()
formatted_time = current_time.strftime("%H:%M:%S")

weather_types = {
    # Group 2xx: Thunderstorm
    "thunderstorm with light rain": "rain_thunder_light",
    "thunderstorm with rain": "rain_thunder_medium",
    "thunderstorm with heavy rain": "rain_thunder_hard",
    "light thunderstorm": "thunder_light",
    "thunderstorm": "thunder_medium",
    "heavy thunderstorm": "thunder_hard",
    "ragged thunderstorm": "thunder_extreme",
    "thunderstorm with light drizzle": "rain_thunder_light",
    "thunderstorm with drizzle": "rain_thunder_medium",
    "thunderstorm with heavy drizzle": "rain_thunder_hard",
    # Group 3xx: Drizzle
    "light intensity drizzle": "rain_light",
    "drizzle": "rain_medium",
    "heavy intensity drizzle": "rain_hard",
    "light intensity drizzle rain": "rain_light",
    "drizzle rain": "rain_medium",
    "heavy intensity drizzle rain": "rain_hard",
    "shower rain and drizzle": "rain_medium",
    "heavy shower rain and drizzle": "rain_hard",
    "shower drizzle": "rain_medium",
    # Group 5xx: Rain
    "light rain": "rain_light",
    "moderate rain": "rain_medium",
    "heavy intensity rain": "rain_hard",
    "very heavy rain": "rain_hard",
    "extreme rain": "rain_hard",
    "freezing rain": "sleet_hard",
    "light intensity shower rain": "rain_light",
    "shower rain": "rain_medium",
    "heavy intensity shower rain": "rain_hard",
    "ragged shower rain": "rain_medium",
    # Group 6xx: Snow
    "light snow": "snow_light",
    "snow": "snow_medium",
    "heavy snow": "snow_hard",
    "sleet": "sleet_hard",
    "light shower sleet": "sleet_light",
    "shower sleet": "sleet_light",
    "light rain and snow": "sleet_light",
    "rain and snow": "sleet_hard",
    "light shower snow": "snow_light",
    "shower snow": "snow_medium",
    "heavy shower snow": "snow_hard",
    # Group 7xx: Atmosphere

    # Group 800: Clear
    "clear sky": "day_clear",
    # Group 80x: Clouds
    "few clouds": "day_partial_cloud",
    "scattered clouds": "day_partial_cloud",
    "broken clouds": "cloudy",
    "overcast clouds": "cloudy",
}

weather_alerts = {
    # Group 2xx: Thunderstorm
    "thunderstorm with light rain": "Burza z drobnym deszczem i piorunami ⛈️",
    "thunderstorm with rain": "Burza z deszczem i piorunami ⛈️",
    "thunderstorm with heavy rain": "Burza z dużym deszczem i piorunami ⚡💧",
    "light thunderstorm": "Mała burza z piorunami 🌩️",
    "thunderstorm": "Burza z piorunami 🌩️",
    "heavy thunderstorm": "Duża burza z piorunami ⚡",
    "ragged thunderstorm": "Rozszalała burza ⚡⚡",
    "thunderstorm with light drizzle": "Burza z drobną mżawką i piorunami ⛈️",
    "thunderstorm with drizzle": "Burza z mżawką i piorunami ⛈️",
    "thunderstorm with heavy drizzle": "Burza z dużą mżawką i piorunami ⚡💧",
    # Group 3xx: Drizzle
    "light intensity drizzle": "Drobna mżawka 🌧️",
    "drizzle": "Mżawka 🌧️",
    "heavy intensity drizzle": "Intensywna mżawka 💧",
    "light intensity drizzle rain": "Mało intensywna mżawka 🌧️",
    "drizzle rain": "Mżawka 🌧️",
    "heavy intensity drizzle rain": "Bardzo intensywna mżawka 💧",
    "shower rain and drizzle": "Ulewa z mżawką 🌧️",
    "heavy shower rain and drizzle": "Intensywna ulewa z mżawką 💧",
    "shower drizzle": "Ulewna mżawka 🌧️",
    # Group 5xx: Rain
    "light rain": "Drobny deszcz 🌧️",
    "moderate rain": "Opady deszczu 🌧️",
    "heavy intensity rain": "Intensywne opady deszczu 🌧️",
    "very heavy rain": "Bardzo intensywne opady deszczu 💧",
    "extreme rain": "Ekstremalne opady deszczu 💧💧",
    "freezing rain": "Deszcz ze śniegiem 🌧️🌨️",
    "light intensity shower rain": "Mało intensywna ulewa 🌧️",
    "shower rain": "Ulewny deszcz 🌧️",
    "heavy intensity shower rain": "Intensywna ulewa 💧",
    "ragged shower rain": "Rozszalałe opady deszczu 💧💧",
    # Group 6xx: Snow
    "light snow": "Drobny śnieg 🌨️",
    "snow": "Opady śniegu 🌨️",
    "heavy snow": "Duże opady śniegu ❄️",
    "sleet": "Deszcz ze śniegiem 🌨️🌧️",
    "light shower sleet": "Drobne opady deszczu ze śniegiem 🌨️🌧️",
    "shower sleet": "Opady deszczu ze śniegiem 🌨️🌧️",
    "light rain and snow": "Drobny deszcz ze śniegiem 🌨️🌧️",
    "rain and snow": "Opady deszczu ze śniegiem 🌨️🌧️",
    "light shower snow": "Drobne opady śniegu 🌨️🌧️",
    "shower snow": "Opady śniegu 🌨️🌧️",
    "heavy shower snow": "Duże opady śniegu ❄️",
    # Group 7xx: Atmosphere

    # Group 800: Clear
    "clear sky": "Czyste niebo ☀️",
    # Group 80x: Clouds
    "few clouds": "Częściowe zachmurzenie (11-25%) 🌤️",
    "scattered clouds": "Rozproszone chmury (25-50%) ⛅",
    "broken clouds": "Rozbite chmury (51-84%) 🌥️",
    "overcast clouds": "Całkowite zachmurzenie (85-100%) ☁️",
}


def is_numeric_with_plus(input_str):
    return all(char.isdigit() or char == '+' for char in input_str)


def show_success(title, text):
    CTkMessagebox(title=title, message=text, icon="check")


def show_error(title, text):
    CTkMessagebox(title=title, message=text, icon="cancel")


def create_label(window, text, row, column, columnspan, font_size, fg_color="transparent"):
    label = customtkinter.CTkLabel(window, text=text, fg_color=fg_color, font=("Times New Roman", font_size))
    label.grid(padx=5, pady=15 if font_size == 90 else 5, row=row, column=column, columnspan=columnspan)
    return label


def create_entry(window, row, column, columnspan, font_size, width):
    entry = customtkinter.CTkEntry(window, font=("Times New Roman", font_size), width=width)
    entry.grid(padx=5, pady=15 if font_size == 90 else 5, row=row, column=column, columnspan=columnspan)
    return entry


def create_button(window, text, row, column, columnspan, font_size, width, command):
    button = customtkinter.CTkButton(window, text=text, font=("Times New Roman", font_size), width=width,
                                     command=command)
    button.grid(padx=5, pady=15 if font_size == 90 else 5, row=row, column=column, columnspan=columnspan)
    return button


def create_weather_widgets(window, index, weather, temp, time):
    weather_image = customtkinter.CTkImage(
        light_image=Image.open("images/" + weather_types[weather] + ".png"),
        dark_image=Image.open("images/" + weather_types[weather] + ".png"),
        size=(128, 128))

    i = index % 6
    j = (index // 6) * 3

    weather_label = customtkinter.CTkLabel(window, image=weather_image, text="")
    weather_label.grid(padx=15, pady=5, row=j + 1, column=i)

    temp_label = customtkinter.CTkLabel(window, text="{:,.2f}".format(round(temp, 2)) + " °C",
                                        font=("Times New Roman", 35), text_color="#0096FF")
    temp_label.grid(padx=5, pady=5, row=j + 2, column=i)

    weather_hour = (time.hour + index + 1) % 24
    weather_hour_label = customtkinter.CTkLabel(window, text=f"{weather_hour}:00", fg_color="transparent",
                                                font=("Times New Roman", 35))
    weather_hour_label.grid(padx=5, pady=5, row=j + 3, column=i)

    return weather_label, weather_hour_label


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def is_valid_phone(phone_arg):
    return len(phone_arg) == 12 and phone_arg.startswith('+') and phone_arg[1:].isdigit()


def send_message(text, to_phone):
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=text,
            from_=TWILIO_NUMBER,
            to=to_phone
        )
        print(message.status)
        return True
    except Exception as e:
        print(f"Failed to send message due to: {e}")
        return False


def generate_forecast_message():
    final_text = "Prognoza na dziś:\n"
    for index, (weather, temp) in enumerate(zip(weather_list, temp_list), start=1):
        weather_hour = (current_time.hour + index) % 24
        final_text += f"{weather_hour}:00 - {weather_alerts[weather]} [{round(temp, 2)} °C]\n"
    return final_text


def update_weather():
    global weather_list, temp_list, town_label, country_label

    weather_params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "exclude": "current,minutely,daily"
    }

    response = requests.get(OWM_ENDPOINT, params=weather_params)
    print(response.status_code)

    response.raise_for_status()
    weather_data = response.json()
    weather_slice = weather_data["list"][:MAX_HOURS]
    weather_list = []
    temp_list = []

    # Extract weather data and update lists
    for hour_data in weather_slice:
        condition_desc = hour_data["weather"][0]["description"]
        condition_temp = kelvin_to_celsius(hour_data["main"]["temp"])
        weather_list.append(condition_desc)
        temp_list.append(condition_temp)

    # City and Country update
    if country_label:
        country_label.destroy()
    if town_label:
        town_label.destroy()

    town_label = customtkinter.CTkLabel(main_window, text=str(city), fg_color="transparent",
                                        font=("Times New Roman", 45))
    town_label.grid(padx=5, pady=15, row=0, column=0, columnspan=2)
    country_label = customtkinter.CTkLabel(main_window, text=str(country), fg_color="transparent",
                                           font=("Times New Roman", 45))
    country_label.grid(padx=5, pady=15, row=0, column=4, columnspan=2)

    # Destroy existing labels
    [weather_label.destroy() for weather_label in weather_labels]

    for index, (weather, temp) in enumerate(zip(weather_list, temp_list)):
        weather_label, weather_hour_label = create_weather_widgets(main_window, index, weather, temp, current_time)
        weather_labels.append(weather_label)
        weather_labels.append(weather_hour_label)


def get_time_zone(city):
    geolocator = Nominatim(user_agent="city_time_zone")

    try:
        location = geolocator.geocode(city)
    except geopy.exc.GeocoderUnavailable:
        show_error("Błąd", "Niestety aktualnie serwery lokalizacyjne są niedostępne lub przeciążone")
        print("Geocoding service timed out. Please try again.")
    else:
        if location is not None:
            tf = TimezoneFinder()

            # Get the time zone for the location
            tz_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
            return tz_str

    return None


def initial_time_update():
    global current_time, formatted_time, hours, minutes, seconds

    # Get the time zone for the specified city
    tz = get_time_zone(city)

    # Get current time
    current_time = datetime.now(pytz.timezone(tz))

    # Update string accordingly
    formatted_time = current_time.strftime("%H:%M:%S")

    # Print the updated string
    if time_label:
        time_label.configure(text=formatted_time)

    # Update global variables
    hours, minutes, seconds = current_time.hour, current_time.minute, current_time.second


def main_menu():
    global main_window, time_label, latitude, longitude

    def update_phone(phone_arg, show_msgbox):
        global phone_number

        if is_valid_phone(phone_arg):
            with open("data.json", "w") as json_file:
                new_data = {"phone": phone_arg, "city": city}
                json.dump(new_data, json_file)
            if show_msgbox:
                show_success("Sukces", "Numer telefonu został poprawnie zaktualizowany")
            phone_number = phone_arg
            if "-phonemode" in sys.argv:
                print("Phone mode activated.")
                forecast = generate_forecast_message()
                send_message(forecast, phone_number)
            else:
                print("Phone mode deactivated.")
        else:
            if show_msgbox:
                show_error("Błąd", "Numer telefonu nie został poprawnie zaktualizowany\n\nUpewnij się, że jest on "
                                   "podany"
                                   "razem z numerem kierunkowym, bez spacji oraz z symbolem +")

    def update_city(city_arg, show_msgbox):
        global latitude, longitude, city, country

        geolocator = Nominatim(user_agent="my_geocoder")

        try:
            location = geolocator.geocode(city_arg)

            if location:
                city = location.address.split(",")[0]  # Extract city from the address
                country = location.address.split(",")[-1].strip()  # Extract country from the address
                latitude, longitude = location.latitude, location.longitude
                print(f"The coordinates of {city_arg} are: Latitude {latitude}, Longitude {longitude}")
                if show_msgbox:
                    with open("data.json", "w") as json_file:
                        new_data = {"phone": phone_number, "city": city_arg.capitalize()}
                        json.dump(new_data, json_file)
                    show_success("Sukces", "Miejscowość została poprawnie zaktualizowana")
                initial_time_update()
                update_weather()
            else:
                if show_msgbox:
                    show_error("Błąd", "Niestety miejscowość z taką nazwą nie została odnaleziona")
                print(f"Unable to find coordinates for {city_arg}.")
        except geopy.exc.GeocoderUnavailable:
            show_error("Błąd", "Niestety aktualnie serwery lokalizacyjne są niedostępne lub przeciążone")
            print("Geocoding service timed out. Please try again.")
        except geopy.exc.GeocoderTimedOut:
            print("Geocoding service timed out. Please try again.")

    def format_time(h, m, s):
        return f"{h:02d}:{m:02d}:{s:02d}"

    def update_time():
        global hours, minutes, seconds

        seconds += 1

        if seconds == 60:
            seconds = 0
            minutes += 1

            if minutes == 60:
                minutes = 0
                hours += 1

                if hours == 24:
                    hours = 0

        if time_label:
            time_label.configure(text=format_time(hours, minutes, seconds))

        # Schedule the function to be called again after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)

    def on_close():
        # Perform any cleanup or thread termination here
        main_window.destroy()

    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
    main_window = customtkinter.CTk()
    main_window.title("WeatherWatch")
    main_window.config(padx=25, pady=25)
    main_window.resizable(False, False)

    # Create labels
    time_label = create_label(main_window, "00:00:00", 0, 2, 2, 90)
    create_label(main_window, "Miejscowość:", 7, 0, 1, 20)
    create_label(main_window, "Telefon:", 8, 0, 1, 20)

    # Create entry fields
    city_entry = create_entry(main_window, 7, 1, 3, 20, 400)
    phone_entry = create_entry(main_window, 8, 1, 3, 20, 400)

    # Create buttons
    create_button(main_window, "Zatwierdź", 7, 4, 2, 20, 200, lambda: update_city(city_entry.get(), True))
    create_button(main_window, "Zatwierdź", 8, 4, 2, 20, 200, lambda: update_phone(phone_entry.get(), True))

    if os.path.exists("data.json"):
        with open("data.json", "r") as json_file:
            data = json.load(json_file)
            update_city(data["city"], False)
            update_phone(data["phone"], False)
    else:
        with open("data.json", "w") as json_file:
            new_data = {"phone": "+48536511079", "city": "Warszawa"}
            json.dump(new_data, json_file)
            update_city("Warszawa", False)
            update_phone("+48123456789", False)

    initial_time_update()

    # Schedule the function to be called again after 1000 milliseconds (1 second)
    time_label.after(1000, update_time)

    # Set a callback for the window close event
    main_window.protocol("WM_DELETE_WINDOW", on_close)

    if "-phonemode" not in sys.argv:
        main_window.mainloop()


if __name__ == "__main__":
    main_menu()
