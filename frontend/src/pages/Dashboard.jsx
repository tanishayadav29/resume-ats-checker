import React, { useState } from 'react';
import { analyzeResume } from '../services/api';
import ScoreChart from '../components/ScoreChart';
import Heatmap from '../components/Heatmap';
import { Upload, CheckCircle2, XCircle, AlertTriangle, FileText, Sparkles } from 'lucide-react';

const statusItems = [
  {
    key: 'contact',
    label: 'Contact Verification',
    trueText: 'Email, phone, LinkedIn & GitHub found',
    falseText: 'Missing one or more verified contact links'
  },
  {
    key: 'pagination',
    label: 'Page Boundaries',
    trueText: 'Text density conforms to 1-page standard',
    falseText: 'Document exceeds ideal length or line count'
  },
  {
    key: 'dates',
    label: 'Timeline Formatting',
    trueText: 'Chronological dates use standard enterprise patterns',
    falseText: 'Date segments require better formatting'
  },
  {
    key: 'metrics',
    label: 'Metric Quantification',
    trueText: 'Goal-driven metrics and percentages detected',
    falseText: 'Add quantifiable business impact statements'
  }
];

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

  const getStatusValue = (item) => {
    if (!results) return false;
    if (item.key === 'contact') return results.validation?.contact?.all_valid;
    if (item.key === 'pagination') return results.validation?.pagination?.page_compliant;
    if (item.key === 'dates') return results.validation?.dates?.timeline_compliant;
    if (item.key === 'metrics') return results.validation?.metrics?.has_enough_metrics;
    return false;
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 pb-12">
      <header className="bg-white border-b border-slate-200 py-4 shadow-sm mb-8">
        <div className="max-w-7xl mx-auto px-4 flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-indigo-600 animate-pulse" />
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Smart ATS Analyzer</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="space-y-6 lg:col-span-1">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
            <h2 className="text-base font-bold mb-4 text-slate-900 flex items-center gap-2">
              <FileText className="w-5 h-5 text-indigo-500" /> Upload Resume
            </h2>
            <div className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:border-indigo-500 transition-all cursor-pointer relative bg-slate-50">
              <input type="file" onChange={handleFileChange} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" accept=".pdf,.docx" />
              <Upload className="w-8 h-8 mx-auto text-slate-400 mb-2" />
              <p className="text-sm font-semibold text-slate-600">{file ? file.name : 'Drop resume here or browse'}</p>
              <p className="text-xs text-slate-400 mt-1">Supports PDF & DOCX profiles</p>
            </div>
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
              {loading ? 'Analyzing Document Framework...' : 'Analyze Resume'}
            </button>
          </div>
        </div>

        <div className="lg:col-span-2 space-y-6">
          {!results ? (
            <div className="bg-white border-2 border-dashed border-slate-200 rounded-2xl h-96 flex flex-col items-center justify-center text-slate-400 p-6 text-center">
              <FileText className="w-12 h-12 stroke-1 mb-2 text-slate-300" />
              <p className="text-sm font-medium">No diagnostic reports compiled yet.</p>
              <p className="text-xs text-slate-400 mt-0.5">Upload artifacts on the left control panel to launch analysis.</p>
            </div>
          ) : (
            <div className="space-y-6 animate-fadeIn">
              <div className="grid grid-cols-1 xl:grid-cols-[320px_1fr] gap-6">
                <div className={`border p-6 rounded-3xl shadow-sm text-center font-bold ${getScoreBadgeColor(results.score)}`}>
                  <span className="text-xs uppercase tracking-wider opacity-80">Overall ATS Index</span>
                  <div className="mt-4 flex items-baseline justify-center gap-2">
                    <span className="text-6xl">{results.score}</span>
                    <span className="text-2xl font-medium text-slate-600">/100</span>
                  </div>
                  <p className="mt-3 text-sm text-slate-600">Enterprise recruiter readiness score based on 8 weighted resume vectors.</p>
                </div>
                <div className="grid grid-cols-1 gap-6">
                  <ScoreChart breakdown={results.breakdown} />
                  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                    <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">Status Summary</h3>
                    <div className="grid grid-cols-1 gap-3">
                      {statusItems.map((item) => {
                        const active = getStatusValue(item);
                        return (
                          <div key={item.key} className={`p-4 rounded-2xl border ${active ? 'border-emerald-200 bg-emerald-50 text-emerald-800' : 'border-rose-200 bg-rose-50 text-rose-800'}`}>
                            <div className="flex items-start gap-3">
                              {active ? <CheckCircle2 className="w-5 h-5 mt-0.5" /> : <XCircle className="w-5 h-5 mt-0.5" />}
                              <div>
                                <p className="text-sm font-semibold">{item.label}</p>
                                <p className="text-xs mt-1 leading-5">{active ? item.trueText : item.falseText}</p>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>

              <Heatmap keywords={results.keyword_heatmap} />

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-slate-900">Detailed Optimization Playbook</h3>
                    <p className="text-sm text-slate-500">Actionable fixes for every dropped vector.</p>
                  </div>
                </div>
                <div className="grid gap-4">
                  {results.detailed_suggestions.map((suggestion, index) => (
                    <div key={index} className="border border-slate-200 rounded-3xl p-5 bg-slate-50">
                      <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
                        <span className="inline-flex items-center rounded-full bg-slate-200 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-700">
                          {suggestion.category}
                        </span>
                        <span className={`inline-flex text-xs font-bold px-3 py-1 rounded-full ${suggestion.impact === 'Critical' ? 'bg-rose-100 text-rose-700' : suggestion.impact === 'High' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'}`}>
                          {suggestion.impact}
                        </span>
                      </div>
                      <div className="space-y-3 text-sm text-slate-700">
                        <div>
                          <p className="font-semibold">Issue Identified</p>
                          <p className="mt-1 text-slate-600">{suggestion.issue}</p>
                        </div>
                        <div className="rounded-2xl bg-white border border-slate-200 p-4">
                          <p className="font-semibold text-slate-800">How to correct it</p>
                          <p className="mt-1 text-slate-600 whitespace-pre-line">{suggestion.fix}</p>
                        </div>
                      </div>
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
