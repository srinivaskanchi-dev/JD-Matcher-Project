# Use an official Python image
FROM python:3.11-slim

# Install system dependencies for mysqlclient and scientific libs
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential pkg-config \
    gcc g++ \
    libpq-dev \
    libffi-dev \
    libblas-dev liblapack-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install Python dependencies in a virtual environment
RUN python -m venv /opt/venv && . /opt/venv/bin/activate \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . /app/

# Activate venv by default
ENV PATH="/opt/venv/bin:$PATH"

# Run Django app (change if needed)
CMD ["gunicorn", "jdmatcher.wsgi:application", "--bind", "0.0.0.0:8000"]
