import asyncio

import requests
from requests_oauthlib import OAuth1

from app.config import settings
from app.models import BrickLinkPriceGuide

BL_API = "https://api.bricklink.com/api/store/v1"


def _oauth() -> OAuth1 | None:
    ck = settings.bricklink_consumer_key
    cs = settings.bricklink_consumer_secret
    tv = settings.bricklink_token_value
    ts = settings.bricklink_token_secret
    if not all([ck, cs, tv, ts]):
        return None
    return OAuth1(ck, client_secret=cs, resource_owner_key=tv, resource_owner_secret=ts)


def _signed_get(path: str) -> dict:
    oauth = _oauth()
    if oauth is None:
        return {"meta": {"code": 401, "message": "BrickLink API not configured"}}

    url = f"{BL_API}{path}"
    resp = requests.get(url, auth=oauth, timeout=15)
    return resp.json()


async def get_price_guide(item_type: str, item_no: str) -> BrickLinkPriceGuide | None:
    type_map = {"PART": "P", "SET": "S", "MINIFIG": "M", "BOOK": "B", "GEAR": "G"}
    bl_type = type_map.get(item_type, "P")

    data = await asyncio.to_thread(_signed_get, f"/items/{bl_type}/{item_no}/price")
    if data.get("meta", {}).get("code") != 200:
        return None

    prices = data.get("data", {})
    return BrickLinkPriceGuide(
        new_min_price=_safe_float(prices, "min_price", "new"),
        new_avg_price=_safe_float(prices, "avg_price", "new"),
        new_qty=_safe_int(prices, "quantity", "new"),
        new_sellers=_safe_int(prices, "seller_count", "new"),
        used_min_price=_safe_float(prices, "min_price", "used"),
        used_avg_price=_safe_float(prices, "avg_price", "used"),
        used_qty=_safe_int(prices, "quantity", "used"),
        used_sellers=_safe_int(prices, "seller_count", "used"),
    )


def _safe_float(data: dict, key: str, condition: str) -> float | None:
    try:
        return float(data.get(condition, {}).get(key, 0))
    except (TypeError, ValueError):
        return None


def _safe_int(data: dict, key: str, condition: str) -> int | None:
    try:
        return int(data.get(condition, {}).get(key, 0))
    except (TypeError, ValueError):
        return None
