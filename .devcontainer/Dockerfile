FROM python:3.12-slim-bullseye

RUN apt-get update && apt-get install -y \
    git curl bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .

RUN pip install -r requirements.txt -r requirements-dev.txt

CMD ["python", "todo_project/run.py"]
