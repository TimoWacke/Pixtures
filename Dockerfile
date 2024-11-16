FROM python:3.12

# Set the working directory in the container
WORKDIR /

# Copy the application code into the container
COPY ./app /app
COPY ./requirements.txt /requirements.txt
COPY ./patterns /patterns

# Install dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Expose the application port
EXPOSE ${APP_PORT}

# Command to run the FastAPI application
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST} --port ${APP_PORT} --forwarded-allow-ips='*'"]
