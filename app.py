import os
import re
import logging
from flask import Flask, request, render_template, redirect
from datetime import datetime
from strategy.IntegratedSMCStrategy import IntegratedSMCStrategy, TradingConfig
from pytz import timezone

app = Flask(__name__)

# 📊 Configuración de estrategia
config = TradingConfig()
strategy = IntegratedSMCStrategy(api_key="TU_API_KEY", config=config)

# 🧾 Logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔄 Ruta principal: redirige a /analyze
@app.route("/")
def home():
    return redirect("/analyze")

# 📈 Ruta de análisis con método POST
@app.route("/analyze", methods=["GET", "POST"])
def analyze_route():
    if request.method == "GET":
        return render_template("formulario.html")  # Asumimos que tenés un HTML con el formulario

    # 🔍 Captura del símbolo
    symbol = request.form.get("symbol", "").strip().upper()
    logger.info(f"📝 Símbolo recibido: '{symbol}'")

    # 🛡️ Validación básica del símbolo (ej: AUDCAD)
    if not re.match(r"^[A-Z]{6,7}$", symbol):
        logger.warning(f"⚠️ Símbolo inválido: '{symbol}'")
        return (
            f"<h1>Activo inválido</h1>"
            f"<p>El símbolo '{symbol}' no tiene el formato correcto. Usá algo tipo 'AUDCAD'.</p>"
        )

    logger.info(f"🔬 Iniciando análisis institucional de {symbol}")
    result = strategy.analyze_symbol(symbol)

    # 🚨 Fallback si hay error
    if "error" in result:
        logger.error(f"❌ Error en el análisis: {result['error']}")
        result = {
            "symbol": symbol,
            "analysis_time": datetime.now(timezone("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%d %H:%M:%S")
            "current_price": "No disponible",
            "structure_1min": "Error",
            "active_kill_zone": None,
            "premium_discount_zones": None,
            "reaction_levels": [],
            "recommendation": f"⚠️ Falló el análisis: {result['error']}"
            
        }
        data.setdefault("recommendation", None)
        data.setdefault("structure_1min", None)
        data.setdefault("premium_discount_zones", None)
        data.setdefault("reaction_levels", [])

    # ✅ Render seguro
    return render_template("report.html", **result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
