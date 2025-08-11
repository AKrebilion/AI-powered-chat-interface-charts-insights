import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, Legend, PieChart, Pie, Cell, LineChart, Line
} from 'recharts';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#8dd1e1', '#a4de6c', '#d0ed57', '#8884d8'];

function isNumericColumn(data, col) {
  return data.every(row => typeof row[col] === 'number' && !isNaN(row[col]));
  // return data.every(row => !isNaN(Number(row[col])));
}

const ChartDisplay = ({ data, columns, chartType }) => {
  if (!data || data.length === 0 || columns.length < 2) return null;

  const xKey = columns[0];
  // Try to find a numeric column for yKey
  let yKey = columns.find(col => isNumericColumn(data, col) && col !== xKey);
  if (!yKey) return <div className="text-gray-500">No numeric data to plot.</div>;

  // Make chart type case-insensitive
  const type = chartType?.toLowerCase();

  console.log("Rendering chart type:", type);
  console.log("X Key:", xKey);
  console.log("Y Key:", yKey);
  console.log("Sample Data:", data?.[0]);

  return (
    <div className="p-4 border rounded-lg shadow bg-white">
      <h2 className="text-lg font-semibold mb-2">Chart</h2>
      <ResponsiveContainer width="100%" height={300}>
        {type === 'pie' ? (
          <PieChart>
            <Pie
              data={data}
              dataKey={yKey}
              nameKey={xKey}
              cx="50%"
              cy="50%"
              outerRadius={100}
              label
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        ) : type === 'line' ? (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xKey} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey={yKey} stroke="#8884d8" />
          </LineChart>
        ) : (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xKey} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey={yKey} fill="#8884d8" />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
};

export default ChartDisplay;
