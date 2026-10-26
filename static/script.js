console.log("JavaScript is working!");

const cityInput = document.getElementById("city-input");

console.log(cityInput);

let searchId = 0;
const searchForm = document.getElementById("search-form");

searchForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const statusMessage = document.getElementById("status-message");
  statusMessage.textContent = "Loading weather...";

  // Clear the previous search results
  document.getElementById("location-name").textContent = "";
  document.getElementById("current-description").textContent = "";
  document.getElementById("current-temperature").textContent = "";
  document.getElementById("current-humidity").textContent = "";
  document.getElementById("current-wind").textContent = "";
  document.getElementById("forecast-list").innerHTML = "";

  const city = cityInput.value.trim();

  if (!city) {
    statusMessage.textContent = "Please enter a city name.";
    return;
  }

  const currentSearchId = ++searchId;

  Promise.all([
    fetch(`/weather?city=${encodeURIComponent(city)}`).then(
      function (response) {
        if (!response.ok) {
          throw new Error(`Weather request failed: ${response.status}`);
        }
        return response.json();
      },
    ),

    fetch(`/forecast?city=${encodeURIComponent(city)}`).then(
      function (response) {
        if (!response.ok) {
          throw new Error(`Forecast request failed: ${response.status}`);
        }
        return response.json();
      },
    ),
  ])
    .then(function ([weatherData, forecastData]) {
      if (currentSearchId !== searchId) {
        return;
      }
      document.getElementById("location-name").textContent =
        `${weatherData.city}, ${weatherData.country}`;

      document.getElementById("current-description").textContent =
        weatherData.weather_description;

      document.getElementById("current-temperature").textContent =
        weatherData.temperature;

      document.getElementById("current-humidity").textContent =
        weatherData.humidity;

      document.getElementById("current-wind").textContent =
        weatherData.wind_speed;

      const forecastList = document.getElementById("forecast-list");
      forecastList.innerHTML = "";

      forecastData.forecast.forEach(function (day) {
        const dayElement = document.createElement("div");
        dayElement.className = "forecast-day";

        dayElement.innerHTML = `
          <h3>${day.date}</h3>
          <p>${day.weather_description}</p>
          <p>High: ${day.max_temperature}°C</p>
          <p>Low: ${day.min_temperature}°C</p>
        `;

        forecastList.appendChild(dayElement);
      });

      statusMessage.textContent = "";
    })
    .catch(function (error) {
      console.error("Weather dashboard error:", error.message);

      if (currentSearchId !== searchId) {
        return;
      }

      if (error.message.includes("404")) {
        statusMessage.textContent =
          "City not found. Please enter a valid city name.";
      } else if (
        error.message.includes("502") ||
        error.message.includes("503")
      ) {
        statusMessage.textContent =
          "Weather service is temporarily unavailable. Please try again later.";
      } else {
        statusMessage.textContent =
          "Unable to connect. Please check your internet connection and try again.";
      }
    });
});
