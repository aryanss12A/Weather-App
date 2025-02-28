import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

# OpenWeatherMap API details
API_KEY = "46a32b30f46394adf16296f3654fbe26"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# List of popular cities
CITIES = ["New York", "London,UK", "Paris,FR", "Tokyo,JP", "Sydney,AU", "Mumbai,IN", "Dubai,AE", "Berlin,DE", "Moscow,RU", "Toronto,CA"]

# Function to fetch and display weather for multiple cities
def get_weather():
    selected_cities = [city_listbox.get(idx) for idx in city_listbox.curselection()]
    if not selected_cities:
        messagebox.showerror("Error", "Please select at least one city")
        return
    
    weather_frame.pack_forget()
    weather_frame.pack(pady=10)

    for widget in weather_frame.winfo_children():
        widget.destroy()
    
    for city in selected_cities:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        print(response.url)
        print(response.status_code)
        print(response.text)
        
        if response.status_code == 200:
            data = response.json()
            city_name = data.get("name", "Unknown City")
            country = data["sys"].get("country", "Unknown Country")
            temp_c = data["main"].get("temp", "N/A")
            temp_f = round((temp_c * 9/5) + 32, 2) if temp_c != "N/A" else "N/A"
            weather_desc = data["weather"][0]["description"].title()
            icon_code = data["weather"][0]["icon"]

            # Fetch weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            if icon_response.status_code == 200:
                img_data = icon_response.content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((50, 50))
                icon_img = ImageTk.PhotoImage(img)

                # Display city weather
                city_frame = tk.Frame(weather_frame)
                city_frame.pack(pady=5)
                icon_label = tk.Label(city_frame, image=icon_img)
                icon_label.image = icon_img
                icon_label.pack(side="left")
                
                details_label = tk.Label(city_frame, text=f"{city_name}, {country}\n{temp_c}°C\n{temp_f}°F\n{weather_desc}", font=("Arial", 10))
                details_label.pack(side="left", padx=10)

                get_forecast(city, city_frame)
        else:
            messagebox.showerror("Error", f"Weather data not found for {city}")

# Function to fetch and display 5-day forecast
def get_forecast(city, parent_frame):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(FORECAST_URL, params=params)
    print(response.url)
    print(response.status_code)
    print(response.text)
    
    if response.status_code == 200:
        data = response.json()
        forecast_list = data.get("list", [])

        forecast_frame = tk.Frame(parent_frame)
        forecast_frame.pack(pady=5)

        for i in range(0, len(forecast_list), 8):
            forecast = forecast_list[i]
            date = forecast.get("dt_txt", "N/A").split(" ")[0]
            temp_c = forecast["main"].get("temp", "N/A")
            temp_f = round((temp_c * 9/5) + 32, 2) if temp_c != "N/A" else "N/A"
            desc = forecast["weather"][0]["description"].title()
            icon_code = forecast["weather"][0]["icon"]

            # Fetch weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            if icon_response.status_code == 200:
                img_data = icon_response.content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((40, 40))
                icon_img = ImageTk.PhotoImage(img)

                # Create forecast label
                forecast_label = tk.Label(forecast_frame, text=f"{date}\n{temp_c}°C\n{temp_f}°F\n{desc}", image=icon_img, compound="top", font=("Arial", 8))
                forecast_label.image = icon_img
                forecast_label.pack(side="left", padx=5)
    
# Create GUI window
root = tk.Tk()
root.title("Multi-City Weather App")
root.geometry("500x600")

# Label for city selection
tk.Label(root, text="Select Cities:", font=("Arial", 12)).pack(pady=5)

# Listbox for city selection
city_listbox = tk.Listbox(root, selectmode="multiple", height=10, font=("Arial", 10))
for city in CITIES:
    city_listbox.insert(tk.END, city)
city_listbox.pack(pady=5)

# Button to fetch weather
search_button = tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather)
search_button.pack(pady=10)

# Frame to display weather results
weather_frame = tk.Frame(root)
weather_frame.pack(pady=10)

# Run the app
root.mainloop()
