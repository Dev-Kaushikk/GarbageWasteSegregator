/**
 * Detection History Page
 * AI-Based Smart Garbage Waste Segregator
 * Full session history and details backed by SQLite persistence with pagination.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  History as HistoryIcon,
  Search,
  Filter,
  Trash2,
  Eye,
  Calendar,
  Layers,
  Inbox,
  ArrowRight,
  X,
  ShieldAlert,
  Clock,
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight
} from 'lucide-react';
import {
  getHistory,
  getHistoryDetail,
  deleteHistoryEntry,
  getUploadUrl,
  getResultUrl
} from '../services/api';
import { DISPOSAL_BADGES } from '../utils/constants';

const HistoryPage = () => {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);

  // Pagination State (Defaults to 10 items per page; toggleable to 15)
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  // Filters
  const [search, setSearch] = useState('');
  const [disposalFilter, setDisposalFilter] = useState('');

  // Detail Modal State
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [sessionDetail, setSessionDetail] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const fetchHistoryList = (page = currentPage, limit = pageSize) => {
    setLoading(true);
    const offset = (page - 1) * limit;
    getHistory({ search, disposal: disposalFilter || undefined, limit, offset })
      .then((res) => {
        setHistory(res.history || []);
        setTotalCount(res.total || 0);
      })
      .catch((err) => console.warn('History fetch error', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    setCurrentPage(1);
    fetchHistoryList(1, pageSize);
  }, [disposalFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchHistoryList(1, pageSize);
  };

  const handlePageSizeChange = (newSize) => {
    setPageSize(newSize);
    setCurrentPage(1);
    fetchHistoryList(1, newSize);
  };

  const totalPages = Math.max(1, Math.ceil(totalCount / pageSize));
  const startEntry = totalCount === 0 ? 0 : (currentPage - 1) * pageSize + 1;
  const endEntry = Math.min(currentPage * pageSize, totalCount);

  const goToPage = (page) => {
    if (page < 1 || page > totalPages || page === currentPage) return;
    setCurrentPage(page);
    fetchHistoryList(page, pageSize);
    // Smooth scroll to top of table
    window.scrollTo({ top: 120, behavior: 'smooth' });
  };

  const getPaginationRange = () => {
    const delta = 1;
    const range = [];
    const rangeWithDots = [];
    let l;

    for (let i = 1; i <= totalPages; i++) {
      if (i === 1 || i === totalPages || (i >= currentPage - delta && i <= currentPage + delta)) {
        range.push(i);
      }
    }

    for (let i of range) {
      if (l) {
        if (i - l === 2) {
          rangeWithDots.push(l + 1);
        } else if (i - l !== 1) {
          rangeWithDots.push('...');
        }
      }
      rangeWithDots.push(i);
      l = i;
    }

    return rangeWithDots;
  };

  const handleDelete = async (e, sessionId) => {
    e.stopPropagation();
    if (!window.confirm(`Delete detection session '${sessionId}' and all recorded objects?`)) return;

    try {
      await deleteHistoryEntry(sessionId);
      if (activeSessionId === sessionId) {
        setActiveSessionId(null);
        setSessionDetail(null);
      }
      const remainingOnPage = history.length - 1;
      const targetPage = remainingOnPage === 0 && currentPage > 1 ? currentPage - 1 : currentPage;
      if (targetPage !== currentPage) {
        setCurrentPage(targetPage);
        fetchHistoryList(targetPage, pageSize);
      } else {
        fetchHistoryList(currentPage, pageSize);
      }
    } catch (err) {
      alert('Delete failed: ' + err.message);
    }
  };

  const openDetail = async (sessionId) => {
    setActiveSessionId(sessionId);
    setDetailLoading(true);
    try {
      const detail = await getHistoryDetail(sessionId);
      setSessionDetail(detail);
    } catch (err) {
      alert('Could not load session details: ' + err.message);
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <HistoryIcon className="w-5 h-5 text-blue-600" />
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">Detection History Archive</h1>
            <span className="text-xs px-2 py-0.5 bg-slate-100 text-slate-700 font-mono font-semibold rounded">
              {totalCount} Sessions
            </span>
            {totalPages > 1 && (
              <span className="text-xs px-2 py-0.5 bg-blue-50 text-blue-700 font-semibold rounded border border-blue-200/60">
                Page {currentPage} of {totalPages}
              </span>
            )}
          </div>
          <p className="text-xs text-slate-500">
            Audit log of all analyzed images, localizations, and generated segregation decisions saved in SQLite.
          </p>
        </div>

        {/* Filter Bar */}
        <div className="flex flex-wrap items-center gap-2">
          <form onSubmit={handleSearchSubmit} className="relative">
            <input
              type="text"
              placeholder="Search filename..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="text-xs pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-300 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-600"
            />
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
          </form>

          <select
            value={disposalFilter}
            onChange={(e) => setDisposalFilter(e.target.value)}
            className="text-xs py-1.5 px-3 bg-slate-50 border border-slate-300 rounded-lg text-slate-800 focus:outline-none focus:ring-1 focus:ring-blue-600 cursor-pointer"
          >
            <option value="">All Disposals</option>
            <option value="Recycle">Recycle</option>
            <option value="Compost">Compost</option>
            <option value="Reuse">Reuse</option>
            <option value="Special disposal">Special Disposal</option>
            <option value="RDF potential">RDF Potential</option>
            <option value="General waste">General Waste</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="py-16 text-center space-y-3">
          <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-medium">Querying SQLite history table...</p>
        </div>
      ) : history.length === 0 ? (
        /* Empty History State */
        <div className="bg-white border border-slate-200 rounded-xl p-12 text-center space-y-4 shadow-xs">
          <div className="w-14 h-14 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-400 mx-auto">
            <Inbox className="w-7 h-7" />
          </div>
          <div className="max-w-md mx-auto">
            <h3 className="font-bold text-base text-slate-900 mb-1">No Historical Records Found</h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-5">
              {search || disposalFilter
                ? 'No detection sessions matched your filter criteria. Clear your search or filter.'
                : 'Run your first inference session on the Waste Detection page to log detection records.'}
            </p>
            <button
              onClick={() => navigate('/detect')}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs inline-flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <span>Go to Detection Workspace</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      ) : (
        /* Sessions Table / List */
        <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="bg-slate-50 text-slate-500 font-semibold uppercase text-[10px] border-b border-slate-200">
                  <th className="py-3 px-4">Preview</th>
                  <th className="py-3 px-4">Session Info</th>
                  <th className="py-3 px-4">Timestamp</th>
                  <th className="py-3 px-4">Objects</th>
                  <th className="py-3 px-4">Detected Categories</th>
                  <th className="py-3 px-4">Primary Disposal</th>
                  <th className="py-3 px-4">Recyclability</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {history.map((session) => {
                  const badge = DISPOSAL_BADGES[session.primary_disposal] || DISPOSAL_BADGES['General waste'];
                  return (
                    <tr
                      key={session.id}
                      onClick={() => openDetail(session.id)}
                      className="hover:bg-slate-50/80 cursor-pointer transition-colors"
                    >
                      {/* Image Thumbnail */}
                      <td className="py-3 px-4">
                        <div className="w-12 h-12 rounded-lg bg-slate-100 border border-slate-200 overflow-hidden flex-shrink-0">
                          {session.annotated_image_url ? (
                            <img
                              src={session.annotated_image_url}
                              alt={session.original_filename}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center text-slate-400 text-xs">
                              IMG
                            </div>
                          )}
                        </div>
                      </td>

                      {/* Session Info */}
                      <td className="py-3 px-4">
                        <div className="font-bold text-slate-900 truncate max-w-[150px]">
                          {session.original_filename}
                        </div>
                        <div className="text-[10px] text-slate-400 font-mono">
                          {session.id.substring(0, 20)}...
                        </div>
                      </td>

                      {/* Timestamp */}
                      <td className="py-3 px-4 text-slate-600 whitespace-nowrap">
                        {new Date(session.created_at).toLocaleString([], {
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </td>

                      {/* Total Objects */}
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 bg-slate-100 text-slate-800 rounded font-bold">
                          {session.total_objects}
                        </span>
                      </td>

                      {/* Categories Badges */}
                      <td className="py-3 px-4">
                        <div className="flex flex-wrap gap-1 max-w-[200px]">
                          {(session.detected_categories || []).slice(0, 3).map((cat, i) => (
                            <span
                              key={i}
                              className="px-1.5 py-0.5 rounded text-[10px] bg-slate-100 text-slate-700"
                            >
                              {cat}
                            </span>
                          ))}
                          {(session.detected_categories || []).length > 3 && (
                            <span className="text-[10px] text-slate-400">
                              +{session.detected_categories.length - 3}
                            </span>
                          )}
                        </div>
                      </td>

                      {/* Primary Disposal */}
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${badge.bg} ${badge.text} ${badge.border}`}>
                          {badge.icon} {badge.label}
                        </span>
                      </td>

                      {/* Recyclability */}
                      <td className="py-3 px-4 font-bold text-emerald-700">
                        {session.recyclability_rate}%
                      </td>

                      {/* Actions */}
                      <td className="py-3 px-4 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              openDetail(session.id);
                            }}
                            className="p-1.5 text-slate-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
                            title="Inspect details"
                          >
                            <Eye className="w-4 h-4" />
                          </button>
                          <button
                            onClick={(e) => handleDelete(e, session.id)}
                            className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded transition-colors"
                            title="Delete record"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Pagination Footer (Shows 10 to 15 per page with page navigation buttons) */}
          <div className="bg-slate-50/90 border-t border-slate-200 px-4 py-3.5 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-600">
            {/* Left: Summary & Per-Page Selector */}
            <div className="flex flex-wrap items-center gap-3">
              <span>
                Showing <strong className="font-bold text-slate-900">{startEntry}</strong>–
                <strong className="font-bold text-slate-900">{endEntry}</strong> of{' '}
                <strong className="font-bold text-slate-900">{totalCount}</strong> sessions
              </span>
              <div className="flex items-center gap-1.5 text-slate-500">
                <span>•</span>
                <span>Show</span>
                <select
                  value={pageSize}
                  onChange={(e) => handlePageSizeChange(Number(e.target.value))}
                  className="py-1 px-2 bg-white border border-slate-300 rounded-md text-slate-800 text-xs font-semibold focus:outline-none focus:ring-1 focus:ring-blue-600 cursor-pointer shadow-2xs"
                >
                  <option value={10}>10</option>
                  <option value={15}>15</option>
                  <option value={20}>20</option>
                </select>
                <span>per page</span>
              </div>
            </div>

            {/* Right: Page Navigation Controls */}
            {totalPages > 1 && (
              <div className="flex items-center gap-1">
                {/* First Page Button */}
                <button
                  onClick={() => goToPage(1)}
                  disabled={currentPage === 1}
                  className={`p-1.5 rounded-lg border text-xs font-medium transition-all ${
                    currentPage === 1
                      ? 'border-slate-200 text-slate-300 cursor-not-allowed bg-slate-50'
                      : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-100 active:scale-95 cursor-pointer shadow-2xs'
                  }`}
                  title="First page"
                >
                  <ChevronsLeft className="w-3.5 h-3.5" />
                </button>

                {/* Previous Page Button */}
                <button
                  onClick={() => goToPage(currentPage - 1)}
                  disabled={currentPage === 1}
                  className={`px-2.5 py-1.5 rounded-lg border text-xs font-semibold flex items-center gap-1 transition-all ${
                    currentPage === 1
                      ? 'border-slate-200 text-slate-300 cursor-not-allowed bg-slate-50'
                      : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-100 active:scale-95 cursor-pointer shadow-2xs'
                  }`}
                  title="Previous page"
                >
                  <ChevronLeft className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Prev</span>
                </button>

                {/* Page Number Buttons */}
                <div className="flex items-center gap-1">
                  {getPaginationRange().map((p, idx) => {
                    if (p === '...') {
                      return (
                        <span key={`dots-${idx}`} className="px-1.5 text-slate-400 select-none font-semibold">
                          …
                        </span>
                      );
                    }
                    const isCurrent = p === currentPage;
                    return (
                      <button
                        key={p}
                        onClick={() => goToPage(p)}
                        className={`min-w-[30px] h-7 px-2 rounded-lg text-xs font-semibold transition-all border ${
                          isCurrent
                            ? 'bg-blue-600 text-white font-bold border-blue-600 shadow-xs'
                            : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-100 hover:border-slate-300 cursor-pointer'
                        }`}
                      >
                        {p}
                      </button>
                    );
                  })}
                </div>

                {/* Next Page Button */}
                <button
                  onClick={() => goToPage(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className={`px-2.5 py-1.5 rounded-lg border text-xs font-semibold flex items-center gap-1 transition-all ${
                    currentPage === totalPages
                      ? 'border-slate-200 text-slate-300 cursor-not-allowed bg-slate-50'
                      : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-100 active:scale-95 cursor-pointer shadow-2xs'
                  }`}
                  title="Next page"
                >
                  <span className="hidden sm:inline">Next</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>

                {/* Last Page Button */}
                <button
                  onClick={() => goToPage(totalPages)}
                  disabled={currentPage === totalPages}
                  className={`p-1.5 rounded-lg border text-xs font-medium transition-all ${
                    currentPage === totalPages
                      ? 'border-slate-200 text-slate-300 cursor-not-allowed bg-slate-50'
                      : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-100 active:scale-95 cursor-pointer shadow-2xs'
                  }`}
                  title="Last page"
                >
                  <ChevronsRight className="w-3.5 h-3.5" />
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Detail Slide-Over Modal */}
      {activeSessionId && (
        <div
          className="fixed inset-0 z-[100] bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto"
          onClick={() => {
            setActiveSessionId(null);
            setSessionDetail(null);
          }}
        >
          <div
            className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border border-slate-200 shadow-2xl p-6 space-y-6 my-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <HistoryIcon className="w-4 h-4 text-blue-600" />
                <h3 className="font-bold text-base text-slate-900">
                  Session Inspection: {sessionDetail?.original_filename || activeSessionId}
                </h3>
              </div>
              <button
                onClick={() => {
                  setActiveSessionId(null);
                  setSessionDetail(null);
                }}
                className="p-1 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {detailLoading || !sessionDetail ? (
              <div className="py-12 text-center text-slate-500 text-xs">
                Loading session from SQLite...
              </div>
            ) : (
              <div className="space-y-6">
                {/* Image Preview & Summary Box */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="rounded-xl overflow-hidden bg-slate-900 border border-slate-200 max-h-60 flex items-center justify-center">
                    <img
                      src={sessionDetail.annotated_image_url || sessionDetail.original_image_url}
                      alt="Annotated"
                      className="max-h-60 w-auto object-contain"
                    />
                  </div>

                  <div className="space-y-2.5 text-xs text-slate-600 bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <div>
                      <span className="text-slate-400 font-bold block uppercase text-[10px]">Session ID</span>
                      <span className="font-mono text-slate-800">{sessionDetail.id}</span>
                    </div>
                    <div>
                      <span className="text-slate-400 font-bold block uppercase text-[10px]">Inference Model</span>
                      <span className="font-semibold text-slate-800">{sessionDetail.model_name}</span>
                    </div>
                    <div>
                      <span className="text-slate-400 font-bold block uppercase text-[10px]">Primary Disposal</span>
                      <span className="font-bold text-slate-900">{sessionDetail.primary_disposal}</span>
                    </div>
                    <div>
                      <span className="text-slate-400 font-bold block uppercase text-[10px]">Recyclability Rate</span>
                      <span className="font-bold text-emerald-700">{sessionDetail.recyclability_rate}%</span>
                    </div>
                    <div>
                      <span className="text-slate-400 font-bold block uppercase text-[10px]">Summary Advice</span>
                      <p className="text-slate-700 leading-relaxed">{sessionDetail.summary_advice}</p>
                    </div>
                  </div>
                </div>

                {/* Detected Objects In This Session */}
                <div>
                  <h4 className="font-bold text-sm text-slate-900 uppercase tracking-wide mb-3">
                    Detected Objects ({sessionDetail.detections?.length || 0})
                  </h4>

                  <div className="space-y-3">
                    {sessionDetail.detections?.map((d) => {
                      const rec = d.recommendation || {};
                      const badge = DISPOSAL_BADGES[d.disposal_action] || DISPOSAL_BADGES['General waste'];
                      return (
                        <div
                          key={d.detection_id}
                          className="p-4 rounded-xl border border-slate-200 bg-white space-y-2 text-xs"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="w-5 h-5 rounded-full bg-slate-100 text-slate-700 text-[10px] font-bold flex items-center justify-center">
                                #{d.detection_id}
                              </span>
                              <span className="font-bold text-slate-900 text-sm">
                                {rec.display_name || d.class_name}
                              </span>
                              <span className="text-slate-400 font-mono text-[11px]">
                                ({(d.confidence * 100).toFixed(1)}%)
                              </span>
                            </div>

                            <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${badge.bg} ${badge.text} ${badge.border}`}>
                              {badge.icon} {badge.label}
                            </span>
                          </div>

                          <div className="text-slate-600">
                            <strong>Material:</strong> {rec.material_description || d.material}
                          </div>

                          {rec.preparation_instructions && (
                            <div className="text-[11px] text-slate-500 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                              <strong>Disposal Instructions:</strong>
                              <ul className="list-disc list-inside mt-0.5 space-y-0.5">
                                {rec.preparation_instructions.map((step, idx) => (
                                  <li key={idx}>{step}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default HistoryPage;
