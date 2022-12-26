<script>
    import { Router, Route, Link } from "svelte-navigator";
    import About from "./About.svelte";
    import App from "./App.svelte";

</script>


<!-- <Router>
    <header>
      <h1>Freight Route Planner</h1>
      <nav>
        <Link to="/">Home</Link>
        <Link to="about">About</Link>
      </nav>
    </header>
    <main>
      <Route path="about" component={About} />
      <Route path="/">
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
  
        <style>
          h1 {
            text-align: center;
          }
          #map-container {
            display: flex;
            flex-direction: row;
          }
          #inputs {
            display: flex;
            flex-direction: column;
            margin-right: 20px;
          }
          #map {
            width: 900px;
            height: 600px;
          }
        </style>
      </Route>
    </main>
  </Router> --> 