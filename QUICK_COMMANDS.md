# 🌊 FloodWatch - Quick Command Reference

## 🚀 START HERE (2 minutes)

```powershell
# 1. Navigate to project folder
cd C:\Users\91924\OneDrive\Documents\rainfall

# 2. Activate environment (first time: run .\setup.ps1)
.\.venv\Scripts\Activate

# 3. Start Flask Dashboard
python webapp\app.py

# 4. Open browser → http://localhost:5000
```

---

## 📊 Main Commands

### Flask Web Dashboard (Recommended)
```bash
python webapp\app.py
# Opens at: http://localhost:5000
# Features: Modern UI, Real-time predictions, Interactive analysis
```

### Streamlit Dashboard (Alternative)
```bash
streamlit run webapp\streamlit_app.py
# Opens at: http://localhost:8501 (automatic)
# Features: Tabs, Plotly charts, Model explanations
```

### Jupyter Notebooks
```bash
cd notebooks
jupyter notebook
# Then open: attention_analysis.ipynb (full analysis)
```

### Generate Attention Report
```bash
cd notebooks
python generate_attention_report.py
# Output: attention_analysis_report.txt
```

---

## 🔧 Setup & Installation

### First-Time Setup (Automatic)
```powershell
# Windows PowerShell
.\setup.ps1

# Or Windows Command Prompt
setup.bat
```

### Manual Setup
```bash
# Create environment
python -m venv .venv
.\.venv\Scripts\Activate

# Install dependencies
pip install -r webapp/requirements.txt
pip install jupyter jupyterlab scipy
```

### Verify Installation
```bash
python -c "import tensorflow; print('TensorFlow OK')"
python -c "import xgboost; print('XGBoost OK')"
python -c "from webapp.app import *; print('App OK')"
```

---

## 📊 Data & Models

### Check Models
```bash
# Verify all models exist
dir models\*.keras models\*.pkl

# Should show:
# - flood_transformer_model.keras
# - flood_lstm_model.keras
# - flood_xgb_model.pkl
# - flood_rf_calibrated.pkl
# - flood_*_scaler.pkl (2 files)
```

### Verify Data
```python
import pandas as pd
df = pd.read_csv('ingestion/data/processed/district_flood_ml_dataset.csv')
print(f"Loaded {len(df)} records")
print(f"Districts: {df['district'].unique()}")
```

---

## 🎯 API Endpoints (Flask)

```bash
# Get all predictions (all districts)
curl http://localhost:5000/api/predict/all

# Get specific district
curl http://localhost:5000/api/predict/Chennai

# Get statistics
curl http://localhost:5000/api/stats

# Get 30-day history
curl http://localhost:5000/api/history/Chennai

# Get districts list
curl http://localhost:5000/api/districts
```

---

## 📝 Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| **README.md** | Main overview | Root folder |
| **DEPLOYMENT.md** | Setup guide | Root folder |
| **PROGRESS.md** | Completion summary | Root folder |
| **QUICK_START.md** | Notebook guide | `notebooks/` |
| **ANALYSIS_GUIDE.md** | Interpretation | `notebooks/` |
| **IMPLEMENTATION_CHECKLIST.md** | Details | `notebooks/` |

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Flask: Use different port
python webapp\app.py --port 5001

# Streamlit: Use different port
streamlit run webapp\streamlit_app.py --server.port 8502

# Find process using port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Module Not Found
```bash
# Reinstall dependencies
pip install --upgrade -r webapp/requirements.txt

# Or install specific package
pip install tensorflow --upgrade
pip install xgboost --upgrade
pip install streamlit --upgrade
```

### Models Not Loading
```bash
# Verify model files exist
python -c "import os; print([f for f in os.listdir('models') if f.endswith(('.keras', '.pkl'))])"

# Check model integrity
python models\train_transformer.py  # Retrain if needed
```

### Data Loading Issues
```bash
# Verify CSV file
python -c "import pandas as pd; print(pd.read_csv('ingestion/data/processed/district_flood_ml_dataset.csv').shape)"

# Check for missing values
python -c "import pandas as pd; df=pd.read_csv('ingestion/data/processed/district_flood_ml_dataset.csv'); print(df.isnull().sum())"
```

---

## 💻 Python Quick Scripts

### Test Predictions Directly
```python
import sys
sys.path.insert(0, 'C:\\Users\\91924\\OneDrive\\Documents\\rainfall')

from webapp.app import predict_flood_risk, load_all_models, load_data

load_data()
load_all_models()

for district in ['Chennai', 'Cuddalore', 'Nagapattinam']:
    result = predict_flood_risk(district)
    prob = result.get('ensemble', 0) * 100
    risk = result.get('risk_level', 'UNKNOWN')
    print(f"{district}: {prob:.1f}% risk ({risk})")
```

### Check Data Statistics
```python
import pandas as pd

df = pd.read_csv('ingestion/data/processed/district_flood_ml_dataset.csv')
print(f"Total records: {len(df)}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Districts: {df['district'].unique()}")
print(f"Flood events: {(df['flood_risk']==1).sum()}")
print(f"Non-flood events: {(df['flood_risk']==0).sum()}")
```

### Generate All Reports
```bash
cd notebooks
python generate_attention_report.py
echo "Report saved to attention_analysis_report.txt"
```

---

## 📂 Project Structure (Quick Reference)

```
rainfall/
├── webapp/                     # Web applications
│   ├── app.py                 # Flask app (http://localhost:5000)
│   ├── streamlit_app.py       # Streamlit app (http://localhost:8501)
│   └── static/, templates/    # CSS, JS, HTML
│
├── notebooks/                 # Jupyter notebooks
│   ├── attention_analysis.ipynb    # Main analysis
│   ├── generate_attention_report.py # Report generator
│   └── ...other notebooks...
│
├── models/                    # Pre-trained models
│   ├── flood_transformer_model.keras
│   ├── flood_lstm_model.keras
│   ├── flood_xgb_model.pkl
│   └── flood_rf_calibrated.pkl
│
├── ingestion/data/processed/  # Data files
│   └── district_flood_ml_dataset.csv
│
├── README.md                  # Main documentation
├── DEPLOYMENT.md              # Setup guide
├── PROGRESS.md                # Completion summary
├── setup.ps1                  # PowerShell setup
└── setup.bat                  # Batch file setup
```

---

## 🎯 Performance Tips

### Faster Loading
```bash
# Use GPU (if available)
pip install tensorflow[and-cuda]

# Cache predictions
# (Already implemented - 1 minute cache)
```

### Reduce Memory
```python
# Only load required features
features = ['rainfall_mm', 'soil_moisture', 'temperature_2m_mean']
# Instead of all features
```

---

## 🆘 Support & Help

### Quick Diagnostics
```bash
# Check Python
python --version

# Check packages
pip list | grep -E "tensorflow|xgboost|streamlit|pandas"

# Check models
dir models\*.keras models\*.pkl | Measure-Object

# Check data
python -c "import pandas as pd; print(f'Data: {len(pd.read_csv(\"ingestion/data/processed/district_flood_ml_dataset.csv\"))} rows')"
```

### Get System Info
```powershell
# Windows
systeminfo | findstr /C:"Memory"

# Or use Python
import psutil
print(f"Available RAM: {psutil.virtual_memory().available / (1024**3):.1f} GB")
```

---

## 📚 Learning Resources

- **QUICK_START.md** - 3-minute notebook guide
- **ANALYSIS_GUIDE.md** - How to interpret attention analysis
- **IMPLEMENTATION_CHECKLIST.md** - What was implemented
- **README.md** - Complete project overview
- **DEPLOYMENT.md** - Detailed setup instructions

---

## 🚀 Next Steps

1. **Start Here**: Run `python webapp\app.py`
2. **Explore**: Visit http://localhost:5000
3. **Analyze**: Open `notebooks/attention_analysis.ipynb`
4. **Learn**: Read `README.md` for full documentation
5. **Deploy**: Follow `DEPLOYMENT.md` for production setup

---

**Version**: 1.0.0  
**Updated**: April 15, 2026  
**Status**: ✅ Ready to use!


