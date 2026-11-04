"""
Waste Segregation Recommendation Engine
AI-Based Smart Garbage Waste Segregator Project

Rule-based recommendation system that takes detected waste classes and material context
to produce environmentally sound disposal, treatment, preparation, and safety actions.

Disposal Categories:
- Recycle
- Reuse
- Compost
- RDF potential
- Special disposal
- General waste / appropriate local disposal
"""

from typing import Dict, Any, List

# The authoritative 15-class target taxonomy
TARGET_TAXONOMY = {
    0: "plastic_bottle",
    1: "plastic_wrapper",
    2: "plastic_bag",
    3: "plastic_container",
    4: "paper",
    5: "cardboard_carton",
    6: "glass",
    7: "metal_can",
    8: "metal_scrap",
    9: "styrofoam",
    10: "food_waste",
    11: "fruit_vegetable_peel",
    12: "garden_waste",
    13: "textile",
    14: "e_waste",
}

# Master Recommendation Rules Database
RECOMMENDATION_RULES: Dict[str, Dict[str, Any]] = {
    "plastic_bottle": {
        "class_id": 0,
        "display_name": "Plastic Bottle",
        "primary_action": "Recycle",
        "disposal_category": "Recycle",
        "bin_type": "Blue Bin (Dry Recyclables)",
        "bin_color": "#2563EB",
        "badge_variant": "success",
        "material_description": "Polyethylene Terephthalate (PET / PETE #1) or High-Density Polyethylene (HDPE #2)",
        "explanation": "Clear and rigid PET beverage bottles have established mechanical recycling value. However, recyclability depends on cleanliness and lack of toxic chemical residues.",
        "preparation_instructions": [
            "Empty all remaining liquids completely.",
            "Rinse lightly with gray water to remove sugar and residue.",
            "Crush or flatten the bottle to reduce collection volume.",
            "Keep the plastic cap securely screwed on (modern MRF facilities recycle caps with bottles).",
            "Do not insert foreign objects inside the bottle."
        ],
        "safety_precautions": [
            "If the bottle stored hazardous chemicals (solvents, motor oil, pesticides), treat as Domestic Hazardous Waste instead of general recycling."
        ],
        "alternative_actions": [
            "Reuse: Repurpose sturdy bottles for plant watering or storage.",
            "RDF potential: If heavily soiled with oil and unrinsable, divert to Refuse Derived Fuel (RDF) or general waste."
        ],
        "condition_qualification": "Ordinary camera images cannot verify chemical residues inside bottles. Verify bottle contents before binning.",
        "environmental_impact": "Recycling 1 ton of PET saves ~3.8 barrels of crude oil and reduces greenhouse gas emissions by up to 1.5 tons.",
        "uncertainty_note": "Check material condition and local municipal recycling guidelines before disposal."
    },
    "plastic_wrapper": {
        "class_id": 1,
        "display_name": "Plastic Wrapper / Foil Packet",
        "primary_action": "RDF potential",
        "disposal_category": "RDF potential",
        "bin_type": "Grey/Black Bin (General Waste / RDF)",
        "bin_color": "#475569",
        "badge_variant": "warning",
        "material_description": "Multi-layer laminate film (Oriented Polypropylene + Aluminum Vapor Barrier)",
        "explanation": "Multi-layer snack packets and metallized candy wrappers cannot be mechanically separated into pure polymer streams at standard sorting facilities.",
        "preparation_instructions": [
            "Shake out all food crumbs and grease.",
            "Do not mix with clean paper or rigid plastic recycling bins.",
            "Pack into an Eco-brick (dense compaction into plastic bottle) if participating in local community programs.",
            "Otherwise deposit in the non-recyclable / dry combustible waste bin."
        ],
        "safety_precautions": [
            "Never incinerate openly; combustion of chlorinated plastic additives releases toxic dioxins and furans."
        ],
        "alternative_actions": [
            "Specialized take-back: Certain brands participate in closed-loop chemical recycling collection programs.",
            "General waste: Safe municipal engineered landfill when no waste-to-energy/RDF infrastructure exists."
        ],
        "condition_qualification": "Cannot determine single-layer vs multi-layer metallized structure from visual appearance alone.",
        "environmental_impact": "High litter dispersal risk. Takes 100–400 years to photodegrade into harmful environmental microplastics.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "plastic_bag": {
        "class_id": 2,
        "display_name": "Plastic Carry Bag / Film",
        "primary_action": "Special disposal",
        "disposal_category": "Special disposal",
        "bin_type": "Supermarket Soft Plastic Drop-Off / Grey Bin",
        "bin_color": "#6366F1",
        "badge_variant": "warning",
        "material_description": "Low-Density Polyethylene (LDPE #4) or High-Density Polyethylene (HDPE #2)",
        "explanation": "Plastic carry bags jam and wrap around spinning gears at automated Material Recovery Facilities (MRFs), shutting down entire sorting lines. They require dedicated collection depots.",
        "preparation_instructions": [
            "Never place loose in curbside blue recycling bins.",
            "Ensure the bag is clean, dry, and free of paper receipts or food scraps.",
            "Bundle multiple clean bags tightly inside a single bag.",
            "Deposit at dedicated grocery store soft-plastic take-back drop boxes."
        ],
        "safety_precautions": [
            "Keep out of reach of infants and small pets (suffocation hazard).",
            "Do not use degraded plastic bags for food storage."
        ],
        "alternative_actions": [
            "Reuse: Use as trash bin liners, dog waste bags, or moving packing cushions.",
            "General waste: If greasy or contaminated, dispose in the non-recyclable waste bin."
        ],
        "condition_qualification": "Biodegradable/compostable plastic bags look identical to standard PE bags in photos. Look for certified 'EN 13432' or 'OK Compost' labels.",
        "environmental_impact": "Major marine wildlife hazard; sea turtles mistake floating bags for jellyfish.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "plastic_container": {
        "class_id": 3,
        "display_name": "Plastic Container / Tub / Box",
        "primary_action": "Recycle",
        "disposal_category": "Recycle",
        "bin_type": "Blue Bin (Dry Recyclables)",
        "bin_color": "#2563EB",
        "badge_variant": "success",
        "material_description": "High-Density Polyethylene (HDPE #2) or Polypropylene (PP #5)",
        "explanation": "Rigid tubs, takeout boxes, and detergent containers are widely recycled when free of organic food residue.",
        "preparation_instructions": [
            "Scrape out all leftover food grease and sauces.",
            "Rinse thoroughly with water.",
            "Peel off peelable foil lids or clear plastic heat seals.",
            "Nest containers of identical resin to save collection volume."
        ],
        "safety_precautions": [
            "Containers previously holding corrosive chemicals or automotive fluids must be sent to Household Hazardous Waste."
        ],
        "alternative_actions": [
            "Reuse: Excellent for organizing hardware, garage screws, or plant potting.",
            "General waste: Heavily grease-soaked, scorched, or black carbon plastic (often invisible to optical sorters) may belong in general waste."
        ],
        "condition_qualification": "Black food takeout containers often fail automated NIR optical sorting. Check resin identification code on bottom.",
        "environmental_impact": "Recycling HDPE/PP saves up to 88% of virgin fossil energy compared to manufacturing new plastic resin.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "paper": {
        "class_id": 4,
        "display_name": "Paper / Documents / Newsprint",
        "primary_action": "Recycle",
        "disposal_category": "Recycle",
        "bin_type": "Blue Bin (Paper & Fiber)",
        "bin_color": "#16A34A",
        "badge_variant": "success",
        "material_description": "Cellulose Plant Fibers",
        "explanation": "Clean and dry paper is an easily recyclable resource that can be re-pulped 5–7 times.",
        "preparation_instructions": [
            "Keep paper strictly dry; wet fibers degrade and rot quickly.",
            "Remove plastic film wraps, metallic spiral binders, and large metal clips.",
            "Do not shred unless containing confidential data (shredded fibers are too short for high-grade recycling).",
            "Deposit in clean paper recycling stream."
        ],
        "safety_precautions": [
            "Handle paper stacks with care to avoid paper cuts.",
            "Keep away from heat sources and open flames."
        ],
        "alternative_actions": [
            "Compost: Shredded non-glossy, untreated paper is an excellent carbon ('brown') source for backyard compost piles.",
            "Reuse: Use blank reverse sides for scrap notes or packing material."
        ],
        "condition_qualification": "Soiled, greasy paper (e.g. food wrapping, grease-stained napkins) cannot be recycled and must go to Compost (Green Bin) or General Waste.",
        "environmental_impact": "Recycling 1 ton of paper saves 17 mature trees, 7,000 gallons of water, and 4,000 kWh of electrical energy.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "cardboard_carton": {
        "class_id": 5,
        "display_name": "Cardboard Carton / Corrugated Box",
        "primary_action": "Recycle",
        "disposal_category": "Recycle",
        "bin_type": "Blue Bin (Cardboard)",
        "bin_color": "#D97706",
        "badge_variant": "success",
        "material_description": "Corrugated Kraft Paperboard / Fluted Liner",
        "explanation": "Corrugated cardboard has one of the highest recovery and remanufacturing rates of any post-consumer packaging.",
        "preparation_instructions": [
            "Remove all plastic bubble wrap, Styrofoam peanuts, and air pillows inside.",
            "Cut, break down, or flatten boxes completely so they lie flat.",
            "Remove excessive heavy plastic packing tape where practical.",
            "Keep cardboard dry; do not leave exposed to rain."
        ],
        "safety_precautions": [
            "Watch out for protruding industrial staples or box cutter blades left inside."
        ],
        "alternative_actions": [
            "Reuse: Reuse sturdy shipping boxes for storage, moving, or mailing packages.",
            "Compost: Non-printed corrugated cardboard can be shredded for sheet mulching or weed suppression in gardens."
        ],
        "condition_qualification": "Grease-saturated sections (such as cheesy pizza box bottoms) cannot be recycled. Tear off clean box lids for recycling and discard soiled bases.",
        "environmental_impact": "Recycled cardboard requires 75% less energy and produces 50% fewer pollutants than virgin cardboard pulp.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "glass": {
        "class_id": 6,
        "display_name": "Glass Container / Bottle / Jar",
        "primary_action": "Recycle",
        "disposal_category": "Recycle",
        "bin_type": "Teal/Blue Bin (Glass Only)",
        "bin_color": "#0284C7",
        "badge_variant": "success",
        "material_description": "Fused Silica, Soda Ash & Limestone",
        "explanation": "Container glass is 100% infinitely recyclable without any loss in purity, quality, or chemical integrity.",
        "preparation_instructions": [
            "Rinse clean of liquid or food remnants.",
            "Remove metal or plastic caps (recycle metal caps separately).",
            "Labels do not need to be removed; they burn off during high-temperature cullet remelting.",
            "Keep jars and bottles intact; do not smash or break them before deposit."
        ],
        "safety_precautions": [
            "CAUTION: Broken glass poses a severe laceration hazard for sanitation workers.",
            "If glass is broken, wrap securely in heavy newspaper or cardboard, seal with tape, label clearly 'BROKEN GLASS', and place in General Waste."
        ],
        "alternative_actions": [
            "Reuse: Wash and sanitize for pantry grain storage, drinkware, or food canning.",
            "General waste: Heat-resistant cookware (Pyrex), light bulbs, ceramics, and window panes have different melting temperatures and MUST NOT go into container glass recycling."
        ],
        "condition_qualification": "Cannot distinguish borosilicate glass (Pyrex) or crystal from soda-lime glass from photographs. Only bottle/jar container glass is curbside recyclable.",
        "environmental_impact": "Every ton of glass recycled saves over 1 ton of raw natural resources and reduces CO2 emissions by ~315 kg.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "metal_can": {
        "class_id": 7,
        "display_name": "Metal Can / Aluminum Can",
        "primary_action": "Recycle",
        "disposal_category": "Recycle",
        "bin_type": "Blue Bin (Metals & Cans)",
        "municipal_bin": "Blue Bin (Metals & Cans)",
        "bin_color": "#2563EB",
        "badge_variant": "success",
        "material_description": "Aluminum Alloy (Beverage Cans) or Tin-Plated Steel (Food Tins)",
        "explanation": "Aluminum and tin-plated steel cans are highly sought-after circular commodities that can be re-smelted indefinitely.",
        "preparation_instructions": [
            "Empty all food remnants or beverages completely.",
            "Give a quick rinse with cold water.",
            "Crush beverage cans lightly if local facility permits to save space.",
            "Leave the pull tab attached to beverage cans.",
            "Tuck sharp tin can lids safely inside the can and crimp slightly."
        ],
        "safety_precautions": [
            "Opened tin lids have razor-sharp serrated edges. Press lid inside the can to prevent injuries to collection handlers."
        ],
        "alternative_actions": [
            "Reuse: Clean cans can serve as desk pencil holders, plant starters, or workshop organizer bins."
        ],
        "condition_qualification": "Confirm can did not contain pressurized flammable propellant or industrial spray paint.",
        "environmental_impact": "Recycling an aluminum can saves 95% of the energy needed to make a new one from raw bauxite ore. Recycled cans return to store shelves in 60 days.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "metal_scrap": {
        "class_id": 8,
        "display_name": "Metal Scrap / Hardware / Foil",
        "primary_action": "Recycle",
        "disposal_category": "Recycle",
        "bin_type": "Scrap Metal Facility / Blue Bin (Enclosed)",
        "municipal_bin": "Scrap Metal Facility / Blue Bin",
        "bin_color": "#2563EB",
        "badge_variant": "warning",
        "material_description": "Ferrous Steel, Brass, Copper, Aluminum, or Cast Iron",
        "explanation": "Metals have immense industrial recycling value, but loose small items (screws, nails, bottle caps) fall through MRF sorting screens and damage sorting belts.",
        "preparation_instructions": [
            "Collect small metal caps and screws inside a steel soup can and crimp closed.",
            "Roll clean aluminum foil into a tight ball at least 2 inches (5 cm) in diameter.",
            "Separate large metal objects (appliances, pipes, automotive parts) and deliver to a certified scrap metal yard.",
            "Ensure free of attached plastic, rubber, or electronics."
        ],
        "safety_precautions": [
            "Watch out for sharp wire ends, rusty nails, and puncture hazards. Wear sturdy work gloves."
        ],
        "alternative_actions": [
            "Reuse: Keep functional screws, bolts, hinges, and fasteners for future repair projects.",
            "Scrap dealer sale: Scrap metal recyclers pay cash for separated copper, brass, and aluminum."
        ],
        "condition_qualification": "Visual inspection cannot differentiate magnetic ferrous iron from non-ferrous alloys. Test with a magnet if separating.",
        "environmental_impact": "Recycling scrap steel saves 1,400 lbs of coal and 2,500 lbs of iron ore per ton recycled.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "styrofoam": {
        "class_id": 9,
        "display_name": "Styrofoam / Expanded Polystyrene (EPS)",
        "primary_action": "Special disposal",
        "disposal_category": "Special disposal",
        "bin_type": "EPS Drop-Off Depot / Grey Landfill Bin",
        "bin_color": "#64748B",
        "badge_variant": "danger",
        "material_description": "Expanded Polystyrene (EPS #6) — 98% Air, 2% Polymer",
        "explanation": "Styrofoam crumbles into billions of static micro-beads that contaminate standard recycling streams. It is virtually non-biodegradable and rejected by nearly all municipal curbside systems.",
        "preparation_instructions": [
            "Never place in curbside blue or green recycling bins.",
            "Check for localized EPS densification / cold-compaction drop-off depots.",
            "If no specialized EPS facility exists, place in a sealed bag inside the General Waste (Landfill) Bin so beads do not scatter.",
            "Do not burn under any circumstances."
        ],
        "safety_precautions": [
            "TOXIC FUMES: Burning polystyrene emits styrene monomer gas and dense toxic black soot. Keep away from heat.",
            "Keep away from children and aquatic bodies."
        ],
        "alternative_actions": [
            "Reuse: Packing peanuts and foam blocks can be reused for packing fragile parcels.",
            "General waste: If contaminated with meat blood or sauces, dispose in general waste."
        ],
        "condition_qualification": "Cannot determine contamination level from distance. Food-soiled foam is rejected everywhere.",
        "environmental_impact": "Takes 500+ years to break down. Ocean wildlife ingests floating fragments, causing starvation and endocrine disruption.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "food_waste": {
        "class_id": 10,
        "display_name": "Food Waste / Organic Scraps",
        "primary_action": "Compost",
        "disposal_category": "Compost",
        "bin_type": "Green Bin (Wet / Organic Waste)",
        "bin_color": "#16A34A",
        "badge_variant": "success",
        "material_description": "Biodegradable Organic Biomass",
        "explanation": "Food waste is organic matter rich in nitrogen and moisture. When sent to anaerobic landfills, it generates potent methane gas; composting converts it into nutrient-rich soil humus.",
        "preparation_instructions": [
            "Remove all plastic wrappers, price stickers, foil seals, and twist ties.",
            "Drain excess liquid before placing in compost bucket.",
            "Deposit in the municipal Green Organic Waste Bin or backyard compost bin.",
            "Mix with dry carbon materials (leaves, straw, shredded cardboard) in home compost."
        ],
        "safety_precautions": [
            "In home backyard composting, avoid meat, bones, dairy, and oils to prevent rodent pests and foul odors (municipal industrial composters can accept them)."
        ],
        "alternative_actions": [
            "Biogas / Anaerobic digestion: Generates clean biomethane gas and organic liquid fertilizer.",
            "Pet / Farm feed: Uncontaminated vegetable scraps can feed farm chickens or livestock."
        ],
        "condition_qualification": "Cannot determine cooked vs raw, or oil/salt content from photography.",
        "environmental_impact": "Diverting 1 kg of food waste from landfills prevents approximately 2.5 kg of CO2-equivalent methane emissions.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "fruit_vegetable_peel": {
        "class_id": 11,
        "display_name": "Fruit & Vegetable Peels",
        "primary_action": "Compost",
        "disposal_category": "Compost",
        "bin_type": "Green Bin (Organic / Vermicompost)",
        "bin_color": "#16A34A",
        "badge_variant": "success",
        "material_description": "Vegetable Cellulose, Water & Plant Nutrients",
        "explanation": "Peels, cores, and rinds are ideal organic 'green' inputs for rapid aerobic decomposition and vermicomposting (worm composting).",
        "preparation_instructions": [
            "Peel off small plastic PLU produce barcode stickers.",
            "Chop thick melon rinds or banana peels into smaller pieces for faster decomposition.",
            "Deposit into municipal Green Bin or home compost tumbler."
        ],
        "safety_precautions": [
            "Avoid adding excessive citrus peels or hot peppers to worm bins (sensitive worm skin)."
        ],
        "alternative_actions": [
            "Vermicomposting: Outstanding feedstock for Red Wiggler worms to produce vermicast.",
            "Bio-enzyme cleaner: Citrus peels can be fermented with water and jaggery into natural household cleaners."
        ],
        "condition_qualification": "Look out for non-biodegradable PLU stickers often adhering to fruit skins.",
        "environmental_impact": "Decomposes in 2 to 6 weeks under proper aerobic composting, enriching soil and sequestering carbon.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "garden_waste": {
        "class_id": 12,
        "display_name": "Garden Waste / Leaves / Twigs",
        "primary_action": "Compost",
        "disposal_category": "Compost",
        "bin_type": "Green Bin (Yard Waste / Mulch Depot)",
        "bin_color": "#15803D",
        "badge_variant": "success",
        "material_description": "Lignocellulosic Plant Residues",
        "explanation": "Leaves, plant trimmings, grass clippings, and small branches provide the essential carbon structure required for balanced soil composting.",
        "preparation_instructions": [
            "Separate thick tree branches (> 5 cm diameter) for municipal wood chipper processing.",
            "Shake off excessive clay or stones.",
            "Do not package in plastic garbage bags (use paper yard bags or bundle with natural twine).",
            "Keep free from treated lumber or synthetic weed barriers."
        ],
        "safety_precautions": [
            "Do not compost invasive weeds with mature seeds or plants diseased with fungal blight.",
            "Wear gloves to protect against thorns and stinging sap."
        ],
        "alternative_actions": [
            "Mulching: Shred leaves and twigs to spread across garden beds as moisture-retaining organic mulch.",
            "Biomass fuel: Wood chips can be pelletized for carbon-neutral biomass boilers."
        ],
        "condition_qualification": "Cannot detect pesticide residues or plant fungal pathogens from visual image.",
        "environmental_impact": "Prevents open burning of garden residues, which is a major source of particulate air pollution (PM2.5/PM10).",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "textile": {
        "class_id": 13,
        "display_name": "Textile / Fabric / Clothing",
        "primary_action": "Reuse",
        "disposal_category": "Reuse",
        "bin_type": "Clothing Donation Box / Textile Recycler",
        "bin_color": "#7C3AED",
        "badge_variant": "warning",
        "material_description": "Natural Cotton, Wool, or Synthetic Polyester/Nylon Fibers",
        "explanation": "Textiles require careful handling. Wearable garments should be reused or donated. Unwearable fabrics can be shredded into industrial insulation, wiping rags, or recycled yarn.",
        "preparation_instructions": [
            "Inspect condition: if clean and wearable, donate to charity or thrift stores.",
            "Wash and dry garments before donating.",
            "If torn, stained, or worn out, cut into household cleaning rags or deliver to specialized textile shredding drop-offs.",
            "Do NOT place in standard curbside plastic/paper recycling bins."
        ],
        "safety_precautions": [
            "Do not donate clothes soiled with biological fluids, motor oil, or mold."
        ],
        "alternative_actions": [
            "Upcycling / Mending: Darn holes, patch jeans, or sew into reusable tote bags.",
            "Textile recycling: Mechanical fiber reclamation produces carpet underlay, vehicle acoustics, and yarn."
        ],
        "condition_qualification": "Cannot determine fiber composition (e.g. 100% cotton vs polyester blend) or hygienic state from standard camera images.",
        "environmental_impact": "Extending garment life by just 9 months reduces carbon, water, and waste footprints by 20–30%.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    },
    "e_waste": {
        "class_id": 14,
        "display_name": "E-Waste / Electronics / Battery",
        "primary_action": "Special disposal",
        "disposal_category": "Special disposal",
        "bin_type": "Authorized E-Waste Depot / Battery Collection Box",
        "bin_color": "#DC2626",
        "badge_variant": "danger",
        "material_description": "Circuit Boards, Copper Wiring, Lithium-ion/Alkaline Cells & Heavy Metals",
        "explanation": "Electronic equipment contains toxic heavy metals (lead, mercury, cadmium, brominated flame retardants) alongside precious metals (gold, silver, palladium). NEVER put in household trash.",
        "preparation_instructions": [
            "CRITICAL: Keep separate from all household waste bins.",
            "If disposal item has a rechargeable battery (Lithium-ion), remove and tape the terminals with clear tape to prevent short-circuit fires.",
            "Wipe personal data / factory reset devices with digital storage before disposal.",
            "Drop off at certified e-Stewards / R2-certified electronic recyclers or municipal electronic waste roundups."
        ],
        "safety_precautions": [
            "FIRE HAZARD: Damaged or swollen lithium batteries can ignite violently if crushed in garbage trucks. Treat with utmost care.",
            "Do not disassemble CRT monitors or break mercury-containing backlights."
        ],
        "alternative_actions": [
            "Repair / Refurbish: Electronic repair centers can replace batteries or capacitors to restore function.",
            "Manufacturer trade-in: Many electronics brands offer trade-in credit or free mail-in recycling."
        ],
        "condition_qualification": "Cannot establish internal battery integrity or device functionality from photos.",
        "environmental_impact": "Proper recycling recovers 99% of valuable gold, silver, and copper while preventing toxic heavy metals from contaminating groundwater tables.",
        "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
    }
}

# Fallback recommendations for classes not explicitly in the 15-class dictionary
GENERIC_FALLBACK: Dict[str, Any] = {
    "class_id": -1,
    "display_name": "Unclassified Waste Item",
    "primary_action": "General waste",
    "disposal_category": "General waste / appropriate local disposal",
    "bin_type": "Grey/Black Bin (General Waste)",
    "bin_color": "#475569",
    "badge_variant": "neutral",
    "material_description": "Unknown or Mixed Composition",
    "explanation": "Object category could not be unambiguously mapped. Segregate carefully to avoid contaminating clean recycling streams.",
    "preparation_instructions": [
        "Inspect the physical object for manufacturer recycling resin codes or disposal labels.",
        "If recyclable, ensure it is clean and dry.",
        "When in doubt, dispose in general waste to prevent recycling batch rejection."
    ],
    "safety_precautions": [
        "Do not touch unfamiliar sharp or chemical containers without protective gloves."
    ],
    "alternative_actions": [
        "Check local municipal waste authority guidelines for specific sorting categories."
    ],
    "condition_qualification": "Material condition, cleanliness, and exact composition cannot be established from this image.",
    "environmental_impact": "Proper source segregation is the first line of defense in sustainable municipal waste management.",
    "uncertainty_note": "Check material condition and local recycling guidelines before disposal."
}

def get_recommendation_for_class(class_name_or_id: Any) -> Dict[str, Any]:
    """
    Retrieve full segregation recommendation, disposal category, preparation instructions,
    and safety notes for a given class name or class ID.
    """
    res = None

    # 1. By integer ID
    if isinstance(class_name_or_id, int) and 0 <= class_name_or_id <= 14:
        cname = TARGET_TAXONOMY.get(class_name_or_id)
        if cname and cname in RECOMMENDATION_RULES:
            res = RECOMMENDATION_RULES[cname].copy()

    # 2. By string name
    elif isinstance(class_name_or_id, str):
        normalized = class_name_or_id.strip().lower()
        if normalized in RECOMMENDATION_RULES:
            res = RECOMMENDATION_RULES[normalized].copy()
        else:
            # Common synonyms & source dataset mappings
            synonyms = {
                "plastic_film_bag": "plastic_bag",
                "plastic film bag": "plastic_bag",
                "carrier bag": "plastic_bag",
                "garbage bag": "plastic_bag",
                "clear plastic bottle": "plastic_bottle",
                "other plastic bottle": "plastic_bottle",
                "crisp packet": "plastic_wrapper",
                "snack wrapper": "plastic_wrapper",
                "disposable plastic cup": "plastic_container",
                "plastic cup": "plastic_container",
                "tupperware": "plastic_container",
                "food container": "plastic_container",
                "magazine paper": "paper",
                "normal paper": "paper",
                "drink carton": "cardboard_carton",
                "corrugated carton": "cardboard_carton",
                "pizza box": "cardboard_carton",
                "glass bottle": "glass",
                "glass jar": "glass",
                "drink can": "metal_can",
                "food can": "metal_can",
                "can": "metal_can",
                "metal_small_item": "metal_scrap",
                "aluminium foil": "metal_scrap",
                "bottle cap": "metal_scrap",
                "pop tab": "metal_scrap",
                "foam cup": "styrofoam",
                "foam container": "styrofoam",
                "battery": "e_waste",
                "electronics": "e_waste",
                "leaf": "garden_waste",
                "leaves": "garden_waste",
                "peel": "fruit_vegetable_peel",
                "vegetable peel": "fruit_vegetable_peel",
                "clothes": "textile",
                "rags": "textile",
            }
            if normalized in synonyms:
                target = synonyms[normalized]
                if target in RECOMMENDATION_RULES:
                    res = RECOMMENDATION_RULES[target].copy()

    # 3. Fallback
    if not res:
        fallback = GENERIC_FALLBACK.copy()
        fallback["display_name"] = str(class_name_or_id).replace("_", " ").title()
        res = fallback

    # Guarantee both bin_type and municipal_bin keys exist
    if "municipal_bin" not in res:
        res["municipal_bin"] = res.get("bin_type", "General Waste")
    if "bin_type" not in res:
        res["bin_type"] = res.get("municipal_bin", "General Waste")

    return res

def analyze_detections_summary(detections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize a collection of detections into high-level environmental actions.
    Computes category breakdown, dominant disposal route, and actionable guidance.
    """
    if not detections:
        return {
            "total_objects": 0,
            "primary_disposal": "No waste detected",
            "primary_bin": "No bin required",
            "primary_bin_color": "#64748B",
            "recyclable_count": 0,
            "compostable_count": 0,
            "special_disposal_count": 0,
            "rdf_count": 0,
            "general_waste_count": 0,
            "recyclability_rate": 0.0,
            "summary_advice": "No waste objects were detected in the image.",
            "disposal_breakdown": {},
            "bin_breakdown": {},
            "requires_safety_warning": False
        }

    total = len(detections)
    disposal_counts: Dict[str, int] = {}
    bin_counts: Dict[str, int] = {}
    has_safety_warning = False

    recyclable_count = 0
    compostable_count = 0
    special_disposal_count = 0
    rdf_count = 0
    general_waste_count = 0
    reuse_count = 0

    for det in detections:
        rec = det.get("recommendation", {})
        action = rec.get("primary_action", "General waste")
        bin_type = rec.get("bin_type") or rec.get("municipal_bin") or "General Waste"

        disposal_counts[action] = disposal_counts.get(action, 0) + 1
        bin_counts[bin_type] = bin_counts.get(bin_type, 0) + 1

        if action == "Recycle":
            recyclable_count += 1
        elif action == "Compost":
            compostable_count += 1
        elif action == "Special disposal":
            special_disposal_count += 1
        elif action == "RDF potential":
            rdf_count += 1
        elif action == "Reuse":
            reuse_count += 1
        else:
            general_waste_count += 1

        if rec.get("badge_variant") == "danger" or rec.get("safety_precautions"):
            has_safety_warning = True

    recyclability_rate = round((recyclable_count / total) * 100, 1)

    # Determine dominant stream
    stream_scores = {
        "Recycle": recyclable_count,
        "Compost": compostable_count,
        "Reuse": reuse_count,
        "Special disposal": special_disposal_count,
        "RDF potential": rdf_count,
        "General waste": general_waste_count
    }
    primary_disposal = max(stream_scores.items(), key=lambda x: x[1])[0]

    if primary_disposal == "Recycle":
        primary_bin = "Blue Bin (Dry Recyclables & Metals)"
        primary_color = "#2563EB"
    elif primary_disposal == "Compost":
        primary_bin = "Green Bin (Organic / Compost)"
        primary_color = "#16A34A"
    elif primary_disposal == "Reuse":
        primary_bin = "Donation / Textile Reclaim"
        primary_color = "#7C3AED"
    elif primary_disposal == "Special disposal":
        primary_bin = "Special Take-Back / E-Waste Depot"
        primary_color = "#DC2626"
    elif primary_disposal == "RDF potential":
        primary_bin = "Grey/Black Bin (RDF / Energy Recovery)"
        primary_color = "#475569"
    else:
        primary_bin = "Grey/Black Bin (General Waste)"
        primary_color = "#475569"

    # Actionable summary advice
    non_recyclable_residuals = rdf_count + general_waste_count
    if special_disposal_count > 0:
        advice = f"Special Handling Alert: Contains {special_disposal_count} item(s) requiring separate Take-Back / hazardous drop-off. Segregate these before discarding remaining waste."
    elif recyclable_count > 0 and non_recyclable_residuals > 0:
        advice = f"Mixed Stream ({recyclability_rate}% Recovery): Deposit {recyclable_count} recyclable item(s) in the Blue Bin. Divert {non_recyclable_residuals} wrapper/residual item(s) to the Grey Bin (RDF)."
    elif compostable_count > 0 and recyclable_count > 0:
        advice = f"Dual Segregation Stream: Separate {recyclable_count} dry recyclable(s) into the Blue Bin and {compostable_count} organic scrap(s) into the Green Compost Bin."
    elif recyclability_rate >= 75.0:
        advice = f"High Recyclability ({recyclability_rate}% Recovery): Empty, rinse, and deposit containers into the {primary_bin}."
    elif compostable_count > 0:
        advice = f"100% Biodegradable Biomass: Place all items into the Green Organic Bin or garden composter."
    elif rdf_count > 0:
        advice = f"Refuse-Derived Fuel: Keep plastic packaging dry for non-recyclable combustible thermal recovery."
    else:
        advice = f"General Waste Stream: Deposit in the {primary_bin}. Verify local municipal recovery guidelines."

    return {
        "total_objects": total,
        "primary_disposal": primary_disposal,
        "primary_bin": primary_bin,
        "primary_bin_color": primary_color,
        "recyclable_count": recyclable_count,
        "compostable_count": compostable_count,
        "special_disposal_count": special_disposal_count,
        "rdf_count": rdf_count,
        "general_waste_count": general_waste_count,
        "recyclability_rate": recyclability_rate,
        "summary_advice": advice,
        "disposal_breakdown": disposal_counts,
        "bin_breakdown": bin_counts,
        "requires_safety_warning": has_safety_warning
    }

