# 🌊 QUICK REFERENCE - TODAY'S CONDITIONS

## 🚀 START HERE

```bash
# 1. Run Flask
python webapp\app.py

# 2. Open browser
http://localhost:5000

# 3. See today's predictions!
# Uses April 15, 2026 conditions
```

---

## 📊 TODAY'S CONDITIONS (Defaults)

| District | Rain | Soil | Temp | Humidity |
|----------|------|------|------|----------|
| Chennai | 2.5mm | 0.45 | 32.5°C | 68% |
| Tiruvallur | 1.8mm | 0.42 | 33.2°C | 65% |
| Chengalpattu | 3.2mm | 0.48 | 31.8°C | 70% |
| Kancheepuram | 2.0mm | 0.40 | 33.5°C | 63% |
| Cuddalore | 1.5mm | 0.38 | 33.8°C | 62% |
| Nagapattinam | 2.8mm | 0.46 | 32.0°C | 72% |

---

## 🔧 UPDATE CONDITIONS

### Via Python
```python
from webapp.todays_conditions import update_conditions

update_conditions('Chennai', {
    'rainfall_mm': 10.0,
    'temperature_2m_mean': 30.0,
    'soil_moisture': 0.55
})
```

### Via API (curl)
```bash
curl -X POST http://localhost:5000/api/update-conditions/Chennai \
  -H "Content-Type: application/json" \
  -d '{"rainfall_mm": 10.0}'
```

---

## 📍 API ENDPOINTS

### Get Data
```
GET /api/conditions              # All districts
GET /api/conditions/Chennai      # One district
GET /api/predict/Chennai         # Prediction
GET /api/stats                   # Statistics
```

### Update Data
```
POST /api/update-conditions/Chennai
```

---

## 📋 AVAILABLE FIELDS (18 total)

### Weather (8)
- rainfall_mm (0-50+)
- temperature_2m_mean (20-40°C)
- relative_humidity_2m_mean (0-100%)
- surface_pressure_mean (1000-1020 hPa)
- wind_speed_10m_mean (0-10 m/s)
- cloud_cover_mean (0-100%)
- soil_moisture (0-1)
- is_monsoon (0 or 1)

### Accumulation (5)
- rain_3d (mm)
- rain_7d (mm)
- rain_14d (mm)
- soil_7d_avg (0-1)
- soil_14d_avg (0-1)

### Derived (2)
- wetness_index (0-1)
- rain_intensity (0-2+)

---

## 🎯 EXAMPLE: HEAVY RAIN SCENARIO

```python
from webapp.todays_conditions import update_conditions

# Simulate heavy rainfall period
update_conditions('Chennai', {
    'rainfall_mm': 50.0,
    'rain_3d': 120.0,
    'rain_7d': 180.0,
    'soil_moisture': 0.75,
    'cloud_cover_mean': 90.0,
    'wetness_index': 0.80
})

# Get prediction
# curl http://localhost:5000/api/predict/Chennai
```

---

## 🎓 FILES TO READ

| File | Purpose | Read Time |
|------|---------|-----------|
| TODAYS_CONDITIONS_GUIDE.md | Complete guide | 10 min |
| TODAYS_CONDITIONS_SUMMARY.md | Overview | 5 min |
| CHANGELOG.md | What changed | 5 min |

---

## ✅ WHAT'S UNCHANGED

✓ Models (4 ensemble models)  
✓ Accuracy (94.2%)  
✓ Architecture (same)  
✓ Training code (same)  

---

## 🆕 WHAT'S NEW

✓ Predictions use April 15, 2026  
✓ Can update conditions via API  
✓ Can update via Python  
✓ 3 new API endpoints  

---

## 📌 KEY FACTS

- **Prediction Date**: April 15, 2026 (today)
- **Models**: 4 (Transformer, LSTM, XGBoost, RF)
- **Accuracy**: 94.2%
- **Districts**: 6 (all Tamil Nadu)
- **Sequence**: 13 history + 1 today = 14 days
- **Update**: Easy via API or Python

---

## 🚨 TROUBLESHOOTING

### "District not found"
Check spelling: Chennai, Tiruvallur, Chengalpattu, Kancheepuram, Cuddalore, Nagapattinam

### "Connection refused"
Start Flask: `python webapp\app.py`

### "Prediction shows old date"
Restart Flask/reload page

### "Update failed"
Check JSON format, all fields required

---

## 💡 PRO TIPS

1. **Batch Update**: Update all districts at once
   ```python
   from webapp.todays_conditions import set_all_conditions
   ```

2. **Get All Conditions**: 
   ```bash
   curl http://localhost:5000/api/conditions
   ```

3. **What-If Analysis**: Update → Predict → Compare

4. **Real Data**: Replace defaults with actual weather API data

---

## 🎪 SCENARIO EXAMPLES

### Monsoon Season
```json
{"is_monsoon": 1, "rainfall_mm": 25.0, "cloud_cover_mean": 80}
```

### Dry Season
```json
{"rainfall_mm": 0.0, "cloud_cover_mean": 5, "soil_moisture": 0.2}
```

### Soil Saturation
```json
{"soil_moisture": 0.80, "rain_3d": 100, "wetness_index": 0.9}
```

---

## ✨ QUICK COMMANDS

```bash
# Start Flask
python webapp\app.py

# Start Streamlit
streamlit run webapp\streamlit_app.py

# Get conditions
curl http://localhost:5000/api/conditions/Chennai

# Update conditions
curl -X POST http://localhost:5000/api/update-conditions/Chennai \
  -H "Content-Type: application/json" \
  -d '{"rainfall_mm": 5.0}'

# Get prediction
curl http://localhost:5000/api/predict/Chennai
```

---

**Version**: 1.0  
**Date**: April 15, 2026  
**Status**: Ready to use! 🌊


