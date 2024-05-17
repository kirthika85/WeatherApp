import streamlit as st
import requests
from pyowm import OWM
from geopy.geocoders import Nominatim

st.title('Weather Prediction App US')
owm_api_key=st.sidebar.text_input('OWM API Key', type='password')
if not owm_api_key:
   st.warning('Please enter your OWM API key!', icon='⚠')
else:
    owm = OWM(owm_api_key)
    mgr = owm.weather_manager()
    city = st.text_input('Enter the city name')
    us_states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
        'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
        'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
        'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
        'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
        'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA',
        'WV', 'WI', 'WY'
    ]    
    selected_state = st.selectbox('Select a state', us_states)
    st.write(selected_state)

    def validate_city_state(city, state):
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(f"{city}, {state}")

        if location:
              api_key = owm_api_key
              url = f'http://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api_key}'
              st.write(url)
              response = requests.get(url)
              weather_data = response.json()

              if 'main' in weather_data:
                  # Valid city and state mapping
                  return True
              else:
                  # Invalid city and state mapping
                  return False
        else:
           # Invalid city or state name
           return False
        
    if st.button('Check'):
        if city and selected_state:
            if validate_city_state(city, selected_state):
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
