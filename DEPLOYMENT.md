# 🚀 FloodWatch Deployment Guide

## Quick Setup (2 minutes)

### 1. Run Setup Script
```powershell
# Windows PowerShell
.\setup.ps1

# Or Windows Command Prompt
setup.bat
```

### 2. Start Flask Dashboard
```bash
python webapp\app.py
```
Visit: **http://localhost:5000**

### 3. Or Start Streamlit Dashboard
```bash
streamlit run webapp\streamlit_app.py
```
Automatically opens at: **http://localhost:8501**

---

## Full Installation (Manual)

### Prerequisites
- Windows 10/11 or Linux/Mac
- Python 3.9+
- 2GB+ RAM

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r webapp/requirements.txt
pip install jupyter jupyterlab scipy
```

### Step 3: Verify Installation
```bash
python -c "import tensorflow; print('TensorFlow OK')"
python -c "import xgboost; print('XGBoost OK')"
python -c "import pandas; print('Pandas OK')"
```

### Step 4: Run Application

#### Flask Dashboard (Recommended)
```bash
cd webapp
python app.py
# Open http://localhost:5000
```

#### Streamlit Dashboard
```bash
cd webapp
streamlit run streamlit_app.py
# Opens automatically at http://localhost:8501
```

#### Jupyter Notebooks
```bash
cd notebooks
jupyter notebook
```

---

## 🌐 Web Application Features

### Flask Dashboard (`http://localhost:5000`)
- **Modern UI**: Minimalist, classy dark theme
- **Real-time Predictions**: Live district risk cards
- **Interactive Analysis**: Select districts to view details
- **Historical Trends**: 30-day rainfall history
- **Model Information**: Ensemble architecture explanation

### Streamlit Dashboard (`http://localhost:8501`)
- **Responsive Design**: Works on all devices
- **Tabbed Interface**: Dashboard → Analysis → Performance → About
- **Advanced Charts**: Plotly visualizations
- **Model Ensemble Info**: Detailed descriptions

---

## 📊 Usage Examples

### 1. Generate Attention Analysis Report
```bash
cd notebooks
python generate_attention_report.py
# Output: attention_analysis_report.txt
```

### 2. Run Attention Analysis Notebook
```bash
jupyter notebook attention_analysis.ipynb
# Full interpretability analysis with 10+ visualizations
```

### 3. API Requests (if using Flask)
```bash
# Get all predictions
curl http://localhost:5000/api/predict/all

# Get specific district
curl http://localhost:5000/api/predict/Chennai

# Get statistics
curl http://localhost:5000/api/stats

# Get 30-day history
curl http://localhost:5000/api/history/Chennai
```

### 4. Python Predictions
```python
import sys
sys.path.insert(0, 'C:\\Users\\91924\\OneDrive\\Documents\\rainfall')

from webapp.app import predict_flood_risk, load_all_models, load_data

load_all_models()
load_data()

result = predict_flood_risk('Chennai')
print(f"Flood Risk: {result['ensemble']*100:.1f}%")
print(f"Risk Level: {result['risk_level']}")
```

---

## 🔧 Configuration

### Change Port
#### Flask
```bash
python webapp/app.py --port 5001
```

#### Streamlit
```bash
streamlit run webapp/streamlit_app.py --server.port 8502
```

### Customize Themes
Edit `~/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#3b82f6"
backgroundColor = "#0a0a0f"
```

---

## 📦 File Structure

```
rainfall/
├── setup.bat                          # Windows batch setup
├── setup.ps1                          # PowerShell setup
├── README.md                          # Main documentation
├── DEPLOYMENT.md                      # This file
│
├── models/                            # Trained models
│   ├── flood_transformer_model.keras  # Transformer
│   ├── flood_lstm_model.keras         # LSTM
│   ├── flood_xgb_model.pkl           # XGBoost
│   └── flood_rf_calibrated.pkl       # Random Forest
│
├── webapp/                            # Web applications
│   ├── app.py                        # Flask app
│   ├── streamlit_app.py              # Streamlit app
│   ├── requirements.txt              # Dependencies
│   ├── static/
│   │   ├── css/style.css            # Styling (minimalist)
│   │   └── js/app.js                # Functionality
│   └── templates/
│       └── index.html               # HTML structure
│
├── notebooks/                         # Jupyter notebooks
│   ├── attention_analysis.ipynb      # Interpretability
│   ├── ml.ipynb                     # Model training
│   ├── eda.ipynb                    # Data exploration
│   ├── ANALYSIS_GUIDE.md            # Interpretation guide
│   ├── QUICK_START.md               # Quick start
│   └── generate_attention_report.py # Report generator
│
└── ingestion/data/processed/         # Processed data
    ├── district_flood_ml_dataset.csv
    └── ...
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: tensorflow"
```bash
pip install tensorflow --upgrade
```

### Issue: "Port 5000 already in use"
```bash
# Change port
python webapp/app.py --port 5001

# Or find and kill process (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: "No module named 'streamlit'"
```bash
pip install streamlit>=1.28.0
```

### Issue: "Models not found"
Verify models directory:
```bash
ls models/*.keras models/*.pkl
# Should show 6 files (2 keras, 4 pkl)
```

### Issue: "Cannot import districts"
```bash
# Ensure you're in correct directory
cd C:\Users\91924\OneDrive\Documents\rainfall

# Add to Python path
set PYTHONPATH=%CD%
```

---

## 📈 Performance Tips

### 1. Use Caching
Both applications cache predictions for 1 minute to reduce load.

### 2. GPU Acceleration
For faster inference (if GPU available):
```bash
pip install tensorflow[and-cuda]
```

### 3. Database
For production, consider:
```bash
pip install sqlalchemy psycopg2-binary
# Use PostgreSQL instead of CSV
```

### 4. Production Deployment
```bash
# Use gunicorn instead of Flask dev server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 webapp.app:app
```

---

## 🔐 Security Considerations

### For Production:
1. Set `debug=False` in Flask
2. Use environment variables for secrets
3. Implement rate limiting
4. Add authentication if needed
5. Use HTTPS/SSL

Example `.env`:
```
FLASK_ENV=production
FLASK_DEBUG=False
API_KEY=your_secret_key
```

---

## 📊 Monitoring

### Check System Status
```bash
python -c "from webapp.app import *; load_data(); load_all_models(); print('✓ System OK')"
```

### View Logs
```bash
# Flask logs are printed to console
# Streamlit logs in ~/.streamlit/logs/
```

---

## 🎓 Next Steps

1. **Explore Notebooks**: Start with `eda.ipynb`
2. **Run Dashboard**: `python webapp/app.py`
3. **Review Analysis**: `attention_analysis.ipynb`
4. **Check Documentation**: See `README.md`

---

## 📞 Support

### Common Commands
```bash
# Activate environment
.\.venv\Scripts\Activate

# Generate attention report
cd notebooks && python generate_attention_report.py

# Run Flask
python webapp/app.py

# Run Streamlit
streamlit run webapp/streamlit_app.py

# Run Jupyter
jupyter notebook
```

### Resources
- **Main README**: `README.md`
- **Quick Start**: `notebooks/QUICK_START.md`
- **Analysis Guide**: `notebooks/ANALYSIS_GUIDE.md`
- **Implementation**: `notebooks/IMPLEMENTATION_CHECKLIST.md`

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] All dependencies installed
- [ ] Models found in `models/` directory
- [ ] Data files in `ingestion/data/processed/`
- [ ] Flask dashboard running at http://localhost:5000
- [ ] Streamlit dashboard running (if using)
- [ ] Attention report generated
- [ ] Notebooks opening in Jupyter

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Production Ready ✅


