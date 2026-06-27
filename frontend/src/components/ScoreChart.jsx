import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ScoreChart({ breakdown }) {
  const data = [
    { name: 'Keyword', score: breakdown['Keyword Match'] ?? 0 },
    { name: 'Skills', score: breakdown['Skills Match'] ?? 0 },
    { name: 'Projects', score: breakdown['Projects Relevance'] ?? 0 },
    { name: 'Impact', score: breakdown['Impact & Quantification'] ?? 0 },
    { name: 'Experience', score: breakdown['Experience Match'] ?? 0 },
    { name: 'Formatting', score: breakdown['Resume Formatting'] ?? 0 },
    { name: 'Grammar', score: breakdown['Grammar & Professional Writing'] ?? 0 },
    { name: 'Action', score: breakdown['Action Verbs'] ?? 0 },
    { name: 'Education', score: breakdown['Education'] ?? 0 },
    { name: 'Links', score: breakdown['Link Validation'] ?? 0 },
    { name: 'Complete', score: breakdown['Resume Completeness'] ?? 0 }
  ];

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-500 mb-4 uppercase tracking-wider">Weighted ATS Diagnostics</h3>
      <div className="h-[420px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart layout="vertical" data={data} margin={{ top: 10, right: 30, left: 100, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 12, fill: '#64748b' }} />
            <YAxis type="category" dataKey="name" tick={{ fontSize: 12, fill: '#334155' }} width={100} />
            <Tooltip formatter={(value) => [`${Number(value).toFixed(0)}%`, 'Score']} />
            <Bar dataKey="score" fill="#4338ca" radius={[0, 6, 6, 0]} barSize={18} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
