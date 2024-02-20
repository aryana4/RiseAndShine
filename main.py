import datetime as dt #used to take timestamp info sent from API
import requests #used to send requests to the API

# Constants
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = open("API_KEY.txt", "r").read() #API key is stored in a separate file
CITY = "Montreal"

def ConvertKelvin(temp):
    celsius = temp - 273.15
    farenheit = (celsius * 9/5) + 32
    return (celsius, farenheit)

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY

response = requests.get(url).json()

# Extracting the different parts of the API response
temp_kelvin = response['main']['temp']                                      #Temparature
temp_celsius, temp_farenheit = ConvertKelvin(temp_kelvin)
feel_like_kelvin = response['main']['feels_like']
feel_like_celsius, feel_like_farenheit = ConvertKelvin(feel_like_kelvin)    #Feels like Temperature
humidity = response['main']['humidity']                                     #Humidity
description = response['weather'][0]['description']                         #Weather Description
sunrise = dt.datetime.utcfromtimestamp(response['sys']['sunrise']   + response['timezone'] )             
sunset = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

# Printing the extracted data
print(f"Temperature in {CITY}: {temp_celsius:.0f}°C, {temp_farenheit:.0f}°F") 
print(f"Feels like: {feel_like_celsius:.0f}°C, {feel_like_farenheit:.0f}°F")
print(f"Humidity: {humidity}%")
print(f"Weather Description: {description}")
print(f"Sunrise: {sunrise}")
print(f"Sunset: {sunset}")