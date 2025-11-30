"""
Unified entry point for Weather MCP Server and REST API

Supports three modes:
  - mcp: Run MCP server only (stdio or SSE)
  - api: Run REST API server only
  - both: Run both MCP (SSE) and REST API simultaneously
"""
import argparse
import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI


@asynccontextmanager
async def lifespan_with_mcp(app: FastAPI):
    """Lifespan manager that starts MCP server alongside FastAPI"""
    from weather_mcp import mcp

    # Start MCP server in background
    mcp_task = asyncio.create_task(
        asyncio.to_thread(mcp.run, transport='sse')
    )

    yield

    # Cleanup (note: this won't actually stop the MCP server cleanly in current implementation)
    mcp_task.cancel()


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

    # Start MCP server in background thread
    import threading
    mcp_thread = threading.Thread(
        target=lambda: mcp.run(transport='sse'),
        daemon=True
    )
    mcp_thread.start()

    # Run FastAPI on different port
    print(f"MCP Server (SSE): http://{host}:{mcp_port}/sse")
    print(f"REST API: http://{host}:{api_port}")
    uvicorn.run(app, host=host, port=api_port)


def main():
    parser = argparse.ArgumentParser(
        description='Weather Server - MCP and/or REST API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # MCP server only (stdio for local clients)
  python server.py --mode mcp --transport stdio

  # MCP server only (SSE for network clients)
  python server.py --mode mcp --transport sse

  # REST API only
  python server.py --mode api --api-port 8080

  # Both MCP (SSE) and REST API
  python server.py --mode both --mcp-port 8000 --api-port 8080
        """
    )

    parser.add_argument(
        '--mode',
        choices=['mcp', 'api', 'both'],
        default='mcp',
        help='Server mode: mcp (MCP only), api (REST API only), both (run both)'
    )

    parser.add_argument(
        '--transport',
        choices=['stdio', 'sse'],
        default='stdio',
        help='MCP transport mode (only used when mode=mcp)'
    )

    parser.add_argument(
        '--mcp-port',
        type=int,
        default=8000,
        help='Port for MCP SSE server (default: 8000, used when mode=both)'
    )

    parser.add_argument(
        '--api-port',
        type=int,
        default=8080,
        help='Port for REST API server (default: 8080)'
    )

    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host to bind servers to (default: 0.0.0.0)'
    )

    args = parser.parse_args()

    if args.mode == 'mcp':
        print(f"Starting MCP server (transport: {args.transport})...")
        run_mcp_only(transport=args.transport)
    elif args.mode == 'api':
        print(f"Starting REST API server on {args.host}:{args.api_port}...")
        run_api_only(port=args.api_port, host=args.host)
    elif args.mode == 'both':
        print("Starting both MCP (SSE) and REST API servers...")
        run_both(mcp_port=args.mcp_port, api_port=args.api_port, host=args.host)


if __name__ == "__main__":
    main()
