# 🌊 FloodWatch - Project Index & Getting Started

Welcome to **FloodWatch**, an AI-powered flood risk prediction system for Tamil Nadu!

---

## 🎯 QUICK START (Choose One)

### Option 1: Web Dashboard (Recommended) ⭐
```bash
python webapp\app.py
# Then open: http://localhost:5000
```
**Best for**: Interactive exploration, visual analysis, predictions for all districts

### Option 2: Streamlit Dashboard
```bash
streamlit run webapp\streamlit_app.py
# Automatically opens at: http://localhost:8501
```
**Best for**: Detailed charts, model explanations, interactive tabs

### Option 3: Jupyter Analysis
```bash
cd notebooks
jupyter notebook attention_analysis.ipynb
```
**Best for**: Deep-dive analysis, research, interpretability

---

## 📚 DOCUMENTATION ROADMAP

### 1. **New to the Project?** → Start Here
- **File**: `README.md`
- **Time**: 10 minutes
- **Content**: Overview, features, architecture, installation

### 2. **Want to Deploy?** → Read This
- **File**: `DEPLOYMENT.md`
- **Time**: 15 minutes
- **Content**: Setup guide, configuration, troubleshooting, production tips

### 3. **Need Quick Commands?** → Use This
- **File**: `QUICK_COMMANDS.md`
- **Time**: 5 minutes
- **Content**: All commands, API endpoints, common issues

### 4. **Want Completion Details?** → See This
- **File**: `PROGRESS.md`
- **Time**: 10 minutes
- **Content**: What's done, current status, next steps

### 5. **Analyze Attention Mechanism?** → Try These
- **File**: `notebooks/QUICK_START.md` (3-minute guide)
- **File**: `notebooks/ANALYSIS_GUIDE.md` (interpretation)
- **File**: `notebooks/attention_analysis.ipynb` (full analysis)
- **Tool**: `notebooks/generate_attention_report.py` (auto-report)

---

## 🗂️ FILE STRUCTURE

```
📦 rainfall/
│
├── 📄 README.md                    ← START HERE for overview
├── 📄 DEPLOYMENT.md                ← Setup & configuration guide
├── 📄 PROGRESS.md                  ← Completion summary
├── 📄 QUICK_COMMANDS.md            ← Command reference
├── 📄 INDEX.md (this file)         ← Navigation guide
│
├── 🌐 WEBAPP (Web Dashboards)
│   ├── 📄 webapp/app.py            → Flask dashboard (http://localhost:5000)
│   ├── 📄 webapp/streamlit_app.py  → Streamlit (http://localhost:8501)
│   ├── 🎨 static/css/style.css     → Modern styling (minimalist)
│   ├── ⚙️ static/js/app.js         → Optimized JavaScript
│   ├── 📰 templates/index.html     → HTML structure
│   └── 📋 requirements.txt         → Python dependencies
│
├── 📊 NOTEBOOKS (Analysis & Training)
│   ├── 📓 attention_analysis.ipynb      → Main interpretability analysis
│   ├── 📓 ml.ipynb                     → Model training details
│   ├── 📓 eda.ipynb                    → Data exploration
│   ├── 📓 feature_engineering.ipynb    → Feature creation
│   ├── 🐍 generate_attention_report.py → Report generator
│   ├── 📘 QUICK_START.md              → 3-minute guide
│   ├── 📘 ANALYSIS_GUIDE.md           → Interpretation guide
│   ├── 📋 IMPLEMENTATION_CHECKLIST.md  → Implementation details
│   └── 📄 attention_analysis_report.txt → Auto-generated report
│
├── 🧠 MODELS (Pre-trained)
│   ├── flood_transformer_model.keras    → Transformer (attention-based)
│   ├── flood_lstm_model.keras           → LSTM (sequential learning)
│   ├── flood_xgb_model.pkl             → XGBoost (gradient boosting)
│   ├── flood_rf_calibrated.pkl         → Random Forest (calibrated)
│   ├── flood_transformer_scaler.pkl    → Transformer feature scaler
│   └── flood_lstm_scaler.pkl           → LSTM feature scaler
│
├── 📥 DATA PROCESSING
│   ├── processing/build_flood_labels.py     → Label engineering
│   ├── processing/merge_soil.py             → Soil data merging
│   ├── processing/merge_weather_soil.py     → Weather-soil fusion
│   ├── processing/simulate_soil.py          → Soil simulation
│   ├── ingestion/fetch_soil.py              → Soil data ingestion
│   ├── ingestion/fetch_weather.py           → Weather ingestion
│   └── ingestion/data/processed/district_flood_ml_dataset.csv → Main dataset
│
├── ⚙️ CONFIGURATION
│   ├── config/districts.py         → District definitions
│   ├── .streamlit/config.toml      → Streamlit theming
│   ├── setup.ps1                   → PowerShell setup script
│   └── setup.bat                   → Batch setup script
│
└── 📊 OUTPUT
    ├── figures/attention_analysis/  → Generated visualizations
    └── output.txt                   → System logs
```

---

## 🚀 GETTING STARTED (5-Minute Guide)

### Step 1: Initial Setup
```bash
cd C:\Users\91924\OneDrive\Documents\rainfall
.\setup.ps1  # or setup.bat
```

### Step 2: Choose Your Tool
```bash
# Option A: Web Dashboard (Recommended)
python webapp\app.py
# Visit http://localhost:5000

# Option B: Streamlit
streamlit run webapp\streamlit_app.py

# Option C: Jupyter
jupyter notebook
```

### Step 3: Explore & Analyze
- **Flask**: Click on districts for detailed analysis
- **Streamlit**: Use tabs for different views
- **Jupyter**: Run cells to see results

### Step 4: Generate Report
```bash
cd notebooks
python generate_attention_report.py
```

---

## 📊 KEY FEATURES

### 1. **Real-Time Predictions** ✅
- Ensemble of 4 models
- All 6 districts analyzed
- Risk assessment with confidence
- Weather context included

### 2. **Interactive Dashboards** ✅
- Modern minimalist design
- Responsive (mobile-friendly)
- Smooth animations
- Fast performance

### 3. **Comprehensive Analysis** ✅
- Attention mechanism interpretability
- Feature importance analysis
- Regional pattern comparison
- Statistical validation

### 4. **Production Ready** ✅
- Full API endpoints
- Error handling
- Performance optimized
- Documented

---

## 💡 COMMON TASKS

| Task | Command | Time |
|------|---------|------|
| Start Flask Dashboard | `python webapp\app.py` | <1 min |
| Start Streamlit | `streamlit run webapp\streamlit_app.py` | <1 min |
| Generate Report | `cd notebooks && python generate_attention_report.py` | 30 sec |
| Run Attention Analysis | `jupyter notebook attention_analysis.ipynb` | 10 min |
| Check Models | `ls models\*.keras models\*.pkl` | 5 sec |
| Verify Installation | `python -c "import tensorflow; print('OK')"` | 5 sec |

---

## 🎓 DOCUMENTATION BY USE CASE

### "I want to run the web dashboard"
→ `QUICK_COMMANDS.md` (Flask section)

### "I want to deploy to production"
→ `DEPLOYMENT.md` (complete guide)

### "I want to understand the models"
→ `README.md` (model architecture section)

### "I want to analyze attention mechanism"
→ `notebooks/QUICK_START.md` + `ANALYSIS_GUIDE.md`

### "I want to understand what was done"
→ `PROGRESS.md` (completion summary)

### "I'm stuck or getting errors"
→ `DEPLOYMENT.md` (troubleshooting section) + `QUICK_COMMANDS.md` (diagnostics)

---

## ✅ VERIFICATION CHECKLIST

Before running, verify:

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Virtual environment created (`.venv` folder exists)
- [ ] Dependencies installed (`pip list | grep tensorflow`)
- [ ] Models exist (`models/*.keras` and `models/*.pkl`)
- [ ] Data file exists (`ingestion/data/processed/district_flood_ml_dataset.csv`)

**All green?** → Run `python webapp\app.py` 🎉

---

## 📞 GETTING HELP

### Quick Diagnostics
```bash
# 1. Check if setup worked
python -c "import tensorflow, xgboost; print('✓ Packages OK')"

# 2. Check if models loaded
python -c "import os; print([f for f in os.listdir('models') if f.endswith(('.keras', '.pkl'))])"

# 3. Check if data loaded
python -c "import pandas as pd; df=pd.read_csv('ingestion/data/processed/district_flood_ml_dataset.csv'); print(f'✓ {len(df)} rows')"
```

### Resources
1. **Quick Help** → `QUICK_COMMANDS.md`
2. **Setup Help** → `DEPLOYMENT.md` (Troubleshooting section)
3. **Code Help** → `README.md` (Architecture section)
4. **Analysis Help** → `notebooks/ANALYSIS_GUIDE.md`

---

## 🌟 HIGHLIGHTS

### What's Special About This Project
- **Ensemble Approach**: 4 complementary models
- **Interpretability**: Comprehensive attention analysis
- **Modern Tech**: Latest frameworks (TensorFlow, XGBoost, Streamlit)
- **Production Ready**: Complete documentation & error handling
- **Research Quality**: Publication-ready analysis

---

## 📈 PROJECT STATUS

| Component | Status | Notes |
|-----------|--------|-------|
| **Data Pipeline** | ✅ Complete | 21,841 records, 6 districts, 10+ years |
| **Models** | ✅ Trained | Transformer, LSTM, XGBoost, Random Forest |
| **Web Apps** | ✅ Ready | Flask & Streamlit dashboards |
| **Analysis Tools** | ✅ Ready | Attention analysis, report generation |
| **Documentation** | ✅ Complete | README, deployment guide, quick start |
| **Production Ready** | ✅ Yes | Error handling, performance optimized |

---

## 🎯 NEXT ACTIONS

### Immediate (Do Now)
1. Run `python webapp\app.py`
2. Visit `http://localhost:5000`
3. Explore district predictions

### Short-term (Today)
1. Read `README.md` for full context
2. Review `DEPLOYMENT.md` if deploying
3. Check `notebooks/attention_analysis.ipynb`

### Medium-term (This Week)
1. Deploy to cloud if needed
2. Fine-tune models if desired
3. Add custom analyses

---

## 📞 SUPPORT

**Question?** → Check relevant doc:
- Installation → `DEPLOYMENT.md`
- Commands → `QUICK_COMMANDS.md`
- Overview → `README.md`
- Status → `PROGRESS.md`

**Still stuck?** → Follow troubleshooting in `DEPLOYMENT.md`

---

## 🎉 YOU'RE READY!

Everything is set up and documented. 

**Just run**: `python webapp\app.py`

**Then visit**: http://localhost:5000

**Happy predicting!** 🌊

---

**Version**: 1.0.0  
**Updated**: April 15, 2026  
**Status**: ✅ Production Ready


