import streamlit as st
import requests
from pyowm import OWM
from geopy.geocoders import Nominatim

owm = OWM('47d570067856f5d716bbea83635e8c26')
mgr = owm.weather_manager()

st.title('Weather Prediction App US')
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

def validate_city_state(city, state):
    # Create a geocoder object
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Geocode the city and state to get coordinates
    location = geolocator.geocode(f"{city}, {state}")

    if location:
        # Reverse geocode the coordinates to get the address components
        reverse_location = geolocator.reverse((location.latitude, location.longitude))

        # Extract city and state from the reverse geocoded address
        reverse_city = reverse_location.raw.get('address', {}).get('city', '')
        reverse_state = reverse_location.raw.get('address', {}).get('state', '')

        # Validate if the reverse geocoded city and state match the user-provided values
        if reverse_city.lower() == city.lower() and reverse_state.lower() == state.lower():
            return True
        else:
            return False
    else:
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
