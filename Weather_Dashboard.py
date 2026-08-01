import streamlit as st
import requests
import pandas as pd
import datetime
from datetime import datetime as dt
import json

st.set_page_config(page_title="India Weather & AQI Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { padding: 20px; }
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 India Weather & AQI Dashboard")
st.markdown("Real-time Air Quality Index and Weather Data")

# Sidebar Navigation
option = st.sidebar.radio(
    "Select Option:",
    ["🌫️ Air Quality Index", "🌡️ Temperature & Weather"]
)

# ==================== AQI SECTION ====================
if option == "🌫️ Air Quality Index":
    st.header("Air Quality Index (AQI) Information")

    # List of major Indian cities for AQI
    indian_cities = {
        "Delhi": "Delhi",
        "Mumbai": "Mumbai",
        "Bangalore": "Bangalore",
        "Kolkata": "Kolkata",
        "Chennai": "Chennai",
        "Hyderabad": "Hyderabad",
        "Pune": "Pune",
        "Ahmedabad": "Ahmedabad",
        "Jaipur": "Jaipur",
        "Lucknow": "Lucknow",
        "Indore": "Indore",
        "Varanasi": "Varanasi",
        "Chandigarh": "Chandigarh",
        "Srinagar": "Srinagar",
        "Visakhapatnam": "Visakhapatnam",
        "Patna": "Patna",
        "Kanpur": "Kanpur",
        "Gurgaon": "Gurgaon",
        "Noida": "Noida",
        "Thane": "Thane",
    }


    @st.cache_data(ttl=3600)
    def fetch_aqi_data(city):
        """Fetch AQI data from WAQI API"""
        try:
            url = f"https://api.waqi.info/feed/{city}/?token=demo"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data['status'] == 'ok':
                return data['data']
            else:
                return None
        except Exception as e:
            st.error(f"Error fetching data for {city}: {str(e)}")
            return None


    def get_aqi_category(aqi_value):
        """Categorize AQI value"""
        if aqi_value <= 50:
            return "🟢 Good", "#00AA00"
        elif aqi_value <= 100:
            return "🟡 Moderate", "#FFFF00"
        elif aqi_value <= 150:
            return "🟠 Unhealthy for Sensitive Groups", "#FFA500"
        elif aqi_value <= 200:
            return "🔴 Unhealthy", "#FF0000"
        elif aqi_value <= 300:
            return "🟣 Very Unhealthy", "#8B0000"
        else:
            return "⬛ Hazardous", "#800080"


    st.subheader("Fetch Top 5 Cleanest & Most Polluted Cities")

    if st.button("📊 Generate AQI Report", key="aqi_button"):
        with st.spinner("Fetching AQI data for all cities..."):
            aqi_results = []

            for city_name in indian_cities.values():
                aqi_data = fetch_aqi_data(city_name)
                if aqi_data and 'aqi' in aqi_data:
                    aqi_results.append({
                        'City': city_name,
                        'AQI': aqi_data['aqi'],
                        'PM2.5': aqi_data.get('iaqi', {}).get('pm25', {}).get('v', 'N/A'),
                        'PM10': aqi_data.get('iaqi', {}).get('pm10', {}).get('v', 'N/A'),
                        'NO2': aqi_data.get('iaqi', {}).get('no2', {}).get('v', 'N/A'),
                    })

            if aqi_results:
                df = pd.DataFrame(aqi_results)
                df = df.sort_values('AQI')

                # Top 5 Cleanest Cities
                st.subheader("🟢 Top 5 Cleanest Cities")
                cleanest = df.head(5)
                for idx, row in cleanest.iterrows():
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col1:
                        st.write(f"**{row['City']}**")
                    with col2:
                        category, color = get_aqi_category(row['AQI'])
                        st.markdown(f"<span style='color: {color}; font-weight: bold;'>{row['AQI']}</span>",
                                    unsafe_allow_html=True)
                    with col3:
                        st.write(f"{category}")

                st.divider()

                # Top 5 Most Polluted Cities
                st.subheader("🔴 Top 5 Most Polluted Cities")
                polluted = df.tail(5)
                for idx, row in polluted.iterrows():
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col1:
                        st.write(f"**{row['City']}**")
                    with col2:
                        category, color = get_aqi_category(row['AQI'])
                        st.markdown(f"<span style='color: {color}; font-weight: bold;'>{row['AQI']}</span>",
                                    unsafe_allow_html=True)
                    with col3:
                        st.write(f"{category}")

                st.divider()

                # Full AQI Table
                st.subheader("📋 All Cities - Detailed AQI Data")
                st.dataframe(df.sort_values('AQI', ascending=False), use_container_width=True)

# ==================== TEMPERATURE SECTION ====================
else:
    st.header("🌡️ Temperature & Weather Information")

    # Indian States and their major cities
    states_data = {
        "Delhi": ["Delhi", "Noida", "Gurgaon"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Aurangabad"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Meerut", "Agra"],
        "Karnataka": ["Bangalore", "Mysore", "Hubli"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
        "Telangana": ["Hyderabad", "Warangal"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur"],
        "West Bengal": ["Kolkata", "Darjeeling", "Siliguri"],
        "Haryana": ["Chandigarh", "Hisar"],
        "Punjab": ["Chandigarh", "Amritsar", "Ludhiana"],
        "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala"],
        "Jammu & Kashmir": ["Srinagar", "Leh", "Jammu"],
        "Bihar": ["Patna", "Gaya"],
        "Madhya Pradesh": ["Indore", "Bhopal", "Gwalior"],
        "Goa": ["Panaji", "Margao"],
        "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"],
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada"],
    }

    col1, col2 = st.columns(2)

    with col1:
        selected_state = st.selectbox("Select State:", list(states_data.keys()))

    with col2:
        cities = states_data[selected_state]
        selected_city = st.selectbox("Select City:", cities)


    @st.cache_data(ttl=3600)
    def fetch_weather_data(city_name):
        """Fetch weather data using Open-Meteo API (no API key needed)"""
        try:
            # First, get coordinates using Geocoding API
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&country=India&language=en&limit=1"
            geo_response = requests.get(geo_url, timeout=10)
            geo_data = geo_response.json()

            if 'results' not in geo_data or len(geo_data['results']) == 0:
                return None

            location = geo_data['results'][0]
            latitude = location['latitude']
            longitude = location['longitude']

            # Fetch weather data
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset&timezone=Asia/Kolkata"

            weather_response = requests.get(weather_url, timeout=10)
            weather_data = weather_response.json()

            if weather_response.status_code == 200:
                return {
                    'current': weather_data['current'],
                    'daily': weather_data['daily'],
                    'timezone': weather_data['timezone']
                }
            else:
                return None
        except Exception as e:
            st.error(f"Error fetching weather data: {str(e)}")
            return None


    def celsius_to_fahrenheit(celsius):
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9 / 5) + 32


    def get_weather_description(code):
        """Get weather description from WMO code"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Heavy drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail",
        }
        return weather_codes.get(code, "Unknown")


    if st.button("🔍 Fetch Weather Data"):
        weather_info = fetch_weather_data(selected_city)

        if weather_info:
            current = weather_info['current']
            daily = weather_info['daily']

            # Current Weather
            st.subheader(f"📍 {selected_city}, {selected_state}")

            col1, col2, col3, col4 = st.columns(4)

            temp_c = current['temperature_2m']
            temp_f = celsius_to_fahrenheit(temp_c)

            with col1:
                st.metric(
                    "🌡️ Current Temperature",
                    f"{temp_c}°C",
                    f"({temp_f:.1f}°F)"
                )

            with col2:
                st.metric(
                    "💧 Humidity",
                    f"{current['relative_humidity_2m']}%"
                )

            with col3:
                st.metric(
                    "💨 Wind Speed",
                    f"{current['wind_speed_10m']} km/h"
                )

            with col4:
                weather_desc = get_weather_description(current.get('weather_code', 0))
                st.metric(
                    "🌤️ Condition",
                    weather_desc
                )

            st.divider()

            # Detailed Information
            st.subheader("📅 5-Day Forecast")

            forecast_data = []
            for i in range(len(daily['time'])):
                date = daily['time'][i]
                max_temp_c = daily['temperature_2m_max'][i]
                min_temp_c = daily['temperature_2m_min'][i]
                max_temp_f = celsius_to_fahrenheit(max_temp_c)
                min_temp_f = celsius_to_fahrenheit(min_temp_c)
                rainfall = daily['precipitation_sum'][i]
                sunrise = daily['sunrise'][i].split('T')[1]
                sunset = daily['sunset'][i].split('T')[1]

                forecast_data.append({
                    'Date': date,
                    'High (°C)': round(max_temp_c, 1),
                    'High (°F)': round(max_temp_f, 1),
                    'Low (°C)': round(min_temp_c, 1),
                    'Low (°F)': round(min_temp_f, 1),
                    'Rainfall (mm)': rainfall,
                    'Sunrise': sunrise,
                    'Sunset': sunset
                })

            forecast_df = pd.DataFrame(forecast_data)
            st.dataframe(forecast_df, use_container_width=True)

            st.divider()

            # Sunrise and Sunset Times
            st.subheader("🌅 Sunrise & Sunset Times (Today)")

            col1, col2 = st.columns(2)

            with col1:
                sunrise_time = daily['sunrise'][0].split('T')[1]
                st.info(f"🌅 Sunrise: **{sunrise_time}**")

            with col2:
                sunset_time = daily['sunset'][0].split('T')[1]
                st.warning(f"🌇 Sunset: **{sunset_time}**")

        else:
            st.error("Could not fetch weather data for the selected city.")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px; margin-top: 20px;'>
    📊 Data Sources: Open-Meteo API | WAQI.info | Last Updated: """ + datetime.datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S") + """
    </div>
    """, unsafe_allow_html=True)