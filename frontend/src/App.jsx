
import React from 'react';
import Header from './components/Header';
import AnalysisForm from './components/AnalysisForm';
import AnalysisResults from './components/AnalysisResults';
import './App.css';

function App() {
  const [analysisResult, setAnalysisResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <AnalysisForm
          setAnalysisResult={setAnalysisResult}
          setLoading={setLoading}
          setError={setError}
        />
        {loading && <p className="text-center text-blue-600">Cargando análisis...</p>}
        {error && <p className="text-center text-red-600">{error}</p>}
        {analysisResult && <AnalysisResults result={analysisResult} />}
      </main>
    </div>
  );
}

export default App;
