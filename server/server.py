import requests
from flask import Flask, request
from flask_cors import CORS
import json

from generate_weather_summary import generate_weather_summary
from generate_report import generate_report

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
  return "Hello World!"

@app.route('/weather')
def get_weather_data():
  lat = request.args.get('lat')
  lng = request.args.get('lng')

  api_key = "YOUR_API_KEY" # Replace with your OpenWeatherMap API key
  url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&units=metric"

  response = requests.get(url)
  data = response.json()

  temperature = data['main']['temp']
  wind_speed = data['wind']['speed']
  visibility = data['visibility']
  weather = data['weather'][0]['main']

  return {"lat": lat, "lng": lng, "temperature": temperature, "wind_speed": wind_speed, "visibility": visibility, "weather": weather}


@app.route('/generate-weather-summary')
def generate_weather_summary_route():
  # Get the weather data from the query parameters
  weather_data_string = request.args.get('weatherData')
  weather_data = json.loads(weather_data_string)

  # Generate the weather summary
  summary = generate_weather_summary(weather_data)

  # Return the summary
  return summary

@app.route('/generate-report')
def generate_report_route():
  # Get the weather data from the query parameters
  weather_data_string = request.args.get('weatherData')
  weather_data = json.loads(weather_data_string)

  # Generate the report
  report = generate_report(weather_data)

  # Return the report
  return report




if __name__ == '__main__':
  app.run()