from collections import defaultdict
from haversine import haversine

def generate_report(weather_data):
    # Create a dictionary to keep track of the frequency of each weather condition
    weather_counts = defaultdict(int)
    for data in weather_data:
        weather_counts[data['weather']] += 1

    # Determine the most common weather condition
    most_common_weather = max(weather_counts, key=weather_counts.get)

    # Generate the summary based on the most common weather condition
    if most_common_weather == 'Clear':
        common_summary = 'Overall, the route is expected to be clear ☀️ '
    elif most_common_weather == 'Rain':
        common_summary = 'Overall, the route is expected to be rainy 🌧️ '
    elif most_common_weather == 'Clouds':
        common_summary = 'Overall, the route is expected to be cloudy ☁️ '
    else:
        common_summary = 'Overall, the weather conditions on the route are expected to vary ⛅ '

    # Initialize variables to store the weather conditions and recommendations
    weatherConditions = []
    recommendations = []

    # Loop through the weather data and extract the weather conditions and recommendations
    visibility_flag = False
    wind_speed_flag = False
    temperature_flag = False
    for data in weather_data:
        weatherConditions.append(data['weather'])
        if data['visibility'] < 5000 and not visibility_flag:
            recommendations.append("You may want to use tires with improved traction due to low visibility.")
            visibility_flag = True
        if data['wind_speed'] > 10 and not wind_speed_flag:
            recommendations.append("It might be a good idea to use tires with improved stability due to high wind speeds.")
            wind_speed_flag = True
        if data['temperature'] < 0 and not temperature_flag:
            recommendations.append("Consider using tires with improved cold weather performance due to low temperatures.")
            temperature_flag = True

    # Determine the overall weather conditions for the route
    if "Rain" in weatherConditions:
        overallConditions = "Weather Advisory: There may be heavy rain along this route. "
    elif "Snow" in weatherConditions:
        overallConditions = "Weather Advisory: There may be snow along this route. "
    elif "Clouds" in weatherConditions:
        overallConditions = "There may be clouds along the route. "
    else:
        overallConditions = "The weather along the route is expected to be clear. "

    # Determine the best time to leave based on the weather conditions
    if "Rain" in weatherConditions:
        bestTimeToLeave = "It may be best to wait until the rain has passed to start your trip. "
    elif "Snow" in weatherConditions:
        bestTimeToLeave = "It may be best to wait until the snow has cleared to start your trip. "
    elif "Clouds" in weatherConditions:
        bestTimeToLeave = "You can leave anytime, as the weather is expected to be mostly cloudy. "
    else:
        bestTimeToLeave = "You can leave anytime, as the weather is expected to be clear. "

    # Determine the recommended freight load based on the distance of the route
    totalDistance = 0
    for i in range(1, len(weather_data)):
        point1 = (float(weather_data[i-1]['lat']), float(weather_data[i-1]['lng']))
        point2 = (float(weather_data[i]['lat']), float(weather_data[i]['lng']))
        totalDistance += haversine(point1, point2)
    if totalDistance > 500: # 500 km
        recommendedLoad = "It is recommended to carry a lighter load due to the long distance of the route. "
    else:
        recommendedLoad = "You can carry a normal load for this distance. "

    # Return the summary
    summary = common_summary + overallConditions + bestTimeToLeave + recommendedLoad + " ".join(recommendations)
    return summary

            

