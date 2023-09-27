// your-script.js

// Initialize the map
const map = L.map('map').setView([0, 0], 2);

// Add a tile layer (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Create a marker layer group
const markers = L.layerGroup().addTo(map);

// Function to fetch weather data from OpenWeatherMap
function fetchWeather(lat, lng) {
    let openweathermap_api_key;
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${openweathermap_api_key}&units=metric`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const weatherInfo = document.getElementById("weather-info");
            weatherInfo.innerHTML = `
                <p>Location: ${data.name}</p>
                <p>Temperature: ${data.main.temp} C</p>
                <p>Weather: ${data.weather[0].description}</p>
            `;
        })
        .catch(error => {
            console.error("Error fetching weather data:", error);
        });
}

// Function to handle map click event
function onMapClick(e) {
    markers.clearLayers();
    const marker = L.marker(e.latlng).addTo(markers);
    fetchWeather(e.latlng.lat, e.latlng.lng);
}

// Add click event listener to the map
map.on('click', onMapClick);

const geocoder = L.Control.geocoder({
    defaultMarkGeocode: false,
}).addTo(map);

// Function to handle geocode result
function onGeocodeResult(result) {
    const latlng = result.center;
    markers.clearLayers();
    L.marker(latlng).addTo(markers);
    map.setView(latlng, 10);
    fetchWeather(latlng.lat, latlng.lng);
}

// Add event listener for geocode result
geocoder.on('markgeocode', e => {
    onGeocodeResult(e.geocode);
});

// Function to handle search button click
