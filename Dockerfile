# Use official Python image with more complete base
FROM python:3.13-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8080

# Streamlit needs to run on port 8080 for Cloud Run
ENV PORT 8080

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
