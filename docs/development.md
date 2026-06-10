# Development

## Local setup (without Docker)

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
pip install -r docs/requirements.txt
```

## Running locally

```bash
cp .env.example .env
# edit .env with your API keys
uvicorn app.main:app --reload
```

The `--reload` flag enables hot-reload when source files change.

## Project layout

```
StudFinder/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app factory
│   ├── config.py            # Settings
│   ├── router.py            # Routes
│   ├── models.py            # Pydantic models
│   ├── brickognize.py       # Brickognize client
│   ├── rebrickable.py       # Rebrickable client
│   ├── bricklink.py         # BrickLink client
│   └── static/              # Frontend
│       ├── index.html
│       ├── style.css
│       └── app.js
├── docs/                    # Documentation site
│   ├── index.md
│   ├── quickstart.md
│   ├── configuration.md
│   ├── api.md
│   ├── architecture.md
│   ├── docker.md
│   ├── development.md
│   └── requirements.txt
├── mkdocs.yml               # Docs config
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Building the docs site

```bash
pip install -r docs/requirements.txt
mkdocs build
```

Output goes to `site/`. To preview locally:

```bash
mkdocs serve
# Open http://localhost:8001
```

## Deploying docs to GitHub Pages

```bash
mkdocs gh-deploy
```

This builds the site and pushes the `site/` directory to the `gh-pages` branch. GitHub Pages must be configured to serve from `gh-pages` in your repo settings.

## Adding a new external API

1. Create a new module in `app/` (e.g. `app/example.py`)
2. Add an async function that returns the data
3. Call it from `router.py` — wrap in try/except for graceful degradation
4. Add the response data to `EnrichedMatch` in `models.py`
5. Update the frontend to display it
