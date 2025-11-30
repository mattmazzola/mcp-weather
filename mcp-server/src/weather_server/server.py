"""Unified entry point for Weather MCP Server and REST API

Supports three modes:
  - mcp: Run MCP server only (stdio or SSE)
  - api: Run REST API server only
  - both: Run both MCP (SSE) and REST API simultaneously
"""
from enum import Enum

import typer
import uvicorn


class ServerMode(str, Enum):
    """Server operation modes"""
    mcp = "mcp"
    api = "api"
    both = "both"


class Transport(str, Enum):
    """MCP transport types"""
    stdio = "stdio"
    sse = "sse"


app = typer.Typer(
    name="weather_server",
    help="Weather Server - MCP and/or REST API",
    add_completion=False,
)


def run_mcp_only(transport: str = 'stdio'):
    """Run only the MCP server"""
    from .weather_mcp import mcp
    mcp.run(transport=transport)


def run_api_only(port: int = 8080, host: str = "0.0.0.0"):
    """Run only the REST API server"""
    from .weather_api import app
    uvicorn.run(app, host=host, port=port)


def run_both(mcp_port: int = 8000, api_port: int = 8080, host: str = "0.0.0.0"):
    """Run both MCP (SSE) and REST API servers

    Note: This runs them in the same process. For production, consider
    running them as separate processes/containers.
    """
    from .weather_api import app
    from .weather_mcp import mcp
    import threading

    # Start MCP server in daemon thread
    mcp_thread = threading.Thread(
        target=lambda: mcp.run(transport='sse'),
        daemon=True
    )
    mcp_thread.start()

    typer.echo(f"MCP Server (SSE): http://{host}:{mcp_port}/sse")
    typer.echo(f"REST API: http://{host}:{api_port}")

    # Run FastAPI server (blocks until stopped)
    uvicorn.run(app, host=host, port=api_port)


@app.command()
def cli(
    mode: ServerMode = typer.Option(
        ServerMode.mcp,
        help="Server mode: mcp (MCP only), api (REST API only), both (run both)"
    ),
    transport: Transport = typer.Option(
        Transport.stdio,
        help="MCP transport mode (only used when mode=mcp)"
    ),
    mcp_port: int = typer.Option(
        8000,
        "--mcp-port",
        help="Port for MCP SSE server (used when mode=both)"
    ),
    api_port: int = typer.Option(
        8080,
        "--api-port",
        help="Port for REST API server"
    ),
    host: str = typer.Option(
        "0.0.0.0",
        help="Host to bind servers to"
    ),
):
    """
    Weather Server - Run MCP server, REST API, or both

    Examples:

      MCP server only (stdio for local clients):
      $ weather_server --mode mcp --transport stdio

      MCP server only (SSE for network clients):
      $ weather_server --mode mcp --transport sse

      REST API only:
      $ weather_server --mode api --api-port 8080

      Both MCP (SSE) and REST API:
      $ weather_server --mode both --mcp-port 8000 --api-port 8080
    """
    if mode == ServerMode.mcp:
        typer.echo(f"Starting MCP server (transport: {transport.value})...")
        run_mcp_only(transport=transport.value)
    elif mode == ServerMode.api:
        typer.echo(f"Starting REST API server on {host}:{api_port}...")
        run_api_only(port=api_port, host=host)
    elif mode == ServerMode.both:
        typer.echo("Starting both MCP (SSE) and REST API servers...")
        run_both(mcp_port=mcp_port, api_port=api_port, host=host)


if __name__ == "__main__":
    app()
