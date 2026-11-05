/**
 * About / System Documentation Page
 * WasteSegregator AI
 */
import React from 'react';
import {
  Target,
  AlertCircle,
  Cpu,
  Database,
  Layers,
  Recycle,
  ShieldCheck,
  Sparkles,
  ArrowRight,
  Leaf,
  ScanLine,
  CheckCircle2,
  FileCheck2,
  Lock
} from 'lucide-react';

const AboutPage = () => {
  const objectives = [
    {
      title: 'Multi-Object Edge Detection',
      desc: 'Localize and classify multiple overlapping waste objects in real time using lightweight YOLO11n.',
      icon: ScanLine,
      color: 'text-blue-600 bg-blue-50 border-blue-100',
    },
    {
      title: 'Decoupled Decision Logic',
      desc: 'Separate neural computer vision from environmental rules to ensure deterministic, safe bin routing.',
      icon: Layers,
      color: 'text-indigo-600 bg-indigo-50 border-indigo-100',
    },
    {
      title: 'Actionable Source Segregation',
      desc: 'Assign standardized municipal bins and clear step-by-step cleaning procedures before disposal.',
      icon: Recycle,
      color: 'text-emerald-600 bg-emerald-50 border-emerald-100',
    },
    {
      title: 'Local Privacy & Storage',
      desc: 'Store all detection logs and analytical trends locally in SQLite with zero off-device image transmission.',
      icon: Lock,
      color: 'text-amber-600 bg-amber-50 border-amber-100',
    },
  ];

  const pipelineStages = [
    {
      step: '01',
      name: 'Image Preprocessing',
      detail: 'Standardizes input images to 640×640px RGB with aspect ratio letterboxing and color normalization.',
    },
    {
      step: '02',
      name: 'YOLO11n Neural Inference',
      detail: 'Predicts bounding box coordinates, class labels, and confidence probabilities across 15 waste categories.',
    },
    {
      step: '03',
      name: 'Recommendation Engine',
      detail: 'Rule-based mapping converts detected classes into municipal bin directives, cleaning rules, and safety alerts.',
    },
    {
      step: '04',
      name: 'Audit & Sustainability Sync',
      detail: 'Persists detection sessions to SQLite and computes CO2, water, and diversion savings in real time.',
    },
  ];

  const wasteStreams = [
    {
      title: 'Plastics & Polymers',
      classes: 'Bottles, Containers, Wrappers, Bags',
      bin: 'Blue Bin / Soft Plastic Depot',
      action: 'Recycle / RDF Potential',
      color: '#2563EB',
    },
    {
      title: 'Paper & Fibers',
      classes: 'Office Paper, Cardboard Cartons',
      bin: 'Blue Bin (Paper & Cardboard)',
      action: 'Recycle',
      color: '#16A34A',
    },
    {
      title: 'Organics & Biomass',
      classes: 'Food Waste, Fruit Peels, Yard Waste',
      bin: 'Green Bin (Compost / Organics)',
      action: 'Compost',
      color: '#15803D',
    },
    {
      title: 'Glass Containers',
      classes: 'Bottles, Jars, Broken Glass',
      bin: 'Teal / Blue Bin (Glass Depot)',
      action: 'Recycle',
      color: '#0284C7',
    },
    {
      title: 'Metals & Scrap',
      classes: 'Aluminum Cans, Small Metal Scrap',
      bin: 'Blue Bin / Metal Depot',
      action: 'Recycle / Scrap Recovery',
      color: '#EA580C',
    },
    {
      title: 'E-Waste & Polystyrene',
      classes: 'Batteries, Cables, Circuitry, EPS',
      bin: 'Special Depot / RDF',
      action: 'Special Hazardous Disposal',
      color: '#DC2626',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Title Header Banner */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 sm:p-7 shadow-xs space-y-3">
        <div className="inline-flex items-center gap-2 px-2.5 py-1 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold rounded-md uppercase tracking-wider">
          <span>Architecture & System Documentation</span>
          <span>•</span>
          <span>Computer Vision & Circular Economy</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          WasteSegregator <span className="text-blue-600">AI</span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 leading-relaxed max-w-3xl">
          An integrated computer vision framework with dedicated recommendation logic to automate municipal waste segregation and accelerate material recovery.
        </p>

        <div className="pt-2 flex flex-wrap items-center gap-2 text-xs">
          <span className="px-2.5 py-1 rounded bg-slate-100 text-slate-700 font-semibold border border-slate-200">
            Model: YOLO11n Nano
          </span>
          <span className="px-2.5 py-1 rounded bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
            15 Target Classes
          </span>
          <span className="px-2.5 py-1 rounded bg-blue-50 text-blue-700 font-semibold border border-blue-200">
            Sub-100ms Inference
          </span>
          <span className="px-2.5 py-1 rounded bg-slate-50 text-slate-600 font-semibold border border-slate-200">
            Local SQLite Persistence
          </span>
        </div>
      </div>

      {/* 1. Problem Statement & Key Objectives */}
      <section className="bg-white border border-slate-200 rounded-xl p-5 sm:p-6 shadow-xs space-y-4">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Target className="w-4 h-4 text-blue-600" />
            <span>System Objectives & Material Recovery</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">Automated source segregation to increase recycling recovery rates</p>
        </div>

        <p className="text-xs sm:text-[13px] text-slate-600 leading-relaxed">
          Municipal solid waste management is among the most urgent global environmental hurdles. Conventional mixed-waste collection
          leads directly to rapid landfill saturation, potent methane emissions, and the irreversible loss of recyclable polymers, fibers,
          and precious metals. Studies indicate that over <strong>70% of recyclable materials</strong> are contaminated at the source when
          mixed with food remnants and organic wastes. Automating real-time detection and actionable preparation instructions directly addresses this gap.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
          {objectives.map((obj, i) => {
            const Icon = obj.icon;
            return (
              <div key={i} className="p-3.5 rounded-xl border border-slate-200/80 bg-slate-50/50 space-y-1.5">
                <div className="flex items-center gap-2">
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center border ${obj.color}`}>
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  <h3 className="text-xs font-bold text-slate-900">{obj.title}</h3>
                </div>
                <p className="text-[11px] text-slate-500 leading-relaxed pl-9">{obj.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* 2. System Architecture & Methodology Flow */}
      <section className="bg-white border border-slate-200 rounded-xl p-5 sm:p-6 shadow-xs space-y-4">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Layers className="w-4 h-4 text-blue-600" />
            <span>End-to-End System Architecture</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">Four-stage decoupled perception and decision-making pipeline</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {pipelineStages.map((stage) => (
            <div key={stage.step} className="p-3.5 rounded-xl border border-slate-200/90 bg-slate-50/60 space-y-2 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between text-xs font-bold mb-1">
                  <span className="font-mono text-blue-600 text-[11px]">STAGE {stage.step}</span>
                  <span className="w-2 h-2 rounded-full bg-blue-500" />
                </div>
                <h4 className="text-xs font-bold text-slate-900 mb-1">{stage.name}</h4>
                <p className="text-[11px] text-slate-500 leading-relaxed">{stage.detail}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 3. Circular Economy Recovery Streams */}
      <section className="bg-white border border-slate-200 rounded-xl p-5 sm:p-6 shadow-xs space-y-4">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Recycle className="w-4 h-4 text-emerald-600" />
            <span>Circular Economy Recovery Streams (15 Categories)</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">Municipal bin allocation and circular disposal pathways</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {wasteStreams.map((stream, idx) => (
            <div
              key={idx}
              className="relative p-3.5 rounded-xl border border-slate-200/80 bg-white hover:border-slate-300 transition-colors shadow-2xs space-y-2 overflow-hidden"
            >
              <div className="absolute top-0 left-0 right-0 h-1" style={{ backgroundColor: stream.color }} />
              <div>
                <h4 className="text-xs font-bold text-slate-900">{stream.title}</h4>
                <p className="text-[11px] text-slate-500 mt-0.5">{stream.classes}</p>
              </div>
              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[10px]">
                <span className="font-semibold text-slate-700">{stream.bin}</span>
                <span className="px-2 py-0.5 rounded font-bold text-white shadow-2xs" style={{ backgroundColor: stream.color }}>
                  {stream.action}
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 4. Engineering Technology Stack */}
      <section className="bg-white border border-slate-200 rounded-xl p-5 sm:p-6 shadow-xs space-y-4">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Cpu className="w-4 h-4 text-blue-600" />
            <span>Engineering Technology Stack</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">Modular components powering real-time inference and state management</p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase font-bold block">Computer Vision</span>
            <span className="font-bold text-slate-900 block">PyTorch & YOLO11n</span>
            <span className="text-[10px] text-blue-600 font-medium">Nano Architecture (2.6M params)</span>
          </div>

          <div className="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase font-bold block">Backend Framework</span>
            <span className="font-bold text-slate-900 block">Python Flask REST</span>
            <span className="text-[10px] text-emerald-600 font-medium">Modular Blueprint APIs</span>
          </div>

          <div className="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase font-bold block">Frontend Client</span>
            <span className="font-bold text-slate-900 block">React 18 & Tailwind</span>
            <span className="text-[10px] text-indigo-600 font-medium">Live Webcam & Speech Synthesis</span>
          </div>

          <div className="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase font-bold block">Data Storage</span>
            <span className="font-bold text-slate-900 block">SQLite 3 (WAL Mode)</span>
            <span className="text-[10px] text-slate-500 font-medium">Local Audit & Aggregation</span>
          </div>
        </div>
      </section>

      {/* 5. Scientific Limitations & Ethical Scope */}
      <section className="bg-white border border-slate-200 rounded-xl p-5 sm:p-6 shadow-xs space-y-3">
        <div className="border-b border-slate-100 pb-2.5">
          <h2 className="text-base font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-600" />
            <span>Assumptions & Technical Limitations</span>
          </h2>
        </div>

        <div className="space-y-2 text-[11px] sm:text-xs text-slate-600 leading-relaxed">
          <ul className="list-disc list-inside space-y-1 text-slate-600">
            <li>
              <strong>Optical Sensing Constraints:</strong> Standard RGB computer vision identifies surface geometry and textures, but cannot verify internal chemical residues, micro-bacterial spoiled contents, or grease penetration. Users must ensure containers are rinsed before binning.
            </li>
            <li>
              <strong>Polymer Differentiation:</strong> Certain biodegradable bioplastics (e.g., PLA) share optical characteristics with non-biodegradable PET. The recommendation engine directs users to check standardized resin identification stamp codes.
            </li>
            <li>
              <strong>Municipal Variability:</strong> Recycling regulations and RDF energy recovery standards vary regionally. Recommendations follow ISO circular economy guidelines and standard color-coded municipal bin practices.
            </li>
          </ul>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;
