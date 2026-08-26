FROM python:3.12-slim

WORKDIR /app/control-plane
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ELO_HOST=0.0.0.0 \
    ELO_PORT=8080

COPY elo-virtual-core/control-plane /app/control-plane

EXPOSE 8080

CMD ["python", "-m", "runtime.http_api"]
