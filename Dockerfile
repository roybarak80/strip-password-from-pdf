FROM python:3.9.6-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    qpdf \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]