FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ffmpeg \
    fonts-noto-cjk \
    fonts-nanum \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY frontend/dist ./frontend/dist

RUN fc-cache -f -v

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
