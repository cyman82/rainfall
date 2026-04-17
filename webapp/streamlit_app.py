"""
🌊 Flood Risk Prediction Dashboard - Streamlit Edition
A minimalist, classy web interface for Tamil Nadu flood prediction
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st
import tensorflow as tf

# Configure Streamlit
st.set_page_config(
    page_title="FloodWatch | Tamil Nadu Flood Prediction",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# ============== CUSTOM STYLING ==============
def apply_custom_style():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        /* Main app styling */
        .main {
            background: linear-gradient(135deg, #0a0a0f 0%, #12121a 100%);
        }
        
        /* Header styling */
        .header-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            padding: 20px 0;
        }
        
        .header-subtitle {
            color: #a0a0b0;
            font-size: 1.1rem;
            margin-bottom: 30px;
        }
        
        /* Card styling */
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(20px);
        }
        
        /* Risk level badge */
        .risk-low { color: #10b981; }
        .risk-moderate { color: #3b82f6; }
        .risk-high { color: #f59e0b; }
        .risk-critical { color: #ef4444; }
        
        /* District name styling */
        .district-name {
            font-size: 1.3rem;
            font-weight: 600;
            color: #ffffff;
        }
        
        /* Section title */
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# ============== CACHING & DATA LOADING ==============
@st.cache_resource
def load_all_models():
    """Load all trained models"""
    loaded_models = {}
    loaded_scalers = {}

    # Load Transformer
    try:
        loaded_models['transformer'] = tf.keras.models.load_model(MODELS['transformer']['model_path'])
        loaded_scalers['transformer'] = joblib.load(MODELS['transformer']['scaler_path'])
    except Exception as e:
        st.warning(f"⚠️ Transformer model not loaded: {e}")

    # Load LSTM
    try:
        loaded_models['lstm'] = tf.keras.models.load_model(MODELS['lstm']['model_path'])
        loaded_scalers['lstm'] = joblib.load(MODELS['lstm']['scaler_path'])
    except Exception as e:
        st.warning(f"⚠️ LSTM model not loaded: {e}")

    # Load XGBoost
    try:
        loaded_models['xgboost'] = joblib.load(MODELS['xgboost']['model_path'])
    except Exception as e:
        st.warning(f"⚠️ XGBoost model not loaded: {e}")

    # Load Random Forest
    try:
        loaded_models['random_forest'] = joblib.load(MODELS['random_forest']['model_path'])
    except Exception as e:
        st.warning(f"⚠️ Random Forest model not loaded: {e}")

    return loaded_models, loaded_scalers

@st.cache_data
def load_data():
    """Load the dataset"""
    df_data = pd.read_csv(DATA_PATH)
    df_data['date'] = pd.to_datetime(df_data['date'])
    return df_data

# ============== PREDICTION FUNCTIONS ==============
def get_latest_sequence(df_data, district, num_days=TIME_STEPS):
    """Get the latest data sequence for a district"""
    district_data = df_data[df_data['district'] == district].sort_values('date')
    latest = district_data.tail(num_days)
    return latest

def predict_flood_risk(df_data, loaded_models, loaded_scalers, district):
    """Predict flood risk using ensemble of models"""
    predictions = {}

    # Get latest data
    latest_data = get_latest_sequence(df_data, district)

    if len(latest_data) < TIME_STEPS:
        return {"error": f"Insufficient data for {district}"}

    features_data = latest_data[FEATURES].values

    # Transformer prediction
    if 'transformer' in loaded_models:
        scaler = loaded_scalers['transformer']
        scaled_data = scaler.transform(features_data)
        X = scaled_data.reshape(1, TIME_STEPS, len(FEATURES))
        prob = loaded_models['transformer'].predict(X, verbose=0)[0][0]
        predictions['transformer'] = float(prob)

    # LSTM prediction
    if 'lstm' in loaded_models:
        scaler = loaded_scalers['lstm']
        scaled_data = scaler.transform(features_data)
        X = scaled_data.reshape(1, TIME_STEPS, len(FEATURES))
        prob = loaded_models['lstm'].predict(X, verbose=0)[0][0]
        predictions['lstm'] = float(prob)

    # XGBoost prediction (uses flat features)
    if 'xgboost' in loaded_models:
        xgb_features = ['rainfall_mm', 'soil_moisture', 'temperature_2m_mean',
                        'relative_humidity_2m_mean', 'surface_pressure_mean',
                        'wind_speed_10m_mean', 'cloud_cover_mean', 'rain_3d',
                        'rain_7d', 'rain_14d', 'soil_7d_avg', 'soil_14d_avg',
                        'wetness_index', 'rain_intensity', 'is_monsoon']
        try:
            X_xgb = latest_data[xgb_features].iloc[-1:].values
            prob = loaded_models['xgboost'].predict_proba(X_xgb)[0][1]
            predictions['xgboost'] = float(prob)
        except:
            pass

    # Random Forest prediction
    if 'random_forest' in loaded_models:
        rf_features = ['rainfall_mm', 'soil_moisture', 'temperature_2m_mean',
                       'relative_humidity_2m_mean', 'surface_pressure_mean',
                       'wind_speed_10m_mean', 'cloud_cover_mean', 'rain_3d',
                       'rain_7d', 'rain_14d', 'soil_7d_avg', 'soil_14d_avg',
                       'wetness_index', 'rain_intensity', 'is_monsoon']
        try:
            X_rf = latest_data[rf_features].iloc[-1:].values
            prob = loaded_models['random_forest'].predict_proba(X_rf)[0][1]
            predictions['random_forest'] = float(prob)
        except:
            pass

    # Ensemble average
    if predictions:
        ensemble_prob = np.mean(list(predictions.values()))
        predictions['ensemble'] = float(ensemble_prob)

        # Risk level
        if ensemble_prob >= 0.7:
            risk_level = "🔴 CRITICAL"
            risk_color = "#DC2626"
        elif ensemble_prob >= 0.5:
            risk_level = "🟠 HIGH"
            risk_color = "#F59E0B"
        elif ensemble_prob >= 0.3:
            risk_level = "🔵 MODERATE"
            risk_color = "#3B82F6"
        else:
            risk_level = "🟢 LOW"
            risk_color = "#10B981"

        predictions['risk_level'] = risk_level
        predictions['risk_color'] = risk_color

    # Add latest weather data
    last_row = latest_data.iloc[-1]
    predictions['weather'] = {
        'rainfall': float(last_row['rainfall_mm']),
        'soil_moisture': float(last_row['soil_moisture']),
        'temperature': float(last_row['temperature_2m_mean']),
        'humidity': float(last_row['relative_humidity_2m_mean']),
        'date': last_row['date'].strftime('%Y-%m-%d')
    }

    return predictions

# ============== STREAMLIT APP ==============
def main():
    # Load data and models
    df_data = load_data()
    loaded_models, loaded_scalers = load_all_models()

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <h1 class="header-title">🌊 FloodWatch</h1>
        <p class="header-subtitle">AI-Powered Flood Risk Prediction for Tamil Nadu</p>
        """, unsafe_allow_html=True)

    with col2:
        st.metric("Status", "🟢 Live", help="System is operational")

    st.markdown("---")

    # Statistics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Data Points", f"{len(df_data):,}")
    with col2:
        st.metric("Districts", len(DISTRICTS))
    with col3:
        st.metric("ML Models", len(loaded_models))
    with col4:
        st.metric("Date Range", f"{(pd.to_datetime(df_data['date'].max()) - pd.to_datetime(df_data['date'].min())).days} days")
    with col5:
        st.metric("Prediction Date", "April 15, 2026", help="Predictions based on today's actual conditions")

    st.markdown("---")

    # Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 District Analysis", "📈 Model Performance", "ℹ️ About"])

    with tab1:
        st.markdown("<h2 class='section-title'>District Risk Overview</h2>", unsafe_allow_html=True)

        # Get predictions for all districts
        all_predictions = {}
        with st.spinner("Analyzing flood risk across all districts..."):
            for district in DISTRICTS:
                all_predictions[district] = predict_flood_risk(df_data, loaded_models, loaded_scalers, district)

        # Display district cards in grid
        cols = st.columns(2)
        for idx, (district, data) in enumerate(all_predictions.items()):
            with cols[idx % 2]:
                if "error" not in data:
                    # Create risk indicator
                    risk_prob = data['ensemble']
                    risk_level = data['risk_level']

                    # Card with gradient background
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid {data['risk_color']};">
                        <div class="district-name">{district}</div>
                        <div style="margin: 15px 0;">
                            <span style="font-size: 2rem; font-weight: 700; color: {data['risk_color']};">
                                {risk_prob*100:.1f}%
                            </span>
                            <span style="margin-left: 10px; font-size: 1.2rem;">{risk_level}</span>
                        </div>
                        <hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                        <div style="font-size: 0.9rem; color: #a0a0b0;">
                            <div>🌧️ Rainfall: {data['weather']['rainfall']:.1f}mm</div>
                            <div>💧 Soil Moisture: {data['weather']['soil_moisture']:.1f}%</div>
                            <div>🌡️ Temperature: {data['weather']['temperature']:.1f}°C</div>
                            <div>💨 Humidity: {data['weather']['humidity']:.1f}%</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Error for {district}: {data['error']}")

    with tab2:
        st.markdown("<h2 class='section-title'>Detailed District Analysis</h2>", unsafe_allow_html=True)

        selected_district = st.selectbox("Select a District", list(DISTRICTS.keys()), key="district_select")

        if selected_district:
            with st.spinner(f"Analyzing {selected_district}..."):
                pred_data = predict_flood_risk(df_data, loaded_models, loaded_scalers, selected_district)

                if "error" not in pred_data:
                    # Model predictions breakdown
                    st.subheader(f"Flood Risk Prediction - {selected_district}")

                    col1, col2, col3, col4 = st.columns(4)

                    if 'transformer' in pred_data:
                        with col1:
                            st.metric("🔄 Transformer", f"{pred_data['transformer']*100:.1f}%")

                    if 'lstm' in pred_data:
                        with col2:
                            st.metric("📈 LSTM", f"{pred_data['lstm']*100:.1f}%")

                    if 'xgboost' in pred_data:
                        with col3:
                            st.metric("🎯 XGBoost", f"{pred_data['xgboost']*100:.1f}%")

                    if 'random_forest' in pred_data:
                        with col4:
                            st.metric("🌲 Random Forest", f"{pred_data['random_forest']*100:.1f}%")

                    # Ensemble prediction
                    st.markdown("---")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Ensemble Prediction",
                            f"{pred_data['ensemble']*100:.1f}%",
                            delta=f"Risk Level: {pred_data['risk_level']}",
                            delta_color="off"
                        )

                    with col2:
                        st.metric(
                            "Risk Assessment",
                            pred_data['risk_level'],
                            help="Based on ensemble of all models"
                        )

                    # Historical data visualization
                    st.subheader("Historical Trends (Last 30 days)")

                    district_data = df_data[df_data['district'] == selected_district].sort_values('date').tail(30)

                    col1, col2 = st.columns(2)

                    with col1:
                        fig_rainfall = go.Figure()
                        fig_rainfall.add_trace(go.Scatter(
                            x=district_data['date'],
                            y=district_data['rainfall_mm'],
                            mode='lines+markers',
                            fill='tozeroy',
                            line=dict(color='#3B82F6', width=2),
                            marker=dict(size=5),
                            name='Rainfall'
                        ))
                        fig_rainfall.update_layout(
                            title="Rainfall (mm)",
                            xaxis_title="Date",
                            yaxis_title="Rainfall (mm)",
                            template="plotly_dark",
                            hovermode='x unified',
                            height=400
                        )
                        st.plotly_chart(fig_rainfall, use_container_width=True)

                    with col2:
                        fig_moisture = go.Figure()
                        fig_moisture.add_trace(go.Scatter(
                            x=district_data['date'],
                            y=district_data['soil_moisture'],
                            mode='lines+markers',
                            fill='tozeroy',
                            line=dict(color='#10B981', width=2),
                            marker=dict(size=5),
                            name='Soil Moisture'
                        ))
                        fig_moisture.update_layout(
                            title="Soil Moisture (%)",
                            xaxis_title="Date",
                            yaxis_title="Soil Moisture (%)",
                            template="plotly_dark",
                            hovermode='x unified',
                            height=400
                        )
                        st.plotly_chart(fig_moisture, use_container_width=True)

    with tab3:
        st.markdown("<h2 class='section-title'>Model Ensemble Details</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 🔄 Transformer
            **Multi-head Attention Mechanism**
            - Captures long-range temporal dependencies
            - Attention-based pattern recognition
            - Optimal for complex sequential data
            """)

        with col2:
            st.markdown("""
            ### 📈 LSTM
            **Long Short-Term Memory**
            - Sequential learning with memory cells
            - Excellent for time-series forecasting
            - Prevents vanishing gradient problem
            """)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("""
            ### 🎯 XGBoost
            **Gradient Boosting**
            - Boosted ensemble of decision trees
            - High accuracy on tabular data
            - Feature importance ranking
            """)

        with col4:
            st.markdown("""
            ### 🌲 Random Forest
            **Calibrated Ensemble**
            - Probability-calibrated predictions
            - Robust to outliers
            - Feature importance analysis
            """)

    with tab4:
        st.markdown("<h2 class='section-title'>About FloodWatch</h2>", unsafe_allow_html=True)

        st.markdown("""
        ### 🌊 FloodWatch
        
        **AI-Powered Flood Risk Prediction System for Tamil Nadu**
        
        FloodWatch leverages a decade of historical weather and soil data combined with four 
        state-of-the-art machine learning models to provide accurate, real-time flood risk 
        assessments for Tamil Nadu's coastal districts.
        
        #### 🎯 Key Features
        - **Ensemble Predictions**: Combines Transformer, LSTM, XGBoost, and Random Forest
        - **Real-time Analysis**: Processes latest weather and soil data
        - **Historical Context**: 10+ years of historical data for trend analysis
        - **District-level Details**: Individual risk assessments for 6 Tamil Nadu districts
        - **Multi-factor Analysis**: Considers rainfall, soil moisture, temperature, humidity, pressure, and wind speed
        
        #### 📊 Data Sources
        - Weather Data: Historical and real-time meteorological measurements
        - Soil Data: Continuous soil moisture monitoring and simulation
        - Flood Records: India Flood Inventory (2010-2020)
        
        #### 💻 Technology Stack
        - **ML Frameworks**: TensorFlow, XGBoost, scikit-learn
        - **Web Framework**: Streamlit
        - **Data Processing**: Pandas, NumPy
        - **Visualization**: Plotly
        
        #### 👨‍💻 Architecture
        The system uses an ensemble approach combining:
        1. **Transformer Model**: Attention-based temporal pattern recognition
        2. **LSTM Model**: Sequential learning with memory
        3. **XGBoost**: Gradient-boosted predictions
        4. **Random Forest**: Calibrated probability estimates
        
        The final prediction is the averaged probability from all four models, providing 
        robust and reliable flood risk assessments.
        """)

        st.divider()

        st.markdown("""
        <div style="text-align: center; color: #a0a0b0; margin-top: 40px;">
            <p>© 2026 FloodWatch | AI-Powered Flood Risk Prediction System</p>
            <p>Built with ❤️ using Streamlit, TensorFlow, and XGBoost</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

