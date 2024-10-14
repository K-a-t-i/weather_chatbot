import os
import requests
import json
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import dateparser

# Load environment variables
load_dotenv()

# Set up API keys (retrieved from environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
METEOBLUE_API_KEY = os.getenv("METEOBLUE_API_KEY")
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
VISUALCROSSING_API_KEY = os.getenv("VISUALCROSSING_API_KEY")

# Initialize OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

def get_future_weather_data(location, date):
    base_url = "https://my.meteoblue.com/packages/basic-1h"
    params = {
        "apikey": METEOBLUE_API_KEY,
        "lat": location["lat"],
        "lon": location["lon"],
        "asl": "0",
        "format": "json",
        "tz": "UTC"
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        
        if "data_1h" not in data:
            return "Sorry, I couldn't retrieve detailed weather information at this time."
        
        forecast = data["data_1h"]
        
        date_index = (date - datetime.now().date()).days
        if 0 <= date_index <= 6:
            # Get the average values for the day
            temp = sum(forecast.get("temperature", [0] * 24)[date_index*24:(date_index+1)*24]) / 24
            wind_speed = sum(forecast.get("windspeed", [0] * 24)[date_index*24:(date_index+1)*24]) / 24
            wind_direction = sum(forecast.get("winddirection", [0] * 24)[date_index*24:(date_index+1)*24]) / 24
            precip = sum(forecast.get("precipitation", [0] * 24)[date_index*24:(date_index+1)*24])
            snow = sum(forecast.get("snowfall", [0] * 24)[date_index*24:(date_index+1)*24])
            relative_humidity = sum(forecast.get("relativehumidity", [0] * 24)[date_index*24:(date_index+1)*24]) / 24
            pressure = sum(forecast.get("pressure", [0] * 24)[date_index*24:(date_index+1)*24]) / 24
            cloud_cover = sum(forecast.get("cloudcover", [0] * 24)[date_index*24:(date_index+1)*24]) / 24
            
            return format_weather_info(location, date, temp, wind_speed, wind_direction, precip, snow, relative_humidity, pressure, cloud_cover)
        else:
            return "Sorry, I can only provide weather information for today and the next 6 days."
    else:
        return "Sorry, I couldn't retrieve the weather information at this time."

def get_historical_weather_data(location, date):
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location['lat']},{location['lon']}/{date.strftime('%Y-%m-%d')}"
    params = {
        "unitGroup": "metric",
        "key": VISUALCROSSING_API_KEY,
        "contentType": "json",
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        day_data = data['days'][0]
        
        temp = day_data['temp']
        wind_speed = day_data['windspeed']
        wind_direction = day_data['winddir']
        precip = day_data['precip']
        snow = day_data['snow']
        relative_humidity = day_data['humidity']
        pressure = day_data['pressure']
        cloud_cover = day_data['cloudcover']
        
        return format_weather_info(location, date, temp, wind_speed, wind_direction, precip, snow, relative_humidity, pressure, cloud_cover, is_historical=True)
    else:
        return "Sorry, I couldn't retrieve the historical weather information at this time."

def format_weather_info(location, date, temp, wind_speed, wind_direction, precip, snow, relative_humidity, pressure, cloud_cover, is_historical=False):
    # Convert wind speed to knots (1 km/h ≈ 0.54 knots)
    wind_speed_knots = wind_speed * 0.54
    
    # Estimating fog/mist
    fog_or_mist = "No fog/mist reported" if relative_humidity < 90 else "Possible fog/mist (FG/BR)"
    
    # Improved weather condition determination
    if snow > 0:
        condition = "snowy"
    elif precip > 5:
        condition = "rainy"
    elif relative_humidity > 90:
        condition = "foggy"
    elif cloud_cover < 20:
        condition = "sunny"
    elif cloud_cover < 70:
        condition = "partly cloudy"
    else:
        condition = "cloudy"
    
    if temp < 0:
        condition = "freezing " + condition
    elif temp > 30:
        condition = "hot and " + condition
    
    verb = "was" if is_historical else "is expected to be"
    
    # Formatting the output
    weather_info = f"""On {date.strftime('%Y-%m-%d')}, the weather in {location['name']} {verb} {condition}. The average temperature {verb} {temp:.2f}°C, with {precip:.1f}mm of precipitation and average wind speeds of {wind_speed:.2f}km/h.

- Average Temperature: {temp:.2f}°C
- Average Wind Speed: {wind_speed:.2f} km/h
- Total Precipitation: {precip:.1f} mm
- Average Relative Humidity: {relative_humidity:.0f}%
- Average Cloud Cover: {cloud_cover:.0f}%

Weather information for our pilots:
- Average Temperature: {temp:.2f}°C
- Wind: {wind_speed:.2f} km/h ({wind_speed_knots:.1f} knots) from {wind_direction:.0f}° (DD)
- Precipitation (RA): {precip:.1f} mm
- Snow (SN): {snow:.1f} mm
- Average Relative Humidity (RH): {relative_humidity:.0f}%
- Average Barometric Pressure (QNH): {pressure:.0f} hPa
- {fog_or_mist}
- Freezing Level (FZ LVL): Information not available
- Ceiling Height (CIG): Information not available"""

    return weather_info

def get_location_coordinates(location_name):
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": location_name,
        "key": OPENCAGE_API_KEY,
        "limit": 1
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            result = data["results"][0]
            return {
                "lat": result["geometry"]["lat"],
                "lon": result["geometry"]["lng"],
                "name": result["formatted"]
            }
    return None

def parse_date(date_string):
    # Handle day names first
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_name = date_string.lower()
    if day_name in days:
        current_date = datetime.now().date()
        current_day = current_date.weekday()
        target_day = days.index(day_name)
        days_ahead = target_day - current_day
        if days_ahead <= 0:  # Target day is today or in the past week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    
    # If not a day name, use dateparser
    parsed_date = dateparser.parse(date_string, settings={'RELATIVE_BASE': datetime.now(), 'PREFER_DATES_FROM': 'future'})
    if parsed_date:
        return parsed_date.date()
    else:
        raise ValueError(f"Unable to parse date: {date_string}")

def get_weather(location, date):
    coordinates = get_location_coordinates(location)
    if coordinates is None:
        return f"I'm sorry, but I don't have information for the location '{location}'. Could you please check the spelling or try asking about a different city?"
    
    today = datetime.now().date()
    if date < today:
        weather_data = get_historical_weather_data(coordinates, date)
    else:
        weather_data = get_future_weather_data(coordinates, date)
    return weather_data

def handle_conversation(query):
    functions = [
        {
            "name": "get_weather",
            "description": "Get weather information for a specific location and date (past, present, or up to 6 days in the future)",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or location for the weather forecast"
                    },
                    "date": {
                        "type": "string",
                        "description": "The date for the weather forecast (e.g., 'today', 'tomorrow', 'next Monday', 'September 26, 2024')"
                    }
                },
                "required": ["location", "date"]
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can engage in general conversation and provide weather information when asked. You can provide historical weather data for past dates, current weather, and forecasts for up to 6 days in the future. If the user doesn't specify a location or date for weather, assume they're asking about Berlin for today."},
            {"role": "user", "content": query}
        ],
        functions=functions,
        function_call="auto"
    )

    message = response.choices[0].message

    if message.function_call:
        function_name = message.function_call.name
        function_args = json.loads(message.function_call.arguments)
        
        if function_name == "get_weather":
            location = function_args.get("location", "Berlin")
            date_string = function_args.get("date", "today")
            
            try:
                date = parse_date(date_string)
                today = datetime.now().date()
                
                if (date - today).days > 6:
                    return f"I'm sorry, but I can only provide weather for the past, today and up to 6 days in the future. The date you asked about ({date.strftime('%Y-%m-%d')}) is too far in the future. The latest date I can provide a forecast for is {(today + timedelta(days=6)).strftime('%Y-%m-%d')}. Would you like to know the weather for {location} on that date instead?"
                
                weather_info = get_weather(location, date)
                
                return weather_info
            except ValueError as e:
                return f"I am happy to tell you the weather, if you give me a date and location. And I'm sorry, I couldn't understand this date. {str(e)}"
        else:
            return "I'm sorry, I don't know how to handle that request."
    else:
        # If no function was called, it means the query wasn't about weather
        return message.content

def main():
    print("Welcome to our Weather Chatbot initialized by Sasha & Fabian!")
    print("You can ask about the weather for any location in the world, for past dates, today, and up to 6 days in the future.")
    print("You can also chat with me about other topics!")
    print("Type 'exit' to quit the chatbot.")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        try:
            response = handle_conversation(user_input)
            print(f"Chatbot: {response}")
        except Exception as e:
            print(f"Chatbot: I'm sorry, I encountered an error: {str(e)}")

if __name__ == "__main__":
    main()
