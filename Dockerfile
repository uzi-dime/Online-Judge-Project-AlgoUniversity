# ================================
# Debug Dockerfile to test Poetry setup
# ================================
FROM python:3.10-slim

# ================================
# Environment configuration
# ================================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

# ================================
# Install system dependencies
# ================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# ================================
# Install Poetry
# ================================
RUN curl -sSL https://install.python-poetry.org | python3 -

# ================================
# Set work directory
# ================================
WORKDIR /app

# ================================
# Copy poetry files and check them
# ================================
COPY pyproject.toml poetry.lock* ./
RUN echo "=== Poetry files copied ===" && ls -la && echo "=== Poetry version ===" && poetry --version

# ================================
# Show poetry config and install dependencies
# ================================
RUN echo "=== Poetry config ===" && poetry config --list \
    && echo "=== Installing dependencies ===" \
    && poetry install --only main --no-root --no-cache --dry-run \
    && echo "=== Actual installation ===" \
    && poetry install --only main --no-root --no-cache

# ================================
# Verify installation
# ================================
RUN echo "=== Checking installed packages ===" \
    && pip list \
    && echo "=== Testing Django import ===" \
    && python -c "import django; print('Django version:', django.__version__)" \
    && echo "=== Testing Celery import ===" \
    && python -c "import celery; print('Celery version:', celery.__version__)"

# ================================
# Copy application code
# ================================
COPY . /app/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]