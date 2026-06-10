from pydantic import BaseModel
from typing import Optional


class BrickognizeMatch(BaseModel):
    item_no: str
    name: str
    item_type: str
    category: str
    confidence: float
    thumbnail_url: Optional[str] = None
    image_url: Optional[str] = None
    bricklink_url: str = ""
    rebrickable_url: str = ""


class RebrickablePart(BaseModel):
    part_num: str
    name: str
    category_name: str = ""
    set_appearances: list[dict] = []


class BrickLinkPriceGuide(BaseModel):
    new_min_price: Optional[float] = None
    new_avg_price: Optional[float] = None
    new_qty: Optional[int] = None
    new_sellers: Optional[int] = None
    used_min_price: Optional[float] = None
    used_avg_price: Optional[float] = None
    used_qty: Optional[int] = None
    used_sellers: Optional[int] = None


class EnrichedMatch(BaseModel):
    item_no: str
    name: str
    item_type: str
    category: str
    confidence: float
    thumbnail_url: Optional[str] = None
    image_url: Optional[str] = None
    bricklink_url: str = ""
    rebrickable_url: str = ""
    set_appearances: list[dict] = []
    pricing: Optional[BrickLinkPriceGuide] = None


class UploadResponse(BaseModel):
    matches: list[EnrichedMatch]
    processing_time: float
