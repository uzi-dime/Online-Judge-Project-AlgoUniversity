# Use official Python slim base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

# Install system dependencies needed for building Python packages and Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set work directory
WORKDIR /app

# Copy poetry config files first for cache
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies without dev dependencies
RUN poetry install --no-dev --no-root

# Copy entire project source code
COPY . /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 (default Django port)
EXPOSE 8000

# Run the Django application with Gunicorn WSGI server
CMD ["gunicorn", "online_judge.wsgi:application", "--bind", "0.0.0.0:8000"]
