"""Main Flask application."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask
from flask_cors import CORS
from backend.api.routes import api_bp
from backend.config.config import Config

# Try to import ML routes (optional if dependencies not installed)
try:
    from backend.api.ml_routes import ml_bp
    ML_AVAILABLE = True
except ImportError as e:
    print(f"ML routes not available: {e}")
    print("Install ML dependencies with: pip install tensorflow prophet xgboost")
    ML_AVAILABLE = False

# Try to import Gemini AI routes
try:
    from backend.api.gemini_routes import gemini_bp
    GEMINI_AVAILABLE = True
except ImportError as e:
    print(f"Gemini routes not available: {e}")
    print("Install Gemini SDK with: pip install google-generativeai")
    GEMINI_AVAILABLE = False

# Try to import Alert routes (requires Cyoda MCP)
try:
    from backend.api.alert_routes import alert_bp
    ALERTS_AVAILABLE = True
except ImportError as e:
    print(f"Alert routes not available: {e}")
    ALERTS_AVAILABLE = False

# Try to import Gemini-Cyoda integration routes
try:
    from backend.api.gemini_cyoda_routes import gemini_cyoda_bp
    GEMINI_CYODA_AVAILABLE = True
except ImportError as e:
    print(f"Gemini-Cyoda integration not available: {e}")
    GEMINI_CYODA_AVAILABLE = False


def create_app(config_class=Config):
    """
    Application factory pattern.

    Args:
        config_class: Configuration class to use

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for React frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register ML routes if available
    if ML_AVAILABLE:
        app.register_blueprint(ml_bp, url_prefix='/api/ml')
        print("✓ ML routes registered")
    else:
        print("✗ ML routes not available (dependencies not installed)")

    # Register Gemini AI routes if available
    if GEMINI_AVAILABLE:
        app.register_blueprint(gemini_bp, url_prefix='/api/ai')
        print("✓ Gemini AI routes registered")
    else:
        print("✗ Gemini AI routes not available (SDK not installed)")

    # Register Alert routes if available
    if ALERTS_AVAILABLE:
        app.register_blueprint(alert_bp, url_prefix='/api/alerts')
        print("✓ Alert routes registered (Cyoda MCP integration)")
    else:
        print("✗ Alert routes not available")

    # Register Gemini-Cyoda integration routes if available
    if GEMINI_CYODA_AVAILABLE:
        app.register_blueprint(gemini_cyoda_bp, url_prefix='/api/gemini-cyoda')
        print("✓ Gemini-Cyoda integration routes registered")
    else:
        print("✗ Gemini-Cyoda integration not available")

    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy', 'service': 'Uruguay Climate Change API'}

    return app


# Create app instance for WSGI servers (gunicorn, etc.)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
