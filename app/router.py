import logging
import time

from fastapi import APIRouter, UploadFile, File

from app.models import EnrichedMatch, UploadResponse
from app.brickognize import identify_image
from app.rebrickable import get_part_detail
from app.bricklink import get_price_guide

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    start = time.time()
    image_bytes = await file.read()
    log.info("Upload received: filename=%s, size=%d bytes", file.filename, len(image_bytes))

    try:
        matches = await identify_image(image_bytes)
    except Exception as exc:
        log.error("Brickognize request failed: %s", exc)
        return UploadResponse(matches=[], processing_time=round(time.time() - start, 2))

    if not matches:
        log.warning("Brickognize returned no candidates")
        return UploadResponse(matches=[], processing_time=round(time.time() - start, 2))

    log.info("Enriching %d match(es) from Brickognize", len(matches))
    enriched = []
    for m in matches:
        detail = None
        pricing = None

        try:
            detail = await get_part_detail(m.item_type, m.item_no)
        except Exception as exc:
            log.warning("Rebrickable request failed for %s %s: %s", m.item_type, m.item_no, exc)

        try:
            pricing = await get_price_guide(m.item_type, m.item_no)
        except Exception as exc:
            log.warning("BrickLink request failed for %s %s: %s", m.item_type, m.item_no, exc)

        enriched.append(
            EnrichedMatch(
                item_no=m.item_no,
                name=detail.name if detail and detail.name else m.name,
                item_type=m.item_type,
                category=m.category,
                confidence=m.confidence,
                thumbnail_url=m.thumbnail_url,
                image_url=m.image_url,
                bricklink_url=m.bricklink_url,
                rebrickable_url=m.rebrickable_url,
                set_appearances=detail.set_appearances if detail else [],
                pricing=pricing,
            )
        )

    elapsed = round(time.time() - start, 2)
    log.info("Upload processed in %.2fs: %d match(es) returned", elapsed, len(enriched))
    return UploadResponse(matches=enriched, processing_time=elapsed)
