# StudFinder

Upload a photo of a LEGO piece and find matching parts on BrickLink.

Built with Python (FastAPI), Docker, and three APIs: Brickognize (image recognition), Rebrickable (catalog data), and BrickLink (market pricing).

## Quick start

```bash
cp .env.example .env
# edit .env with your API keys (see docs for details)
docker compose up -d
open http://localhost:8000
```

## How it works

1. **Upload** a photo via drag-and-drop
2. **Brickognize** identifies the LEGO item (98.5% accuracy)
3. **Rebrickable** enriches with category and set appearances
4. **BrickLink** fetches current new/used pricing
5. **Results** are displayed with images, prices, and direct links

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- Free [Rebrickable API key](https://rebrickable.com/api/)
- Optional: [BrickLink OAuth credentials](https://www.bricklink.com/v3/api.register.html) for pricing

## Documentation

Full docs at [decafsunrise.github.io/StudFinder](https://decafsunrise.github.io/StudFinder) — includes configuration guide, API reference, architecture overview, and development setup.

## Tech stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, uvicorn |
| Frontend | Vanilla HTML/CSS/JS (dark theme) |
| Container | Docker, docker-compose |
| Recognition | Brickognize API (free, no auth) |
| Catalog | Rebrickable API (free key) |
| Pricing | BrickLink API (OAuth 1.0) |
