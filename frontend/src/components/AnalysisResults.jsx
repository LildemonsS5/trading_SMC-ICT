
import React from 'react';

function AnalysisResults({ result }) {
  if (result.error) {
    return <div className="text-red-600 text-center">{result.error}</div>;
  }

  const { symbol, current_price, analysis_time, structure_1min, reaction_levels, active_kill_zone, premium_discount_zones, closest_elements, recommendation } = result;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">📊 Análisis SMC + ICT - {symbol}</h2>
      <p className="mb-2">🕒 {analysis_time}</p>
      <p className="mb-4">💰 Precio Actual: {current_price.toFixed(5)}</p>

      <h3 className="text-lg font-semibold mb-2">Contexto ICT</h3>
      <p>🕒 Kill Zone Activa: {active_kill_zone.is_active ? active_kill_zone.name : 'Ninguna'} (Prioridad: {active_kill_zone.priority.toUpperCase()})</p>
      {premium_discount_zones.equilibrium ? (
        <>
          <p>📈 Rango de Trading (15min): {premium_discount_zones.range_low.toFixed(5)} - {premium_discount_zones.range_high.toFixed(5)}</p>
          <p>⚖️ Equilibrio (50%): {premium_discount_zones.equilibrium.toFixed(5)}</p>
          <p>📍 Posición Actual: Zona {current_price > premium_discount_zones.premium_start ? 'PREMIUM (Ventas)' : current_price < premium_discount_zones.discount_end ? 'DISCOUNT (Compras)' : 'EQUILIBRIUM'}</p>
        </>
      ) : (
        <p>📉 Zonas Premium/Discount: No se pudo determinar el rango.</p>
      )}

      <h3 className="text-lg font-semibold mb-2 mt-4">Estructura SMC (1min)</h3>
      <p>Tendencia: {structure_1min.trend.toUpperCase()} | BOS: {structure_1min.bos.toString()} | CHOCH: {structure_1min.choch.toString()} | Señal: {structure_1min.signal || 'N/A'}</p>

      <h3 className="text-lg font-semibold mb-2 mt-4">Elementos Más Cercanos al Precio</h3>
      {closest_elements.closest_order_block ? (
        <p>🔷 Order Block: {closest_elements.closest_order_block.type.toUpperCase()} @ {closest_elements.closest_order_block.price.toFixed(5)} ({(Math.abs(closest_elements.closest_order_block.price - current_price) * 100000).toFixed(1)} pips)</p>
      ) : (
        <p>🔷 Order Block: No encontrado</p>
      )}
      {closest_elements.closest_fvg ? (
        <p>📊 FVG: {closest_elements.closest_fvg.type.toUpperCase()} @ {closest_elements.closest_fvg.price.toFixed(5)} ({(Math.abs(closest_elements.closest_fvg.price - current_price) * 100000).toFixed(1)} pips)</p>
      ) : (
        <p>📊 FVG: No encontrado</p>
      )}
      {closest_elements.closest_liquidity ? (
        <p>💧 Liquidez: {closest_elements.closest_liquidity.type.toUpperCase()} @ {closest_elements.closest_liquidity.price.toFixed(5)} ({(Math.abs(closest_elements.closest_liquidity.price - current_price) * 100000).toFixed(1)} pips)</p>
      ) : (
        <p>💧 Liquidez: No encontrada</p>
      )}
      {closest_elements.closest_sweep ? (
        <p>🌊 Sweep: {closest_elements.closest_sweep.type.toUpperCase()} @ {closest_elements.closest_sweep.level_price.toFixed(5)} ({(Math.abs(closest_elements.closest_sweep.level_price - current_price) * 100000).toFixed(1)} pips)</p>
      ) : (
        <p>🌊 Sweep: No encontrado</p>
      )}
      {closest_elements.market_structure_shift ? (
        <p>🔄 MSS: {closest_elements.market_structure_shift.type} - {closest_elements.market_structure_shift.description}</p>
      ) : (
        <p>🔄 MSS: No detectado</p>
      )}

      <h3 className="text-lg font-semibold mb-2 mt-4">Niveles de Reacción (1min)</h3>
      {reaction_levels.length > 0 ? (
        reaction_levels.map((level, index) => (
          <div key={index} className="mb-2">
            <p>{index + 1}. {level.action} @ {level.price.toFixed(5)} (Confianza: {level.confidence}%)</p>
            <p className="ml-4">Distancia: {level.distance_pips.toFixed(1)} pips | Frescura: {level.freshness.toFixed(1)} min</p>
            <p className="ml-4">Razón: {level.reason}</p>
            {index < reaction_levels.length - 1 && <hr className="my-2" />}
          </div>
        ))
      ) : (
        <p>No se encontraron niveles de reacción cercanos con alta confluencia.</p>
      )}

      <h3 className="text-lg font-semibold mb-2 mt-4">Recomendación Final</h3>
      <p>Acción: {recommendation.action}</p>
      {recommendation.entry_zone && <p>Zona de Entrada: {recommendation.entry_zone}</p>}
      <p>Confianza: {recommendation.confidence}%</p>
      <p>Razón: {recommendation.reason}</p>
    </div>
  );
}

export default AnalysisResults;
