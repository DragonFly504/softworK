#!/bin/bash
# TTCP Worldwide - Quick Start Script

echo "🚀 Starting TTCP Worldwide Tracking System..."

# Navigate to project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
elif [ -d "env" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
fi

# Apply migrations if needed
echo "🔄 Checking database migrations..."
python manage.py migrate --run-syncdb

# Start the server
echo "✅ Server starting at http://127.0.0.1:8000"
echo "📊 Admin panel: http://127.0.0.1:8000/admin/"
echo "🔍 Tracking page: http://127.0.0.1:8000/track/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

python manage.py runserver
