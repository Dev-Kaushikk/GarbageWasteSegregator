/**
 * Settings & Model Engine Configuration Page
 * AI-Based Smart Garbage Waste Segregator
 * Inspection and controls for active model weights, device acceleration, and taxonomy.
 */
import React, { useState, useEffect } from 'react';
import {
  Sliders,
  Cpu,
  Database,
  CheckCircle2,
  AlertCircle,
  FileCheck2,
  RefreshCw
} from 'lucide-react';
import { getModelInfo, checkHealth, switchModel } from '../services/api';
import { PLATFORM_INFO } from '../utils/constants';

const SettingsPage = () => {
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
        <p className="text-xs text-slate-500 font-medium">Inspecting YOLO model checkpoints & hardware...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Sliders className="w-5 h-5 text-blue-600" />
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">Model Engine & System Settings</h1>
          </div>
          <p className="text-xs text-slate-500">
            Inspect loaded weights, hardware acceleration state, and model registry slots.
          </p>
        </div>

        <button
          onClick={loadData}
          className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Status</span>
        </button>
      </div>

      {/* Active Model & Device Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center gap-2 border-b border-slate-100 pb-3">
          <Cpu className="w-4 h-4 text-blue-600" />
          <span>Active Inference Engine</span>
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[10px] text-slate-400 font-bold uppercase block">Active Model Checkpoint</span>
            <span className="font-extrabold text-sm text-slate-900 block">{modelData?.active_model_name}</span>
            <span className="text-[11px] text-blue-600 font-semibold">{modelData?.model_type}</span>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[10px] text-slate-400 font-bold uppercase block">Hardware Device</span>
            <span className="font-extrabold text-sm text-slate-900 block">{modelData?.device_display}</span>
            <span className="text-[11px] text-emerald-600 font-semibold">Acceleration Active</span>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[10px] text-slate-400 font-bold uppercase block">Supported Classes</span>
            <span className="font-extrabold text-sm text-slate-900 block">{modelData?.supported_classes_count} Classes</span>
            <span className="text-[11px] text-emerald-600 font-semibold">15 / 15 Target Classes Active</span>
          </div>
        </div>

        <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-800 leading-relaxed">
          <strong>Architecture Guarantee:</strong> {modelData?.architecture_note}
        </div>
      </div>

      {/* Registered Model Slots */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center gap-2 border-b border-slate-100 pb-3">
          <FileCheck2 className="w-4 h-4 text-blue-600" />
          <span>Registered Model Checkpoints</span>
        </h2>

        <div className="space-y-3">
          {modelData?.registered_models?.map((m) => (
            <div
              key={m.id}
              className={`p-4 rounded-xl border text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                m.id === modelData.active_model_id
                  ? 'border-blue-600 bg-blue-50/20'
                  : 'border-slate-200 bg-white'
              }`}
            >
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-slate-900 text-sm">{m.name}</span>
                  {m.id === modelData.active_model_id && (
                    <span className="px-2 py-0.5 bg-blue-600 text-white font-bold text-[10px] rounded">
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
                <p className="text-slate-500 text-[11px] mt-1">{m.description}</p>
                <div className="text-[10px] text-slate-400 font-mono mt-0.5">Path: {m.path}</div>
              </div>

              <div className="text-right flex-shrink-0 flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-2">
                <div>
                  <span className="text-[11px] font-bold text-slate-700 block">
                    {m.mAP50 ? `mAP50: ${(m.mAP50 * 100).toFixed(1)}%` : 'Target Checkpoint'}
                  </span>
                  <span className="text-[10px] text-slate-400">{m.supported_classes_count} Classes</span>
                </div>
                {m.available && m.id !== modelData.active_model_id && (
                  <button
                    onClick={() => handleActivate(m.id)}
                    className="px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-[10px] rounded transition-colors"
                  >
                    Activate
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Local Storage Information */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-3 text-xs">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center gap-2 border-b border-slate-100 pb-3">
          <Database className="w-4 h-4 text-blue-600" />
          <span>Local Data Sovereignty</span>
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-slate-600">
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span className="text-[10px] text-slate-400 uppercase font-bold block">Database File</span>
            <span className="font-mono text-slate-800">backend/database/waste_segregator.db</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span className="text-[10px] text-slate-400 uppercase font-bold block">Uploads Directory</span>
            <span className="font-mono text-slate-800">backend/uploads/</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;

