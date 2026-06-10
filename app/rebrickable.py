import logging

import httpx
from app.config import settings
from app.models import RebrickablePart

log = logging.getLogger(__name__)

BASE_URL = "https://rebrickable.com/api/v3"


async def get_part_detail(item_type: str, item_no: str) -> RebrickablePart | None:
    if not settings.rebrickable_api_key:
        log.warning("Rebrickable API key not set — skipping enrichment for %s %s", item_type, item_no)
        return None

    log.info("Rebrickable: fetching detail for %s %s", item_type, item_no)
    headers = {"Authorization": f"Key {settings.rebrickable_api_key}"}
    part = RebrickablePart(part_num=item_no, name="")

    async with httpx.AsyncClient(timeout=15, headers=headers) as client:
        if item_type == "PART":
            resp = await client.get(f"{BASE_URL}/lego/parts/{item_no}/")
            if resp.is_success:
                d = resp.json()
                part.name = d.get("name", "")
                cat_id = d.get("part_cat_id")
                if cat_id:
                    cat_resp = await client.get(f"{BASE_URL}/lego/part_categories/{cat_id}/")
                    if cat_resp.is_success:
                        part.category_name = cat_resp.json().get("name", "")
            else:
                log.warning("Rebrickable parts detail returned %d for %s", resp.status_code, item_no)
        elif item_type == "SET":
            resp = await client.get(f"{BASE_URL}/lego/sets/{item_no}/")
            if resp.is_success:
                d = resp.json()
                part.name = d.get("name", "")
                part.category_name = d.get("theme", {}).get("name", "") if isinstance(d.get("theme"), dict) else ""
            else:
                log.warning("Rebrickable sets detail returned %d for %s", resp.status_code, item_no)
        elif item_type == "MINIFIG":
            resp = await client.get(f"{BASE_URL}/lego/minifigs/{item_no}/")
            if resp.is_success:
                d = resp.json()
                part.name = d.get("name", "")
            else:
                log.warning("Rebrickable minifigs detail returned %d for %s", resp.status_code, item_no)
        else:
            log.warning("Rebrickable: unknown item_type %s for %s, skipping", item_type, item_no)

        if item_type == "PART":
            sets_resp = await client.get(f"{BASE_URL}/lego/parts/{item_no}/sets/")
            if sets_resp.is_success:
                results = sets_resp.json().get("results", [])
                part.set_appearances = [
                    {"set_num": s.get("set_num", ""), "name": s.get("name", "")}
                    for s in results[:5]
                ]
                log.info("Rebrickable: found %d set appearance(s) for %s", len(results), item_no)
            else:
                log.warning("Rebrickable sets list returned %d for %s", sets_resp.status_code, item_no)

    log.info("Rebrickable: done with %s %s — name=%r", item_type, item_no, part.name)
    return part
