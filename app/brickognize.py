import logging

import httpx
from app.models import BrickognizeMatch

log = logging.getLogger(__name__)

BRICKOGNIZE_URL = "https://api.brickognize.com/predict/"

ITEM_TYPE_MAP = {
    "part": "PART",
    "set": "SET",
    "fig": "MINIFIG",
    "sticker": "STICKER_SHEET",
}


async def identify_image(image_bytes: bytes) -> list[BrickognizeMatch]:
    log.info("Sending request to Brickognize API")

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            BRICKOGNIZE_URL,
            files={"query_image": ("image.jpg", image_bytes, "image/jpeg")},
        )
        resp.raise_for_status()
        data = resp.json()

    items = data.get("items", data.get("candidates", data.get("results", [])))
    log.info("Brickognize returned %d candidate(s)", len(items))

    if not items:
        return []

    matches = []
    for c in items[:5]:
        item_no = c.get("id", "")
        item_type_raw = c.get("type", "part")
        item_type = ITEM_TYPE_MAP.get(item_type_raw.lower(), item_type_raw.upper())
        img = c.get("img_url", "")

        matches.append(
            BrickognizeMatch(
                item_no=item_no,
                name=c.get("name", "Unknown"),
                item_type=item_type,
                category=c.get("category", ""),
                confidence=c.get("score", 0),
                thumbnail_url=img,
                image_url=img,
                bricklink_url=_bricklink_url(item_type, item_no),
                rebrickable_url=_rebrickable_url(item_type, item_no),
            )
        )

    log.info("Kept top %d match(es) for enrichment", len(matches))
    return matches


def _bricklink_url(item_type: str, item_no: str) -> str:
    type_param = {"PART": "P", "SET": "S", "MINIFIG": "M", "BOOK": "B", "GEAR": "G"}.get(item_type, "P")
    return f"https://www.bricklink.com/v2/catalog/catalogitem.page?{type_param}={item_no}"


def _rebrickable_url(item_type: str, item_no: str) -> str:
    type_path = {"PART": "parts", "SET": "sets", "MINIFIG": "minifigs"}.get(item_type, "parts")
    return f"https://rebrickable.com/{type_path}/{item_no}/"
