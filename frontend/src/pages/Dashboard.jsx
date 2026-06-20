import React, { useState } from 'react';
import { analyzeResume } from '../services/api';
import ScoreChart from '../components/ScoreChart';
import Heatmap from '../components/Heatmap';
import { Upload, CheckCircle2, XCircle, AlertTriangle, FileText, Sparkles } from 'lucide-react';

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleSubmit = async () => {
    if (!file) return alert('Please upload a resume file first.');
    setLoading(true);
    try {
      const data = await analyzeResume(file, jobDesc);
      setResults(data);
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getScoreBadgeColor = (score) => {
    if (score >= 90) return 'text-emerald-600 border-emerald-200 bg-emerald-50';
    if (score >= 70) return 'text-amber-600 border-amber-200 bg-amber-50';
    return 'text-rose-600 border-rose-200 bg-rose-50';
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 pb-12">
      {/* Navbar header */}
      <header className="bg-white border-b border-slate-200 py-4 shadow-sm mb-8">
        <div className="max-w-7xl mx-auto px-4 flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-indigo-600 animate-pulse" />
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Smart ATS Analyzer</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* LEFT COLUMN: CONTROL INPUTS */}
        <div className="space-y-6 lg:col-span-1">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
            <h2 className="text-base font-bold mb-4 text-slate-900 flex items-center gap-2">
              <FileText className="w-5 h-5 text-indigo-500" /> Upload Profile
            </h2>
            
            {/* Input area upload component */}
            <div className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:border-indigo-500 transition-all cursor-pointer relative bg-slate-50">
              <input type="file" onChange={handleFileChange} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" accept=".pdf,.docx" />
              <Upload className="w-8 h-8 mx-auto text-slate-400 mb-2" />
              <p className="text-sm font-semibold text-slate-600">{file ? file.name : "Drop resume here or browse"}</p>
              <p className="text-xs text-slate-400 mt-1">Supports PDF & DOCX profiles</p>
            </div>

            {/* Job Criteria text submission container */}
            <div className="mt-5">
              <label className="block text-xs font-bold uppercase text-slate-500 tracking-wider mb-2">Target Job Description</label>
              <textarea 
                rows="6" 
                value={jobDesc}
                onChange={(e) => setJobDesc(e.target.value)}
                placeholder="Paste the target application requirements here to verify keywords..."
                className="w-full text-sm p-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-slate-50"
              />
            </div>

            <button 
              onClick={handleSubmit} 
              disabled={loading}
              className="w-full mt-5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white font-semibold py-3 rounded-xl shadow transition-colors"
            >
              {loading ? "Analyzing Document Framework..." : "Analyze Resume"}
            </button>
          </div>
        </div>

        {/* RIGHT COLUMN: RECHARTS & DIAGNOSTICS DISPLAY FEED */}
        <div className="lg:col-span-2">
          {!results ? (
            <div className="bg-white border-2 border-dashed border-slate-200 rounded-2xl h-96 flex flex-col items-center justify-center text-slate-400 p-6 text-center">
              <FileText className="w-12 h-12 stroke-1 mb-2 text-slate-300" />
              <p className="text-sm font-medium">No diagnostic reports compiled yet.</p>
              <p className="text-xs text-slate-400 mt-0.5">Upload artifacts on the left control panel to launch analysis.</p>
            </div>
          ) : (
            <div className="space-y-6 animate-fadeIn">
              
              {/* Score breakdown metrics display */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className={`border p-6 rounded-2xl shadow-sm text-center font-bold flex flex-col justify-center items-center ${getScoreBadgeColor(results.score)}`}>
                  <span className="text-xs uppercase tracking-wider opacity-80">ATS Score</span>
                  <span className="text-6xl mt-1">{results.score}<span className="text-2xl font-normal text-slate-400">/100</span></span>
                </div>
                <div className="md:col-span-2">
                  <ScoreChart breakdown={results.breakdown} />
                </div>
              </div>

              {/* Layout structure checks presence array container */}
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <h3 className="text-sm font-bold mb-4 text-slate-900 tracking-wide uppercase text-slate-500">Component Validation Matrix</h3>
                <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
                  {Object.entries(results.sections).map(([name, present]) => (
                    <div key={name} className={`flex items-center gap-2 p-3 rounded-xl border text-xs font-bold ${present ? 'bg-emerald-50 border-emerald-100 text-emerald-800' : 'bg-rose-50 border-rose-100 text-rose-800'}`}>
                      {present ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <XCircle className="w-4 h-4 text-rose-500" />}
                      <span>{name}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Heatmap & Keywords analysis component anchor */}
              <Heatmap keywords={results.keyword_heatmap} />

              {/* Review Improvement suggestions list feed */}
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <h3 className="text-md font-bold mb-3 text-slate-900">Optimization Strategy Recommendations</h3>
                <div className="space-y-2">
                  {results.suggestions.map((suggestion, idx) => (
                    <div key={idx} className="flex gap-3 bg-slate-50 p-3 rounded-xl border border-slate-100">
                      <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                      <p className="text-xs font-semibold text-slate-600 leading-relaxed">{suggestion}</p>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}
        </div>
      </main>
    </div>
  );
}