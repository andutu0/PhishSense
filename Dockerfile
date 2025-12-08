FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for zbar (QR code scanning)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libzbar-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create model directory
RUN mkdir -p model

# Train models (optional - you can also mount pre-trained models)
RUN python3 ml_offline/train.py --csv data/urls_dataset.csv && \
    python3 ml_offline/train_email.py --csv data/email_dataset.csv

# Expose port
EXPOSE 60000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Run the application
CMD ["python3", "run.py"]