import React from 'react';

export default function Heatmap({ keywords }) {
  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <h3 className="text-md font-bold text-slate-900 mb-1">Resume vs Job Description Heatmap</h3>
      <p className="text-xs text-slate-400 mb-4">Visual matching density tracking based on structural keyword repetitions.</p>
      
      <div className="space-y-3">
        {Object.entries(keywords).map(([keyword, matchPercent]) => (
          <div key={keyword} className="space-y-1">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-slate-700 font-mono bg-slate-100 px-1.5 py-0.5 rounded">{keyword}</span>
              <span className="text-slate-500">{matchPercent}% match</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2.5">
              <div 
                className={`h-2.5 rounded-full transition-all duration-500 ${
                  matchPercent >= 70 ? 'bg-emerald-500' : matchPercent > 0 ? 'bg-amber-400' : 'bg-slate-200'
                }`} 
                style={{ width: `${matchPercent}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}