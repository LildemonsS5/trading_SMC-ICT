from flask import Flask, request, render_templates
from strategy.IntegratedSMCStrategy import IntegratedSMCStrategy, TradingConfig

app = Flask(__name__)
config = TradingConfig()
strategy = IntegratedSMCStrategy(api_key="TU_API_KEY", config=config)

@app.route("/analyze")
def analyze_route():
    symbol = request.args.get("symbol", "EURUSD")
    result = strategy.analyze_symbol(symbol)
    return render_templates("report.html", 
                           symbol=result["symbol"],
                           analysis_time=result["analysis_time"],
                           current_price=result["current_price"],
                           structure=result["structure_1min"],
                           kill_zone=result["active_kill_zone"],
                           premium_discount=result["premium_discount_zones"],
                           reaction_levels=result["reaction_levels"],
                           recommendation=result["recommendation"])
