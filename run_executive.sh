#!/bin/bash

echo "🏆 Starting BiteBalance Executive Dashboard"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please run: python setup.py"
    exit 1
fi

# Start the Executive Dashboard
echo "🚀 Launching Executive Decision Intelligence Dashboard..."
echo ""
echo "📊 Professional-grade meal optimization"
echo "🎯 Multi-dimensional trade-off analysis" 
echo "🛡️ Executive constraint enforcement"
echo ""
echo "Access at: http://localhost:8502"
echo ""

streamlit run app_executive.py