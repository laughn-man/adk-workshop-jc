
import urllib.request
import json
import os

import requests

from config import GOOGLE_MAPS_KEY

def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch weather forecast from the National Weather Service API.
    
    Args:
        latitude: The latitude of the location
        longitude: The longitude of the location
        
    Returns:
        A dictionary containing the weather forecast data
        
    Raises:
        requests.HTTPError: If the API request fails
        ValueError: If the coordinates are invalid
    """
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise ValueError("Invalid coordinates. Latitude must be between -90 and 90, "
                         "longitude must be between -180 and 180.")

    headers = {
        "User-Agent": "WeatherApp/1.0 (your@email.com)",
        "Accept": "application/geo+json"
    }

    # Step 1: Get the grid points for the given coordinates
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(points_url, headers=headers)
    response.raise_for_status()
    points_data = response.json()

    properties = points_data.get("properties", {})
    forecast_url = properties.get("forecast")
    location_info = {
        "city": properties.get("relativeLocation", {}).get("properties", {}).get("city"),
        "state": properties.get("relativeLocation", {}).get("properties", {}).get("state"),
        "grid_office": properties.get("gridId"),
    }

    if not forecast_url:
        raise ValueError("Could not retrieve forecast URL from NWS API.")

    # Step 2: Get the forecast using the forecast URL
    forecast_response = requests.get(forecast_url, headers=headers)
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    periods = forecast_data.get("properties", {}).get("periods", [])

    return {
        "location": location_info,
        "forecast": [
            {
                "name": period.get("name"),
                "temperature": period.get("temperature"),
                "temperature_unit": period.get("temperatureUnit"),
                "wind_speed": period.get("windSpeed"),
                "wind_direction": period.get("windDirection"),
                "short_forecast": period.get("shortForecast"),
                "detailed_forecast": period.get("detailedForecast"),
                "is_daytime": period.get("isDaytime"),
            }
            for period in periods
        ],
    }

def get_lat_lon(city: str, state: str) -> tuple[float, float]:
    """
    Fetch latitude and longitude for a given city and state using Google Geocoding API.

    Args:
        city: City name (e.g. "Austin")
        state: State name or abbreviation (e.g. "TX" or "Texas")

    Returns:
        A tuple of (latitude, longitude)

    Raises:
        ValueError: If the location is not found or the API returns an error
    """
    address = urllib.parse.quote(f"{city}, {state}")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_KEY}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    if data["status"] != "OK":
        raise ValueError(f"Geocoding API error: {data['status']} for '{city}, {state}'")

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]