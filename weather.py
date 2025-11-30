"""
MCP Weather Server using FastMCP

This server exposes weather tools using the National Weather Service API.
It provides two main tools:
- get_alerts: Get weather alerts for a US state
- get_forecast: Get weather forecast for a location using latitude/longitude
"""

import httpx
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
DEFAULT_TIMEOUT = 30.0
MAX_FORECAST_PERIODS = 5


async def make_nws_request(url: str) -> dict | None:
    """Make a request to the National Weather Service API."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return None
        except httpx.HTTPStatusError:
            return None
        except httpx.RequestError:
            return None


def format_alert(feature: dict) -> str:
    """Format a single weather alert for display."""
    props = feature.get("properties", {})
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No instructions provided')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g., CA, NY, TX)

    Returns:
        Current weather alerts for the specified state
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
    data = await make_nws_request(url)

    if not data:
        return f"Unable to fetch alerts for {state}. Please check the state code and try again."

    features = data.get("features", [])
    if not features:
        return f"No active alerts for {state}"

    alerts = [format_alert(feature) for feature in features]
    return f"Active alerts for {state}:\n" + "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location (e.g., 37.7749)
        longitude: Longitude of the location (e.g., -122.4194)

    Returns:
        Weather forecast for the specified location
    """
    # First, get the grid point for the coordinates
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return f"Unable to fetch forecast data for coordinates ({latitude}, {longitude}). The location may be outside the US."

    # Extract the forecast URL from the response
    properties = points_data.get("properties", {})
    forecast_url = properties.get("forecast")

    if not forecast_url:
        return "Unable to get forecast URL from weather service."

    # Fetch the actual forecast
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch forecast data."

    # Format the forecast periods
    periods = forecast_data.get("properties", {}).get("periods", [])
    if not periods:
        return "No forecast periods available."

    forecasts = []
    for period in periods[:MAX_FORECAST_PERIODS]:
        forecast = f"""
{period.get('name', 'Unknown')}:
Temperature: {period.get('temperature', 'N/A')}°{period.get('temperatureUnit', 'F')}
Wind: {period.get('windSpeed', 'N/A')} {period.get('windDirection', '')}
Forecast: {period.get('detailedForecast', 'No details available')}
"""
        forecasts.append(forecast)

    return f"Weather forecast for ({latitude}, {longitude}):\n" + "\n---\n".join(forecasts)


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
