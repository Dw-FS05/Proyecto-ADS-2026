FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN printf '%s\n' \
  '#!/bin/sh' \
  'set -e' \
  'python - <<PY' \
  'from app import app, db' \
  'with app.app_context():' \
  '    db.create_all()' \
  'PY' \
  'exec gunicorn --bind 0.0.0.0:5001 --workers 2 app:app' \
  > /entrypoint.sh \
  && chmod +x /entrypoint.sh
EXPOSE 5001
ENTRYPOINT ["/entrypoint.sh"]
