/**
 * Home / Landing Page
 * AI-Based Smart Garbage Waste Segregator
 * Designed following the clean AutomataX academic interface style.
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ScanLine,
  ArrowRight,
  ShieldCheck,
  Cpu,
  Layers,
  Database,
  Recycle,
  Leaf,
  FileCheck2,
  ExternalLink
} from 'lucide-react';
import { TARGET_15_CLASSES, PLATFORM_INFO } from '../utils/constants';

const CLASS_ICONS = {
  0: '🍾',  // plastic bottle
  1: '🍬',  // wrapper
  2: '🛍️',  // plastic bag
  3: '🥡',  // plastic container
  4: '📄',  // paper
  5: '📦',  // cardboard carton
  6: '🥛',  // glass
  7: '🥫',  // metal can
  8: '🔩',  // metal scrap
  9: '🧊',  // styrofoam
  10: '🍎', // food waste
  11: '🍌', // fruit vegetable peel
  12: '🌿', // garden waste
  13: '👕', // textile
  14: '🔋', // e-waste
};

const HomePage = () => {
  const navigate = useNavigate();

  const workflowSteps = [
    {
      step: '01',
      title: 'Image Acquisition',
      desc: 'Upload single or multi-object waste imagery via drag-and-drop, camera capture, or sample datasets.',
      icon: ScanLine,
    },
    {
      step: '02',
      title: 'YOLO Detection',
      desc: 'Inference engine localizes bounding boxes, material labels, and confidence metrics in real time.',
      icon: Cpu,
    },
    {
      step: '03',
      title: 'Recommendation Engine',
      desc: 'Independent rule-based intelligence classifies objects into Recycle, Compost, Reuse, RDF, or Special Disposal.',
      icon: Recycle,
    },
    {
      step: '04',
      title: 'Audit & Analytics',
      desc: 'Structured sessions and metrics are committed to local SQLite storage for longitudinal environmental tracking.',
      icon: Database,
    },
  ];

  const features = [
    {
      title: 'Independent Architecture',
      desc: 'Decoupled machine learning detection and rule-based environmental recommendation engines.',
      icon: Layers,
    },
    {
      title: 'Multi-Object Detection',
      desc: 'Simultaneously localize and classify multiple overlapping waste objects in cluttered environments.',
      icon: ScanLine,
    },
    {
      title: 'Real-Time Edge Inference',
      desc: 'Hardware accelerated neural pipeline delivering sub-100ms multi-object detection and sorting.',
      icon: Cpu,
    },
    {
      title: 'Actionable Segregation',
      desc: 'Specific preparation procedures, safety warnings for hazardous items, and eco-friendly alternatives.',
      icon: Leaf,
    },
    {
      title: 'Local Data Sovereignty',
      desc: 'All detection sessions and analytics are recorded locally in a high-performance SQLite database.',
      icon: Database,
    },
    {
      title: '15-Class Target Taxonomy',
      desc: 'Standardized municipal waste ontology covering plastics, fibers, metals, organics, and e-waste.',
      icon: FileCheck2,
    },
  ];

  return (
    <div className="space-y-7">
      {/* Hero Section */}
      <section className="bg-white border border-slate-200 rounded-xl p-6 sm:p-8 shadow-xs">
        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold uppercase tracking-wider">
            <span>Machine Learning & Computer Vision Research</span>
            <span>•</span>
            <span>v2.0</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight leading-tight">
            AI-Based Smart Garbage Waste Segregator
          </h1>

          <p className="text-slate-600 text-sm sm:text-base leading-relaxed">
            An intelligent computer vision system that localizes waste objects, identifies material categories,
            and generates deterministic, rule-based segregation recommendations to support municipal circularity
            and responsible disposal.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-1">
            <button
              onClick={() => navigate('/detect')}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-xs sm:text-sm font-semibold rounded-lg shadow-xs flex items-center gap-2 transition-colors"
            >
              <ScanLine className="w-4 h-4" />
              <span>Start Waste Detection</span>
              <ArrowRight className="w-4 h-4 ml-0.5" />
            </button>

            <button
              onClick={() => navigate('/dashboard')}
              className="px-4 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 text-xs sm:text-sm font-medium rounded-lg shadow-xs transition-colors"
            >
              View Dashboard Analytics
            </button>

            <button
              onClick={() => navigate('/about')}
              className="px-3.5 py-2 text-slate-500 hover:text-slate-800 text-xs sm:text-sm font-medium transition-colors flex items-center gap-1.5"
            >
              <span>Project Documentation</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Status Callout Bar */}
        <div className="mt-6 pt-5 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div>
            <span className="text-slate-400 block font-medium">Model Architecture</span>
            <span className="font-semibold text-blue-700">YOLO11n 15-Class Master</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Active Taxonomy</span>
            <span className="font-semibold text-emerald-700">15 / 15 Target Classes</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Recommendation Rules</span>
            <span className="font-semibold text-emerald-700">6 Circular Disposal Routes</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Inference Speed</span>
            <span className="font-semibold text-slate-800">Sub-100ms Real-Time</span>
          </div>
        </div>
      </section>

      {/* How It Works (Workflow) */}
      <section className="space-y-3">
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight">System Workflow</h2>
          <p className="text-xs text-slate-500">Separation of Computer Vision localization from environmental decision logic</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {workflowSteps.map((step) => {
            const Icon = step.icon;
            return (
              <div key={step.step} className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-2.5">
                <div className="flex items-center justify-between">
                  <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600">
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-mono font-bold text-slate-400">{step.step}</span>
                </div>
                <div>
                  <h3 className="font-bold text-sm text-slate-900 mb-0.5">{step.title}</h3>
                  <p className="text-xs text-slate-500 leading-relaxed">{step.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 15-Class Target Taxonomy Overview (Refined Directory) */}
      <section className="bg-white border border-slate-200 rounded-xl p-5 sm:p-6 shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Standardized 15-Class Waste Taxonomy</h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Ontology structure designed for automated waste sorting and circular materials recovery
            </p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-md self-start sm:self-auto">
            15 Active Categories
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {TARGET_15_CLASSES.map((cls) => (
            <div
              key={cls.id}
              className="relative rounded-xl border border-slate-200 bg-white p-3.5 shadow-2xs hover:shadow-xs hover:border-blue-400 transition-all duration-150 flex flex-col justify-between group overflow-hidden"
            >
              {/* Top Colored Category Accent Bar */}
              <div
                className="absolute top-0 left-0 right-0 h-1"
                style={{ backgroundColor: cls.color }}
              />

              <div>
                <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1.5 pt-0.5">
                  <span className="font-mono font-bold px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded">
                    #{cls.id}
                  </span>
                  <span className="text-base group-hover:scale-110 transition-transform">
                    {CLASS_ICONS[cls.id] || '🗑️'}
                  </span>
                </div>

                <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400 mb-0.5">
                  {cls.category}
                </div>

                <div className="text-xs font-bold text-slate-800 leading-snug">
                  {cls.display}
                </div>
              </div>

              {/* Destination Bin Pill */}
              <div className="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px]">
                <span
                  className="font-bold px-2 py-0.5 rounded text-white text-[9.5px] shadow-2xs"
                  style={{ backgroundColor: cls.color }}
                >
                  {cls.bin.split('(')[0].trim()}
                </span>
                <span className="text-slate-400 font-medium truncate max-w-[80px]">
                  {cls.bin.includes('(') ? cls.bin.split('(')[1].replace(')', '') : ''}
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Key Architectural Features Grid */}
      <section className="space-y-3">
        <div>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight">System Capabilities</h2>
          <p className="text-xs text-slate-500">Core engineering highlights of the application</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {features.map((f, i) => {
            const Icon = f.icon;
            return (
              <div key={i} className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-2">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700">
                    <Icon className="w-4 h-4" />
                  </div>
                  <h3 className="font-bold text-sm text-slate-900">{f.title}</h3>
                </div>
                <p className="text-xs text-slate-500 leading-relaxed pl-10">{f.desc}</p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
};

export default HomePage;

