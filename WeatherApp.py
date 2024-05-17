import streamlit as st
import requests
from pyowm import OWM
owm = OWM('47d570067856f5d716bbea83635e8c26')
mgr = owm.weather_manager()

st.title('Weather Prediction App US')
city = st.text_input('Enter the city name')
us_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
    'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
    'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
    'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
    'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West Virginia', 'Wisconsin', 'Wyoming'
]
selected_state = st.selectbox('Select a state', us_states)

def is_valid_city_state(city, state):
    api_key = "47d570067856f5d716bbea83635e8c26"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{state},US&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False
        
if st.button('Check'):
    if city and selected_state:
        if is_valid_city_state(city, selected_state):
            st.success(f'{city} is a valid city in {selected_state}')
        else:
            st.error(f'{city} is not a valid city in {selected_state}')
    else:
        st.warning('Please enter both a city and select a state')

if st.button('Predict Weather'):
    if city and selected_state:
        location = f'{city},{selected_state},US'
        try:
            input = mgr.weather_at_place(location)
            weather = input.weather
            st.write(f'Weather forecast for {city}, {selected_state}:')
            st.write(f'Temperature: {weather.temperature("fahrenheit")["temp"]} °F')
            st.write(f'Humidity: {weather.humidity} %')
            st.write(f'Wind Speed: {weather.wind()["speed"]} m/s')
            st.write(f'Weather Status: {weather.status}')
        except Exception as e:
            st.error(f'Error: {e}')
    else:
        st.warning('Please enter city and selected_state')
