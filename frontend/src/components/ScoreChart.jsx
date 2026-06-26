import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ScoreChart({ breakdown }) {
  const data = [
    { name: 'Keywords', score: breakdown.Keywords },
    { name: 'Sections', score: breakdown.Sections },
    { name: 'Contact', score: breakdown.Contact },
    { name: 'Layout', score: breakdown.Layout },
    { name: 'Pagination', score: breakdown.Pagination },
    { name: 'Dates', score: breakdown.Dates },
    { name: 'Actions', score: breakdown.Actions },
    { name: 'Metrics', score: breakdown.Metrics }
  ];

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-500 mb-4 uppercase tracking-wider">8-Vector Resume Diagnostics</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748b' }} interval={0} />
            <YAxis domain={[0, 12.5]} tick={{ fontSize: 12, fill: '#64748b' }} />
            <Tooltip formatter={(value) => [`${Number(value).toFixed(2)}/12.5`, 'Score']} />
            <Bar dataKey="score" fill="#4338ca" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
