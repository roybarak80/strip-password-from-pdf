# Use official Python 3.9.6 base image
FROM python:3.9.6-slim

# Set working directory
WORKDIR /app

# Install system dependencies (qpdf and poppler-utils)
RUN apt-get update && apt-get install -y \
    qpdf \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Render assigns dynamically)
EXPOSE 8000

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]