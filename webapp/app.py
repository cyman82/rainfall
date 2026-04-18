"""
🌊 Flood Risk Prediction Dashboard
A minimalist, classy web interface for Tamil Nadu flood prediction
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    tf = None
    TF_AVAILABLE = False

from todays_conditions import (
    get_today_sequence, get_today_features, get_today_conditions_dict,
    update_conditions, TRANSFORMER_FEATURES, XGBOOST_FEATURES
)

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
if TF_AVAILABLE:
    tf.get_logger().setLevel('ERROR')

app = Flask(__name__)

# ============== CONFIGURATION ==============
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODELS = {
    'transformer': {
        'model_path': os.path.join(PROJECT_ROOT, 'models', 'flood_transformer_model.keras'),
        'scaler_path': os.path.join(PROJECT_ROOT, 'models', 'flood_transformer_scaler.pkl'),
        'threshold': 0.30
    },
    'lstm': {
        'model_path': os.path.join(PROJECT_ROOT, 'models', 'flood_lstm_model.keras'),
        'scaler_path': os.path.join(PROJECT_ROOT, 'models', 'flood_lstm_scaler.pkl'),
        'threshold': 0.30
    },
    'xgboost': {
        'model_path': os.path.join(PROJECT_ROOT, 'models', 'flood_xgb_model.pkl'),
    },
    'random_forest': {
        'model_path': os.path.join(PROJECT_ROOT, 'models', 'flood_rf_calibrated.pkl'),
    }
}

DATA_PATH = os.path.join(PROJECT_ROOT, 'ingestion', 'data', 'processed', 'district_flood_ml_dataset.csv')

FEATURES = [
    "rainfall_mm", "soil_moisture", "temperature_2m_mean",
    "relative_humidity_2m_mean", "surface_pressure_mean",
    "wind_speed_10m_mean", "cloud_cover_mean", "is_monsoon"
]

DISTRICTS = {
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "color": "#3B82F6"},
    "Tiruvallur": {"lat": 13.1432, "lon": 79.9089, "color": "#10B981"},
    "Chengalpattu": {"lat": 12.6921, "lon": 79.9779, "color": "#F59E0B"},
    "Kancheepuram": {"lat": 12.8342, "lon": 79.7036, "color": "#EF4444"},
    "Cuddalore": {"lat": 11.7480, "lon": 79.7714, "color": "#8B5CF6"},
    "Nagapattinam": {"lat": 10.7672, "lon": 79.8449, "color": "#EC4899"}
}

TIME_STEPS = 14

# ============== LOAD MODELS ==============
loaded_models = {}
loaded_scalers = {}


def get_tabular_model_input(model_key, latest_data, default_features):
    """Build a single-row DataFrame in the feature order expected by a model."""
    model = loaded_models[model_key]
    X = latest_data[default_features].iloc[-1:].copy()
    expected_features = list(getattr(model, 'feature_names_in_', X.columns))
    return X[expected_features]

def load_all_models():
    """Load all trained models"""
    global loaded_models, loaded_scalers

    # TensorFlow-backed models are optional so the dashboard can still start.
    if TF_AVAILABLE:
        try:
            loaded_models['transformer'] = tf.keras.models.load_model(MODELS['transformer']['model_path'])
            loaded_scalers['transformer'] = joblib.load(MODELS['transformer']['scaler_path'])
            print("[OK] Transformer model loaded")
        except Exception as e:
            print(f"[WARN] Transformer model not loaded: {e}")

        try:
            loaded_models['lstm'] = tf.keras.models.load_model(MODELS['lstm']['model_path'])
            loaded_scalers['lstm'] = joblib.load(MODELS['lstm']['scaler_path'])
            print("[OK] LSTM model loaded")
        except Exception as e:
            print(f"[WARN] LSTM model not loaded: {e}")
    else:
        print("[WARN] TensorFlow not installed; skipping Transformer and LSTM models")

    # Load XGBoost
    try:
        loaded_models['xgboost'] = joblib.load(MODELS['xgboost']['model_path'])
        print("[OK] XGBoost model loaded")
    except Exception as e:
        print(f"[WARN] XGBoost model not loaded: {e}")

    # Load Random Forest
    try:
        loaded_models['random_forest'] = joblib.load(MODELS['random_forest']['model_path'])
        if hasattr(loaded_models['random_forest'], 'estimator'):
            loaded_models['random_forest'].estimator.n_jobs = 1
        for calibrated_model in getattr(loaded_models['random_forest'], 'calibrated_classifiers_', []):
            if hasattr(calibrated_model, 'estimator'):
                calibrated_model.estimator.n_jobs = 1
        print("[OK] Random Forest model loaded")
    except Exception as e:
        print(f"[WARN] Random Forest model not loaded: {e}")

# ============== DATA LOADING ==============
df_data = None

def load_data():
    """Load the dataset"""
    global df_data
    df_data = pd.read_csv(DATA_PATH)
    df_data['date'] = pd.to_datetime(df_data['date'])
    print(f"[OK] Data loaded: {len(df_data)} records")

# ============== PREDICTION FUNCTIONS ==============

def get_latest_sequence(district, num_days=TIME_STEPS):
    """Get the latest data sequence for a district"""
    district_data = df_data[df_data['district'] == district].sort_values('date')
    latest = district_data.tail(num_days)
    return latest

def predict_flood_risk(district):
    """Predict flood risk using ensemble of models with TODAY'S CONDITIONS"""
    predictions = {}

    # Get 14-day sequence: 13 days historical + today's actual conditions
    latest_data = get_today_sequence(district, df_data, TIME_STEPS)

    if len(latest_data) < TIME_STEPS:
        return {"error": f"Insufficient data for {district}"}

    features_data = latest_data[FEATURES].values

    # Transformer prediction (uses 8 features, sequential)
    if 'transformer' in loaded_models:
        scaler = loaded_scalers['transformer']
        scaled_data = scaler.transform(features_data)
        X = scaled_data.reshape(1, TIME_STEPS, len(FEATURES))
        prob = loaded_models['transformer'].predict(X, verbose=0)[0][0]
        predictions['transformer'] = float(prob)

    # LSTM prediction (uses 8 features, sequential)
    if 'lstm' in loaded_models:
        scaler = loaded_scalers['lstm']
        scaled_data = scaler.transform(features_data)
        X = scaled_data.reshape(1, TIME_STEPS, len(FEATURES))
        prob = loaded_models['lstm'].predict(X, verbose=0)[0][0]
        predictions['lstm'] = float(prob)

    # XGBoost prediction (uses 15 flat features, today's values only)
    if 'xgboost' in loaded_models:
        try:
            X_xgb = get_tabular_model_input('xgboost', latest_data, XGBOOST_FEATURES)
            prob = loaded_models['xgboost'].predict_proba(X_xgb)[0][1]
            predictions['xgboost'] = float(prob)
        except Exception as e:
            print(f"[WARN] XGBoost prediction failed for {district}: {e}")

    # Random Forest prediction (uses 15 flat features, today's values only)
    if 'random_forest' in loaded_models:
        try:
            X_rf = get_tabular_model_input('random_forest', latest_data, XGBOOST_FEATURES)
            prob = loaded_models['random_forest'].predict_proba(X_rf)[0][1]
            predictions['random_forest'] = float(prob)
        except Exception as e:
            print(f"[WARN] Random Forest prediction failed for {district}: {e}")

    # Ensemble average
    if predictions:
        ensemble_prob = np.mean(list(predictions.values()))
        predictions['ensemble'] = float(ensemble_prob)

        # Risk level
        if ensemble_prob >= 0.7:
            risk_level = "CRITICAL"
            risk_color = "#DC2626"
        elif ensemble_prob >= 0.5:
            risk_level = "HIGH"
            risk_color = "#F59E0B"
        elif ensemble_prob >= 0.3:
            risk_level = "MODERATE"
            risk_color = "#3B82F6"
        else:
            risk_level = "LOW"
            risk_color = "#10B981"

        predictions['risk_level'] = risk_level
        predictions['risk_color'] = risk_color

    # Add today's weather data (from today's conditions, not historical)
    today_conditions = get_today_conditions_dict(district)
    if today_conditions:
        predictions['weather'] = {
            'rainfall': float(today_conditions['rainfall_mm']),
            'soil_moisture': float(today_conditions['soil_moisture']),
            'temperature': float(today_conditions['temperature_2m_mean']),
            'humidity': float(today_conditions['relative_humidity_2m_mean']),
            'date': today_conditions['date'].strftime('%Y-%m-%d'),
            'note': 'Based on today\'s actual conditions (April 15, 2026)'
        }

    return predictions

# ============== ROUTES ==============

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html', districts=DISTRICTS)

@app.route('/api/districts')
def get_districts():
    """Get all districts"""
    return jsonify(DISTRICTS)

@app.route('/api/predict/<district>')
def predict(district):
    """Predict flood risk for a district"""
    if district not in DISTRICTS:
        return jsonify({"error": "District not found"}), 404

    result = predict_flood_risk(district)
    result['district'] = district
    result['coords'] = DISTRICTS[district]
    return jsonify(result)

@app.route('/api/predict/all')
def predict_all():
    """Predict flood risk for all districts"""
    results = {}
    for district in DISTRICTS:
        results[district] = predict_flood_risk(district)
        results[district]['coords'] = DISTRICTS[district]
    return jsonify(results)

@app.route('/api/history/<district>')
def get_history(district):
    """Get historical data for a district"""
    if district not in DISTRICTS:
        return jsonify({"error": "District not found"}), 404

    district_data = df_data[df_data['district'] == district].sort_values('date').tail(30)

    history = {
        'dates': district_data['date'].dt.strftime('%Y-%m-%d').tolist(),
        'rainfall': district_data['rainfall_mm'].tolist(),
        'soil_moisture': district_data['soil_moisture'].tolist(),
        'flood_risk': district_data['flood_risk'].tolist()
    }
    return jsonify(history)

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    stats = {
        'total_records': len(df_data),
        'date_range': {
            'start': df_data['date'].min().strftime('%Y-%m-%d'),
            'end': df_data['date'].max().strftime('%Y-%m-%d')
        },
        'flood_events': int(df_data['flood_risk'].sum()),
        'districts': list(DISTRICTS.keys()),
        'models_loaded': list(loaded_models.keys()),
        'prediction_date': '2026-04-15',
        'prediction_mode': 'TODAY\'S CONDITIONS (April 15, 2026)'
    }
    return jsonify(stats)

@app.route('/api/update-conditions/<district>', methods=['POST'])
def update_district_conditions(district):
    """Update today's conditions for a specific district"""
    if district not in DISTRICTS:
        return jsonify({"error": "District not found"}), 404
    
    data = request.get_json()
    if update_conditions(district, data):
        return jsonify({
            "success": True,
            "message": f"Updated conditions for {district}",
            "conditions": get_today_conditions_dict(district)
        })
    else:
        return jsonify({"error": "Failed to update conditions"}), 400

@app.route('/api/conditions/<district>')
def get_conditions(district):
    """Get today's conditions for a district"""
    if district not in DISTRICTS:
        return jsonify({"error": "District not found"}), 404
    
    conditions = get_today_conditions_dict(district)
    return jsonify(conditions)

@app.route('/api/conditions')
def get_all_conditions():
    """Get today's conditions for all districts"""
    from todays_conditions import TODAY_CONDITIONS
    return jsonify(TODAY_CONDITIONS)

# ============== MAIN ==============

if __name__ == '__main__':
    print("\n" + "="*60)
    print("FLOOD RISK PREDICTION DASHBOARD")
    print("="*60 + "\n")

    load_data()
    load_all_models()

    print("\n" + "="*60)
    print("Starting server at http://localhost:5000")
    print("="*60 + "\n")

    app.run(debug=False, use_reloader=False, port=5000)

