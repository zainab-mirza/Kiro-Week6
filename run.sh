#!/bin/bash

echo "🥗 Starting BiteBalance - The AI Menu Referee"
echo "============================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please run: python setup.py"
    exit 1
fi

# Start the Streamlit app
echo "🚀 Launching BiteBalance..."
streamlit run app.py