
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_dataframe(df: pd.DataFrame, required_columns: list = None) -> bool:
    """Valida que el DataFrame tenga la estructura correcta."""
    if required_columns is None:
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    
    if df.empty:
        logger.warning("DataFrame está vacío")
        return False
        
    if not all(col in df.columns for col in required_columns):
        logger.warning(f"Columnas faltantes: {set(required_columns) - set(df.columns)}")
        return False
        
    return True
