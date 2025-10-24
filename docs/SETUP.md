# 🚀 Setup & Installation Guide

Complete guide to setting up and running the Uruguay Climate Change Monitoring & AI Analysis System.

---

## 📋 Prerequisites

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8 GB
- Disk: 5 GB free space
- OS: Linux, macOS, or Windows 10+

**Recommended:**
- CPU: 8+ cores
- RAM: 16 GB
- Disk: 10 GB free space
- GPU: Optional (CUDA-compatible for faster ML training)

### Software Dependencies

**Required:**
- **Python:** 3.9 or higher
- **Node.js:** 16.x or higher
- **npm:** 8.x or higher
- **Git:** Latest version

**Optional (for Docker deployment):**
- **Docker:** 20.x or higher
- **Docker Compose:** 2.x or higher

---

## ⚡ Quick Start (5 Minutes)

### Option 1: Docker Compose (Recommended)

**Best for:** Quick demo, production deployment

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/uruguay-climate-change.git
cd uruguay-climate-change

# 2. Set up environment variables
cp .env.example .env
nano .env  # Add your GEMINI_API_KEY

# 3. Build and run
docker-compose up -d

# 4. Wait for services to start (30-60 seconds)
docker-compose logs -f

# 5. Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

**That's it!** Skip to [Usage Examples](#-usage-examples) below.

---

### Option 2: Manual Setup (Development)

**Best for:** Development, customization, learning

Follow the detailed steps in the next sections.

---

## 🐍 Backend Setup (Python/Flask)

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/uruguay-climate-change.git
cd uruguay-climate-change
```

### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected installation time:** 3-5 minutes

**Troubleshooting:**
```bash
# If TensorFlow installation fails:
pip install tensorflow-cpu  # Use CPU-only version

# If Prophet fails on Windows:
conda install -c conda-forge prophet  # Use conda instead

# If gcc/compiler errors on Linux:
sudo apt-get install build-essential python3-dev
```

### Step 4: Verify Installation

```bash
python -c "import tensorflow; print(tensorflow.__version__)"
python -c "import prophet; print('Prophet OK')"
python -c "import google.generativeai as genai; print('Gemini SDK OK')"
```

### Step 5: Set Up Environment Variables

Create `.env` file in project root:

```bash
# Create from template
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

**Required variables:**
```bash
# .env file
FLASK_APP=backend/app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here-change-in-production

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Cyoda MCP (optional - for bonus features)
CYODA_API_URL=https://api.cyoda.net
CYODA_API_KEY=your_cyoda_api_key_here

# Model paths
MODEL_PATH=./models
DATA_PATH=./src/data

# Port configuration
BACKEND_PORT=5000
FRONTEND_PORT=3000
```

**Get Gemini API Key:**
1. Visit https://ai.google.dev/
2. Click "Get API Key"
3. Create new project or select existing
4. Copy API key to `.env` file

**Get Cyoda Access (optional):**
- Contact Cyoda for MCP access: https://cyoda.com/contact
- Add credentials to `.env` file

### Step 6: Download/Prepare Data

**Option A: Use included dataset**
```bash
# Data already included in src/data/
ls src/data/climate-change_ury.csv
```

**Option B: Download fresh data**
```bash
bash scripts/download_data.sh
```

### Step 7: Train ML Models

**This step takes 5-10 minutes**

```bash
# Train all models at once
python scripts/train_ml_models.py
```

**Expected output:**
```
Training LSTM model...
Epoch 1/50 - loss: 0.0523 - val_loss: 0.0421
...
Epoch 50/50 - loss: 0.0087 - val_loss: 0.0095
✓ LSTM model saved to models/lstm_temperature.keras

Training Prophet model...
✓ Prophet model saved to models/prophet_seasonal.pkl

Training Anomaly Detector...
✓ Anomaly detector saved to models/anomaly_detector.pkl

Training Climate Classifier...
✓ Classifier saved to models/climate_classifier_xgb.pkl

All models trained successfully!
```

**Verify models:**
```bash
ls -lh models/
# Should see:
# - lstm_temperature.keras
# - lstm_scaler.pkl
# - prophet_seasonal.pkl
# - anomaly_detector.pkl
# - climate_classifier_xgb.pkl
# - climate_classifier_lgb.pkl
```

### Step 8: Start Backend Server

**Development mode:**
```bash
# From project root
export FLASK_APP=backend/app.py
export FLASK_ENV=development
export GEMINI_API_KEY=your_key_here

flask run --host=0.0.0.0 --port=5000
```

**Or use Python directly:**
```bash
python backend/app.py
```

**Production mode (with Gunicorn):**
```bash
gunicorn -b 0.0.0.0:5000 -w 4 backend.app:app
```

**Expected output:**
```
 * Serving Flask app 'backend/app.py'
 * Debug mode: on
✓ ML routes registered
✓ Gemini AI routes registered
✓ Alert routes registered (Cyoda MCP integration)
✓ Gemini-Cyoda integration routes registered
 * Running on http://0.0.0.0:5000
```

**Test backend:**
```bash
# Health check
curl http://localhost:5000/health

# Get climate data
curl http://localhost:5000/api/data | jq

# Expected response:
# {"status": "healthy", "service": "Uruguay Climate Change API"}
```

---

## ⚛️ Frontend Setup (React)

### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 2: Install Node Dependencies

```bash
npm install
```

**Expected installation time:** 2-3 minutes

**Troubleshooting:**
```bash
# If npm install fails, try:
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Or use yarn instead:
yarn install
```

### Step 3: Configure Environment

Create `frontend/.env`:

```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENABLE_GEMINI=true
REACT_APP_ENABLE_CYODA=true
```

**For production:**
```bash
# frontend/.env.production
REACT_APP_API_URL=https://your-backend-url.com
REACT_APP_ENABLE_GEMINI=true
REACT_APP_ENABLE_CYODA=true
```

### Step 4: Start Development Server

```bash
npm start
```

**Expected output:**
```
Compiled successfully!

You can now view uruguay-climate-change-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

**Browser should automatically open to http://localhost:3000**

### Step 5: Build for Production (Optional)

```bash
npm run build
```

**Output:** `build/` directory with optimized static files

**Serve production build:**
```bash
# Using serve
npx serve -s build -p 3000

# Or with nginx (see Docker section)
```

---

## 🐳 Docker Deployment

### Single-Container Backend

**1. Create Dockerfile:**

```dockerfile
# Dockerfile (project root)
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p models logs

# Train models (optional - can be done externally)
# RUN python scripts/train_ml_models.py

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=backend/app.py
ENV PYTHONUNBUFFERED=1

# Start Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "--timeout", "120", "backend.app:app"]
```

**2. Build and run:**

```bash
docker build -t uruguay-climate-backend .
docker run -p 5000:5000 \
  -e GEMINI_API_KEY=your_key_here \
  -v $(pwd)/models:/app/models \
  uruguay-climate-backend
```

### Single-Container Frontend

**1. Create frontend/Dockerfile:**

```dockerfile
# frontend/Dockerfile
FROM node:16-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source
COPY . .

# Build
RUN npm run build

# Production stage with nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**2. Create frontend/nginx.conf:**

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (optional)
    location /api {
        proxy_pass http://backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**3. Build and run:**

```bash
cd frontend
docker build -t uruguay-climate-frontend .
docker run -p 3000:80 uruguay-climate-frontend
```

### Multi-Container with Docker Compose

**1. Create docker-compose.yml:**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: climate-backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=backend/app.py
      - FLASK_ENV=production
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - CYODA_API_KEY=${CYODA_API_KEY}
      - CYODA_API_URL=${CYODA_API_URL}
    volumes:
      - ./models:/app/models
      - ./src/data:/app/src/data
      - ./logs:/app/logs
    networks:
      - climate-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: climate-frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    depends_on:
      - backend
    networks:
      - climate-network
    restart: unless-stopped

  redis:  # Optional: for caching
    image: redis:alpine
    container_name: climate-redis
    ports:
      - "6379:6379"
    networks:
      - climate-network
    restart: unless-stopped

networks:
  climate-network:
    driver: bridge

volumes:
  models:
  data:
  logs:
```

**2. Create .env file:**

```bash
# .env (project root)
GEMINI_API_KEY=your_gemini_key_here
CYODA_API_KEY=your_cyoda_key_here
CYODA_API_URL=https://api.cyoda.net
```

**3. Run:**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop services
docker-compose down
```

**4. Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Redis: localhost:6379

---

## ☸️ Kubernetes Deployment

### Prerequisites

```bash
# Install kubectl
# macOS:
brew install kubectl

# Linux:
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify
kubectl version --client
```

### Step 1: Build and Push Images

```bash
# Tag images
docker tag uruguay-climate-backend your-registry/uruguay-climate-backend:latest
docker tag uruguay-climate-frontend your-registry/uruguay-climate-frontend:latest

# Push to registry
docker push your-registry/uruguay-climate-backend:latest
docker push your-registry/uruguay-climate-frontend:latest
```

### Step 2: Create Kubernetes Secrets

```bash
# Create secret for API keys
kubectl create secret generic climate-secrets \
  --from-literal=gemini-api-key=your_key_here \
  --from-literal=cyoda-api-key=your_key_here
```

### Step 3: Apply Configurations

```bash
# Apply all Kubernetes configs
kubectl apply -f kubernetes/

# Or apply individually:
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
kubectl apply -f kubernetes/frontend/deployment.yaml
kubectl apply -f kubernetes/frontend/service.yaml
kubectl apply -f kubernetes/frontend/ingress.yaml
```

### Step 4: Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check ingress
kubectl get ingress

# View logs
kubectl logs -l app=climate-backend
kubectl logs -l app=climate-frontend
```

### Step 5: Access Application

```bash
# Get external IP
kubectl get ingress climate-ingress

# Or use port-forward for testing
kubectl port-forward svc/frontend-service 3000:80
kubectl port-forward svc/backend-service 5000:5000
```

**Production URL:**
- Live at: https://client-app-uruguay-climate-eb270b9abddf48108ee3a64e82fcebc3.eu.cyoda.net/

---

## 🧪 Testing the Setup

### Backend Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_models/
pytest tests/test_api/

# Run with coverage
pytest --cov=src --cov-report=html tests/

# View coverage report
open htmlcov/index.html
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test ClimateChart.test.js
```

### Integration Tests

```bash
# Test backend API
bash scripts/test_frontend_backend_connection.sh

# Expected output:
# ✓ Backend health check: OK
# ✓ Data endpoint: 200 OK
# ✓ ML endpoint: 200 OK
# ✓ AI endpoint: 200 OK
```

### Manual Testing Checklist

- [ ] Backend health endpoint: http://localhost:5000/health
- [ ] Frontend loads: http://localhost:3000
- [ ] Dashboard displays climate data
- [ ] Charts render correctly
- [ ] ML predictions load (may take 5-10 seconds)
- [ ] Gemini AI analysis works (requires API key)
- [ ] Cyoda alerts create successfully (requires MCP access)
- [ ] No console errors in browser DevTools

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'tensorflow'"

**Solution:**
```bash
pip install tensorflow
# Or for CPU-only:
pip install tensorflow-cpu
```

#### 2. "Port 5000 already in use"

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
flask run --port=5001
```

#### 3. "Cannot find module 'axios'"

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### 4. "Gemini API error: Invalid API key"

**Solution:**
- Verify API key in `.env` file
- Check key at https://ai.google.dev/
- Ensure no extra spaces/newlines in key
- Restart Flask server after changing `.env`

#### 5. "CUDA not available" (for GPU training)

**Solution:**
```bash
# Verify CUDA installation
nvidia-smi

# Install TensorFlow with GPU support
pip install tensorflow[and-cuda]

# Or use CPU version (works fine)
pip install tensorflow-cpu
```

#### 6. "Models not found" error

**Solution:**
```bash
# Retrain models
python scripts/train_ml_models.py

# Verify model files
ls -lh models/

# Check MODEL_PATH in .env
echo $MODEL_PATH
```

#### 7. Docker build fails

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check disk space
df -h
```

---

## 🔄 Updating the System

### Update Code

```bash
# Pull latest changes
git pull origin main

# Backend: reinstall dependencies
pip install -r requirements.txt

# Frontend: reinstall dependencies
cd frontend
npm install
```

### Update Models

```bash
# Retrain with new data
python scripts/train_ml_models.py

# Restart backend
# Ctrl+C to stop, then:
flask run
```

### Update Docker

```bash
# Rebuild images
docker-compose build

# Restart containers
docker-compose up -d
```

---

## 📝 Environment Variables Reference

### Backend (.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FLASK_APP` | Yes | `backend/app.py` | Flask app entry point |
| `FLASK_ENV` | No | `production` | Environment (development/production) |
| `SECRET_KEY` | Yes | - | Flask secret key |
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |
| `CYODA_API_KEY` | No | - | Cyoda MCP API key (for bonus features) |
| `CYODA_API_URL` | No | `https://api.cyoda.net` | Cyoda API endpoint |
| `MODEL_PATH` | No | `./models` | Path to trained models |
| `DATA_PATH` | No | `./src/data` | Path to data files |
| `LOG_LEVEL` | No | `INFO` | Logging level |

### Frontend (.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REACT_APP_API_URL` | Yes | `http://localhost:5000` | Backend API URL |
| `REACT_APP_ENABLE_GEMINI` | No | `true` | Enable Gemini features |
| `REACT_APP_ENABLE_CYODA` | No | `true` | Enable Cyoda features |

---

## 📞 Getting Help

### Documentation
- [README.md](README.md) - Project overview
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [DATASET.md](DATASET.md) - Dataset documentation
- [ML_MODELS.md](ML_MODELS.md) - Model details

### Community
- **GitHub Issues:** [Report bugs](https://github.com/YOUR_USERNAME/uruguay-climate-change/issues)
- **Discussions:** [Ask questions](https://github.com/YOUR_USERNAME/uruguay-climate-change/discussions)

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [TensorFlow Guides](https://www.tensorflow.org/tutorials)
- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Google Gemini API Docs](https://ai.google.dev/docs)

---

## ✅ Setup Verification Checklist

Before submitting/demoing, verify:

- [ ] All dependencies installed (no errors)
- [ ] `.env` file configured with API keys
- [ ] ML models trained and saved in `models/`
- [ ] Backend starts without errors
- [ ] Frontend builds successfully
- [ ] Can access http://localhost:3000
- [ ] Dashboard displays climate data
- [ ] ML predictions work
- [ ] Gemini AI responds (if API key provided)
- [ ] No console errors in browser
- [ ] Docker containers start (if using Docker)
- [ ] All tests pass (`pytest`, `npm test`)

---

**Setup complete! 🎉**

Proceed to [Usage Examples](#-usage-examples) in README.md or start exploring the application.

**Estimated total setup time:**
- Docker Compose: 5 minutes
- Manual setup: 20-30 minutes
- Including model training: 30-40 minutes

---

**Last Updated:** October 2025
**Version:** 1.0.0
