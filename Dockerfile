# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (if any, e.g., libpq-dev for psycopg2, build-essential for some packages)
# For psycopg2-binary, typically no build-time OS deps are needed, but for psycopg2 (source) they are.
# Adding libpq-dev for good measure, as it's often needed for PostgreSQL C extensions.
# Also add postgresql-client for pg_dump and psql utilities inside the container (useful for manage.py backup_database)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code into the container
COPY . .

# Expose port (Gunicorn will run on this port)
EXPOSE 8000

# Add a script to run migrations and collect staticfiles (optional, can also be done in docker-compose command)
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Command to run the application (using Gunicorn)
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "taf_project.wsgi:application"]
# Using entrypoint to handle migrations etc. before starting Gunicorn
ENTRYPOINT ["/entrypoint.sh"]
# CMD will be provided by entrypoint.sh or docker-compose
