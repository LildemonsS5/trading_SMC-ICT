from flask import Flask, request, render_template, redirect
from strategy.IntegratedSMCStrategy import IntegratedSMCStrategy, TradingConfig

app = Flask(__name__)

# 🔧 Configuración de estrategia
config = TradingConfig()
strategy = IntegratedSMCStrategy(api_key="TU_API_KEY", config=config)

# 🌐 Ruta principal redirige a /analyze
@app.route("/")
def home():
    return redirect("/analyze")

# 📊 Ruta de análisis con símbolo configurable
@app.route("/analyze")
def analyze_route():
    symbol = request.args.get("symbol", "EURUSD")
    result = strategy.analyze_symbol(symbol)

    # 🛡️ Validación contra errores internos
    if "error" in result:
        return f"<h1>Error en el análisis</h1><p>{result['error']}</p>"

    # 🔍 Validación de claves obligatorias
    expected_keys = [
        "symbol", "analysis_time", "current_price", "structure_1min",
        "active_kill_zone", "premium_discount_zones",
        "reaction_levels", "recommendation"
    ]

    missing_keys = [key for key in expected_keys if key not in result]

    if missing_keys:
        return (
            f"<h1>Faltan datos en el análisis</h1>"
            f"<p>Claves faltantes: {', '.join(missing_keys)}</p>"
        )

    # ✅ Render seguro con claves existentes
    return render_template("report.html", 
        symbol=result.get("symbol", "No disponible"),
        analysis_time=result.get("analysis_time", "No disponible"),
        current_price=result.get("current_price", "No disponible"),
        structure_1min=result.get("structure_1min", "Sin estructura definida"),
        active_kill_zone=result.get("active_kill_zone", None),
        premium_discount_zones=result.get("premium_discount_zones", []),
        reaction_levels=result.get("reaction_levels", []),
        recommendation=result.get("recommendation", "Sin recomendación disponible")
    )

if __name__ == "__main__":
    app.run(debug=True)
