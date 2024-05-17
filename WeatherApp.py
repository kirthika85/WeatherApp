import streamlit as st
import requests
from pyowm import OWM
owm = OWM('47d570067856f5d716bbea83635e8c26')
mgr = owm.weather_manager()

# Streamlit app
st.title('Weather Prediction App')

# Input fields for city and state
city = st.text_input('Enter the city name')
state = st.text_input('Enter the state name')

# Button to predict weather
if st.button('Predict Weather'):
    if city and state:
        location = f'{city},{state},US'
        try:
            # Get weather forecast
            observation = mgr.weather_at_place(location)
            weather = observation.weather

            # Display weather forecast
            st.write(f'Weather forecast for {city}, {state}:')
            st.write(f'Temperature: {weather.temperature("fahrenheit")["temp"]} °F')
            st.write(f'Humidity: {weather.humidity} %')
            st.write(f'Wind Speed: {weather.wind()["speed"]} m/s')
            st.write(f'Weather Status: {weather.status}')
        except Exception as e:
            st.error(f'Error: {e}')
    else:
        st.warning('Please enter city and state')
