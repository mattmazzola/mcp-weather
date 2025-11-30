"""
MCP Server wrapper - exposes weather service as MCP tools
"""
from mcp.server.fastmcp import FastMCP

from .weather_service import get_alerts_for_state, get_forecast_for_location

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    return await get_alerts_for_state(state)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    return await get_forecast_for_location(latitude, longitude)
