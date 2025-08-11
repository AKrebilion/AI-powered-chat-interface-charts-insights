// src/App.jsx
import React, { useState } from 'react';
import axios from 'axios';
import ChartDisplay from './components/ChartDisplay';

function App() {
  const [question, setQuestion] = useState('');
  const [sql, setSQL] = useState('');
  const [charts, setCharts] = useState([]); // Store multiple charts
  const [summary, setSummary] = useState('');
  const [error, setError] = useState('');

  const handleAsk = async () => {
    if (!question.trim()) return;
    setError('');
    try {
      const res = await axios.post('http://localhost:5000/ask', { question });
      setSQL(res.data.sql);
      setSummary(res.data.summary);
      setCharts(res.data.charts || []); // Array of chart objects
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred.');
      setSQL('');
      setSummary('');
      setCharts([]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Keydraft Chat Insights</h1>

        {/* Question input */}
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            className="w-full border p-2 rounded shadow"
            placeholder="Ask a question (e.g., Top 5 products by sales)"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            onClick={handleAsk}
          >
            Ask
          </button>
        </div>

        {/* Error display */}
        {error && (
          <div className="bg-red-100 text-red-800 p-3 rounded mb-4">
            <strong>Error:</strong> {error}
            {sql && <div className="mt-2 text-sm">SQL: {sql}</div>}
          </div>
        )}

        {/* SQL display */}
        {!error && sql && (
          <div className="bg-green-50 border p-4 rounded mb-4">
            <p className="text-sm text-gray-600 mb-1">Generated SQL:</p>
            <code className="block text-sm text-gray-800 bg-white p-2 rounded border">
              {sql}
            </code>
          </div>
        )}

        {/* Summary display */}
        {!error && summary && (
          <div className="bg-yellow-50 border p-4 rounded mb-4">
            <p className="text-sm text-gray-600 mb-1">Summary:</p>
            <p className="text-gray-800">{summary}</p>
          </div>
        )}

        {/* Render multiple charts */}
        {!error && charts.length > 0 && (
          <div className="space-y-8">
            {charts.map((chart, idx) => (
              <ChartDisplay
                key={idx}
                data={chart.data}
                columns={chart.columns}
                chartType={chart.chartType}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
