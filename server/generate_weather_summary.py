def generate_weather_summary(weather_data):
    total_temperature = 0
    min_temperature = float("inf")
    max_temperature = float("-inf")
    weather_count = {}
    windiest_location = {"lat": None, "lng": None, "wind_speed": 0}
    
    # Iterate over the weather data to calculate the summary
    for data in weather_data:
        # Calculate the total temperature and find the min and max temperatures
        total_temperature += data["temperature"]
        min_temperature = min(min_temperature, data["temperature"])
        max_temperature = max(max_temperature, data["temperature"])
        
        # Update the weather count
        if data["weather"] not in weather_count:
            weather_count[data["weather"]] = 1
        else:
            weather_count[data["weather"]] += 1
        
        # Update the windiest location
        if data["wind_speed"] > windiest_location["wind_speed"]:
            windiest_location = {
                "lat": data["lat"],
                "lng": data["lng"],
                "wind_speed": data["wind_speed"],
            }
    
    # Calculate the average temperature
    average_temperature = total_temperature / len(weather_data)
    
    # Find the most common weather condition
    most_common_weather = None
    max_weather_count = 0
    for weather in weather_count:
        if weather_count[weather] > max_weather_count:
            most_common_weather = weather
            max_weather_count = weather_count[weather]
    
    # Return the summary
    return {
        "averageTemperature": average_temperature,
        "minTemperature": min_temperature,
        "maxTemperature": max_temperature,
        "mostCommonWeather": most_common_weather,
        "windiestLocation": windiest_location,
    }
