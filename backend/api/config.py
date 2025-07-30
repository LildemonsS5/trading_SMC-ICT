
from dataclasses import dataclass
from typing import List

@dataclass
class TradingConfig:
    """Clase para una configuración de parámetros más flexible y controlada."""
    swing_period: int = 5
    liquidity_tolerance: float = 0.00005
    max_distance_pips: float = 50.0
    min_confluence_score: int = 70
    risk_per_trade: float = 0.02
    price_multiplier: int = 100000
    max_freshness_minutes: int = 120
    preferred_pairs: List[str] = None
    trading_sessions: List[str] = None

    def __post_init__(self):
        if self.preferred_pairs is None:
            self.preferred_pairs = ["EURUSD", "GBPUSD", "USDJPY"]
        if self.trading_sessions is None:
            self.trading_sessions = ["London", "New York"]
