"""
Today's Conditions Module for FloodWatch
Allows prediction based on current day's actual weather conditions
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Default reasonable values for April 15, 2026 (can be updated via API)
# These represent typical monsoon-transition season conditions in Tamil Nadu
TODAY_CONDITIONS = {
    'Chennai': {
        'date': datetime(2026, 4, 15),
        'rainfall_mm': 2.5,  # Light rainfall typical for April
        'soil_moisture': 0.45,  # Post-monsoon soil moisture
        'temperature_2m_mean': 32.5,  # April heat
        'relative_humidity_2m_mean': 68.0,  # Moderate humidity
        'surface_pressure_mean': 1010.5,  # Normal pressure
        'wind_speed_10m_mean': 3.2,  # Light winds
        'cloud_cover_mean': 25.0,  # Partly cloudy
        'rain_3d': 8.5,  # 3-day accumulated
        'rain_7d': 15.2,  # 7-day accumulated
        'rain_14d': 28.3,  # 14-day accumulated
        'soil_7d_avg': 0.44,
        'soil_14d_avg': 0.42,
        'wetness_index': 0.35,
        'rain_intensity': 0.8,
        'is_monsoon': 0,  # Not monsoon season (happens June-Sept)
    },
    'Tiruvallur': {
        'date': datetime(2026, 4, 15),
        'rainfall_mm': 1.8,
        'soil_moisture': 0.42,
        'temperature_2m_mean': 33.2,
        'relative_humidity_2m_mean': 65.0,
        'surface_pressure_mean': 1010.3,
        'wind_speed_10m_mean': 3.5,
        'cloud_cover_mean': 20.0,
        'rain_3d': 6.2,
        'rain_7d': 12.0,
        'rain_14d': 24.5,
        'soil_7d_avg': 0.41,
        'soil_14d_avg': 0.40,
        'wetness_index': 0.32,
        'rain_intensity': 0.6,
        'is_monsoon': 0,
    },
    'Chengalpattu': {
        'date': datetime(2026, 4, 15),
        'rainfall_mm': 3.2,
        'soil_moisture': 0.48,
        'temperature_2m_mean': 31.8,
        'relative_humidity_2m_mean': 70.0,
        'surface_pressure_mean': 1010.4,
        'wind_speed_10m_mean': 3.0,
        'cloud_cover_mean': 30.0,
        'rain_3d': 10.1,
        'rain_7d': 18.5,
        'rain_14d': 32.0,
        'soil_7d_avg': 0.46,
        'soil_14d_avg': 0.44,
        'wetness_index': 0.38,
        'rain_intensity': 1.0,
        'is_monsoon': 0,
    },
    'Kancheepuram': {
        'date': datetime(2026, 4, 15),
        'rainfall_mm': 2.0,
        'soil_moisture': 0.40,
        'temperature_2m_mean': 33.5,
        'relative_humidity_2m_mean': 63.0,
        'surface_pressure_mean': 1010.2,
        'wind_speed_10m_mean': 3.8,
        'cloud_cover_mean': 15.0,
        'rain_3d': 5.5,
        'rain_7d': 11.0,
        'rain_14d': 22.0,
        'soil_7d_avg': 0.39,
        'soil_14d_avg': 0.38,
        'wetness_index': 0.30,
        'rain_intensity': 0.5,
        'is_monsoon': 0,
    },
    'Cuddalore': {
        'date': datetime(2026, 4, 15),
        'rainfall_mm': 1.5,
        'soil_moisture': 0.38,
        'temperature_2m_mean': 33.8,
        'relative_humidity_2m_mean': 62.0,
        'surface_pressure_mean': 1010.1,
        'wind_speed_10m_mean': 4.2,
        'cloud_cover_mean': 10.0,
        'rain_3d': 4.2,
        'rain_7d': 9.0,
        'rain_14d': 18.5,
        'soil_7d_avg': 0.37,
        'soil_14d_avg': 0.36,
        'wetness_index': 0.28,
        'rain_intensity': 0.4,
        'is_monsoon': 0,
    },
    'Nagapattinam': {
        'date': datetime(2026, 4, 15),
        'rainfall_mm': 2.8,
        'soil_moisture': 0.46,
        'temperature_2m_mean': 32.0,
        'relative_humidity_2m_mean': 72.0,
        'surface_pressure_mean': 1010.5,
        'wind_speed_10m_mean': 3.1,
        'cloud_cover_mean': 28.0,
        'rain_3d': 9.2,
        'rain_7d': 16.8,
        'rain_14d': 30.2,
        'soil_7d_avg': 0.45,
        'soil_14d_avg': 0.43,
        'wetness_index': 0.36,
        'rain_intensity': 0.9,
        'is_monsoon': 0,
    }
}

# Features for different models
TRANSFORMER_FEATURES = [
    'rainfall_mm', 'soil_moisture', 'temperature_2m_mean',
    'relative_humidity_2m_mean', 'surface_pressure_mean',
    'wind_speed_10m_mean', 'cloud_cover_mean', 'is_monsoon'
]

XGBOOST_FEATURES = [
    'rainfall_mm', 'soil_moisture', 'temperature_2m_mean',
    'relative_humidity_2m_mean', 'surface_pressure_mean',
    'wind_speed_10m_mean', 'cloud_cover_mean', 'rain_3d',
    'rain_7d', 'rain_14d', 'soil_7d_avg', 'soil_14d_avg',
    'wetness_index', 'rain_intensity', 'is_monsoon'
]


def update_conditions(district, conditions_dict):
    """
    Update today's conditions for a district
    
    Args:
        district: District name
        conditions_dict: Dictionary with weather/soil values
    
    Example:
        update_conditions('Chennai', {
            'rainfall_mm': 5.0,
            'soil_moisture': 0.55,
            'temperature_2m_mean': 30.0,
            ...
        })
    """
    if district not in TODAY_CONDITIONS:
        return False
    
    for key, value in conditions_dict.items():
        if key in TODAY_CONDITIONS[district]:
            TODAY_CONDITIONS[district][key] = value
    return True


def get_today_sequence(district, historical_df, time_steps=14):
    """
    Create a sequence using 13 days of historical data + today's conditions
    
    Args:
        district: District name
        historical_df: Historical DataFrame
        time_steps: Number of time steps (default 14)
    
    Returns:
        DataFrame with 14 rows (13 historical + 1 today)
    """
    # Get last 13 days from historical data
    district_data = historical_df[historical_df['district'] == district].sort_values('date')
    historical_sequence = district_data.tail(time_steps - 1).copy()
    
    # Create today's row
    today_row = pd.DataFrame([TODAY_CONDITIONS[district]])
    today_row['district'] = district
    
    # Combine
    sequence = pd.concat([historical_sequence, today_row], ignore_index=True)
    
    return sequence[-time_steps:]


def get_today_features(district, feature_list):
    """
    Get today's feature values for a specific district
    
    Args:
        district: District name
        feature_list: List of feature names
    
    Returns:
        List of feature values in same order as feature_list
    """
    if district not in TODAY_CONDITIONS:
        return None
    
    today_data = TODAY_CONDITIONS[district]
    return [today_data.get(feat, 0.0) for feat in feature_list]


def get_today_conditions_dict(district):
    """Get all today's conditions for a district as a dictionary"""
    if district not in TODAY_CONDITIONS:
        return None
    return TODAY_CONDITIONS[district].copy()


def set_all_conditions(conditions_dict):
    """
    Update conditions for all districts at once
    
    Args:
        conditions_dict: {district: {feature: value, ...}, ...}
    """
    for district, values in conditions_dict.items():
        if district in TODAY_CONDITIONS:
            update_conditions(district, values)

