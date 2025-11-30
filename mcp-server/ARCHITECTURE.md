# Weather Server - MCP + REST API Architecture

This project demonstrates **best practices** for running FastMCP and FastAPI side-by-side, sharing the same core business logic.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Clients                           │
│  ┌──────────────┐              ┌─────────────────┐ │
│  │ MCP Clients  │              │  HTTP Clients   │ │
│  │ (Claude, etc)│              │  (curl, browser)│ │
│  └──────┬───────┘              └────────┬────────┘ │
└─────────┼──────────────────────────────┼──────────┘
          │                              │
          │ stdio/SSE                    │ HTTP/REST
          │                              │
┌─────────▼──────────────────────────────▼──────────┐
│              Server Layer                         │
│  ┌──────────────┐              ┌───────────────┐ │
│  │  MCP Server  │              │  FastAPI      │ │
│  │ (FastMCP)    │              │  REST API     │ │
│  │ weather_mcp  │              │ weather_api   │ │
│  └──────┬───────┘              └───────┬───────┘ │
│         │                              │         │
│         └──────────────┬───────────────┘         │
│                        │                         │
│                ┌───────▼────────┐                │
│                │ Core Business  │                │
│                │     Logic      │                │
│                │weather_service │                │
│                └────────────────┘                │
└──────────────────────────────────────────────────┘
```

## File Structure

- **`weather_service.py`** - Core business logic (shared)
  - `get_alerts_for_state()` - Fetch weather alerts
  - `get_forecast_for_location()` - Fetch weather forecast
  - All NWS API interaction logic

- **`weather_mcp.py`** - MCP server wrapper
  - Thin wrappers exposing service functions as MCP tools
  - Uses FastMCP decorators

- **`weather_api.py`** - REST API wrapper
  - Thin wrappers exposing service functions as HTTP endpoints
  - Uses FastAPI decorators
  - Includes Pydantic models for validation

- **`server.py`** - Unified entry point
  - Can run MCP only, API only, or both
  - Command-line interface for all modes

- **`weather.py`** - Legacy single-file implementation (kept for compatibility)

## Usage

### 1. Run MCP Server Only (stdio - for local clients)

```bash
uv run python -m weather_server --mode mcp --transport stdio
# or simply:
uv run python -m weather_server
```

### 2. Run MCP Server Only (SSE - for network clients)

```bash
uv run python -m weather_server --mode mcp --transport sse
# Runs on http://localhost:8000/sse
```

### 3. Run REST API Only

```bash
uv run python -m weather_server --mode api --api-port 8080
# Access at http://localhost:8080
```

### 4. Run Both MCP (SSE) and REST API

```bash
uv run python -m weather_server --mode both --mcp-port 8000 --api-port 8080
# MCP on http://localhost:8000/sse
# API on http://localhost:8080
```

## REST API Endpoints

### GET `/`
Root endpoint with API information

### GET `/alerts/{state}`
Get weather alerts for a US state
- **Parameters**: `state` - Two-letter state code (e.g., CA, NY)
- **Example**: `curl http://localhost:8080/alerts/CA`

### POST `/forecast`
Get weather forecast for coordinates
- **Body**: `{"latitude": 47.6062, "longitude": -122.3321}`
- **Example**:
  ```bash
  curl -X POST http://localhost:8080/forecast \
    -H "Content-Type: application/json" \
    -d '{"latitude": 47.6062, "longitude": -122.3321}'
  ```

### GET `/health`
Health check endpoint

## MCP Tools

### `get_alerts(state: str)`
Get weather alerts for a US state

### `get_forecast(latitude: float, longitude: float)`
Get weather forecast for a location

## Best Practices Demonstrated

1. **Separation of Concerns**
   - Core logic in `weather_service.py` - no framework dependencies
   - Thin adapters in `weather_mcp.py` and `weather_api.py`

2. **Code Reuse**
   - Both MCP and REST API call the same underlying functions
   - No duplication of business logic

3. **Flexibility**
   - Can run MCP only, API only, or both
   - Different transports for different use cases

4. **Type Safety**
   - Pydantic models for REST API validation
   - Type hints throughout

5. **Single Entry Point**
   - `server.py` provides unified CLI
   - Easy to configure and deploy

## Production Considerations

For production deployments, consider:

1. **Separate Processes**
   - Run MCP and REST API as separate containers/processes
   - Use process managers (systemd, supervisor) or container orchestration

2. **Configuration**
   - Use environment variables for ports, hosts
   - Externalize configuration (config files, env vars)

3. **Monitoring**
   - Add structured logging
   - Metrics and health checks
   - Error tracking (Sentry, etc.)

4. **Security**
   - Add authentication/authorization
   - Rate limiting
   - Input validation and sanitization

5. **Scaling**
   - Load balancing for REST API
   - Multiple MCP server instances if needed
