import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  ComposedChart,
} from 'recharts';
import './ClimateChart.css';

const PredictionChart = ({ data, title }) => {
  return (
    <div className="chart-container">
      <h3 className="chart-title">{title}</h3>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(226, 232, 240, 0.1)" />
          <XAxis
            dataKey="date"
            stroke="#e2e8f0"
            tick={{ fontSize: 12, fill: '#e2e8f0' }}
          />
          <YAxis stroke="#e2e8f0" tick={{ fontSize: 12, fill: '#e2e8f0' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(17, 16, 28, 0.95)',
              border: '1px solid rgba(16, 185, 129, 0.5)',
              borderRadius: '8px',
              color: '#e2e8f0',
            }}
          />
          <Legend wrapperStyle={{ color: '#e2e8f0' }} />
          <Area
            type="monotone"
            dataKey="upper_bound"
            stackId="1"
            stroke="none"
            fill="#10b981"
            fillOpacity={0.2}
            name="Confidence Interval"
          />
          <Area
            type="monotone"
            dataKey="lower_bound"
            stackId="1"
            stroke="none"
            fill="#11101C"
            fillOpacity={1}
          />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#10b981"
            strokeWidth={3}
            dot={{ fill: '#10b981', r: 4 }}
            activeDot={{ r: 6, fill: '#34d399' }}
            name="Predicted Value"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionChart;
