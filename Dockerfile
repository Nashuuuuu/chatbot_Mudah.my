# Use an official Python runtime that matches your local working state
FROM python:3.10-slim

# Set system working directories
WORKDIR /app

# Install system dependencies needed to compile native packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /lib/apt/lists/*

# Force internal package installer configurations to use legacy-safe versions
RUN pip install --no-cache-dir "setuptools<60.0.0" "packaging<22.0" wheel

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Rasa project application files
COPY . .

# Expose port 10000 for Render routing
EXPOSE 10000

# Start the Rasa production server environment
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "10000"]