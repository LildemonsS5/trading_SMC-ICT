from flask import Flask, request, jsonify
from strategy.smc_strategy import IntegratedSMCStrategy, TradingConfig
import os

app = Flask(__name__)

# API Key desde entorno o valor por defecto
API_KEY = os.getenv("FMP_API_KEY", "1OFGTIDh9osWhsdERKSn6lL7Q9lUgeNH")

# Configuración base para la estrategia
config = TradingConfig(
    risk_per_trade=0.02,
    min_confluence_score=75,
    preferred_pairs=['EURUSD', 'GBPUSD', 'USDJPY', 'AUDCAD'],
    trading_sessions=['London', 'New York']
)

strategy = IntegratedSMCStrategy(API_KEY, config)

@app.route("/analyze", methods=["POST"])
def analyze_symbol():
    data = request.get_json()
    symbol = data.get("symbol", "EURUSD")
    result = strategy.analyze_symbol(symbol)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
