# Multi-stage build for production
FROM python:3.10-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --user -r requirements.txt \
    && pip install --no-cache-dir --user gunicorn

# Production stage
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=production

# Production environment variables with safe defaults
# SECURITY NOTE: Override these values using docker run -e or docker-compose environment
# NOTE: DB_PASSWORD must be provided via docker run -e DB_PASSWORD=xxx for security
ENV DB_NAME=essenza_db_prod
ENV DB_USER=essenza_user
ENV DB_HOST=db
ENV DB_PORT=3306
ENV ALLOWED_HOSTS=localhost,127.0.0.1,*
ENV CORS_ALLOWED_ORIGINS=https://localhost,https://127.0.0.1,http://localhost:8000

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage to global location
COPY --from=builder /root/.local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /root/.local/bin /usr/local/bin

# Make sure Python can find the packages
ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages
ENV PATH=/usr/local/bin:$PATH

# Set work directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/static \
    && mkdir -p /app/media \
    && mkdir -p /app/logs

# Copy project files
COPY . /app/

# Set proper permissions
RUN chmod +x /app/manage.py

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN groupadd -r django && useradd -r -g django django

# Ensure log directory exists and copy gunicorn config
RUN mkdir -p /app/logs
COPY gunicorn.conf.py /app/gunicorn.conf.py
RUN chown -R django:django /app /app/logs /app/gunicorn.conf.py

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user
USER django

CMD ["gunicorn", "--config", "/app/gunicorn.conf.py", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
