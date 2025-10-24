# Multi-stage Docker build for Uruguay Climate Change Backend
# Stage 1: Builder - Install dependencies and train models
FROM python:3.9-slim as builder

WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime - Minimal production image
FROM python:3.9-slim

WORKDIR /app

# Install runtime system dependencies only
RUN apt-get update && apt-get install -y \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p models logs src/data

# Copy pre-trained models if available (optional)
# COPY models/ ./models/

# Environment variables
ENV FLASK_APP=backend/app.py
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose Flask port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Entry point script for initialization
COPY scripts/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Start application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "backend.app:app"]

# Alternative: Use entrypoint script for custom initialization
# ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
