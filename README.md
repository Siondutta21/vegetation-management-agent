# Vegetation Management Agent

## What is this?

A complete AI-powered vegetation management system for power line maintenance. This agent uses machine learning to detect vegetation risks, predict growth patterns, and generate professional reports.

## Quick Start

1. Install Python 3.7 or higher
2. Install dependencies: `pip install -r requirements_render.txt`
3. Start backend: `python simple_backend.py`
4. Open index.html in browser (ORIGINAL FULL VERSION)

## 🌐 **Deploy to Render (Get Your Shareable Link!)**

### **Step 1: Go to Render.com**
1. Visit: https://render.com
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"

### **Step 2: Configure Your Service**
1. **Name**: `vegetation-management-agent-backend`
2. **Build Command**: `pip install -r requirements_render.txt`
3. **Start Command**: `python simple_backend.py`
4. **Environment Variable**: `PYTHON_VERSION=3.12.0`
5. **Click "Create Web Service"**

### **Step 3: Get Your Backend URL**
- You'll get: `https://your-service.onrender.com`
- Test: `https://your-service.onrender.com/health`

### **Step 4: Update Your Frontend**
1. Edit your GitHub `index.html`
2. Change line 1038: `let apiBaseUrl = 'https://your-service.onrender.com';`
3. Commit changes

## Features

- AI Vegetation Detection: Machine learning-powered analysis
- Risk Assessment: Distance-based risk calculations
- Growth Prediction: Future vegetation forecasting
- Interactive Maps: Real-time KML visualization
- PDF Reports: Professional analysis reports
- KML Processing: Transmission line data handling

## Files Included

- `simple_backend.py` - AI backend server (Python 3.13 compatible)
- `requirements_render.txt` - Python 3.12 compatible dependencies (NO BUILD ERRORS)
- `render.yaml` - Render deployment configuration
- `index.html` - Main interactive dashboard (ORIGINAL FULL VERSION)
- `START_AGENT.bat` - Windows startup script
- `requirements.txt` - Full dependencies (may cause build errors)
- `kml_files/` - Sample transmission line data
- `RENDER_DEPLOYMENT_GUIDE.md` - Detailed deployment instructions

## System Requirements

- Python: 3.7 or higher
- Memory: 4GB RAM minimum
- Storage: 100MB free space
- Browser: Chrome, Firefox, Edge, or Safari

## How to Use

1. Start the backend using the startup script
2. Open the dashboard by opening index.html in your browser
3. Upload KML files to analyze transmission lines
4. View AI analysis including risk assessment and growth prediction
5. Generate reports in PDF format for documentation

## Important Note

- **For Render deployment**: Use `simple_backend.py` + `requirements_render.txt` + Python 3.12
- **For local use**: Use `simple_backend.py` + `requirements.txt`
- **Use index.html** for the FULL ORIGINAL FUNCTIONALITY
- This is the exact same file as your original dashboard
- All features, design, and functionality are preserved

## Sharing

This package is designed to be completely self-contained. Share the entire folder with team members - they just need to run the startup script and open index.html.

## Support

- Check the terminal for error messages
- Ensure Python is installed and in PATH
- Verify port 8000 is not in use by other applications
- Try different browsers if you encounter display issues
- For Render deployment issues, see `RENDER_DEPLOYMENT_GUIDE.md`

## Sample Data

The kml_files/ folder contains sample transmission line data you can use to test the system. Upload any of these files to see the AI analysis in action.

---
Powered by AI and Machine Learning
