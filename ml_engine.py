"""
Machine Learning Module
Handles model training and predictions
"""

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from config import ML_CONFIG


def prepare_ml_features(df):
    """
    Prepare features and target for ML model
    
    Args:
        df (pd.DataFrame): Dataframe with indicators
    
    Returns:
        tuple: (features DataFrame, target Series)
    """
    # Select feature columns
    feature_cols = [
        'rsi', 'macd_diff', 'stoch_k', 'bb_width', 'atr',
        'cmf', 'mfi', 'adx', 'roc', 'cci', 'williams_r',
        'volume_ratio', 'ema_9', 'ema_21', 'ema_50'
    ]
    
    features = df[feature_cols].copy()
    
    # Create target variable
    future_periods = ML_CONFIG['future_periods']
    target_return = ML_CONFIG['target_return']
    
    df['future_return'] = df['close'].shift(-future_periods) / df['close'] - 1
    df['target'] = (df['future_return'] > target_return).astype(int)
    
    # Remove last N rows (no future data)
    features = features.iloc[:-future_periods]
    target = df['target'].iloc[:-future_periods]
    
    # Remove rows with NaN
    valid_idx = features.dropna().index
    features = features.loc[valid_idx]
    target = target.loc[valid_idx]
    
    return features, target


def train_ml_model(df):
    """
    Train machine learning model
    
    Args:
        df (pd.DataFrame): Dataframe with indicators
    
    Returns:
        tuple: (model, scaler, accuracy)
    """
    try:
        features, target = prepare_ml_features(df)
        
        # Check minimum samples
        if len(features) < ML_CONFIG['min_samples']:
            st.warning(f"Not enough data for ML training. Need at least {ML_CONFIG['min_samples']} samples.")
            return None, None, 0
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, target,
            test_size=ML_CONFIG['test_size'],
            random_state=ML_CONFIG['random_state']
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = GradientBoostingClassifier(
            n_estimators=ML_CONFIG['n_estimators'],
            learning_rate=ML_CONFIG['learning_rate'],
            max_depth=ML_CONFIG['max_depth'],
            random_state=ML_CONFIG['random_state']
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Calculate accuracy
        accuracy = model.score(X_test_scaled, y_test)
        
        return model, scaler, accuracy
    
    except Exception as e:
        st.error(f"ML Training Error: {e}")
        return None, None, 0


def predict_with_ml(df, model, scaler):
    """
    Make prediction with trained ML model
    
    Args:
        df (pd.DataFrame): Dataframe with indicators
        model: Trained ML model
        scaler: Fitted scaler
    
    Returns:
        dict: Prediction results
    """
    if model is None or scaler is None:
        return None
    
    try:
        # Prepare features
        feature_cols = [
            'rsi', 'macd_diff', 'stoch_k', 'bb_width', 'atr',
            'cmf', 'mfi', 'adx', 'roc', 'cci', 'williams_r',
            'volume_ratio', 'ema_9', 'ema_21', 'ema_50'
        ]
        
        features = df[feature_cols].iloc[-1:].fillna(0)
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        return {
            'prediction': 'BULLISH' if prediction == 1 else 'BEARISH',
            'confidence': max(probability) * 100
        }
    
    except Exception as e:
        st.warning(f"ML Prediction Error: {e}")
        return None


def get_feature_importance(model, feature_names):
    """
    Get feature importance from trained model
    
    Args:
        model: Trained ML model
        feature_names (list): List of feature names
    
    Returns:
        pd.DataFrame: Feature importance dataframe
    """
    if model is None:
        return None
    
    try:
        importances = model.feature_importances_
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    except Exception as e:
        st.warning(f"Error getting feature importance: {e}")
        return None
