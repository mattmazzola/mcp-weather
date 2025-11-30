"""
REST API wrapper - exposes weather service as HTTP endpoints
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .weather_service import get_alerts_for_state, get_forecast_for_location

app = FastAPI(
    title="Weather API",
    description="Weather alerts and forecasts from the National Weather Service",
    version="1.0.0",
)


class ForecastRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of the location")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of the location")


@app.get("/")
async def root():
    """API root with basic information"""
    return {
        "name": "Weather API",
        "version": "1.0.0",
        "endpoints": {
            "alerts": "/alerts/{state}",
            "forecast": "/forecast",
        },
    }


@app.get("/alerts/{state}")
async def get_alerts(state: str):
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g., CA, NY)
    """
    if len(state) != 2:
        raise HTTPException(status_code=400, detail="State must be a two-letter code")

    result = await get_alerts_for_state(state.upper())

    if "Unable to fetch" in result:
        raise HTTPException(status_code=503, detail=result)

    return {"state": state.upper(), "alerts": result}


@app.post("/forecast")
async def get_forecast(request: ForecastRequest):
    """Get weather forecast for a location.

    Request body should contain latitude and longitude.
    """
    result = await get_forecast_for_location(request.latitude, request.longitude)

    if "Unable to fetch" in result:
        raise HTTPException(status_code=503, detail=result)

    return {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "forecast": result,
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
