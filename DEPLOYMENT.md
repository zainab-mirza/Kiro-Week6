# 🚀 BiteBalance Deployment Guide

## Quick Start (Windows)

1. **Setup Environment**
   ```cmd
   python setup.py
   ```

2. **Add API Key**
   - Edit `.env` file
   - Add your Gemini API key: `GEMINI_API_KEY=your_key_here`

3. **Run the App**
   ```cmd
   run.bat
   ```
   OR
   ```cmd
   streamlit run app.py
   ```

## Quick Start (Linux/Mac)

1. **Setup Environment**
   ```bash
   python setup.py
   chmod +x run.sh
   ```

2. **Add API Key**
   - Edit `.env` file
   - Add your Gemini API key: `GEMINI_API_KEY=your_key_here`

3. **Run the App**
   ```bash
   ./run.sh
   ```
   OR
   ```bash
   streamlit run app.py
   ```

## Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here

# Test the setup
python test_app.py

# Run the app
streamlit run app.py
```

## Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key to your `.env` file

## Project Structure

```
BiteBalance/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Your API keys (create this)
├── setup.py              # Automated setup script
├── test_app.py           # Test functionality
├── run.bat               # Windows launcher
├── run.sh                # Linux/Mac launcher
├── README.md             # Project documentation
├── DEPLOYMENT.md         # This file
└── src/                  # Source code modules
    ├── __init__.py
    ├── models.py         # Data models and enums
    ├── referee.py        # AI referee logic
    └── ui_components.py  # Streamlit UI components
```

## Troubleshooting

### Common Issues

1. **"No module named 'streamlit'"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"API Error: 403"**
   - Check your Gemini API key in `.env`
   - Ensure the key has proper permissions

3. **"Unable to parse menu"**
   - Format your menu with clear item names
   - Include prices and descriptions when possible

4. **App won't start**
   - Run `python test_app.py` to check setup
   - Ensure all dependencies are installed

### Performance Tips

- Use clear, structured menu formats
- Include item descriptions for better AI analysis
- Set budget constraints to narrow choices
- Try both Zen and Gremlin modes for comparison

## Production Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add `GEMINI_API_KEY` to secrets
4. Deploy!

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## Features Implemented

✅ **Core Features**
- Dual-mode AI steering (Zen/Gremlin)
- Real-time menu analysis
- Health vs Taste scoring
- Budget constraints
- Visual score bars
- AI reasoning explanations

✅ **UI/UX**
- Split-personality color scheme
- Responsive design
- Animated transitions
- Clear visual hierarchy

✅ **Technical**
- Modular architecture
- Error handling
- Input validation
- API key management

## Next Steps for Enhancement

- Add cuisine type preferences
- Implement dietary restrictions
- Add meal planning features
- Create user preference learning
- Add nutrition database integration