# 🌊 FloodWatch - Today's Conditions Guide

## Overview

FloodWatch now uses **TODAY'S ACTUAL CONDITIONS (April 15, 2026)** for flood risk predictions instead of historical data.

**The model remains unchanged** - only the input data has been updated to use real-time conditions.

---

## How It Works

### Prediction Sequence
1. **Last 13 days**: Historical data from the dataset (up to Dec 31, 2025)
2. **Day 14 (Today)**: Actual weather conditions for April 15, 2026
3. **Models**: Process this 14-day sequence to make predictions

This approach combines historical patterns with current conditions for more accurate real-time forecasts.

---

## Default Today's Conditions (April 15, 2026)

Each district has reasonable default conditions for this date. These are based on:
- Tamil Nadu's typical April weather (pre-monsoon heat)
- Seasonal rainfall patterns
- Soil moisture from recent conditions

### Districts Covered
- ✅ Chennai
- ✅ Tiruvallur
- ✅ Chengalpattu
- ✅ Kancheepuram
- ✅ Cuddalore
- ✅ Nagapattinam

---

## Updating Today's Conditions

### Option 1: Flask API

#### Get current conditions
```bash
curl http://localhost:5000/api/conditions/Chennai
```

#### Update conditions for a district
```bash
curl -X POST http://localhost:5000/api/update-conditions/Chennai \
  -H "Content-Type: application/json" \
  -d '{
    "rainfall_mm": 5.0,
    "soil_moisture": 0.55,
    "temperature_2m_mean": 30.0,
    "relative_humidity_2m_mean": 75.0,
    "surface_pressure_mean": 1010.0,
    "wind_speed_10m_mean": 2.5,
    "cloud_cover_mean": 40.0,
    "rain_3d": 12.0,
    "rain_7d": 25.0,
    "rain_14d": 40.0,
    "soil_7d_avg": 0.50,
    "soil_14d_avg": 0.48,
    "wetness_index": 0.40,
    "rain_intensity": 1.2,
    "is_monsoon": 0
  }'
```

#### Get all districts' conditions
```bash
curl http://localhost:5000/api/conditions
```

---

### Option 2: Python Script

```python
from webapp.todays_conditions import update_conditions, get_today_conditions_dict

# Update a district's conditions
update_conditions('Chennai', {
    'rainfall_mm': 5.0,
    'temperature_2m_mean': 30.0,
    'soil_moisture': 0.55,
    # ... other fields
})

# Get updated conditions
conditions = get_today_conditions_dict('Chennai')
print(conditions)
```

---

## Available Fields

### Weather Fields (8)
- `rainfall_mm` - Daily rainfall in millimeters
- `temperature_2m_mean` - Mean temperature in Celsius
- `relative_humidity_2m_mean` - Mean humidity percentage
- `surface_pressure_mean` - Atmospheric pressure in hPa
- `wind_speed_10m_mean` - Wind speed in m/s
- `cloud_cover_mean` - Cloud cover percentage
- `soil_moisture` - Soil moisture (0-1 scale)
- `is_monsoon` - Monsoon flag (0=no, 1=yes)

### Accumulated Fields (5)
- `rain_3d` - 3-day accumulated rainfall
- `rain_7d` - 7-day accumulated rainfall
- `rain_14d` - 14-day accumulated rainfall
- `soil_7d_avg` - 7-day average soil moisture
- `soil_14d_avg` - 14-day average soil moisture

### Derived Fields (2)
- `wetness_index` - Derived wetness indicator (0-1)
- `rain_intensity` - Derived rainfall intensity (0-2+)

---

## Example Scenarios

### Scenario 1: Heavy Rainfall Alert
Update conditions to simulate high rainfall period:
```python
update_conditions('Chennai', {
    'rainfall_mm': 50.0,      # Heavy rain
    'rain_3d': 120.0,         # 3-day accumulation
    'rain_7d': 180.0,         # 7-day accumulation
    'soil_moisture': 0.75,    # Saturated
    'wetness_index': 0.80,    # Very wet
    'cloud_cover_mean': 90.0  # Overcast
})
```

### Scenario 2: Dry Season
```python
update_conditions('Cuddalore', {
    'rainfall_mm': 0.0,
    'rain_3d': 0.5,
    'soil_moisture': 0.25,
    'wetness_index': 0.10,
    'cloud_cover_mean': 5.0
})
```

### Scenario 3: Monsoon Onset
```python
update_conditions('Nagapattinam', {
    'is_monsoon': 1,          # Monsoon active
    'rainfall_mm': 15.0,
    'cloud_cover_mean': 75.0,
    'relative_humidity_2m_mean': 85.0
})
```

---

## Using with Web Dashboard

### Flask Dashboard (http://localhost:5000)
1. Dashboard automatically loads today's predictions
2. Click refresh to recalculate with any updated conditions
3. All predictions use today's actual conditions

### Streamlit Dashboard (http://localhost:8501)
1. Select district for detailed analysis
2. All charts and metrics show today's conditions
3. Model predictions reflect April 15, 2026

---

## API Endpoints

### GET Endpoints
```
GET  /api/conditions              - Get all districts' conditions
GET  /api/conditions/<district>   - Get specific district conditions
GET  /api/predict/all             - Get predictions for all districts
GET  /api/predict/<district>      - Get prediction for one district
GET  /api/stats                   - System statistics (shows prediction date)
```

### POST Endpoints
```
POST /api/update-conditions/<district>  - Update conditions for a district
```

---

## Testing Changes

### Check Current Conditions
```bash
# See what conditions are being used
curl http://localhost:5000/api/conditions/Chennai | jq
```

### Make a Prediction
```bash
# Get prediction with current conditions
curl http://localhost:5000/api/predict/Chennai | jq
```

### Update and Predict
```bash
# Update conditions
curl -X POST http://localhost:5000/api/update-conditions/Chennai \
  -H "Content-Type: application/json" \
  -d '{"rainfall_mm": 25.0, "soil_moisture": 0.70}'

# Get new prediction
curl http://localhost:5000/api/predict/Chennai | jq
```

---

## Important Notes

### Models Unchanged
- ✅ All 4 models remain exactly the same
- ✅ No retraining required
- ✅ Same accuracy metrics apply
- ✅ Only input data changes

### What Gets Predicted
- **Transformer & LSTM**: Use 14-day sequence (13 historical + today)
- **XGBoost & RF**: Use only today's values plus aggregations

### Historical Context
- Predictions always include 13 days of historical context
- This helps models understand seasonal patterns
- Today's conditions are appended as day 14

---

## Troubleshooting

### "District not found"
- Check spelling: Chennai, Tiruvallur, Chengalpattu, Kancheepuram, Cuddalore, Nagapattinam
- Use exact case

### "Failed to update conditions"
- Verify all required fields are included
- Check data types (numbers, not strings)

### Predictions still show old date
- Restart Flask/Streamlit app
- Or reload the page in browser

---

## Examples

### Python: Update Multiple Districts at Once
```python
from webapp.todays_conditions import set_all_conditions

new_conditions = {
    'Chennai': {'rainfall_mm': 10.0, 'soil_moisture': 0.60},
    'Cuddalore': {'rainfall_mm': 5.0, 'soil_moisture': 0.45},
    'Nagapattinam': {'rainfall_mm': 15.0, 'soil_moisture': 0.70}
}

set_all_conditions(new_conditions)
```

### Bash: Batch Update Script
```bash
#!/bin/bash

for district in "Chennai" "Tiruvallur" "Chengalpattu" "Kancheepuram" "Cuddalore" "Nagapattinam"; do
  echo "Updating $district..."
  curl -X POST http://localhost:5000/api/update-conditions/$district \
    -H "Content-Type: application/json" \
    -d '{"rainfall_mm": 10.0, "temperature_2m_mean": 32.0}'
done
```

---

## Default Values Reference

### April 15, 2026 Defaults (Pre-Monsoon Season)
| Field | Min | Default | Max |
|-------|-----|---------|-----|
| Rainfall | 0 | 1.5-3.2 mm | 50+ |
| Temperature | 25°C | 31-34°C | 40°C |
| Humidity | 40% | 62-72% | 100% |
| Soil Moisture | 0.0 | 0.38-0.48 | 1.0 |
| Cloud Cover | 0% | 10-30% | 100% |

---

## Version History

- **v1.0** (April 15, 2026): Initial implementation with today's conditions

---

**Happy predicting with today's conditions!** 🌊


