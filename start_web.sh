#!/bin/bash

# Start the DuckDuckGo Scraper Web UI

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the Flask app
echo "Starting DuckDuckGo Scraper Web UI..."
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

