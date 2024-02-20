import tkinter as tk
from tkinter import ttk, messagebox
import requests
import webbrowser
import keyboard

# Spotify API credentials
SPOTIFY_CLIENT_ID = open("SPOTIFY_CLIENT.txt", "r").read()
SPOTIFY_CLIENT_SECRET = open("SPOTIFY_SECRET.txt", "r").read()

# OpenWeatherMap API credentials
API_KEY = open("API_KEY.txt", "r").read()
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

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

def get_genre(weather_description):
    # Example logic to determine genre based on weather description
    if "rain" in weather_description:
        return "cozy mix"
    elif "cloud" in weather_description:
        return "coldplay"
    elif "sun" in weather_description:
        return "happy hits"
    elif "snow" in weather_description:
        return "christmas hits"
    else:
        return "party"

def play_music(city):
    data = fetch_weather(city)
    if data:
        weather_description = data['weather'][0]['description']
        genre = get_genre(weather_description)
        token = authenticate_spotify()
        if token:
            playlist_uri = search_playlist(genre, token)
            if playlist_uri:
                open_spotify_uri(playlist_uri)  # Open Spotify URI after starting playback
                keyboard.press_and_release('space') # Press space to start playback
            else:
                messagebox.showinfo("Info", "No playlist found for the current weather.")
    else:
        messagebox.showinfo("Info", "Weather data not available.")


def authenticate_spotify():
    auth_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    try:
        response = requests.post(auth_url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to authenticate with Spotify: {e}")
        return None

def search_playlist(genre, token):
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": f"genre:{genre}",
        "type": "playlist",
        "limit": 1
    }
    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        playlists = data.get("playlists", {}).get("items", [])
        if playlists:
            return playlists[0]["uri"]
        return None
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to search playlist on Spotify: {e}")
        return None
    
    

def open_spotify_uri(uri):
    webbrowser.open(uri)

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
        play_music(city)
    else:
        temp_label.config(text="")
        description_label.config(text="")
        humidity_label.config(text="")

root = tk.Tk()
root.title("Weather Music Player")

style = ttk.Style()
style.configure("TFrame", background="#ADD8E6")
style.configure("TButton", background="#b1b1b1", font=("Helvetica", 12))
style.configure("TLabel", background="#ADD8E6", font=("Helvetica", 12))

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
