import time

from fastapi import APIRouter, UploadFile, File

from app.models import EnrichedMatch, UploadResponse
from app.brickognize import identify_image
from app.rebrickable import get_part_detail
from app.bricklink import get_price_guide

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    start = time.time()
    image_bytes = await file.read()

    try:
        matches = await identify_image(image_bytes)
    except Exception:
        return UploadResponse(matches=[], processing_time=round(time.time() - start, 2))

    enriched = []
    for m in matches:
        detail = None
        pricing = None

        try:
            detail = await get_part_detail(m.item_type, m.item_no)
        except Exception:
            pass

        try:
            pricing = await get_price_guide(m.item_type, m.item_no)
        except Exception:
            pass

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
    return UploadResponse(matches=enriched, processing_time=elapsed)
