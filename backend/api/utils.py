import pandas as pd
from datetime import datetime
import pytz

def fetch_ohlc_data(api_key: str, symbol: str, timeframe: str) -> pd.DataFrame:
    import requests
    url = f"https://financialmodelingprep.com/api/v3/historical-chart/{timeframe}/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if not data or 'error' in data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    return df

def detect_imbalance(df: pd.DataFrame) -> list:
    return []

def is_valid_session(current_time: datetime, sessions: list) -> bool:
    ny_tz = pytz.timezone('America/New_York')
    current_time_ny = current_time.astimezone(ny_tz)
    hour = current_time_ny.hour
    minute = current_time_ny.minute
    if 'London' in sessions and 3 <= hour <= 11:
        return True
    if 'New York' in sessions and 8 <= hour <= 16:
        return True
    return False

def validate_dataframe(df: pd.DataFrame) -> bool:
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    if df.empty:
        return False
    if not all(col in df.columns for col in required_columns):
        return False
    if len(df) < 10:
        return False
    return True
