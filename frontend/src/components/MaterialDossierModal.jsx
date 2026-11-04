/**
 * MaterialDossierModal Component
 * Deep-dive handling protocol and environmental lifespan dossier for detected waste items
 * AI-Based Smart Garbage Waste Segregator
 */
import React, { useEffect } from 'react';
import { X, Info, CheckCircle2, AlertTriangle, Clock, Recycle, ShieldAlert, Sparkles } from 'lucide-react';
import { DISPOSAL_BADGES } from '../utils/constants';

// Lifespan & recycling codes dictionary
const MATERIAL_SPECS = {
  plastic_bottle: {
    code: '♳ PETE 1',
    lifespan: '450 Years in Landfill',
    hazard: 'Low (Microplastic risk if degraded in ocean)',
    prep: ['Drain all residual liquids', 'Remove plastic cap & ring if required by municipal facility', 'Crush bottle flat to conserve collection volume'],
    circular: 'High value: Can be flaked and spun into recycled polyester yarn or new food-grade bottles.'
  },
  plastic_wrapper: {
    code: '♶ PP 5 / Mixed Films',
    lifespan: '200 - 400 Years in Landfill',
    hazard: 'High windblown litter hazard, clogs standard sorting machinery',
    prep: ['Shake out crumbs and food residue', 'Bundle multiple wrappers together if soft plastic drop-off is available', 'Keep dry to avoid mold'],
    circular: 'Typically converted to Refuse-Derived Fuel (RDF) or downcycled plastic lumber.'
  },
  plastic_bag: {
    code: '♴ HDPE 2 / ♶ LDPE 4',
    lifespan: '100 - 300 Years in Landfill',
    hazard: 'High choke hazard for wildlife, tangles automated sorting rollers',
    prep: ['Empty completely', 'Never place loose in standard single-stream recycling bin', 'Return to specialized soft-plastic store collection bin'],
    circular: 'Re-granulated into composite decking and industrial packaging films.'
  },
  plastic_container: {
    code: '♴ HDPE 2 / ♷ OTHER 7',
    lifespan: '400 - 500 Years in Landfill',
    hazard: 'Moderate (Chemical/oil contamination risk)',
    prep: ['Scrape off food remnants', 'Rinse with small amount of warm water', 'Separate distinct lid if made of different polymer'],
    circular: 'High demand for automotive parts, detergent jugs, and drainage pipes.'
  },
  paper: {
    code: 'PAP 22',
    lifespan: '2 - 6 Weeks in Landfill',
    hazard: 'Generates methane gas if decomposing anaerobically in landfill',
    prep: ['Keep clean and completely dry', 'Do not shred unless required for confidentiality', 'Remove metallic spiral binders'],
    circular: 'Can be repulped up to 5 to 7 times into newspaper, egg cartons, and cardboard.'
  },
  cardboard_carton: {
    code: 'PAP 20',
    lifespan: '2 - 3 Months in Landfill',
    hazard: 'Low (High bulk volume in trucks and landfills)',
    prep: ['Flatten all boxes flat to save bin space', 'Remove excessive plastic shipping tapes', 'Avoid greasy pizza carton bases'],
    circular: 'Highest recycling efficiency: 100% repulpable into new corrugated boxes.'
  },
  glass: {
    code: 'GL 70 / 71',
    lifespan: '1,000,000+ Years (Never truly biodegrades)',
    hazard: 'Sharp cut risk for sanitation workers, contamination if shattered in commingled bins',
    prep: ['Rinse clear', 'Keep whole without deliberately smashing', 'Sort by color (clear/amber/green) if requested'],
    circular: 'Infinitely recyclable with zero loss of quality or purity.'
  },
  metal_can: {
    code: 'ALU 41 / FE 40',
    lifespan: '50 - 200 Years in Landfill',
    hazard: 'Sharp edges when opened, cuts hazard',
    prep: ['Rinse out residual beverage or soup', 'Push metal lid inside or compress can', 'Do not need to remove paper labels'],
    circular: 'Most energy-efficient material: recycling aluminum saves 95% of energy vs raw bauxite ore.'
  },
  metal_scrap: {
    code: 'FERROUS / NON-FERROUS',
    lifespan: '100 - 500 Years in Landfill',
    hazard: 'Puncture wounds, rust, heavy object hazard',
    prep: ['Keep free of hazardous chemicals, oils, or pressurized gases', 'Transport directly to authorized scrap metal yards'],
    circular: 'High monetary value: melted in electric arc furnaces for construction rebar.'
  },
  styrofoam: {
    code: '♶ PS 6 (Expanded Polystyrene)',
    lifespan: '500+ Years in Landfill',
    hazard: 'Extreme fragmentation risk into micro-beads, absorbs environmental toxins',
    prep: ['Keep dry and separate from food residues', 'Deliver to specialized EPS drop-off densification points', 'Do not crush into loose fragments'],
    circular: 'Compacted with heat densifiers into picture frames and architectural moldings.'
  },
  food_waste: {
    code: 'ORGANIC BIO-MASS',
    lifespan: '1 - 6 Months (Produces potent Methane CH₄ if trapped in landfill)',
    hazard: 'Odor, pest attraction, greenhouse gas generation',
    prep: ['Separate all plastic wrappers, twist-ties, and produce stickers', 'Place in green aeration bin or home vermicompost'],
    circular: 'Converted into nutrient-rich organic compost fertilizer or biogas electricity.'
  },
  fruit_vegetable_peel: {
    code: 'ORGANIC BIO-MASS',
    lifespan: '2 - 4 Weeks',
    hazard: 'None (Pure biological matter)',
    prep: ['Remove non-biodegradable PLU stickers', 'Ideal for compost pile, bokashi, or garden mulching'],
    circular: 'Generates nitrogen-rich compost and regenerates topsoil microbiology.'
  },
  garden_waste: {
    code: 'LIGNOCELLULOSIC BIOMASS',
    lifespan: '1 - 3 Months',
    hazard: 'Fire risk if dry; weed seeds contamination',
    prep: ['Cut branches to under 1 meter length', 'Bundle with natural twine, not plastic cord'],
    circular: 'Mulched into organic groundcover and municipal park soil conditioner.'
  },
  textile: {
    code: 'FIBER (Cotton/Poly)',
    lifespan: '20 - 200 Years in Landfill (Synthetic microfibers persist indefinitely)',
    hazard: 'Water dye pollution and landfill space saturation',
    prep: ['Wash and dry thoroughly', 'Pair shoes with laces tied together', 'Donate reusable clothes or deliver to textile shredding bin'],
    circular: 'Repurposed into acoustic insulation, industrial wiping rags, or yarn.'
  },
  e_waste: {
    code: 'WEEE / HAZMAT',
    lifespan: 'Indefinite (Heavy metals toxic in soil)',
    hazard: 'HIGH: Contains lead, cadmium, mercury, and fire-prone lithium batteries',
    prep: ['NEVER throw into municipal trash or recycling bin', 'Remove detachable batteries', 'Deliver to authorized e-waste reclamation hub'],
    circular: 'Critical resource recovery: gold, copper, lithium, and rare earth minerals reclaimed.'
  }
};

const MaterialDossierModal = ({ isOpen, onClose, detection }) => {
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

  if (!isOpen || !detection) return null;

  const rec = detection.recommendation || {};
  const className = detection.class_name || '';
  const spec = MATERIAL_SPECS[className] || {
    code: 'GENERAL RESIDUAL',
    lifespan: 'Variable',
    hazard: 'Assess individually',
    prep: ['Follow local sanitation guidelines', 'Keep dry and contained'],
    circular: 'Consult local recycling authority.'
  };

  const badge = DISPOSAL_BADGES[rec.primary_action] || DISPOSAL_BADGES['General waste'];

  return (
    <div
      className="fixed inset-0 z-[100] overflow-y-auto bg-slate-950/80 backdrop-blur-md p-4 sm:p-6 flex justify-center items-start sm:py-12"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-2xl max-w-lg w-full border border-slate-200 shadow-2xl overflow-hidden space-y-0 my-4 sm:my-6 animate-in fade-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 z-20 flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50/95 backdrop-blur-sm">
          <div className="flex items-center gap-2">
            <span className="w-6 h-6 rounded-md bg-blue-100 text-blue-700 text-xs font-bold flex items-center justify-center">
              #{detection.detection_id}
            </span>
            <h3 className="font-bold text-slate-900 text-base">{rec.display_name || className}</h3>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-200/60 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5 text-xs">
          {/* Bin & Action Highlight */}
          <div className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200 bg-slate-50">
            <div>
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
                Target Municipal Bin
              </span>
              <strong className="text-sm font-bold text-slate-900 block mt-0.5">
                {rec.municipal_bin || rec.bin_type || 'General Waste Bin'}
              </strong>
            </div>

            <span className={`px-2.5 py-1 rounded text-xs font-semibold border ${badge.bg} ${badge.text} ${badge.border}`}>
              {badge.icon} {badge.label}
            </span>
          </div>

          {/* Key Facts Grid */}
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200/80">
              <span className="text-[10px] text-slate-400 uppercase font-bold flex items-center gap-1 mb-1">
                <Recycle className="w-3 h-3 text-blue-600" />
                <span>Identification Code</span>
              </span>
              <strong className="text-slate-800 text-xs block">{spec.code}</strong>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200/80">
              <span className="text-[10px] text-slate-400 uppercase font-bold flex items-center gap-1 mb-1">
                <Clock className="w-3 h-3 text-amber-500" />
                <span>Landfill Lifespan</span>
              </span>
              <strong className="text-slate-800 text-xs block">{spec.lifespan}</strong>
            </div>
          </div>

          {/* Preparation Checklist */}
          <div className="space-y-2">
            <strong className="text-slate-800 font-bold uppercase tracking-wide text-[11px] block">
              Step-by-Step Handling Protocol:
            </strong>
            <ul className="space-y-1.5">
              {(spec.prep || rec.preparation_instructions || []).map((step, idx) => (
                <li key={idx} className="flex items-start gap-2 text-slate-600 bg-blue-50/30 p-2 rounded-lg border border-blue-100">
                  <CheckCircle2 className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
                  <span className="leading-snug">{step}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Environmental & Circular Value */}
          <div className="p-3 bg-emerald-50/50 border border-emerald-200 rounded-lg space-y-1 text-slate-700">
            <div className="font-bold text-[10px] uppercase text-emerald-700 flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Circular Economy Potential</span>
            </div>
            <p className="text-[11px] leading-relaxed text-emerald-900">
              {spec.circular}
            </p>
          </div>

          {/* Safety & Hazard Note */}
          <div className="p-3 bg-amber-50/60 border border-amber-200 rounded-lg space-y-1 text-slate-700">
            <div className="font-bold text-[10px] uppercase text-amber-700 flex items-center gap-1">
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>Environmental Risk Profile</span>
            </div>
            <p className="text-[11px] leading-relaxed text-amber-900">
              {spec.hazard}
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 bg-slate-50 border-t border-slate-100 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold shadow-xs transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};

export default MaterialDossierModal;

