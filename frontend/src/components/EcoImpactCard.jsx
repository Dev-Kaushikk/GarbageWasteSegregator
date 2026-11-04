/**
 * EcoImpactCard Component
 * Real-time Environmental & Sustainability Metrics
 * AI-Based Smart Garbage Waste Segregator
 */
import React from 'react';
import { Leaf, Droplets, Zap, Recycle, Award, TrendingUp } from 'lucide-react';

const EcoImpactCard = ({ detections = [], summary = {} }) => {
  if (!detections || detections.length === 0) return null;

  // Compute metrics based on detected items
  let plasticCount = 0;
  let metalCount = 0;
  let paperCount = 0;
  let organicCount = 0;
  let recyclableCount = 0;
  let compostCount = 0;
  let landfillCount = 0;

  detections.forEach((det) => {
    const c = (det.class_name || '').toLowerCase();
    const action = (det.recommendation?.primary_action || '').toLowerCase();

    if (c.includes('plastic') || c.includes('bottle') || c.includes('container') || c.includes('wrapper') || c.includes('bag')) {
      plasticCount++;
    } else if (c.includes('metal') || c.includes('can') || c.includes('scrap')) {
      metalCount++;
    } else if (c.includes('paper') || c.includes('cardboard')) {
      paperCount++;
    } else if (c.includes('food') || c.includes('peel') || c.includes('garden')) {
      organicCount++;
    }

    if (action.includes('recycle') || action.includes('reuse')) {
      recyclableCount++;
    } else if (action.includes('compost')) {
      compostCount++;
    } else {
      landfillCount++;
    }
  });

  const total = detections.length;

  // Scientific estimates (EPA WARM & Circular Economy benchmarks)
  const co2AvoidedKg = (
    plasticCount * 0.18 +
    metalCount * 0.35 +
    paperCount * 0.15 +
    organicCount * 0.12
  ).toFixed(2);

  const waterSavedLiters = (
    paperCount * 2.8 +
    plasticCount * 1.5 +
    metalCount * 0.8
  ).toFixed(1);

  const energySavedKwh = (
    metalCount * 0.75 +
    plasticCount * 0.35 +
    paperCount * 0.2
  ).toFixed(2);

  const diversionRate = total > 0 ? Math.round(((recyclableCount + compostCount) / total) * 100) : 0;
  const phoneCharges = Math.round(parseFloat(energySavedKwh) * 80); // ~12Wh per smartphone charge

  let ratingBadge = { label: 'High Circular Impact', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' };
  if (diversionRate < 40) {
    ratingBadge = { label: 'Moderate Diversion', color: 'bg-amber-50 text-amber-700 border-amber-200' };
  } else if (diversionRate < 20) {
    ratingBadge = { label: 'Low Diversion Potential', color: 'bg-rose-50 text-rose-700 border-rose-200' };
  }

  return (
    <div className="bg-gradient-to-br from-emerald-50/60 via-white to-blue-50/40 border border-emerald-200/80 rounded-xl p-5 shadow-xs space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-emerald-100 pb-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-600 text-white flex items-center justify-center shadow-xs">
            <Leaf className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-bold text-sm text-slate-900 tracking-tight flex items-center gap-2">
              <span>Eco-Impact & Sustainability Metrics</span>
            </h3>
            <p className="text-[11px] text-slate-500">
              Quantifiable environmental savings when segregated according to AI recommendations.
            </p>
          </div>
        </div>

        <span className={`self-start sm:self-auto px-2.5 py-1 rounded-full text-[11px] font-semibold border ${ratingBadge.color} flex items-center gap-1`}>
          <Award className="w-3.5 h-3.5" />
          <span>{ratingBadge.label}</span>
        </span>
      </div>

      {/* 4 Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Metric 1: CO2 */}
        <div className="bg-white border border-slate-200/90 rounded-lg p-3 shadow-2xs">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">CO₂e Avoided</span>
            <Leaf className="w-3.5 h-3.5 text-emerald-600" />
          </div>
          <div className="text-lg font-black text-slate-900">
            {co2AvoidedKg} <span className="text-xs font-semibold text-slate-500">kg</span>
          </div>
          <p className="text-[10px] text-slate-400 mt-0.5">Diverted from atmosphere</p>
        </div>

        {/* Metric 2: Water */}
        <div className="bg-white border border-slate-200/90 rounded-lg p-3 shadow-2xs">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">Water Saved</span>
            <Droplets className="w-3.5 h-3.5 text-sky-600" />
          </div>
          <div className="text-lg font-black text-slate-900">
            {waterSavedLiters} <span className="text-xs font-semibold text-slate-500">Liters</span>
          </div>
          <p className="text-[10px] text-slate-400 mt-0.5">Conserved vs virgin supply</p>
        </div>

        {/* Metric 3: Energy */}
        <div className="bg-white border border-slate-200/90 rounded-lg p-3 shadow-2xs">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">Energy Conserved</span>
            <Zap className="w-3.5 h-3.5 text-amber-500" />
          </div>
          <div className="text-lg font-black text-slate-900">
            {energySavedKwh} <span className="text-xs font-semibold text-slate-500">kWh</span>
          </div>
          <p className="text-[10px] text-slate-400 mt-0.5">~{phoneCharges} smartphone charges</p>
        </div>

        {/* Metric 4: Diversion Rate */}
        <div className="bg-white border border-slate-200/90 rounded-lg p-3 shadow-2xs">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">Diversion Rate</span>
            <Recycle className="w-3.5 h-3.5 text-blue-600" />
          </div>
          <div className="text-lg font-black text-slate-900">
            {diversionRate}%
          </div>
          <p className="text-[10px] text-slate-400 mt-0.5">
            {recyclableCount + compostCount} of {total} items recovered
          </p>
        </div>
      </div>

      {/* Diversion Progress Bar & Milestone */}
      <div className="bg-white/80 border border-slate-200 rounded-lg p-3 space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="font-semibold text-slate-700 flex items-center gap-1.5">
            <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
            <span>Landfill Diversion Ratio</span>
          </span>
          <span className="font-bold text-slate-800">{diversionRate}% Recycled or Composted</span>
        </div>

        {/* Multi-segment bar */}
        <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden flex">
          <div
            style={{ width: `${(recyclableCount / total) * 100}%` }}
            className="bg-blue-600 transition-all duration-500"
            title={`Recyclable: ${recyclableCount}`}
          />
          <div
            style={{ width: `${(compostCount / total) * 100}%` }}
            className="bg-emerald-500 transition-all duration-500"
            title={`Compostable: ${compostCount}`}
          />
          <div
            style={{ width: `${(landfillCount / total) * 100}%` }}
            className="bg-slate-400 transition-all duration-500"
            title={`Landfill: ${landfillCount}`}
          />
        </div>

        <div className="flex items-center justify-between text-[10px] text-slate-500 pt-0.5">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-blue-600 inline-block" />
            <span>Recyclables ({recyclableCount})</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block" />
            <span>Organics ({compostCount})</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-slate-400 inline-block" />
            <span>Landfill / RDF ({landfillCount})</span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default EcoImpactCard;

