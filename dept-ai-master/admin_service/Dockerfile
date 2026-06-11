FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY admin_service/requirements-lite.txt .
RUN pip install --no-cache-dir -r requirements-lite.txt

# Copy application code
COPY config.py .
COPY admin_service/ ./admin_service/

# Copy the admin dashboard HTML so it's baked into the image
# (volume mount in docker-compose will override this at runtime)
COPY admin_dashboard.html ./admin_dashboard.html

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8005

# Run the application
CMD ["uvicorn", "admin_service.main:app", "--host", "0.0.0.0", "--port", "8005"]
