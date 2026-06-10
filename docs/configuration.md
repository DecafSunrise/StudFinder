# Configuration

All configuration is via environment variables (loaded from `.env` at startup).

## Environment variables

### `REBRICKABLE_API_KEY`

:material-required: **Required**

Your Rebrickable API key. Get one for free at [rebrickable.com/api](https://rebrickable.com/api/).

```ini
REBRICKABLE_API_KEY=abc123def456abc789def012abc345de
```

Controls: part name resolution, category lookup, set appearance data.

---

### `BRICKLINK_CONSUMER_KEY`

:material-optional: Optional

Your BrickLink OAuth 1.0 consumer key. Requires applying at [bricklink.com/v3/api.register.html](https://www.bricklink.com/v3/api.register.html).

```ini
BRICKLINK_CONSUMER_KEY=your_key_here
```

---

### `BRICKLINK_CONSUMER_SECRET`

:material-optional: Optional

Your BrickLink OAuth 1.0 consumer secret.

```ini
BRICKLINK_CONSUMER_SECRET=your_secret_here
```

---

### `BRICKLINK_TOKEN_VALUE`

:material-optional: Optional

Your BrickLink OAuth 1.0 token value (access token).

```ini
BRICKLINK_TOKEN_VALUE=your_token_here
```

---

### `BRICKLINK_TOKEN_SECRET`

:material-optional: Optional

Your BrickLink OAuth 1.0 token secret.

```ini
BRICKLINK_TOKEN_SECRET=your_token_secret_here
```

---

### `HOST`

:material-optional: Optional (default: `0.0.0.0`)

The host address the uvicorn server binds to.

```ini
HOST=0.0.0.0
```

---

### `PORT`

:material-optional: Optional (default: `8000`)

The port the uvicorn server listens on.

```ini
PORT=8000
```

## Sample `.env` file

```ini
REBRICKABLE_API_KEY=abc123def456abc789def012abc345de
BRICKLINK_CONSUMER_KEY=ck_xxxxxxxxxxxx
BRICKLINK_CONSUMER_SECRET=cs_xxxxxxxxxxxx
BRICKLINK_TOKEN_VALUE=tv_xxxxxxxxxxxx
BRICKLINK_TOKEN_SECRET=ts_xxxxxxxxxxxx
HOST=0.0.0.0
PORT=8000
```

## Graceful degradation

Each external API is independent:

| Service missing | What you lose |
|----------------|---------------|
| Rebrickable key | Part name falls back to Brickognize name, no category, no set appearances |
| BrickLink credentials | No pricing data (new/used prices, seller counts) |
| Both | App still identifies parts via Brickognize and links to BrickLink/Rebrickable |
