FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies first so Docker can reuse this layer
# when application source code changes.
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source and supporting files.
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY seed.py .
COPY run_migrations.py .
COPY README.md .
COPY NOTES.md .

# Create the directory used for generated Excel reports.
RUN mkdir -p /app/reports

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]