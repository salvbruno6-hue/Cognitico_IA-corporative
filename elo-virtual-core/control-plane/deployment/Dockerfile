FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . /app

# Application dependencies will be pinned when the ELO runtime package is introduced.
EXPOSE 8080

CMD ["python", "-m", "elo_virtual_core.control_plane"]
