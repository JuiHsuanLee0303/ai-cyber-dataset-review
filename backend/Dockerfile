# syntax=docker/dockerfile:1

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code
COPY . .

# Command to run the application
# Run uvicorn from the project root, pointing to the app object in app/main.py
# Use HTTPS if SSL certificates are available
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/app/ssl/private.key", "--ssl-certfile", "/app/ssl/certificate.crt", "--reload"] 