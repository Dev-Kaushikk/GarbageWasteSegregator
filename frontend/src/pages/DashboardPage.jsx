/**
 * Dashboard Page
 * AI-Based Smart Garbage Waste Segregator
 * Real-time analytics loaded directly from SQLite database.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ScanLine,
  Layers,
  Recycle,
  Leaf,
  AlertTriangle,
  Clock,
  ArrowUpRight,
  Inbox,
  Activity,
  Calendar,
  Sparkles,
  Camera,
  CheckCircle2,
  TrendingUp
} from 'lucide-react';
import { getAnalytics } from '../services/api';
import { DISPOSAL_BADGES } from '../utils/constants';

const DashboardPage = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getAnalytics()
      .then((res) => {
        setData(res);
      })
      .catch((err) => {
        setError('Failed to fetch analytics from SQLite database.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="py-16 text-center space-y-3">
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs text-slate-500 font-medium">Loading session analytics from database...</p>
      </div>
    );
  }

  const isEmpty = !data || data.total_images === 0;

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white border border-slate-200 rounded-xl p-5 sm:p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">Analytics & Waste Dashboard</h1>
            <span className="text-[11px] px-2.5 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 rounded-full font-semibold">
              Live SQLite Data
            </span>
          </div>
          <p className="text-xs text-slate-500">
            Real-time material streams, circular recovery metrics, and audit records from local persistent storage.
          </p>
        </div>

        <button
          onClick={() => navigate('/detect')}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white rounded-lg text-xs font-semibold shadow-xs flex items-center gap-1.5 self-start sm:self-auto transition-colors"
        >
          <ScanLine className="w-3.5 h-3.5" />
          <span>New Detection Session</span>
        </button>
      </div>

      {isEmpty ? (
        /* Meaningful Empty State */
        <div className="bg-white border border-slate-200 rounded-xl p-12 text-center space-y-4 shadow-xs">
          <div className="w-14 h-14 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-400 mx-auto">
            <Inbox className="w-7 h-7" />
          </div>
          <div className="max-w-md mx-auto">
            <h3 className="font-bold text-base text-slate-900 mb-1">No Detection Records Yet</h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-5">
              The SQLite database is initialized and ready. Upload an image or run detection with one of the quick test sample images to generate real analytics.
            </p>
            <button
              onClick={() => navigate('/detect')}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs inline-flex items-center gap-1.5 transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Run First Detection</span>
            </button>
          </div>
        </div>
      ) : (
        <>
          {/* Top Metric Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-1 hover:border-slate-300 transition-colors">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-[10px] uppercase font-bold tracking-wider">Total Images</span>
                <Camera className="w-3.5 h-3.5 text-slate-400" />
              </div>
              <div className="text-2xl font-black text-slate-900">{data.total_images}</div>
              <span className="text-[11px] text-slate-500 block">Analyzed sessions</span>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-1 hover:border-slate-300 transition-colors">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-[10px] uppercase font-bold tracking-wider">Total Objects</span>
                <Layers className="w-3.5 h-3.5 text-blue-500" />
              </div>
              <div className="text-2xl font-black text-blue-600">{data.total_objects}</div>
              <span className="text-[11px] text-slate-500 block">Localizations</span>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-1 hover:border-slate-300 transition-colors">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-[10px] uppercase font-bold tracking-wider">Recyclable</span>
                <Recycle className="w-3.5 h-3.5 text-emerald-500" />
              </div>
              <div className="text-2xl font-black text-emerald-600">{data.recycle_count}</div>
              <span className="text-[11px] text-slate-500 block">Items diverted</span>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-1 hover:border-slate-300 transition-colors">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-[10px] uppercase font-bold tracking-wider">Compostable</span>
                <Leaf className="w-3.5 h-3.5 text-green-600" />
              </div>
              <div className="text-2xl font-black text-green-700">{data.compost_count}</div>
              <span className="text-[11px] text-slate-500 block">Organic matter</span>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-1 hover:border-slate-300 transition-colors">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-[10px] uppercase font-bold tracking-wider">Special Disposal</span>
                <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
              </div>
              <div className="text-2xl font-black text-amber-600">{data.special_disposal_count}</div>
              <span className="text-[11px] text-slate-500 block">Soft/Hazard/RDF</span>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-1 hover:border-slate-300 transition-colors">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-[10px] uppercase font-bold tracking-wider">Recovery Rate</span>
                <TrendingUp className="w-3.5 h-3.5 text-blue-600" />
              </div>
              <div className="text-2xl font-black text-slate-900">{data.avg_recyclability_rate}%</div>
              <span className="text-[11px] text-slate-500 block">Mean stream rate</span>
            </div>
          </div>

          {/* Charts & Breakdown Row */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
            {/* Class Frequency Distribution (7 cols) */}
            <div className="lg:col-span-7 bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-3.5">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <h3 className="font-bold text-sm text-slate-900">Detected Waste Category Frequency</h3>
                <span className="text-[10px] text-slate-400 font-mono">SQLite Object Audit</span>
              </div>

              {data.class_distribution.length === 0 ? (
                <p className="text-xs text-slate-400 py-6 text-center">No class distribution recorded yet.</p>
              ) : (
                <div className="space-y-2.5">
                  {data.class_distribution.map((item) => {
                    const maxCount = Math.max(...data.class_distribution.map((c) => c.count)) || 1;
                    const percent = Math.round((item.count / maxCount) * 100);
                    return (
                      <div key={item.class_name} className="space-y-1">
                        <div className="flex justify-between text-xs font-medium">
                          <span className="text-slate-700 font-semibold">{item.name}</span>
                          <span className="text-slate-500 font-mono text-[11px]">{item.count} items ({Math.round((item.count / (data.total_objects || 1)) * 100)}%)</span>
                        </div>
                        <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-500"
                            style={{ width: `${percent}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Disposal Recommendation Distribution (5 cols) */}
            <div className="lg:col-span-5 bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-3.5">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <h3 className="font-bold text-sm text-slate-900">Disposal Actions Breakdown</h3>
                <span className="text-[10px] text-slate-400 font-mono">Rule-Based Output</span>
              </div>

              {data.disposal_distribution.length === 0 ? (
                <p className="text-xs text-slate-400 py-6 text-center">No disposal actions recorded yet.</p>
              ) : (
                <div className="space-y-2.5">
                  {data.disposal_distribution.map((d) => {
                    const badge = DISPOSAL_BADGES[d.action] || DISPOSAL_BADGES['General waste'];
                    const share = Math.round((d.count / (data.total_objects || 1)) * 100);
                    return (
                      <div
                        key={d.action}
                        className="p-3 rounded-lg border border-slate-100 bg-slate-50/70 hover:bg-slate-50 transition-colors space-y-1.5"
                      >
                        <div className="flex items-center justify-between">
                          <span className={`px-2 py-0.5 rounded text-xs font-bold border ${badge.bg} ${badge.text} ${badge.border}`}>
                            {badge.icon} {badge.label}
                          </span>
                          <span className="text-xs font-bold text-slate-800">{d.count} objects <span className="text-[11px] text-slate-400 font-normal">({share}%)</span></span>
                        </div>
                        <div className="w-full bg-slate-200/80 h-1.5 rounded-full overflow-hidden">
                          <div
                            className="bg-emerald-500 h-full rounded-full transition-all duration-500"
                            style={{ width: `${share}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          {/* Recent Detection Activity Feed */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-3.5">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-blue-600" />
                <h3 className="font-bold text-sm text-slate-900">Recent Detection Activity</h3>
              </div>
              <button
                onClick={() => navigate('/history')}
                className="text-xs text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-1 transition-colors"
              >
                <span>View Full History</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead>
                  <tr className="text-slate-400 font-semibold uppercase text-[10px] border-b border-slate-100">
                    <th className="pb-2.5">Session ID</th>
                    <th className="pb-2.5">Timestamp</th>
                    <th className="pb-2.5">Filename</th>
                    <th className="pb-2.5">Objects</th>
                    <th className="pb-2.5">Primary Action</th>
                    <th className="pb-2.5">Recyclability</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-medium">
                  {data.recent_activity.map((session) => (
                    <tr
                      key={session.id}
                      onClick={() => navigate('/history')}
                      className="hover:bg-slate-50 cursor-pointer transition-colors"
                    >
                      <td className="py-2.5 font-mono text-blue-600">{session.id.substring(0, 18)}...</td>
                      <td className="py-2.5 text-slate-500">
                        {session.created_at ? new Date(session.created_at).toLocaleString() : 'N/A'}
                      </td>
                      <td className="py-2.5 font-semibold text-slate-800 truncate max-w-[140px]">
                        {session.filename}
                      </td>
                      <td className="py-2.5">
                        <span className="px-2 py-0.5 bg-slate-100 rounded text-slate-700 font-bold text-[11px]">
                          {session.total_objects} items
                        </span>
                      </td>
                      <td className="py-2.5 text-slate-700">{session.primary_disposal}</td>
                      <td className="py-2.5 font-bold text-emerald-600">{session.recyclability_rate}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default DashboardPage;

