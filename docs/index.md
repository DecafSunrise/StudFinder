# StudFinder

**Upload a photo of a LEGO piece. Find it on BrickLink.**

StudFinder is a Docker-based Python web app that identifies LEGO parts, sets, minifigures, and sticker sheets from photographs. It chains three free/public APIs together to give you instant identification, catalog details, and current market pricing.

## How it works

```
You upload a photo
    ↓
Brickognize API — identifies the item (98.5% accuracy, 125k catalog)
    ↓
Rebrickable API — enriches with category, set appearances
    ↓
BrickLink API — fetches current new/used prices and seller counts
    ↓
You see match results with images, prices, and direct links
```

## Features

- **Image recognition** — identify parts, sets, minifigs, and sticker sheets from a photo
- **Drag-and-drop UI** — polished dark-theme interface with preview and skeleton loading
- **Market pricing** — real-time new/used prices from BrickLink (when configured)
- **Set appearances** — see which sets a part appears in
- **Graceful degradation** — each API is independent; if one fails, you still get partial results
- **Docker single-container** — one `docker compose up` and you're running

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (Engine + Compose)
- A free [Rebrickable API key](https://rebrickable.com/api/)
- (Optional) [BrickLink API OAuth credentials](https://www.bricklink.com/v3/api.register.html) for pricing

## Quick start

```bash
git clone <your-repo>
cd StudFinder
cp .env.example .env
# edit .env with your API keys
docker compose up -d
open http://localhost:8000
```

[Get started →](quickstart.md){ .md-button .md-button--primary }
[View on GitHub :fontawesome-brands-github:](https://github.com/danvargic/StudFinder){ .md-button }
