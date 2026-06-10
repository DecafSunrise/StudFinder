# Docker

## Building and running

### Default (docker compose)

```bash
docker compose up -d
```

This builds the image and starts the container. The app is available at `http://localhost:8000`.

### Manual docker build

```bash
docker build -t studfinder .
docker run -d -p 8000:8000 --env-file .env --name studfinder studfinder
```

### Stop

```bash
docker compose down
```

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The image uses `python:3.12-slim` as a lightweight base. Dependencies are cached by copying `requirements.txt` first — the layer is reused unless dependencies change.

## docker-compose.yml

```yaml
services:
  studfinder:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

Environment variables are loaded from `.env`. The container restarts automatically unless explicitly stopped.

## Port mapping

To use a different port on the host:

```bash
# docker compose
ports:
  - "9000:8000"

# docker run
docker run -d -p 9000:8000 ...
```
