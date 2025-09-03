# Use official Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies 
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Expose port if running a Streamlit/Flask app (optional, remove if CLI only)
#EXPOSE 8501

# Start FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
