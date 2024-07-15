import streamlit as st
import requests
from geopy.geocoders import Nominatim
import time

def get_weather(city):
    locator = Nominatim(user_agent="weather_app")
    location = locator.geocode(city)
    
    if location:
        latitude, longitude = location.latitude, location.longitude
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather = data['current_weather']
            temp = weather['temperature']
            wind_speed = weather['windspeed']
            time = weather['time']
            
            return location.address, temp, wind_speed, time
        else:
            return "Error fetching weather data. Please try again.", None, None, None
    else:
        return "Location not found.", None, None, None

# Streamlit UI
st.set_page_config(page_title="Weather Wizard", page_icon=":partly_sunny:", layout="wide")
st.title("🌤️ Weather Wizard")
st.markdown("### Your personal weather companion")
st.markdown("#### Developed by Shahid")

# Form for input and button
with st.form(key='weather_form'):
    city_name = st.text_input("Enter the name of country, city or village:", max_chars=50)
    submit_button = st.form_submit_button(label='Get Weather')

if submit_button and city_name:
    with st.spinner('Fetching weather data...'):
        time.sleep(2)  # Simulate loading time
        address, temp, wind_speed, time = get_weather(city_name)
    
    if address and temp is not None:
        st.success(f"Complete Address: {address}")
        st.write(f"**Current Temperature:** {temp} °C")
        st.write(f"**Current Wind Speed:** {wind_speed} km/h")
        st.write(f"**Time:** {time}")
    else:
        st.error(address)
