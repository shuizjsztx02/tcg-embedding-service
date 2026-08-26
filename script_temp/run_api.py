#!/usr/bin/env python3
"""Start the TCG API server via uvicorn.

Usage:
    python script_temp/run_api.py
    # or
    python script_temp/run_api.py --port 8000 --host 0.0.0.0
"""

import argparse
import sys
import os

# Ensure app/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app"))

import uvicorn


def main():
    ap = argparse.ArgumentParser(description="Start TCG Card Matching API")
    ap.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    ap.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    args = ap.parse_args()

    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
