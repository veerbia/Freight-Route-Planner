<script>
  import { onMount } from "svelte";
  import axios from "axios";
  import { set_now } from "svelte/internal";

  let map; // variable to hold the map object
  let directionsService; // variable to hold the directions service object
  let directionsRenderer; // variable to hold the directions renderer object
  let summary = {};
  let report = "";

  // Initialize the map and set up the autocomplete for the start and end inputs
  onMount(async () => {
    const apiKey = "YOUR_API_KEY"; // Replace with your Google Maps API key
    const mapElement = document.getElementById("map");
    const startInput = document.getElementById("start");
    const endInput = document.getElementById("end");

    // Load the Google Maps JavaScript API and the Places library
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
    document.head.appendChild(script);

    // Wait for the API and library to load
    await new Promise((resolve) => {
      script.onload = resolve;
    });

    // Initialize the map
    map = new google.maps.Map(mapElement, {
      zoom: 8,
      center: { lat: 37.7749, lng: -122.4194 }, // default center is San Francisco
    });

    // Initialize the autocomplete for the start and end inputs
    const startAutocomplete = new google.maps.places.Autocomplete(startInput);
    const endAutocomplete = new google.maps.places.Autocomplete(endInput);

    // Initialize the directions service and directions renderer
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
  });

  // Calculate and display the route when the "Get Directions" button is clicked
  async function getDirections() {
    // Get the start and end points from the textboxes
    const start = document.getElementById("start").value;
    const end = document.getElementById("end").value;

    // Use the Geocoding API to convert the text input into latitude and longitude coordinates
    const startCoords = await getCoordinates(start);
    const endCoords = await getCoordinates(end);

    // Set the start and end locations for the directions service
    const request = {
      origin: startCoords,
      destination: endCoords,
      travelMode: "DRIVING", // set the mode of transportation to driving
    };

    // Call the directions service to calculate the route
    directionsService.route(request, async (result, status) => {
      if (status === "OK") {
        // Set the map and display the route
        directionsRenderer.setMap(map);
        directionsRenderer.setDirections(result);

        // Extract the list of steps along the route
        const steps = result.routes[0].legs[0].steps;
        // console.log(steps);
        // Create a list to store the weather data for each step
        const weatherData = [];
        // Get the weather data for each step
        for (const step of steps) {
          // Extract the latitude and longitude for the step
          const lat = step.end_location.lat();
          const lng = step.end_location.lng();

          // Get the weather data for the step
          const data = await getWeatherData(lat, lng);
          // console.log(data); // log the weather data to the console as {"lat": lat, "lng": lng, "temperature": temperature, "wind_speed": wind_speed, "visibility": visibility, "weather": weather}
          weatherData.push(data);
        }
        // Generate a summary of the weather along the route
        summary = await generateWeatherSummary(weatherData);
        console.log(summary); // log the summary to the console

        // Generate a report of the weather along the route and recommendations
        report = await generateReport(weatherData);
        console.log(report); // log the report to the console

      } else {
        // If the request fails, display an error message
        console.error(`Error: ${status}`);
      }
    });
  }

  // Convert text input into latitude and longitude coordinates using the Geocoding API
  async function getCoordinates(address) {
    const apiKey = "YOUR_API_KEY"; // replace with your Google Maps API key
    const url = `https://maps.googleapis.com/maps/api/geocode/json?key=${apiKey}&address=${encodeURIComponent(
      address
    )}`;
    // Make the request to the Geocoding API
    const response = await fetch(url);
    const data = await response.json();

    // Extract the latitude and longitude from the API response
    const location = data.results[0].geometry.location;
    return { lat: location.lat, lng: location.lng };
  }

  // Get the weather data for a given location using the Python server
  async function getWeatherData(lat, lng) {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/weather?lat=${lat}&lng=${lng}`
      );
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  // Generate a summary of the weather along the route and recommendations
  // Generate the weather summary for a given list of weather data using the Python server
  async function generateWeatherSummary(weatherData) {
    try {
      const weatherDataString = JSON.stringify(weatherData);
      const response = await axios.get(
        `http://127.0.0.1:5000/generate-weather-summary?weatherData=${weatherDataString}`
      );
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  // Generate a report of the weather along the route and recommendations
  async function generateReport(weatherData) {
    try {
      const weatherDataString = JSON.stringify(weatherData);
      const response = await axios.get(
        `http://127.0.0.1:5000/generate-report?weatherData=${weatherDataString}`
      );
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }
</script>

<h1>Freight Route Planner</h1>
<!-- Place the endpoints input boxes and get directions button next to the map, stacked vertically -->
<div id="map-container">
  <div id="inputs">
    <input
      type="text"
      id="start"
      placeholder="Enter start location"
      autocomplete="on"
    />
    <input
      type="text"
      id="end"
      placeholder="Enter end location"
      autocomplete="on"
    />
    <button on:click={getDirections}>Get Directions</button>
  </div>
  <div id="map" />
</div>

