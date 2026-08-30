FROM python:3.11-slim
WORKDIR /app

# Install dependencies first (better layer caching on rebuilds)
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . .

<<<<<<< HEAD
# Run as a non-root user instead of root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Basic liveness check against the home route
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Gunicorn instead of the Flask dev server. -w sets worker count;
# tune based on CPU cores (rule of thumb: 2 * cores + 1).
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--timeout", "120", "application:app"]
=======
EXPOSE 5000
CMD ["python3", "application.py"]
>>>>>>> 256d806252efebb7f4d48ceb1e9cde7e12d3f95d
