import os
import re
import logging
from flask import Flask, request, render_template, redirect
from datetime import datetime
from pytz import timezone
from strategy.IntegratedSMCStrategy import IntegratedSMCStrategy, TradingConfig

app = Flask(__name__)

# 📊 Configuración de estrategia
config = TradingConfig()
strategy = IntegratedSMCStrategy(api_key="1OFGTIDh9osWhsdERKSn6lL7Q9lUgeNH", config=config)

# 🧾 Logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔄 Ruta principal: redirige a /analyze
@app.route("/")
def home():
    return redirect("/analyze")

# 📈 Ruta de análisis
@app.route("/analyze", methods=["GET", "POST"])
def analyze_route():
    if request.method == "GET":
        return render_template("report.html") # Asegurate que exista este template para el formulario

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

    # ⏱️ Hora UTC-3
    local_time = datetime.now(timezone("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%d %H:%M:%S")
    result["analysis_time"] = local_time
    result["symbol"] = symbol  # Por si falla el análisis

    # 🚨 Fallback si hay error
    if "error" in result:
        logger.error(f"❌ Error en el análisis: {result['error']}")
        result = {
            "symbol": symbol,
            "analysis_time": local_time,
            "current_price": "No disponible",
            "structure_1min": None,
            "active_kill_zone": None,
            "premium_discount_zones": None,
            "reaction_levels": [],
            "recommendation": None,
            "swing_points": [],
            "order_blocks": [],
            "fair_value_gaps": [],
            "liquidity_sweeps": [],
            "confluence": {
                "score": None,
                "factors": [],
                "zone": "Neutral"
            }
        }

    # 🛡️ Blindaje adicional ante claves faltantes
    result.setdefault("current_price", "No disponible")
    result.setdefault("structure_1min", None)
    result.setdefault("active_kill_zone", None)
    result.setdefault("premium_discount_zones", None)
    result.setdefault("reaction_levels", [])
    result.setdefault("recommendation", None)
    result.setdefault("swing_points", [])
    result.setdefault("order_blocks", [])
    result.setdefault("fair_value_gaps", [])
    result.setdefault("liquidity_sweeps", [])
    result.setdefault("confluence", {
        "score": None,
        "factors": [],
        "zone": "Neutral"
    })

    # ✅ Render final
    return render_template("report.html", **result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
