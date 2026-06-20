import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ScoreChart({ breakdown }) {
  const data = [
    { name: 'Keywords', score: breakdown.keywords, max: 35 },
    { name: 'Sections', score: breakdown.sections, max: 20 },
    { name: 'Formatting', score: breakdown.formatting, max: 15 },
    { name: 'Metrics', score: breakdown.experience, max: 15 },
    { name: 'Grammar', score: breakdown.grammar, max: 15 },
  ];

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-500 mb-4 uppercase tracking-wider">Score Distribution</h3>
      <div className="h-48">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#64748b' }} />
            <YAxis domain={[0, 'auto']} tick={{ fontSize: 12, fill: '#64748b' }} />
            <Tooltip />
            <Bar dataKey="score" fill="#4f46e5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}