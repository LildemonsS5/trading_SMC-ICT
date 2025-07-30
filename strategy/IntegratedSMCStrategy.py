import pandas as pd
import numpy as np

class SMCAnalysis:
    def __init__(self, ohlc, timeframe):
        self.ohlc = ohlc
        self.timeframe = timeframe
        self.swing_points = self.detect_swing_points()
        self.order_blocks = self.detect_order_blocks()
        self.fvg = self.detect_fvg()
        self.liquidity = self.detect_liquidity()
        self.trend = self.detect_trend()
        self.bos = self.detect_bos()
        self.choch = self.detect_choch()

    def detect_swing_points(self):
        swings = []
        for i in range(2, len(self.ohlc) - 2):
            if (self.ohlc['high'].iloc[i] > self.ohlc['high'].iloc[i-1] and 
                self.ohlc['high'].iloc[i] > self.ohlc['high'].iloc[i+1]):
                swings.append({'time': self.ohlc.index[i], 'price': self.ohlc['high'].iloc[i], 'type': 'high'})
            elif (self.ohlc['low'].iloc[i] < self.ohlc['low'].iloc[i-1] and 
                  self.ohlc['low'].iloc[i] < self.ohlc['low'].iloc[i+1]):
                swings.append({'time': self.ohlc.index[i], 'price': self.ohlc['low'].iloc[i], 'type': 'low'})
        return swings

    def detect_order_blocks(self):
        ob_list = []
        for i in range(2, len(self.ohlc) - 1):
            if (self.ohlc['close'].iloc[i-1] < self.ohlc['open'].iloc[i-1] and  # Vela bajista
                self.ohlc['low'].iloc[i] < self.ohlc['low'].iloc[i-1] and      # Rompe el mínimo
                self.ohlc['close'].iloc[i] > self.ohlc['open'].iloc[i]):       # Movimiento alcista
                ob_list.append({
                    'time': self.ohlc.index[i-1],
                    'price': self.ohlc['high'].iloc[i-1],
                    'type': 'bullish',
                    'mitigated': False
                })
        return ob_list

    def detect_fvg(self):
        fvg_list = []
        for i in range(1, len(self.ohlc) - 1):
            if self.ohlc['high'].iloc[i-1] < self.ohlc['low'].iloc[i+1]:  # FVG alcista
                fvg_list.append({
                    'time': self.ohlc.index[i],
                    'top': self.ohlc['high'].iloc[i-1],
                    'bottom': self.ohlc['low'].iloc[i+1],
                    'type': 'bullish',
                    'mitigated': False
                })
            elif self.ohlc['low'].iloc[i-1] > self.ohlc['high'].iloc[i+1]:  # FVG bajista
                fvg_list.append({
                    'time': self.ohlc.index[i],
                    'top': self.ohlc['low'].iloc[i-1],
                    'bottom': self.ohlc['high'].iloc[i+1],
                    'type': 'bearish',
                    'mitigated': False
                })
        return fvg_list

    def detect_liquidity(self):
        liquidity = []
        for swing in self.swing_points:
            if swing['type'] == 'low':
                liquidity.append({
                    'time': swing['time'],
                    'price': swing['price'],
                    'type': 'buy_liquidity'
                })
        return liquidity

    def detect_trend(self):
        last_swings = self.swing_points[-4:]
        highs = [s['price'] for s in last_swings if s['type'] == 'high']
        lows = [s['price'] for s in last_swings if s['type'] == 'low']
        if len(highs) >= 2 and len(lows) >= 2:
            if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
                return 'BULLISH'
            elif highs[-1] < highs[-2] and lows[-1] < lows[-2]:
                return 'BEARISH'
        return 'SIDEWAYS'

    def detect_bos(self):
        last_swings = self.swing_points[-4:]
        highs = [s['price'] for s in last_swings if s['type'] == 'high']
        if len(highs) >= 2 and self.ohlc['high'].iloc[-1] > max(highs):
            return True
        return False

    def detect_choch(self):
        return False  # Simplificado para el ejemplo

    def calculate_confluence(self, level):
        score = 0
        if level['source'] == 'Order Block':
            score += 30
        if level['source'] == 'Fair Value Gap':
            score += 20
        if level['source'] == 'Liquidity':
            score += 20
        if level['zone'] == 'discount' and self.trend == 'BULLISH':
            score += 10
        return score

    def get_levels(self):
        levels = []
        current_price = self.ohlc['close'].iloc[-1]
        equilibrium = (max([s['price'] for s in self.swing_points[-10:]]) + 
                       min([s['price'] for s in self.swing_points[-10:]])) / 2
        zone = 'discount' if current_price < equilibrium else 'premium'

        for ob in self.order_blocks[:1]:
            if not ob['mitigated']:
                levels.append({
                    'time': ob['time'],
                    'signal': 'BUY' if ob['type'] == 'bullish' else 'SELL',
                    'price': ob['price'],
                    'zone': f"{ob['price'] - 0.0005:.5f} - {ob['price'] + 0.0005:.5f}",
                    'source': 'Order Block',
                    'reason': f"{ob['type'].capitalize()} Order Block sin mitigar, confluencia con FVG y liquidez",
                    'confluence': self.calculate_confluence({'source': 'Order Block', 'zone': zone}),
                    'pips': abs(current_price - ob['price']) * 10000
                })
        for fvg in self.fvg[:1]:
            if not fvg['mitigated']:
                levels.append({
                    'time': fvg['time'],
                    'signal': 'BUY' if fvg['type'] == 'bullish' else 'SELL',
                    'price': (fvg['top'] + fvg['bottom']) / 2,
                    'zone': f"{fvg['bottom']:.5f} - {fvg['top']:.5f}",
                    'source': 'Fair Value Gap',
                    'reason': f"FVG {fvg['type']} no mitigado en {self.timeframe}",
                    'confluence': self.calculate_confluence({'source': 'Fair Value Gap', 'zone': zone}),
                    'pips': abs(current_price - (fvg['top'] + fvg['bottom']) / 2) * 10000
                })
        for liq in self.liquidity[:1]:
            levels.append({
                'time': liq['time'],
                'signal': 'BUY',
                'price': liq['price'],
                'zone': f"{liq['price'] - 0.0005:.5f} - {liq['price'] + 0.0005:.5f}",
                'source': 'Liquidity',
                'reason': "Acumulación de liquidez en mínimos estructurales",
                'confluence': self.calculate_confluence({'source': 'Liquidity', 'zone': zone}),
                'pips': abs(current_price - liq['price']) * 10000
            })
        return sorted(levels, key=lambda x: x['confluence'], reverse=True)

    def analyze(self):
        current_price = self.ohlc['close'].iloc[-1]
        high_range = max([s['price'] for s in self.swing_points[-10:]]) if self.swing_points else self.ohlc['high'].iloc[-1]
        low_range = min([s['price'] for s in self.swing_points[-10:]]) if self.swing_points else self.ohlc['low'].iloc[-1]
        equilibrium = (high_range + low_range) / 2
        zone = 'discount' if current_price < equilibrium else 'premium'
        
        levels = self.get_levels()
        avg_confluence = sum(l['confluence'] for l in levels) / max(1, len(levels)) if levels else 0
        recommendation = {
            'signal': levels[0]['signal'] if levels else 'NEUTRAL',
            'confidence': max(l['confluence'] for l in levels) if levels else 0,
            'zone': levels[0]['zone'] if levels else None
        }
        
        return {
            'price': current_price,
            'trend': self.trend,
            'bos': self.bos,
            'choch': self.choch,
            'zone': zone,
            'equilibrium': equilibrium,
            'range': f"{low_range:.5f} - {high_range:.5f}",
            'levels': levels,
            'avg_confluence': avg_confluence,
            'recommendation': recommendation
        }
