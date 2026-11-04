function getWeatherIcon(code) {
  if (code === 0) {
    return "☀️";
  } else if (code === 1 || code === 2) {
    return "🌤️";
  } else if (code === 3) {
    return "☁️";
  } else if (code === 45 || code === 48) {
    return "🌫️";
  } else if (code >= 51 && code <= 67) {
    return "🌧️";
  } else if (code >= 71 && code <= 77) {
    return "❄️";
  } else if (code >= 80 && code <= 82) {
    return "🌦️";
  } else if (code === 85 || code === 86) {
    return "🌨️";
  } else if (code >= 95 && code <= 99) {
    return "⛈️";
  }

  return "🌡️";
}

async function fetchWeatherData(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

function renderTemperatureChart(forecast) {
  const chart = document.getElementById("temperature-chart");
  chart.innerHTML = "";

  const chartDays = document.createElement("div");
  chartDays.className = "temperature-days";

  const temperatures = forecast.flatMap(function (day) {
    return [day.max_temperature, day.min_temperature];
  });

  const minTemperature = Math.min(...temperatures);
  const maxTemperature = Math.max(...temperatures);
  const temperatureRange = maxTemperature - minTemperature || 1;

  forecast.forEach(function (day) {
    const dayElement = document.createElement("div");
    dayElement.className = "temperature-day";

    const date = new Date(day.date + "T00:00:00");

    const readableDate = date.toLocaleDateString("en-GB", {
      weekday: "short",
      day: "numeric",
    });

    const highHeight =
      ((day.max_temperature - minTemperature) / temperatureRange) * 120 + 20;

    const lowHeight =
      ((day.min_temperature - minTemperature) / temperatureRange) * 120 + 20;

    const highLabel = document.createElement("p");
    highLabel.textContent = `${day.max_temperature}°C`;

    const bars = document.createElement("div");
    bars.className = "temperature-bars";

    const highBar = document.createElement("div");
    highBar.className = "temperature-bar temperature-high";
    highBar.style.height = `${highHeight}px`;
    highBar.title = `High: ${day.max_temperature}°C`;

    const lowBar = document.createElement("div");
    lowBar.className = "temperature-bar temperature-low";
    lowBar.style.height = `${lowHeight}px`;
    lowBar.title = `Low: ${day.min_temperature}°C`;

    bars.appendChild(highBar);
    bars.appendChild(lowBar);

    const lowLabel = document.createElement("p");
    lowLabel.textContent = `${day.min_temperature}°C`;

    const dateLabel = document.createElement("p");
    dateLabel.textContent = readableDate;

    dayElement.append(highLabel, bars, lowLabel, dateLabel);

    chartDays.appendChild(dayElement);
  });

  const legend = document.createElement("div");
  legend.className = "temperature-legend";

  const highLegend = document.createElement("span");
  highLegend.innerHTML = '<span class="legend-color legend-high"></span>High';

  const lowLegend = document.createElement("span");
  lowLegend.innerHTML = '<span class="legend-color legend-low"></span>Low';

  legend.append(highLegend, lowLegend);

  chart.append(chartDays, legend);
}

function renderForecast(forecast) {
  const forecastList = document.getElementById("forecast-list");
  forecastList.innerHTML = "";

  forecast.forEach(function (day) {
    const dayElement = document.createElement("div");
    dayElement.className = "forecast-day";

    const forecastDate = new Date(day.date + "T00:00:00");

    const readableDate = forecastDate.toLocaleDateString("en-GB", {
      weekday: "short",
      month: "short",
      day: "numeric",
    });

    const dateHeading = document.createElement("h3");
    dateHeading.textContent = readableDate;

    const description = document.createElement("p");
    description.textContent = `${getWeatherIcon(day.weather_code)} ${day.weather_description}`;

    const highTemperature = document.createElement("p");
    highTemperature.textContent = `High: ${day.max_temperature}°C`;

    const lowTemperature = document.createElement("p");
    lowTemperature.textContent = `Low: ${day.min_temperature}°C`;

    dayElement.append(
      dateHeading,
      description,
      highTemperature,
      lowTemperature,
    );

    forecastList.appendChild(dayElement);
  });
}

function clearWeatherData() {
  document.getElementById("location-name").textContent = "";
  document.getElementById("current-description").textContent = "";
  document.getElementById("current-temperature").textContent = "--";
  document.getElementById("current-humidity").textContent = "--";
  document.getElementById("current-wind").textContent = "--";

  document.getElementById("forecast-list").innerHTML = "";
  document.getElementById("temperature-chart").innerHTML = "";
}

function showErrorMessage(error) {
  if (error.message.includes("404")) {
    return "City not found. Please enter a valid city name.";
  }

  if (error.message.includes("502") || error.message.includes("503")) {
    return "Weather service is temporarily unavailable. Please try again later.";
  }

  return "Unable to connect. Please check your internet connection and try again.";
}

const cityInput = document.getElementById("city-input");
const searchForm = document.getElementById("search-form");
const searchButton = searchForm.querySelector("button");
const statusMessage = document.getElementById("status-message");

let searchId = 0;

searchForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const city = cityInput.value.trim();

  if (!city) {
    statusMessage.textContent = "Please enter a city name.";
    return;
  }

  const currentSearchId = ++searchId;

  statusMessage.textContent = "Loading weather...";
  searchButton.disabled = true;

  clearWeatherData();

  document.getElementById("forecast-list").textContent = "Loading forecast...";

  document.getElementById("temperature-chart").textContent =
    "Loading temperature trend...";

  try {
    const [weatherData, forecastData] = await Promise.all([
      fetchWeatherData(`/weather?city=${encodeURIComponent(city)}`),
      fetchWeatherData(`/forecast?city=${encodeURIComponent(city)}`),
    ]);

    if (currentSearchId !== searchId) {
      return;
    }

    document.getElementById("location-name").textContent =
      `${weatherData.city}, ${weatherData.country}`;

    document.getElementById("current-description").textContent =
      `${getWeatherIcon(weatherData.weather_code)} ${weatherData.weather_description}`;

    document.getElementById("current-temperature").textContent =
      weatherData.temperature;

    document.getElementById("current-humidity").textContent =
      weatherData.humidity;

    document.getElementById("current-wind").textContent =
      weatherData.wind_speed;

    renderForecast(forecastData.forecast);
    renderTemperatureChart(forecastData.forecast);

    statusMessage.textContent = "";
  } catch (error) {
    console.error("Weather dashboard error:", error);

    if (currentSearchId !== searchId) {
      return;
    }

    clearWeatherData();

    statusMessage.textContent = showErrorMessage(error);
  } finally {
    if (currentSearchId === searchId) {
      searchButton.disabled = false;
    }
  }
});
