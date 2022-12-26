def generate_weather_summary(weather_data):
    total_temperature = 0
    total_wind_speed = 0
    total_visibility = 0
    weather_count = {}
    
    # Iterate over the weather data to calculate the summary
    for data in weather_data:
        # Calculate the total temperature, wind speed, and visibility
        total_temperature += data["temperature"]
        total_wind_speed += data["wind_speed"]
        total_visibility += data["visibility"]
        
        # Update the weather count
        if data["weather"] not in weather_count:
            weather_count[data["weather"]] = 1
        else:
            weather_count[data["weather"]] += 1
    
    
    # Calculate the average temperature
    average_temperature = total_temperature / len(weather_data)
    average_wind_speed = total_wind_speed / len(weather_data)
    average_visibility = total_visibility / len(weather_data)
    
    # Find the most common weather condition
    most_common_weather = None
    max_weather_count = 0
    for weather in weather_count:
        if weather_count[weather] > max_weather_count:
            most_common_weather = weather
            max_weather_count = weather_count[weather]
    
    # Return the summary
    return {
        "averageTemperature": int(average_temperature),
        "mostCommonWeather": most_common_weather,
        "averageWindSpeed": int(average_wind_speed),
        "averageVisibility": int(average_visibility)
    }
