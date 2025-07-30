✅ Paso 3 completo y corregido:
Te paso el main.py actualizado completo, con:

✅ Caché con fastapi-cache2
✅ Sin cambiar tu lógica actual (IntegratedSMCStrategy)
✅ Compatible con Render (gunicorn + $PORT)
✅ Sin timeout gracias a caché
✅ main.py (versión final recomendada para Render)
python

from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from api.strategy import IntegratedSMCStrategy
from api.config import TradingConfig
import logging
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://smc-trading-frontend.onrender.com", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar caché al arrancar
@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

# Ruta principal
@app.get("/")
async def root():
    return {"message": "SMC Trading App Backend - Use POST /analyze to analyze a symbol"}

# Ruta de prueba
@app.get("/test")
async def test():
    return {"message": "Test endpoint is working"}

# Ruta de análisis con caché
@app.post("/analyze")
@cache(expire=3600)  # Cache por 1 hora
async def analyze_symbol(
    symbol: str = Form(...),
    timeframe: str = Form("1h"),
    confluence: float = Form(75.0)
):
    try:
        config = TradingConfig(
            risk_per_trade=0.02,
            min_confluence_score=confluence,
            preferred_pairs=['EURUSD', 'GBPUSD', 'USDJPY'],
            trading_sessions=['London', 'New York']
        )
        api_key = os.getenv("API_KEY", "1OFGTIDh9osWhsdERKSn6lL7Q9lUgeNH")
        strategy = IntegratedSMCStrategy(api_key=api_key, config=config)
        result = strategy.analyze_symbol(symbol.upper())
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except Exception as e:
        logger.error(f"Error analizando símbolo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Solo para pruebas locales
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
