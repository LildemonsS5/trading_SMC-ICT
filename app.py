import os
from flask import Flask, request, render_template, redirect
from datetime import datetime
from strategy.IntegratedSMCStrategy import IntegratedSMCStrategy, TradingConfig
import logging
import re

app = Flask(__name__)

# 🔧 Configuración de estrategia
config = TradingConfig()
strategy = IntegratedSMCStrategy(api_key="TU_API_KEY", config=config)

# 🧾 Configuración de logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🌐 Ruta principal redirige a /analyze
@app.route("/")
def home():
    return redirect("/analyze")

# 📊 Ruta de análisis con símbolo configurable
@app.route("/analyze")
def analyze_route():
    # Captura dinámica del símbolo desde formulario POST
    symbol = request.form.get("symbol", "").strip().upper()

    # Validación del formato: solo letras, 6 o 7 caracteres (ej: AUDCAD, BTCUSD)
    if not re.match(r"^[A-Z]{6,7}$", symbol):
        logger.warning(f"Símbolo inválido recibido: {symbol}")
        return (
            f"<h1>Activo inválido</h1>"
            f"<p>El símbolo '{symbol}' no tiene el formato correcto. Usá algo tipo 'AUDCAD'.</p>"
        )

    logger.info(f"Iniciando análisis institucional de {symbol}")

    # Llamada a la estrategia
    result = strategy.analyze_symbol(symbol)

    # 🛡️ Fallback si hay error en el análisis
    if "error" in result:
        logger.error(f"❌ Error en el análisis: {result['error']}")
        result = {
            "symbol": symbol,
            "analysis_time": datetime.utcnow().isoformat(),
            "current_price": "No disponible",
            "structure_1min": "Error",
            "active_kill_zone": None,
            "premium_discount_zones": None,
            "reaction_levels": [],
            "recommendation": f"⚠️ Análisis fallido: {result['error']}"
        }

    # 🔎 Opcional: logueo del resultado para debugging
    logger.info(f"Resultado de {symbol}: {result}")
    
    # Seguirías con el render del HTML usando result
    return render_template("informe.html", **result)

    # ✅ Render institucional del HTML
    return render_template("report.html",
        symbol=result["symbol"],
        analysis_time=result["analysis_time"],
        current_price=result["current_price"],
        structure_1min=result["structure_1min"],
        active_kill_zone=result["active_kill_zone"],
        premium_discount_zones=result["premium_discount_zones"],
        reaction_levels=result["reaction_levels"],
        recommendation=result["recommendation"]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)

