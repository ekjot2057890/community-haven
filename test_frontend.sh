#!/bin/bash

# Install http-server if not installed
if ! command -v python3 -m http.server &> /dev/null; then
    echo "Using Python's built-in HTTP server..."
fi

# Serve the current directory (which contains all the HTML files)
echo "Starting HTTP server on port 8000..."
echo "Access the site at http://localhost:8000"
echo "Press Ctrl+C to stop the server"

# Start the server
python3 -m http.server 8000 