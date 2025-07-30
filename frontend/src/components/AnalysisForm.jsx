
import React, { useState } from 'react';

function AnalysisForm({ setAnalysisResult, setLoading, setError }) {
  const [symbol, setSymbol] = useState('');
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'; // Usar variable de entorno o localhost para desarrollo

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: symbol.toUpperCase() }),
      });
      if (!response.ok) {
        throw new Error('Error en el análisis');
      }
      const data = await response.json();
      setAnalysisResult(data);
    } catch (err) {
      setError('No se pudo realizar el análisis. Por favor, intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-8">
      <h2 className="text-xl font-semibold mb-4">Analizar Par de Divisas</h2>
      <div className="flex space-x-4">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Ej. EURUSD"
          className="flex-1 p-2 border rounded"
        />
        <button
          onClick={handleSubmit}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Analizar
        </button>
      </div>
    </div>
  );
}

export default AnalysisForm;
