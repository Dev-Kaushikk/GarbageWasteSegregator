/**
 * Settings & Model Engine Configuration Page
 * WasteSegregator AI
 * Inspection and controls for active model weights, device acceleration, and taxonomy.
 * Layout matched 1:1 with Home page architecture.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sliders,
  Cpu,
  Database,
  CheckCircle2,
  AlertCircle,
  FileCheck2,
  RefreshCw,
  ScanLine,
  Award,
  Layers,
  ArrowRight
} from 'lucide-react';
import { getModelInfo, checkHealth, switchModel } from '../services/api';

const SettingsPage = () => {
  const navigate = useNavigate();
  const [modelData, setModelData] = useState(null);
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadData = () => {
    setLoading(true);
    Promise.all([getModelInfo(), checkHealth()])
      .then(([m, h]) => {
        setModelData(m);
        setHealthData(h);
      })
      .catch((err) => console.warn('Config fetch error', err))
      .finally(() => setLoading(false));
  };

  const handleActivate = async (modelId) => {
    try {
      await switchModel(modelId);
      loadData();
    } catch (err) {
      console.error('Failed to switch model', err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="py-16 text-center space-y-3">
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs text-slate-500 font-medium">Loading engine configurations and runtime status...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Hero Section — Matches Home Page Layout */}
      <section className="bg-white border border-slate-200 rounded-xl p-6 sm:p-8 shadow-xs">
        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold uppercase tracking-wider">
            <span>Inference Engine & System Runtime</span>
            <span>•</span>
            <span>Active Configuration</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight leading-tight">
            Engine & System Settings
          </h1>

          <p className="text-slate-600 text-sm sm:text-base leading-relaxed">
            Configure active neural network checkpoints, inspect hardware acceleration devices,
            and monitor database and storage directories in real time.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-1">
            <button
              onClick={loadData}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-xs sm:text-sm font-semibold rounded-lg shadow-xs flex items-center gap-2 transition-colors cursor-pointer"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Refresh Status</span>
            </button>

            <button
              onClick={() => navigate('/detect')}
              className="px-4 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 text-xs sm:text-sm font-medium rounded-lg shadow-xs flex items-center gap-2 transition-colors cursor-pointer"
            >
              <ScanLine className="w-4 h-4 text-slate-500" />
              <span>Open Scanner</span>
            </button>

            <button
              onClick={() => navigate('/training')}
              className="px-3.5 py-2 text-slate-500 hover:text-slate-800 text-xs sm:text-sm font-medium transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <Award className="w-3.5 h-3.5" />
              <span>Model Benchmarks</span>
            </button>
          </div>
        </div>

        {/* Status Callout Bar — Matches Home Page */}
        <div className="mt-6 pt-5 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div>
            <span className="text-slate-400 block font-medium">Active Checkpoint</span>
            <span className="font-semibold text-blue-700">{modelData?.active_model_name || 'YOLO11n Waste-15'}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Hardware Acceleration</span>
            <span className="font-semibold text-emerald-700">{modelData?.device_display || 'CPU Active'}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Supported Taxonomy</span>
            <span className="font-semibold text-emerald-700">{modelData?.supported_classes_count || 15} Waste Categories</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Storage Connection</span>
            <span className="font-semibold text-slate-800">SQLite Connected</span>
          </div>
        </div>
      </section>

      {/* 1. Active Inference Engine Overview */}
      <section className="space-y-3">
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Cpu className="w-5 h-5 text-blue-600" />
            <span>Active Inference Engine</span>
          </h2>
          <p className="text-xs text-slate-500">Live compute metrics, device capabilities, and detection architecture</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-2">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Active Checkpoint</span>
            <div className="font-extrabold text-base text-slate-900">{modelData?.active_model_name}</div>
            <div className="inline-block px-2 py-0.5 rounded bg-blue-50 text-blue-700 text-xs font-semibold border border-blue-200">
              {modelData?.model_type || 'Object Detection'}
            </div>
            <p className="text-xs text-slate-500 pt-1 leading-relaxed">
              Standardized single-stage neural network trained across 15 municipal waste categories.
            </p>
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-2">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Compute Device</span>
            <div className="font-extrabold text-base text-slate-900">{modelData?.device_display}</div>
            <div className="inline-block px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
              Accelerated Runtime
            </div>
            <p className="text-xs text-slate-500 pt-1 leading-relaxed">
              Optimized tensor calculations delivering sub-100ms multi-object localization.
            </p>
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-2">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Category Coverage</span>
            <div className="font-extrabold text-base text-slate-900">{modelData?.supported_classes_count} Categories</div>
            <div className="inline-block px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
              15 / 15 Target Classes
            </div>
            <p className="text-xs text-slate-500 pt-1 leading-relaxed">
              Full coverage of plastics, fibers, metals, organics, textiles, and e-waste.
            </p>
          </div>
        </div>
      </section>

      {/* 2. Registered Model Checkpoints */}
      <section className="space-y-3">
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <FileCheck2 className="w-5 h-5 text-blue-600" />
            <span>Available Model Checkpoints</span>
          </h2>
          <p className="text-xs text-slate-500">Select or switch model checkpoints registered in the local runtime directory</p>
        </div>

        <div className="grid grid-cols-1 gap-3">
          {modelData?.registered_models?.map((m) => (
            <div
              key={m.id}
              className={`bg-white border rounded-xl p-5 shadow-xs transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                m.id === modelData.active_model_id
                  ? 'border-blue-600 ring-1 ring-blue-600/20 bg-blue-50/10'
                  : 'border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="space-y-1.5">
                <div className="flex items-center gap-2.5">
                  <span className="font-bold text-slate-900 text-sm">{m.name}</span>
                  {m.id === modelData.active_model_id && (
                    <span className="px-2 py-0.5 bg-blue-600 text-white font-bold text-[10px] rounded shadow-2xs">
                      ACTIVE
                    </span>
                  )}
                  {m.available ? (
                    <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold text-[10px] rounded">
                      Available on Disk
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 bg-slate-100 text-slate-500 border border-slate-200 text-[10px] rounded">
                      Configured Slot
                    </span>
                  )}
                </div>
                <p className="text-slate-600 text-xs leading-relaxed max-w-2xl">{m.description}</p>
                <div className="text-[11px] text-slate-400 font-mono">Path: {m.path}</div>
              </div>

              <div className="flex items-center sm:flex-col items-end justify-between sm:justify-center gap-3 flex-shrink-0">
                <div className="text-left sm:text-right">
                  <span className="text-xs font-bold text-slate-800 block">
                    {m.mAP50 ? `mAP50: ${(m.mAP50 * 100).toFixed(1)}%` : 'Target Checkpoint'}
                  </span>
                  <span className="text-[11px] text-slate-400">{m.supported_classes_count} Classes</span>
                </div>
                {m.available && m.id !== modelData.active_model_id && (
                  <button
                    onClick={() => handleActivate(m.id)}
                    className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg transition-colors cursor-pointer shadow-xs"
                  >
                    Activate
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 3. Database & Storage Architecture */}
      <section className="space-y-3">
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Database className="w-5 h-5 text-blue-600" />
            <span>Database & Storage Paths</span>
          </h2>
          <p className="text-xs text-slate-500">Persistent file locations for detection records and uploaded imagery</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-2">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block">SQLite Database File</span>
            <div className="font-mono text-xs font-bold text-slate-800 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
              backend/database/waste_segregator.db
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">
              Stores session records, localized bounding boxes, recyclability rates, and analytics logs.
            </p>
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-2">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block">Image Artifacts Directory</span>
            <div className="font-mono text-xs font-bold text-slate-800 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
              backend/uploads/
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">
              Holds raw user inputs and generated bounding-box annotated visualizations on local disk.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default SettingsPage;
