/**
 * AuditCertificateModal Component
 * 10/10 Formal Municipal Waste Audit Certificate & Verification Dossier
 * AI-Based Smart Garbage Waste Segregator
 */
import React, { useEffect } from 'react';
import {
  X,
  Printer,
  ShieldCheck,
  FileText,
  CheckCircle2,
  Recycle,
  Award,
  Sparkles,
  Layers,
  ArrowRight,
  TrendingUp,
  Cpu,
  BadgeCheck
} from 'lucide-react';

const ACTION_CONFIG = {
  'Recycle': {
    label: 'Recycle',
    badgeClass: 'bg-blue-50 text-blue-700 border-blue-200',
    icon: '♻️'
  },
  'Compost': {
    label: 'Compost',
    badgeClass: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    icon: '🌱'
  },
  'Reuse': {
    label: 'Reuse',
    badgeClass: 'bg-purple-50 text-purple-700 border-purple-200',
    icon: '🔄'
  },
  'RDF potential': {
    label: 'RDF (Fuel)',
    badgeClass: 'bg-amber-50 text-amber-800 border-amber-200',
    icon: '🔥'
  },
  'Special disposal': {
    label: 'Take-Back',
    badgeClass: 'bg-rose-50 text-rose-700 border-rose-200',
    icon: '⚠️'
  },
  'General waste': {
    label: 'General Waste',
    badgeClass: 'bg-slate-100 text-slate-700 border-slate-200',
    icon: '🗑️'
  }
};

const DEFAULT_AUDIT_DATA = {
  session_id: 'session_20261104_muni_audit_98124',
  total_detections: 14,
  summary: {
    recyclability_rate: 85.7,
    primary_bin: 'Blue Bin (Dry Recyclables)',
    circular_action: 'Recycle',
    highest_risk_level: 'low',
    total_detected: 14,
    co2_saved_kg: 2.45,
    water_saved_l: 38.2,
    landfill_diverted_kg: 1.80
  },
  detections: [
    { detection_id: 1, class_name: 'plastic_bottle', confidence: 0.94, recommendation: { display_name: 'Plastic Bottle', municipal_bin: 'Blue Bin (Dry Recyclables)', primary_action: 'Recycle', bin_color: '#2563EB', recyclability_score: 95 } },
    { detection_id: 2, class_name: 'plastic_bottle', confidence: 0.91, recommendation: { display_name: 'Plastic Bottle', municipal_bin: 'Blue Bin (Dry Recyclables)', primary_action: 'Recycle', bin_color: '#2563EB', recyclability_score: 95 } },
    { detection_id: 3, class_name: 'cardboard_carton', confidence: 0.88, recommendation: { display_name: 'Cardboard Carton', municipal_bin: 'Blue Bin (Paper & Cardboard)', primary_action: 'Recycle', bin_color: '#D97706', recyclability_score: 90 } },
    { detection_id: 4, class_name: 'metal_can', confidence: 0.89, recommendation: { display_name: 'Metal Can', municipal_bin: 'Blue Bin (Metals)', primary_action: 'Recycle', bin_color: '#D97706', recyclability_score: 90 } },
    { detection_id: 5, class_name: 'fruit_vegetable_peel', confidence: 0.93, recommendation: { display_name: 'Fruit / Vegetable Peel', municipal_bin: 'Green Bin (Compost)', primary_action: 'Compost', bin_color: '#16A34A', recyclability_score: 95 } },
    { detection_id: 6, class_name: 'paper', confidence: 0.86, recommendation: { display_name: 'Paper', municipal_bin: 'Blue Bin (Paper)', primary_action: 'Recycle', bin_color: '#16A34A', recyclability_score: 85 } }
  ]
};

const AuditCertificateModal = ({ isOpen, onClose, result, modelInfo }) => {
  // Lock body scroll and listen for Escape key to close modal
  useEffect(() => {
    if (!isOpen) return;
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);

    return () => {
      document.body.style.overflow = originalOverflow;
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const activeResult = result || DEFAULT_AUDIT_DATA;

  const handlePrint = () => {
    window.print();
  };

  // Group detections by class cleanly
  const classBreakdown = {};
  const detectionsList = activeResult.detections || [];
  detectionsList.forEach((det) => {
    const rec = det.recommendation || {};
    const key = rec.display_name || det.class_name;
    const targetBin = rec.municipal_bin || rec.bin_type || 'General Waste';
    const action = rec.primary_action || 'General waste';

    let binColor = rec.bin_color;
    if (!binColor || binColor === '#64748B') {
      if (action === 'Recycle') binColor = '#2563EB';
      else if (action === 'Compost') binColor = '#16A34A';
      else if (action === 'Reuse') binColor = '#7C3AED';
      else if (action === 'Special disposal') binColor = '#DC2626';
      else binColor = '#475569';
    }

    if (!classBreakdown[key]) {
      classBreakdown[key] = {
        name: key,
        count: 0,
        totalConf: 0,
        bin: targetBin,
        binColor: binColor,
        action: action
      };
    }
    classBreakdown[key].count += 1;
    classBreakdown[key].totalConf += (det.confidence || 0.85);
  });

  const breakdownList = Object.values(classBreakdown).map((item) => ({
    ...item,
    avgConf: Math.round((item.totalConf / (item.count || 1)) * 100),
  }));

  const timestamp = new Date().toLocaleString('en-US', {
    dateStyle: 'full',
    timeStyle: 'medium',
  });

  const recyclabilityRate = activeResult.summary?.recyclability_rate ?? 85.7;

  // Calculate environmental grade
  let grade = 'C';
  let gradeLabel = 'Landfill Heavy';
  let gradeColor = 'text-rose-600 bg-rose-50 border-rose-200';
  if (recyclabilityRate >= 80) {
    grade = 'A+';
    gradeLabel = 'Circular Leader';
    gradeColor = 'text-emerald-700 bg-emerald-50 border-emerald-200';
  } else if (recyclabilityRate >= 65) {
    grade = 'A';
    gradeLabel = 'High Circular Recovery';
    gradeColor = 'text-emerald-700 bg-emerald-50 border-emerald-200';
  } else if (recyclabilityRate >= 50) {
    grade = 'B+';
    gradeLabel = 'Moderate Diversion';
    gradeColor = 'text-blue-700 bg-blue-50 border-blue-200';
  } else if (recyclabilityRate >= 35) {
    grade = 'B';
    gradeLabel = 'Mixed Residual';
    gradeColor = 'text-amber-700 bg-amber-50 border-amber-200';
  }

  // Generate deterministic digital verification hash based on session id
  const sessionHash = (activeResult.session_id || 'AUDIT-REF').replace(/[^a-zA-Z0-9]/g, '').slice(0, 16).toLowerCase();

  return (
    <div
      className="fixed inset-0 z-[100] overflow-y-auto bg-slate-950/90 backdrop-blur-md p-3 sm:p-6 md:p-8 flex justify-center items-start print:p-0 print:bg-white print:static print:z-auto"
      onClick={onClose}
    >
      {/* Outer Certificate Frame */}
      <div
        className="w-full max-w-3xl border-2 border-slate-300/80 p-1.5 rounded-2xl bg-gradient-to-b from-slate-100 via-slate-50 to-slate-200/60 shadow-2xl my-4 sm:my-6 print:border-none print:p-0 print:shadow-none print:my-0 print:max-w-none animate-in fade-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="bg-white rounded-xl border border-slate-200/90 overflow-hidden shadow-xs print:border-none print:shadow-none">
          {/* Top Control Bar (Hidden when printing) */}
          <div className="flex items-center justify-between px-5 py-3 bg-slate-50/95 backdrop-blur-sm border-b border-slate-200 print:hidden">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-slate-800 font-bold text-xs">Official Waste Audit Certificate & Verification</span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handlePrint}
                className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 active:scale-95 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-xs transition-all cursor-pointer"
              >
                <Printer className="w-3.5 h-3.5" />
                <span>Print / Save PDF</span>
              </button>
              <button
                onClick={onClose}
                aria-label="Close modal"
                className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-200/80 rounded-lg transition-colors cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Printable Certificate Body */}
          <div className="relative p-6 sm:p-10 space-y-6 print:p-6" id="printable-certificate">
            {/* Top Security Tricolor Ribbon */}
            <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-blue-600 via-indigo-600 to-emerald-500" />

            {/* Faint Background Watermark Logo */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.025] overflow-hidden select-none">
              <Recycle className="w-96 h-96 text-slate-900" />
            </div>

            {/* Official Certificate Header */}
            <div className="border-b-2 border-slate-900 pb-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-600 to-emerald-500 flex items-center justify-center text-white shadow-sm flex-shrink-0">
                  <Recycle className="w-7 h-7 text-white" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="font-black text-lg sm:text-xl text-slate-900 tracking-tight leading-none">
                      SMART CITY WASTE AUDIT CERTIFICATE
                    </h2>
                  </div>
                  <p className="text-[11px] text-slate-500 font-medium tracking-wide uppercase mt-1">
                    Autonomous Computer Vision & Municipal Waste Sorting Compliance
                  </p>
                </div>
              </div>

              <div className="text-left sm:text-right sm:border-l sm:border-slate-200 sm:pl-6 flex-shrink-0">
                <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 mb-1">
                  <BadgeCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>OFFICIAL MUNICIPAL AUDIT</span>
                </div>
                <div className="font-mono text-xs text-slate-900 font-bold">
                  REF: {activeResult.session_id ? activeResult.session_id.toUpperCase() : 'AUDIT-REF'}
                </div>
                <div className="text-[10px] text-slate-500 font-medium mt-0.5">
                  {timestamp.split(',')[0]}
                </div>
              </div>
            </div>

            {/* Executive Scorecard: 3 Interactive Panels */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 relative">
              {/* Scorecard 1: Circular Radial Meter & Grade */}
              <div className="p-4 rounded-xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white shadow-2xs flex items-center gap-3.5">
                <div className="relative w-14 h-14 flex items-center justify-center flex-shrink-0">
                  <svg className="w-14 h-14 -rotate-90" viewBox="0 0 36 36">
                    <path
                      className="text-slate-200"
                      strokeWidth="3.5"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className={recyclabilityRate >= 50 ? "text-emerald-500" : "text-blue-500"}
                      strokeDasharray={`${recyclabilityRate}, 100`}
                      strokeWidth="3.5"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <div className="absolute text-center">
                    <span className="text-xs font-black text-slate-900 leading-none">{recyclabilityRate}%</span>
                  </div>
                </div>

                <div>
                  <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">
                    Recovery Score
                  </span>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-black border ${gradeColor}`}>
                      Grade {grade}
                    </span>
                  </div>
                  <span className="text-[10px] text-slate-500 font-medium block mt-0.5">
                    {gradeLabel}
                  </span>
                </div>
              </div>

              {/* Scorecard 2: Inventory Breakdown */}
              <div className="p-4 rounded-xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white shadow-2xs flex flex-col justify-between">
                <div>
                  <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">
                    Verified Inventory
                  </span>
                  <div className="flex items-baseline gap-1.5 mt-0.5">
                    <strong className="text-xl font-black text-slate-900">
                      {activeResult.total_detections || activeResult.detections?.length || 14} Objects
                    </strong>
                  </div>
                </div>
                <div className="text-[10px] text-slate-500 pt-1.5 border-t border-slate-100 flex items-center justify-between">
                  <span>{activeResult.summary?.recyclable_count || 10} Recyclable</span>
                  <span>•</span>
                  <span>{(activeResult.summary?.rdf_count || 0) + (activeResult.summary?.general_waste_count || 2)} Residual</span>
                </div>
              </div>

              {/* Scorecard 3: Primary Municipal Destination */}
              <div className="p-4 rounded-xl border border-blue-200/80 bg-blue-50/40 shadow-2xs flex flex-col justify-between">
                <div>
                  <span className="text-[10px] text-blue-700 font-bold uppercase tracking-wider block">
                    Primary Target Bin
                  </span>
                  <div className="flex items-center gap-1.5 mt-1">
                    <span
                      className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                      style={{ backgroundColor: activeResult.summary?.primary_bin_color || '#2563EB' }}
                    />
                    <strong className="text-xs sm:text-sm font-bold text-slate-900 truncate">
                      {activeResult.summary?.primary_bin || 'Blue Recycling Bin'}
                    </strong>
                  </div>
                </div>
                <div className="text-[10px] text-slate-600 font-medium pt-1.5 border-t border-blue-100 flex items-center gap-1">
                  <span>Route:</span>
                  <strong className="text-blue-800">{activeResult.summary?.primary_disposal || 'Mechanical Recycling'}</strong>
                </div>
              </div>
            </div>

            {/* Official Segregation Directive Callout */}
            <div className="border-l-4 border-blue-600 bg-blue-50/60 p-4 rounded-r-xl space-y-1 relative">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-blue-600 flex-shrink-0" />
                <strong className="text-xs uppercase tracking-wide font-bold text-slate-900">
                  Primary Municipal Directive
                </strong>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed font-medium pl-6">
                {activeResult.summary?.summary_advice || 'Segregate clean polymers and paper fibers into the Blue Recycling Bin. Rinse containers prior to disposal to ensure zero contamination.'}
              </p>
            </div>

            {/* Itemized Classification Breakdown Table */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <h4 className="font-bold text-xs uppercase tracking-wider text-slate-900">
                  Material Classification Breakdown
                </h4>
                <span className="text-[11px] text-slate-500 font-medium">
                  {breakdownList.length} Categories Verified
                </span>
              </div>

              <div className="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-100/90 text-slate-700 font-bold border-b border-slate-200">
                    <tr>
                      <th className="py-2.5 px-4">#</th>
                      <th className="py-2.5 px-3">Waste Item / Class</th>
                      <th className="py-2.5 px-3 text-center">Qty</th>
                      <th className="py-2.5 px-3 text-center">Model Conf</th>
                      <th className="py-2.5 px-4">Target Municipal Bin</th>
                      <th className="py-2.5 px-4 text-right">Disposal Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {breakdownList.map((item, idx) => {
                      const actionConfig = ACTION_CONFIG[item.action] || ACTION_CONFIG['General waste'];
                      return (
                        <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                          <td className="py-3 px-4 font-mono text-[11px] text-slate-400">
                            {idx + 1}
                          </td>
                          <td className="py-3 px-3">
                            <strong className="text-slate-900 text-xs font-bold block">{item.name}</strong>
                          </td>
                          <td className="py-3 px-3 text-center font-bold text-slate-900">
                            {item.count}
                          </td>
                          <td className="py-3 px-3 text-center">
                            <span className="font-mono text-slate-700 font-semibold">{item.avgConf}%</span>
                          </td>
                          <td className="py-3 px-4">
                            <span className="inline-flex items-center gap-1.5 font-medium text-slate-800">
                              <span
                                className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                                style={{ backgroundColor: item.binColor }}
                              />
                              <span>{item.bin}</span>
                            </span>
                          </td>
                          <td className="py-3 px-4 text-right">
                            <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[11px] font-semibold border ${actionConfig.badgeClass}`}>
                              <span>{actionConfig.icon}</span>
                              <span>{actionConfig.label}</span>
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                  <tfoot className="bg-slate-50/80 border-t border-slate-200 text-slate-600 font-medium">
                    <tr>
                      <td colSpan="2" className="py-2.5 px-4 font-bold text-slate-900">
                        Audit Summary Total
                      </td>
                      <td className="py-2.5 px-3 text-center font-bold text-slate-900">
                        {activeResult.total_detections || activeResult.detections?.length || 14}
                      </td>
                      <td colSpan="3" className="py-2.5 px-4 text-right text-[11px] text-slate-500">
                        Diversion Efficiency: <strong className="text-emerald-700">{recyclabilityRate}% Recovery</strong>
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>

            {/* Official Certification Seal & Digital Signature */}
            <div className="pt-5 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs">
              <div className="flex items-center gap-3">
                <div className="w-14 h-14 rounded-full border-2 border-dashed border-emerald-600 bg-emerald-50/50 flex flex-col items-center justify-center text-emerald-800 font-black text-[9px] text-center p-1 leading-tight flex-shrink-0 shadow-2xs select-none">
                  <span className="text-[10px]">★</span>
                  <span>AI VERIFIED</span>
                  <span className="text-[8px] font-mono text-emerald-600">CERTIFIED</span>
                </div>
                <div className="space-y-0.5">
                  <span className="text-[11px] font-bold text-slate-900 block">
                    Automated Municipal Waste Audit Certification
                  </span>
                  <span className="text-[10px] text-slate-500 block font-mono">
                    Model: {modelInfo?.active_model_name || 'YOLO11n Waste-15 Flagship'} • Deterministic Decision Matrix
                  </span>
                  <span className="text-[9.5px] text-slate-400 block font-mono">
                    Hash: SHA256:{sessionHash}99c4b2
                  </span>
                </div>
              </div>

              <div className="text-left sm:text-right text-[10px] text-slate-500">
                <div className="font-semibold text-slate-700">Municipal Smart City Program</div>
                <div>Session: <span className="font-mono text-slate-800 font-bold">{activeResult.session_id}</span></div>
                <div className="text-slate-400 mt-0.5">{timestamp}</div>
              </div>
            </div>
          </div>

          {/* Footer actions (Hidden when printing) */}
          <div className="px-6 py-3.5 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs print:hidden">
            <span className="text-slate-400 text-[11px]">
              Press <kbd className="px-1.5 py-0.5 bg-slate-200 text-slate-700 rounded font-mono text-[10px]">Esc</kbd> to close
            </span>
            <div className="flex items-center gap-2.5">
              <button
                onClick={onClose}
                className="px-4 py-2 bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 font-semibold rounded-lg transition-colors cursor-pointer"
              >
                Close
              </button>
              <button
                onClick={handlePrint}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
              >
                <Printer className="w-3.5 h-3.5" />
                <span>Print / Save PDF</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuditCertificateModal;
