import urllib.request
import json

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
        raise ValueError(
            f"Geocoding API error: {data['status']} for '{city}, {state}'")

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]


_ROUTES_API_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

def get_routes(origin: str, destination: str, travel_mode: str = "DRIVE") -> str:
    """
    Find routes between two locations using the Google Routes API.

    Args:
        origin:       The starting location (e.g. "New York, NY")
        destination:  The destination location (e.g. "Boston, MA")
        travel_mode:  Mode of travel - "DRIVE", "WALK", "BICYCLE", or "TRANSIT"
                      (default: "DRIVE")

    Returns:
        A JSON string containing either:
        - A list of routes with duration, distance, and turn-by-turn directions
        - An error message if the request fails
    """
    valid_modes = {"DRIVE", "WALK", "BICYCLE", "TRANSIT"}
    travel_mode = travel_mode.upper()
    if travel_mode not in valid_modes:
        return json.dumps({"error": f"Invalid travel_mode '{travel_mode}'. Must be one of {valid_modes}"})

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_KEY,
        "X-Goog-FieldMask": (
            "routes.description,"
            "routes.duration,"
            "routes.distanceMeters,"
            "routes.legs.steps.navigationInstruction,"
            "routes.legs.steps.distanceMeters,"
            "routes.legs.steps.staticDuration,"
            "routes.warnings"
        ),
    }

    payload = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": travel_mode,
        "computeAlternativeRoutes": True,
        "languageCode": "en-US",
        "units": "METRIC",
    }

    try:
        response = requests.post(_ROUTES_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError:
        return json.dumps({"error": f"HTTP error {response.status_code}", "details": response.text})
    except requests.exceptions.ConnectionError:
        return json.dumps({"error": "Connection error. Please check your internet connection."})
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Request failed: {str(e)}"})

    raw_routes = data.get("routes", [])
    if not raw_routes:
        return json.dumps({"error": "No routes found between the given locations."})

    routes = []
    for i, route in enumerate(raw_routes, 1):
        duration_secs = int(route.get("duration", "0s").replace("s", ""))
        hours, remainder = divmod(duration_secs, 3600)
        minutes = remainder // 60

        steps = []
        for leg in route.get("legs", []):
            for step in leg.get("steps", []):
                instruction = step.get("navigationInstruction", {}).get("instructions", "")
                step_dist_m = step.get("distanceMeters", 0)
                step_dur_secs = int(step.get("staticDuration", "0s").replace("s", ""))
                if instruction:
                    steps.append({
                        "instruction": instruction,
                        "distance_km": round(step_dist_m / 1000, 2),
                        "duration_minutes": round(step_dur_secs / 60, 1),
                    })

        routes.append({
            "route_number": i,
            "name": route.get("displayName", f"Route {i}"),
            "description": route.get("description", ""),
            "duration": f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m",
            "distance_km": round(route.get("distanceMeters", 0) / 1000, 1),
            "warnings": route.get("warnings", []),
            "steps": steps,
        })

    return json.dumps({"origin": origin, "destination": destination, "travel_mode": travel_mode, "routes": routes}, indent=2)