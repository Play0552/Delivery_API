FROM python:3.11-slim


WORKDIR /app
COPY . /app/
RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install -r requirements.txt

CMD alembic upgrade head \
    && gunicorn delivery.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000