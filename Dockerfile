FROM python:3.12

# Set the working directory in the container
WORKDIR /

# Copy the application code into the container
COPY ./app /app
COPY ./requirements.txt /requirements.txt
COPY ./patterns /patterns

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

# Install dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Expose the application port
EXPOSE ${APP_PORT}

# Command to run the FastAPI application
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST} --port ${APP_PORT} --forwarded-allow-ips='*' --workers 2"]
