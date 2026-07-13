FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --force-reinstall "setuptools<60.0.0"

# Copy the rest of your chatbot files
COPY . .

# CRITICAL: Tell Render to train the model during the build process
RUN rasa train

EXPOSE 10000

# Start the Rasa server using the newly trained model automatically
CMD ["rasa", "run", "-p", "10000", "--enable-api", "--cors", "*"]
