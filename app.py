from flask import Flask, render_template, request
import yfinance as yf
from datetime import datetime, timedelta
import pytz
from strategy.IntegratedSMCStrategy import SMCAnalysis

app = Flask(__name__)

def get_kill_zone_info(current_time):
    ny_tz = pytz.timezone('America/New_York')
    current_time_ny = current_time.astimezone(ny_tz)
    hour = current_time_ny.hour
    minute = current_time_ny.minute
    if 2 <= hour < 5:  # Londres
        remaining = (5 - hour - 1) * 60 + (60 - minute)
        return {"active": True, "name": "London", "priority": "medium", "remaining": remaining}
    elif 8 <= hour < 11:  # Nueva York
        remaining = (11 - hour - 1) * 60 + (60 - minute)
        return {"active": True, "name": "New York", "priority": "high", "remaining": remaining}
    else:
        return {"active": False, "name": None, "priority": None, "remaining": None}

@app.route('/', methods=['GET', 'POST'])
def analyze():
    pair = "EURUSD=X"
    timeframe = "15m"
    confluencia_min = 70
    error = None
    
    if request.method == 'POST':
        pair = request.form.get('pair', 'EURUSD=X')
        timeframe = request.form.get('timeframe', '15m')
        confluencia_min = float(request.form.get('confluencia_min', 70))

    try:
        ohlc = yf.download(pair, period='5d', interval=timeframe)
        ohlc.columns = ohlc.columns.str.lower()
        if ohlc.empty:
            error = "No se recibieron datos válidos"
            return render_template('report.html', error=error)
        
        analysis = SMCAnalysis(ohlc, timeframe)
        results = analysis.analyze()
        kill_zone = get_kill_zone_info(datetime.now(pytz.timezone('America/Santiago')))
        
        price_times = ohlc.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        price_data = ohlc['close'].tolist()
        levels = analysis.get_levels()
        # Formatear niveles para el gráfico
        chart_levels = [{'x': level['time'].strftime('%Y-%m-%d %H:%M:%S'), 'y': level['price']} 
                       for level in levels if 'time' in level]
        
        return render_template('report.html',
                             pair=pair.replace('=X', ''),
                             timeframe=timeframe,
                             confluencia_min=confluencia_min,
                             results=results,
                             kill_zone=kill_zone,
                             price_times=price_times,
                             price_data=price_data,
                             chart_levels=chart_levels,
                             current_time=datetime.now(pytz.timezone('America/Santiago')).strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        error = f"Error al procesar el análisis: {e}"
        return render_template('report.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
