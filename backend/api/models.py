
from dataclasses import dataclass
from typing import Optional

@dataclass
class KillZoneInfo:
    """Información de Kill Zone"""
    name: Optional[str]
    priority: str
    remaining_minutes: int
    is_active: bool

@dataclass
class PremiumDiscountZones:
    """Zonas Premium y Discount"""
    equilibrium: Optional[float]
    premium_start: Optional[float]
    discount_end: Optional[float]
    range_high: Optional[float]
    range_low: Optional[float]
    current_zone: str
