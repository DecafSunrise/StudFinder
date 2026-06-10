# API Reference

## `GET /health`

Health check endpoint.

**Response:**

```json
{"status": "ok"}
```

---

## `POST /upload`

Upload an image for LEGO part identification.

### Request

**Content-Type:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | Image (JPEG/PNG) | Yes | Photo of a LEGO piece |

**Example using `curl`:**

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@photo.jpg"
```

### Response

```json
{
  "matches": [
    {
      "item_no": "3001",
      "name": "Brick 2 x 4",
      "item_type": "PART",
      "category": "Brick",
      "confidence": 0.97,
      "thumbnail_url": "https://cdn.rebrickable.com/...",
      "image_url": "https://cdn.rebrickable.com/...",
      "bricklink_url": "https://www.bricklink.com/v2/catalog/catalogitem.page?P=3001",
      "rebrickable_url": "https://rebrickable.com/parts/3001/",
      "set_appearances": [
        {"set_num": "10700-1", "name": "Police Patrol Bike"},
        {"set_num": "10717-1", "name": "Bricks & More 1000 Bricks"}
      ],
      "pricing": {
        "new_min_price": 0.05,
        "new_avg_price": 0.08,
        "new_qty": 15842,
        "new_sellers": 47,
        "used_min_price": 0.01,
        "used_avg_price": 0.03,
        "used_qty": 98753,
        "used_sellers": 312
      }
    }
  ],
  "processing_time": 1.87
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `matches` | array | List of identified items, ordered by confidence (descending) |
| `matches[].item_no` | string | BrickLink / Rebrickable item number |
| `matches[].name` | string | Human-readable item name |
| `matches[].item_type` | string | `PART`, `SET`, `MINIFIG`, or `STICKER_SHEET` |
| `matches[].category` | string | Category name (e.g. "Brick", "Plate") |
| `matches[].confidence` | float | Match confidence score (0.0 – 1.0) |
| `matches[].thumbnail_url` | string | Thumbnail image URL |
| `matches[].bricklink_url` | string | Direct link to BrickLink catalog page |
| `matches[].rebrickable_url` | string | Direct link to Rebrickable page |
| `matches[].set_appearances` | array | Up to 5 sets this part appears in (parts only) |
| `matches[].pricing` | object | Current BrickLink price guide (null if unconfigured) |
| `processing_time` | float | Server-side processing time in seconds |
