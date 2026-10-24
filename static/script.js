console.log("JavaScript is working!");

const cityInput = document.getElementById("city-input");

console.log(cityInput);

const searchForm = document.getElementById("search-form");

searchForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const city = cityInput.value;

  fetch(`/weather?city=${encodeURIComponent(city)}`)
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Could not fetch weather");
      }

      return response.json();
    })
    .then(function (data) {
      document.getElementById("location-name").textContent =
        `${data.city}, ${data.country}`;

      document.getElementById("current-description").textContent =
        data.weather_description;

      document.getElementById("current-temperature").textContent =
        data.temperature;

      document.getElementById("current-humidity").textContent = data.humidity;

      document.getElementById("current-wind").textContent = data.wind_speed;
    })
    .catch(function (error) {
      console.log(error.message);
    });

  fetch(`/forecast?city=${encodeURIComponent(city)}`)
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Could not fetch forecast");
      }

      return response.json();
    })
    .then(function (data) {
      const forecastList = document.getElementById("forecast-list");

      forecastList.innerHTML = "";

      data.forecast.forEach(function (day) {
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
    })

    .catch(function (error) {
      console.error("Forecast error:", error.message);

      document.getElementById("status-message").textContent =
        "Unable to fetch the forecast. Please try again.";
    });
});
