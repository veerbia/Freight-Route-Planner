<script>
  import { onMount } from 'svelte';

  let map; // variable to hold the map object
  let startMarker; // variable to hold the start marker object
  let endMarker; // variable to hold the end marker object
  let directionsService; // variable to hold the directions service object
  let directionsRenderer; // variable to hold the directions renderer object

  // Initialize the map and set up event listeners to allow users to select start and endpoints
  onMount(async () => {
    const apiKey = 'YOUR_API_KEY'; // replace with your Google Maps API key
    const mapElement = document.getElementById('map');

    // Load the Google Maps JavaScript API
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}`;
    document.head.appendChild(script);

    // Wait for the API to load
    await new Promise((resolve) => {
      script.onload = resolve;
    });

    // Initialize the map
    map = new google.maps.Map(mapElement, {
      zoom: 8,
      center: { lat: 37.7749, lng: -122.4194 }, // default center is San Francisco

      
    });

    // Set up event listeners to allow users to select start and endpoints
    google.maps.event.addListener(map, 'click', (event) => {
      // If no start marker has been set, create a start marker at the clicked location
      if (!startMarker) {
        startMarker = new google.maps.Marker({
          position: event.latLng,
          map: map,
          label: 'S',
        });
      }
      // If a start marker has been set but no end marker, create an end marker at the clicked location
      else if (!endMarker) {
        endMarker = new google.maps.Marker({
          position: event.latLng,
          map: map,
          label: 'E',
        });
      }
      // If both start and end markers have been set, remove them and create new ones at the clicked locations
      else {
        startMarker.setMap(null);
        endMarker.setMap(null);
        startMarker = new google.maps.Marker({
          position: event.latLng,
          map: map,
          label: 'S',
        });
        endMarker = null;
      }
    });
    // Initialize the directions service and directions renderer
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
  });

  // Calculate and display the route when the "Get Directions" button is clicked
  function getDirections() {
  // Get the start and end points from the markers
  const start = startMarker.getPosition();
  const end = endMarker.getPosition();
  // Set the start and end locations for the directions service
  const request = {
    origin: start,
    destination: end,
    travelMode: 'DRIVING', // set the mode of transportation to driving
  };

  // Call the directions service to calculate the route
  directionsService.route(request, (result, status) => {
    if (status === 'OK') {
      // Set the map and display the route
      directionsRenderer.setMap(map);
      directionsRenderer.setDirections(result);
    } else {
      // If the request fails, display an error message
      console.error(`Error: ${status}`);
    }
  });
}
</script>

<!-- HTML for the map and "Get Directions" button -->
<div id="map" style="height: 1000px; width: 1000px;"></div>
<button on:click={getDirections}>Get Directions</button>




