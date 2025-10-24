#!/bin/bash
set -e

echo "=========================================="
echo "Uruguay Climate Change Backend Startup"
echo "=========================================="

# Check if models directory exists
if [ ! -d "/app/models" ]; then
    echo "Creating models directory..."
    mkdir -p /app/models
fi

# Check if models are already trained
MODELS_TRAINED=true

if [ ! -f "/app/models/lstm_temperature.keras" ]; then
    echo "⚠️  LSTM model not found"
    MODELS_TRAINED=false
fi

if [ ! -f "/app/models/prophet_seasonal.pkl" ]; then
    echo "⚠️  Prophet model not found"
    MODELS_TRAINED=false
fi

if [ ! -f "/app/models/anomaly_model.pkl" ]; then
    echo "⚠️  Anomaly detector not found"
    MODELS_TRAINED=false
fi

if [ ! -f "/app/models/climate_classifier.pkl" ]; then
    echo "⚠️  Climate classifier not found"
    MODELS_TRAINED=false
fi

# Train models if not already trained
if [ "$MODELS_TRAINED" = false ]; then
    echo ""
    echo "=========================================="
    echo "Training ML Models (First-time setup)"
    echo "=========================================="
    echo "This may take 2-5 minutes..."
    echo ""
    
    # Run training script
    python3 scripts/train_ml_models.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ All models trained successfully!"
        echo ""
    else
        echo ""
        echo "❌ Model training failed!"
        echo "The application will start but ML features may not work."
        echo ""
    fi
else
    echo "✅ All ML models already trained"
fi

echo ""
echo "=========================================="
echo "Starting Flask Application"
echo "=========================================="
echo ""

# Execute the CMD from Dockerfile (passed as arguments to this script)
exec "$@"

