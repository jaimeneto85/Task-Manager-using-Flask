# Application image used by docker-compose for the monitored runtime.
FROM python:3.12-slim-bullseye

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source (see .dockerignore for exclusions).
COPY . .

# The Flask app lives in the inner package todo_project/todo_project; putting the outer
# folder on PYTHONPATH makes `import todo_project` resolve to it (mirrors pytest.ini).
ENV PYTHONPATH=/app/todo_project

EXPOSE 5000

# Serve with gunicorn. A single worker keeps the Prometheus metrics in one process, so
# /metrics reports accurate totals without multiprocess aggregation.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "todo_project:app"]
