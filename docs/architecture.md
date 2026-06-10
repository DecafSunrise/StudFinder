# Architecture

## System overview

```
┌─────────────────────────────────────┐
│  Browser                            │
│  ┌───────────┐  ┌────────────────┐  │
│  │ Upload    │  │ Results Grid   │  │
│  │ (drag &   │  │ with cards,    │  │
│  │  drop)    │  │ prices, links  │  │
│  └─────┬─────┘  └───────▲────────┘  │
│        │                │           │
└────────┼────────────────┼───────────┘
         │ POST /upload   │ JSON
         ▼                │
┌─────────────────────────┴─────────┐
│  FastAPI Server (Python)         │
│                                   │
│  ┌──────────┐  ┌──────────────┐  │
│  │ Router   │  │ Static Files │  │
│  │ /upload  │  │ (HTML/CSS/JS)│  │
│  │ /health  │  └──────────────┘  │
│  └────┬─────┘                    │
│       │                          │
│  ┌────┴─────────────────────┐    │
│  │  External API Clients    │    │
│  │                          │    │
│  │  ┌───────────┐           │    │
│  │  │Brickognize│ (async)   │    │
│  │  └─────┬─────┘           │    │
│  │  ┌───────────┐           │    │
│  │  │Rebrickable│ (async)   │    │
│  │  └─────┬─────┘           │    │
│  │  ┌───────────┐           │    │
│  │  │BrickLink  │ (sync via │    │
│  │  │           │ thread)   │    │
│  │  └───────────┘           │    │
│  └────┬─────────────────────┘    │
└───────┼──────────────────────────┘
        │ HTTP
┌───────┴──────────┐  ┌──────────────┐  ┌──────────────┐
│ Brickognize API  │  │ Rebrickable  │  │ BrickLink    │
│ (free, no auth)  │  │ API (key)    │  │ API (OAuth1) │
│ Identify items   │  │ Part details │  │ Price guide  │
│ from photos      │  │ Set lists    │  │ Seller data  │
└──────────────────┘  └──────────────┘  └──────────────┘
```

## Request flow

1. User drags an image onto the upload zone in the browser
2. Browser shows a local preview and sends a `POST /upload` with the file
3. FastAPI reads the image bytes and calls Brickognize API
4. Brickognize returns up to 5 candidate matches with item numbers and confidence scores
5. For each match, FastAPI calls Rebrickable and BrickLink in parallel:
    - Rebrickable resolves the part name, category, and set appearances
    - BrickLink fetches current new/used pricing
6. FastAPI merges all data into an enriched response
7. Browser renders result cards with images, badges, pricing, and links

## Error handling

Each external call is wrapped in its own try/except. If any API fails:
- Brickognize failure → empty results (nothing to show)
- Rebrickable failure → fall back to Brickognize's name, no set appearances
- BrickLink failure → no pricing shown, card still renders

This means the app works even with minimal configuration (Brickognize only).

## File layout

```
app/
├── main.py           # FastAPI app, static file mount
├── config.py         # Pydantic Settings from env
├── router.py         # Route handlers
├── models.py         # Pydantic response/request models
├── brickognize.py    # Async HTTP client
├── rebrickable.py    # Async HTTP client
└── bricklink.py      # Sync OAuth 1.0 client (offloaded to thread)
```

### Why sync for BrickLink?

The BrickLink API uses OAuth 1.0. The `requests-oauthlib` library (which handles the signing) is synchronous. Rather than reimplementing OAuth 1.0 signing for `httpx`, the call is offloaded to a thread pool with `asyncio.to_thread` so it doesn't block the event loop.
