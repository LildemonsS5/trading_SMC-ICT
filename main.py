from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.strategy import IntegratedSMCStrategy
from api.config import TradingConfig
import logging
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SymbolRequest(BaseModel):
    symbol: str

@app.post("/analyze")
async def analyze_symbol(request: SymbolRequest):
    try:
        config = TradingConfig(
            risk_per_trade=0.02,
            min_confluence_score=75,
            preferred_pairs=['EURUSD', 'GBPUSD', 'USDJPY'],
            trading_sessions=['London', 'New York']
        )
        api_key = os.getenv("API_KEY", "1OFGTIDh9osWhsdERKSn6lL7Q9lUgeNH")  # Obtener API key desde variable de entorno
        strategy = IntegratedSMCStrategy(api_key=api_key, config=config)
        result = strategy.analyze_symbol(request.symbol.upper())
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except Exception as e:
        logger.error(f"Error analizando símbolo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Usar puerto de Render o 8000 para desarrollo local
    uvicorn.run(app, host="0.0.0.0", port=port)
