import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import datetime as dt #used to take timestamp info sent from API
import requests #used to send requests to the API

# Constants
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = open("API_KEY.txt", "r").read() #API key is stored in a separate file


def fetch_weather(city):
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {e}")
        return None


def update_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city.")
        return

    data = fetch_weather(city)
    if data:
        temp_label.config(text=f"Temperature: {data['main']['temp']}°C")
        description_label.config(text=f"Description: {data['weather'][0]['description']}")
        humidity_label.config(text=f"Humidity: {data['main']['humidity']}%")

        icon_code = data['weather'][0]['icon']
        icon_path = get_weather_icon(icon_code)
        if icon_path:
            image = Image.open(icon_path)
            image = image.resize((100, 100), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            weather_icon_label.config(image=photo)
            weather_icon_label.image = photo  # Keep a reference to the image to avoid garbage collection
    else:
        temp_label.config(text="")
        description_label.config(text="")
        humidity_label.config(text="")
        weather_icon_label.config(image="")



root = tk.Tk()
root.title("Rise and Shine")

style = ttk.Style()
style.configure("TFrame", background="#ececec")
style.configure("TButton", background="#b1b1b1", font=("Helvetica", 12))
style.configure("TLabel", background="#ececec", font=("Helvetica", 12))

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky="nsew")

city_label = ttk.Label(main_frame, text="Enter City:")
city_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

city_entry = ttk.Entry(main_frame, width=20, font=("Helvetica", 12))
city_entry.grid(row=0, column=1, padx=5, pady=5)

fetch_button = ttk.Button(main_frame, text="Fetch Weather", command=update_weather)
fetch_button.grid(row=0, column=2, padx=5, pady=5)

temp_label = ttk.Label(main_frame, text="")
temp_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

description_label = ttk.Label(main_frame, text="")
description_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="w")

humidity_label = ttk.Label(main_frame, text="")
humidity_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")

root.mainloop()