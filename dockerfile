FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for mysqlclient + build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

# collect static & migrate at container start (Render-friendly)
CMD bash -lc "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn aah_guru.wsgi:application --bind 0.0.0.0:${PORT:-8000}"
