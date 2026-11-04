/**
 * AI-Based Smart Garbage Waste Segregator — Constants & Taxonomy
 * Exactly maps the 15-class target taxonomy and AutomataX theme parameters.
 */

// Target 15-Class Waste Taxonomy
export const TARGET_15_CLASSES = [
  { id: 0, name: 'plastic_bottle', display: 'Plastic Bottle', category: 'Plastics', bin: 'Blue (Recyclable)', color: '#2563EB' },
  { id: 1, name: 'plastic_wrapper', display: 'Plastic Wrapper', category: 'Plastics', bin: 'Grey (RDF / General)', color: '#475569' },
  { id: 2, name: 'plastic_bag', display: 'Plastic Bag', category: 'Plastics', bin: 'Soft Plastic Depot', color: '#6366F1' },
  { id: 3, name: 'plastic_container', display: 'Plastic Container', category: 'Plastics', bin: 'Blue (Recyclable)', color: '#0284C7' },
  { id: 4, name: 'paper', display: 'Paper', category: 'Paper & Fiber', bin: 'Blue (Paper)', color: '#16A34A' },
  { id: 5, name: 'cardboard_carton', display: 'Cardboard Carton', category: 'Paper & Fiber', bin: 'Blue (Cardboard)', color: '#D97706' },
  { id: 6, name: 'glass', display: 'Glass', category: 'Glass', bin: 'Teal/Blue (Glass)', color: '#0284C7' },
  { id: 7, name: 'metal_can', display: 'Metal Can', category: 'Metals', bin: 'Blue (Metals)', color: '#D97706' },
  { id: 8, name: 'metal_scrap', display: 'Metal Scrap', category: 'Metals', bin: 'Scrap Metal Depot', color: '#EA580C' },
  { id: 9, name: 'styrofoam', display: 'Styrofoam (EPS)', category: 'Polystyrene', bin: 'EPS Depot / Grey', color: '#64748B' },
  { id: 10, name: 'food_waste', display: 'Food Waste', category: 'Organics', bin: 'Green (Compost)', color: '#16A34A' },
  { id: 11, name: 'fruit_vegetable_peel', display: 'Fruit / Vegetable Peel', category: 'Organics', bin: 'Green (Compost)', color: '#16A34A' },
  { id: 12, name: 'garden_waste', display: 'Garden Waste', category: 'Organics', bin: 'Green (Yard Waste)', color: '#15803D' },
  { id: 13, name: 'textile', display: 'Textile', category: 'Textiles', bin: 'Clothing Donation', color: '#7C3AED' },
  { id: 14, name: 'e_waste', display: 'E-Waste', category: 'Electronics', bin: 'E-Waste Depot', color: '#DC2626' },
];

export const CLASS_NAMES = TARGET_15_CLASSES;

export const classIndex = (id) => TARGET_15_CLASSES.findIndex((cls) => cls.id === Number(id));

export const className = (id) => {
  const cls = TARGET_15_CLASSES.find((c) => c.id === Number(id));
  return cls ? cls.name : `unknown_${id}`;
};

export const displayClassName = (id) => {
  const cls = TARGET_15_CLASSES.find((c) => c.id === Number(id));
  return cls ? cls.display : `Class ${id}`;
};

export const getClassInfo = (idOrName) => {
  if (typeof idOrName === 'number') {
    return TARGET_15_CLASSES.find((c) => c.id === idOrName) || {
      id: -1,
      name: 'unknown',
      display: `Class ${idOrName}`,
      color: '#64748B',
      bin: 'General Waste',
    };
  }
  const clean = String(idOrName).toLowerCase().trim();
  return TARGET_15_CLASSES.find((c) => c.name === clean) || {
    id: -1,
    name: clean,
    display: String(idOrName).replace('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
    color: '#64748B',
    bin: 'General Waste',
  };
};

// AutomataX Restrained Disposal Action Badges
export const DISPOSAL_BADGES = {
  Recycle: {
    label: 'Recycle',
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    border: 'border-emerald-200',
    icon: '♻️',
  },
  Reuse: {
    label: 'Reuse',
    bg: 'bg-blue-50',
    text: 'text-blue-700',
    border: 'border-blue-200',
    icon: '🔄',
  },
  Compost: {
    label: 'Compost',
    bg: 'bg-green-50',
    text: 'text-green-700',
    border: 'border-green-200',
    icon: '🍂',
  },
  'RDF potential': {
    label: 'RDF Potential',
    bg: 'bg-amber-50',
    text: 'text-amber-700',
    border: 'border-amber-200',
    icon: '⚡',
  },
  'Special disposal': {
    label: 'Special Disposal',
    bg: 'bg-rose-50',
    text: 'text-rose-700',
    border: 'border-rose-200',
    icon: '⚠️',
  },
  'General waste': {
    label: 'General Waste',
    bg: 'bg-slate-100',
    text: 'text-slate-700',
    border: 'border-slate-200',
    icon: '🗑️',
  },
};

export const PLATFORM_INFO = {
  os: 'Edge / Cloud Environment',
  gpu: 'Hardware Accelerated',
  activeModel: 'YOLO11n Waste-15 Master Model',
  targetTaxonomy: '15 Target Classes',
  database: 'SQLite Database',
};

export const SPLIT_NAMES = ['train', 'val', 'test'];
