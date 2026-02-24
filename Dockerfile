# Use official Python image with more complete base
FROM python:3.13-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies and upgrade sqlite3
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    wget \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && wget https://www.sqlite.org/2024/sqlite-autoconf-3460000.tar.gz && \
    tar xzf sqlite-autoconf-3460000.tar.gz && \
    cd sqlite-autoconf-3460000 && \
    ./configure --prefix=/usr/local && \
    make && make install && \
    cd .. && rm -rf sqlite-autoconf-3460000* && \
    apt-get clean && \
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
