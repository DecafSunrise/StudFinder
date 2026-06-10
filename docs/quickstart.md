# Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/danvargic/StudFinder.git
cd StudFinder
```

## 2. Set up API credentials

Copy the example environment file and fill in your keys:

```bash
cp .env.example .env
```

### Rebrickable API key (required)

1. Go to [rebrickable.com/api](https://rebrickable.com/api/)
2. Create a free account
3. Copy your API key
4. Add it to `.env`:

```ini
REBRICKABLE_API_KEY=your_32_char_hex_key
```

### BrickLink API credentials (optional — enables pricing)

BrickLink pricing data requires OAuth 1.0 credentials. Apply at [bricklink.com/v3/api.register.html](https://www.bricklink.com/v3/api.register.html).

Once approved, add to `.env`:

```ini
BRICKLINK_CONSUMER_KEY=your_consumer_key
BRICKLINK_CONSUMER_SECRET=your_consumer_secret
BRICKLINK_TOKEN_VALUE=your_token_value
BRICKLINK_TOKEN_SECRET=your_token_secret
```

!!! note
    Without BrickLink credentials the app still works — you'll get identification and Rebrickable data, just no pricing.

## 3. Start the app

```bash
docker compose up -d
```

This builds the image (if needed) and starts the container on port 8000.

## 4. Open the UI

[http://localhost:8000](http://localhost:8000)

Drag a photo of a LEGO piece onto the upload zone. Results appear within seconds.

## What to expect

| Item type | Works? |
|-----------|--------|
| LEGO parts (bricks, plates, tiles, etc.) | ✅ |
| LEGO sets (boxed sets) | ✅ |
| Minifigures | ✅ |
| Sticker sheets | ✅ |
| Non-LEGO items | ❌ (may give false positives) |

### Tips for best results

- Place the piece on a **plain, contrasting background** (white or black)
- Use **good, even lighting** — avoid harsh shadows
- Photograph the piece **from the top** in a clear, focused shot
- For printed/stickered pieces, make sure the print is visible
