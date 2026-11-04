"""
Waste Knowledge Base for Garbage Waste Segregator.
Provides detailed metadata, environmental analysis, and segregation guidance for all waste classes.
"""

WASTE_CLASSES_INFO = {
    0: {
        "id": 0,
        "name": "plastic_bottle",
        "display": "Plastic Bottle",
        "material": "Polyethylene Terephthalate (PET / PETE #1)",
        "category": "Recyclable Dry Waste",
        "bin_type": "Blue Bin (Recyclables)",
        "bin_color": "#2563EB",
        "bin_icon": "🟦",
        "recyclable": True,
        "recyclability_score": 95,
        "biodegradable": False,
        "decomposition_time": "450 years",
        "decomposition_years": 450,
        "hazard_level": "Medium (Microplastics)",
        "disposal_instructions": [
            "Empty any remaining liquids completely",
            "Rinse briefly with clean water to prevent odor",
            "Crush or flatten bottle to save space in bin",
            "Replace cap tightly (caps are recycled with bottles)",
            "Deposit into the Blue Recyclables Bin"
        ],
        "environmental_impact": "Takes over 400 years to break down into toxic microplastics that contaminate soil and marine food webs. Recycling 1 ton of PET plastic saves 3.8 barrels of petroleum and 1.5 tons of carbon emissions.",
        "carbon_saved": "~0.08 kg CO₂ per bottle recycled",
        "eco_alternative": "Carry a refillable stainless steel or insulated glass water bottle."
    },
    1: {
        "id": 1,
        "name": "plastic_wrapper",
        "display": "Plastic Wrapper / Snack Packaging",
        "material": "Oriented Polypropylene (OPP) & Multilayer Metallized Film",
        "category": "Non-Recyclable Dry Waste / Landfill",
        "bin_type": "Grey/Black Bin (General Waste / Eco-Brick)",
        "bin_color": "#4B5563",
        "bin_icon": "⬛",
        "recyclable": False,
        "recyclability_score": 15,
        "biodegradable": False,
        "decomposition_time": "100 - 400 years",
        "decomposition_years": 250,
        "hazard_level": "High (Lightweight litter, wildlife hazard)",
        "disposal_instructions": [
            "Ensure wrapper is completely empty of food crumbs",
            "Check local grocery stores for specialized multi-layer plastic take-back",
            "If no soft-plastic drop-off is nearby, pack into an Eco-brick or place in General Waste Bin",
            "Do NOT mix with rigid paper/plastic recyclables as it clogs optical sorters"
        ],
        "environmental_impact": "Multi-material layers (aluminum + plastic) cannot be mechanically separated by standard municipal MRF facilities. Often blown into rivers and oceans by wind.",
        "carbon_saved": "~0.02 kg CO₂ when diverted to eco-bricks or waste-to-energy",
        "eco_alternative": "Buy bulk snacks in reusable cloth bags or make homemade snacks stored in glass jars."
    },
    2: {
        "id": 2,
        "name": "plastic_film_bag",
        "display": "Plastic Film & Carry Bag",
        "material": "Low-Density Polyethylene (LDPE #4) / High-Density Polyethylene (HDPE #2)",
        "category": "Soft Plastic (Specialized Recycling)",
        "bin_type": "Store Drop-off / Soft Plastics Depot (or Grey Bin)",
        "bin_color": "#6366F1",
        "bin_icon": "🟪",
        "recyclable": True,
        "recyclability_score": 40,
        "biodegradable": False,
        "decomposition_time": "20 - 500 years",
        "decomposition_years": 300,
        "hazard_level": "High (Clogs sorting gear, harms marine turtles)",
        "disposal_instructions": [
            "Never put loose bags in curbside recycling bins (they tangle recycling gears)",
            "Clean and shake out dry; remove receipts and staples",
            "Bundle multiple clean bags together into a single bag",
            "Drop off at designated supermarket soft plastic bins or take-back kiosks"
        ],
        "environmental_impact": "Turtles and seabirds mistake floating bags for jellyfish. Degradation under sunlight produces endocrine-disrupting chemicals.",
        "carbon_saved": "~0.05 kg CO₂ per bag recycled",
        "eco_alternative": "Keep foldable cotton, canvas, or jute tote bags in your vehicle or backpack."
    },
    3: {
        "id": 3,
        "name": "plastic_container",
        "display": "Rigid Plastic Container / Tub",
        "material": "High-Density Polyethylene (HDPE #2) or Polypropylene (PP #5)",
        "category": "Recyclable Dry Waste",
        "bin_type": "Blue Bin (Recyclables)",
        "bin_color": "#2563EB",
        "bin_icon": "🟦",
        "recyclable": True,
        "recyclability_score": 85,
        "biodegradable": False,
        "decomposition_time": "200 - 450 years",
        "decomposition_years": 350,
        "hazard_level": "Medium (Persistent polymer)",
        "disposal_instructions": [
            "Scrape out food residue and rinse with a sponge or gray water",
            "Remove plastic film seals and peel-off foil lids",
            "Nest similar containers to save storage space",
            "Place into the Blue Recyclables Bin"
        ],
        "environmental_impact": "HDPE and PP are prized commodities for manufacturing plastic lumber, playground equipment, recycling bins, and drainage pipes.",
        "carbon_saved": "~0.15 kg CO₂ per container recycled",
        "eco_alternative": "Opt for products in refillable jars or glass tubs; reuse containers for pantry bulk storage."
    },
    4: {
        "id": 4,
        "name": "paper",
        "display": "Paper / Documents / Newsprint",
        "material": "Cellulose Plant Fibers",
        "category": "Recyclable Dry Waste (or Compost if soiled)",
        "bin_type": "Blue Bin (Clean Paper) / Green Bin (Soiled)",
        "bin_color": "#10B981",
        "bin_icon": "🟩",
        "recyclable": True,
        "recyclability_score": 90,
        "biodegradable": True,
        "decomposition_time": "2 - 6 weeks",
        "decomposition_years": 0.1,
        "hazard_level": "Low (Biodegradable)",
        "disposal_instructions": [
            "Keep dry and clean; moisture degrades fiber quality",
            "Remove plastic wrap, windows from envelopes, and heavy tape",
            "If stained with food grease (e.g., pizza boxes), tear stained portion into Green Compost Bin",
            "Place clean dry sheets and newspapers into the Blue Paper Bin"
        ],
        "environmental_impact": "Recycling 1 ton of paper saves 17 mature trees, 7,000 gallons of water, and 4,000 kilowatts of electricity.",
        "carbon_saved": "~0.25 kg CO₂ per kg of paper recycled",
        "eco_alternative": "Embrace digital receipts, electronic invoices, and double-sided printing."
    },
    5: {
        "id": 5,
        "name": "cardboard_carton",
        "display": "Cardboard Box / Corrugated Carton",
        "material": "Kraft Corrugated Paperboard",
        "category": "Recyclable Dry Waste",
        "bin_type": "Blue Bin (Recyclables)",
        "bin_color": "#D97706",
        "bin_icon": "📦",
        "recyclable": True,
        "recyclability_score": 95,
        "biodegradable": True,
        "decomposition_time": "2 - 3 months",
        "decomposition_years": 0.25,
        "hazard_level": "Low (Natural organic fibers)",
        "disposal_instructions": [
            "Remove Styrofoam inserts, plastic bubble wrap, and shipping labels if feasible",
            "Cut or break down boxes so they lay completely flat",
            "Bundle large cartons with twine or slide into another carton",
            "Place in dry cardboard recycling section or Blue Bin"
        ],
        "environmental_impact": "Corrugated cardboard fibers can be recycled 5 to 7 times into new boxes, cartons, and paper bags before fibers become too short.",
        "carbon_saved": "~0.40 kg CO₂ per flattened carton recycled",
        "eco_alternative": "Reuse boxes for home storage, moving, or weed barrier in gardens."
    },
    6: {
        "id": 6,
        "name": "glass",
        "display": "Glass Bottle / Jar / Cullet",
        "material": "Silica, Soda Ash & Limestone (Fused Glass)",
        "category": "100% Infinitely Recyclable Waste",
        "bin_type": "Teal/Blue Bin (Glass Recycling)",
        "bin_color": "#06B6D4",
        "bin_icon": "🍶",
        "recyclable": True,
        "recyclability_score": 100,
        "biodegradable": False,
        "decomposition_time": "1,000,000+ years (Permanent)",
        "decomposition_years": 1000000,
        "hazard_level": "Medium (Sharp injury hazard when broken)",
        "disposal_instructions": [
            "Rinse away liquid or sauce residue",
            "Remove metal or cork caps (recycle metal caps separately)",
            "Do NOT smash glass—broken shards endanger handlers and contaminate paper bales",
            "Deposit unbroken jars and bottles into the Glass Bin"
        ],
        "environmental_impact": "Glass never decomposes in landfills, yet is 100% infinitely recyclable with ZERO loss of purity or quality! Over 1 ton of natural resources are saved for every ton of glass recycled.",
        "carbon_saved": "~0.31 kg CO₂ per glass bottle recycled",
        "eco_alternative": "Wash and reuse glass jars for spices, overnight oats, candle holders, or pantry organizing."
    },
    7: {
        "id": 7,
        "name": "metal_can",
        "display": "Metal Can / Aluminum Beverage Can",
        "material": "Aluminum Alloy (Beverage) / Tin-Coated Steel (Food Can)",
        "category": "100% Infinitely Recyclable Waste",
        "bin_type": "Blue Bin (Metals & Cans)",
        "bin_color": "#F59E0B",
        "bin_icon": "🥫",
        "recyclable": True,
        "recyclability_score": 98,
        "biodegradable": False,
        "decomposition_time": "50 - 200 years",
        "decomposition_years": 100,
        "hazard_level": "Low (Recycling superstar)",
        "disposal_instructions": [
            "Empty drink or food contents completely",
            "Quick rinse with cold water",
            "Crush can gently if desired to save space",
            "Leave pull tabs attached to the can",
            "Drop into the Blue Metals Bin"
        ],
        "environmental_impact": "Aluminum is a closed-loop recycling hero. Recycling an aluminum can saves 95% of the massive energy needed to extract and smelt bauxite ore. An aluminum can can be recycled and back on store shelves in just 60 days!",
        "carbon_saved": "~0.18 kg CO₂ per aluminum can recycled",
        "eco_alternative": "Choose canned drinks over single-use plastic bottles, or brew tea/coffee at home."
    },
    8: {
        "id": 8,
        "name": "metal_small_item",
        "display": "Small Metal Item / Cap / Foil / Hardware",
        "material": "Ferrous Steel, Brass, Copper or Aluminum Foil",
        "category": "Scrap Metal / Specialized Collection",
        "bin_type": "Blue Bin (Enclosed) / Scrap Yard",
        "bin_color": "#EF4444",
        "bin_icon": "🔩",
        "recyclable": True,
        "recyclability_score": 75,
        "biodegradable": False,
        "decomposition_time": "50 - 100 years",
        "decomposition_years": 75,
        "hazard_level": "Medium (Puncture/tangle hazard for MRF belts)",
        "disposal_instructions": [
            "Small items like bottle caps or paperclips can slip through MRF sorting screens",
            "Collect small metal caps inside an empty aluminum/steel soup can and crimp top closed",
            "Clean aluminum foil and scrunch into a ball larger than a golf ball",
            "Deposit in the Blue Metal Bin or local metal scrap collector"
        ],
        "environmental_impact": "Metal scrap melts down cleanly without degradation, saving vast open-pit mining operations and toxic tailings waste.",
        "carbon_saved": "~0.10 kg CO₂ per item recycled",
        "eco_alternative": "Repair mechanical hardware; repurpose sturdy screws, clips, and containers."
    },
    9: {
        "id": 9,
        "name": "styrofoam",
        "display": "Styrofoam / Expanded Polystyrene (EPS)",
        "material": "Expanded Polystyrene (EPS #6)",
        "category": "Non-Recyclable Domestic Waste / Specialized Drop-off",
        "bin_type": "Black/Grey Bin (Landfill) or EPS Depot",
        "bin_color": "#84CC16",
        "bin_icon": "🥡",
        "recyclable": False,
        "recyclability_score": 10,
        "biodegradable": False,
        "decomposition_time": "500+ years (Virtually non-biodegradable)",
        "decomposition_years": 500,
        "hazard_level": "Severe (High ocean micro-plastic fragmentation, styrene leaching)",
        "disposal_instructions": [
            "Never place in curbside blue/green recycling bins—shreds into millions of static beads",
            "Check for specialized regional EPS densification drop-off depots",
            "If no facility exists, bag securely so fragments cannot blow away, and dispose in Grey Landfill Bin",
            "Do NOT burn under any circumstances (releases toxic styrene fumes)"
        ],
        "environmental_impact": "Consists of 98% air and 2% petroleum-derived polystyrene. Fractures into billions of micro-beads ingested by fish and birds.",
        "carbon_saved": "~0.01 kg CO₂ when diverted to specialized densifiers",
        "eco_alternative": "Choose compostable molded pulp cardboard, bagasse (sugarcane), or mycelium mushroom packaging."
    }
}

# COCO label fallback mapping
COCO_FALLBACK_MAP = {
    "bottle": 0,
    "cup": 3,
    "wine glass": 6,
    "bowl": 3,
    "fork": 8,
    "knife": 8,
    "spoon": 8,
    "scissors": 8,
    "book": 4,
    "cell phone": 8,
}

NAME_TO_ID = {info["name"]: info["id"] for info in WASTE_CLASSES_INFO.values()}

def get_waste_info(class_id_or_name):
    """Retrieve full waste intelligence given either a numeric class id or a string name."""
    if isinstance(class_id_or_name, int) and class_id_or_name in WASTE_CLASSES_INFO:
        return WASTE_CLASSES_INFO[class_id_or_name]

    if isinstance(class_id_or_name, str):
        clean_name = class_id_or_name.lower().strip()
        if clean_name in NAME_TO_ID:
            return WASTE_CLASSES_INFO[NAME_TO_ID[clean_name]]
        if clean_name in COCO_FALLBACK_MAP:
            return WASTE_CLASSES_INFO[COCO_FALLBACK_MAP[clean_name]]

    # Generic fallback
    return {
        "id": -1,
        "name": str(class_id_or_name),
        "display": str(class_id_or_name).replace("_", " ").title(),
        "material": "Mixed / Unclassified Material",
        "category": "General Waste",
        "bin_type": "Grey Bin (General Waste)",
        "bin_color": "#64748B",
        "bin_icon": "🗑️",
        "recyclable": False,
        "recyclability_score": 30,
        "biodegradable": False,
        "decomposition_time": "Unknown",
        "decomposition_years": 50,
        "hazard_level": "Low",
        "disposal_instructions": ["Dispose in general waste bin or check local municipal guidelines."],
        "environmental_impact": "Proper segregation prevents non-recyclables from contaminating clean recyclable streams.",
        "carbon_saved": "N/A",
        "eco_alternative": "Reduce consumption of single-use items."
    }

def analyze_waste_collection(predictions):
    """Analyze a collection of detected items and return high-level segregation metrics."""
    if not predictions:
        return {
            "total_items": 0,
            "recyclable_count": 0,
            "non_recyclable_count": 0,
            "recyclability_rate": 0,
            "primary_bin": "No waste detected",
            "primary_bin_color": "#64748B",
            "max_decomposition": "N/A",
            "summary_advice": "No waste detected in image.",
            "bin_breakdown": {}
        }

    total = len(predictions)
    recyclable_count = sum(1 for p in predictions if p.get("waste_info", {}).get("recyclable", False))
    non_recyclable_count = total - recyclable_count
    recyclability_rate = round((recyclable_count / total) * 100, 1) if total > 0 else 0

    bin_counts = {}
    max_decomp_years = 0
    max_decomp_str = "N/A"

    for p in predictions:
        info = p.get("waste_info", {})
        bin_type = info.get("bin_type", "General Waste")
        bin_counts[bin_type] = bin_counts.get(bin_type, 0) + 1

        decomp_years = info.get("decomposition_years", 0)
        if decomp_years > max_decomp_years:
            max_decomp_years = decomp_years
            max_decomp_str = info.get("decomposition_time", f"{decomp_years} years")

    # Determine dominant primary bin
    primary_bin = max(bin_counts.items(), key=lambda x: x[1])[0] if bin_counts else "General Waste"

    # Color for primary bin
    primary_color = "#2563EB"
    if "Blue" in primary_bin:
        primary_color = "#2563EB"
    elif "Green" in primary_bin:
        primary_color = "#10B981"
    elif "Grey" in primary_bin or "Black" in primary_bin:
        primary_color = "#4B5563"
    elif "Teal" in primary_bin:
        primary_color = "#06B6D4"

    # Actionable summary advice
    if recyclability_rate >= 80:
        advice = f"Excellent! {recyclability_rate}% of detected items are recyclable. Rinse and place into the {primary_bin}."
    elif recyclability_rate >= 40:
        advice = f"Mixed waste detected ({recyclability_rate}% recyclable). Please separate recyclables (Blue bin) from soft plastics/general waste before disposal."
    else:
        advice = f"Predominantly non-recyclable or soft plastic waste. Place items into {primary_bin} to avoid contaminating municipal recycling streams."

    return {
        "total_items": total,
        "recyclable_count": recyclable_count,
        "non_recyclable_count": non_recyclable_count,
        "recyclability_rate": recyclability_rate,
        "primary_bin": primary_bin,
        "primary_bin_color": primary_color,
        "max_decomposition": max_decomp_str,
        "summary_advice": advice,
        "bin_breakdown": bin_counts
    }

