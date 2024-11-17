# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    chromium \
    chromium-driver \
    chromium-sandbox \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONUNBUFFERED=1

# Copy requirements first to leverage Docker cache
COPY app/hooks/mh_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r mh_requirements.txt

# Copy application files to the root directory
COPY app/hooks/map_hook.py /app/
COPY app/api/v1/get_map.py /app/
COPY app/core/settings.py /app/

# Set Python path to include `/app`
ENV PYTHONPATH=/app

# Set default environment variables
ENV APP_PORT=8000
ENV HOST=0.0.0.0
ENV FLASK_APP=/app/get_map.py
ENV ENVIRONMENT=local
ENV MONGO_USERNAME=placeholder
ENV MONGO_PASSWORD=placeholder
ENV PRINTFUL_BEARER=placeholder


# Add Chrome flags for running in container
ENV CHROME_FLAGS="--headless --disable-gpu --no-sandbox --disable-dev-shm-usage"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]

# BUILD VIA: docker buildx build -t pixtures-screenshot-service -f MapAPI.Dockerfile . FROM PROJECT ROOT DIR
# RUN VIA: docker run -p 8000:8000 pixtures-screenshot-service:latest