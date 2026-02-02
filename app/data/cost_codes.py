"""
Comprehensive cost code database for EV charging station installations.
Contains 83+ cost codes across 9 categories.
"""
from typing import List, Dict
from app.models import CostCode, CostCategory


# Complete cost code database
COST_CODES_DATA: List[Dict] = [
    # CONCRETE (CONC-001 to CONC-010)
    {
        "code": "CONC-001",
        "category": CostCategory.CONCRETE,
        "description": "4-inch concrete pad",
        "unit": "SF",
        "unit_cost": 8.50,
        "material_cost": 4.25,
        "labor_cost": 4.25
    },
    {
        "code": "CONC-002",
        "category": CostCategory.CONCRETE,
        "description": "6-inch concrete pad",
        "unit": "SF",
        "unit_cost": 12.00,
        "material_cost": 6.00,
        "labor_cost": 6.00
    },
    {
        "code": "CONC-003",
        "category": CostCategory.CONCRETE,
        "description": "Concrete curb stop",
        "unit": "EA",
        "unit_cost": 75.00,
        "material_cost": 35.00,
        "labor_cost": 40.00
    },
    {
        "code": "CONC-004",
        "category": CostCategory.CONCRETE,
        "description": "Concrete footings",
        "unit": "CY",
        "unit_cost": 450.00,
        "material_cost": 200.00,
        "labor_cost": 250.00
    },
    {
        "code": "CONC-005",
        "category": CostCategory.CONCRETE,
        "description": "Concrete encasement for conduit",
        "unit": "LF",
        "unit_cost": 18.00,
        "material_cost": 8.00,
        "labor_cost": 10.00
    },
    {
        "code": "CONC-006",
        "category": CostCategory.CONCRETE,
        "description": "Bollard concrete base",
        "unit": "EA",
        "unit_cost": 125.00,
        "material_cost": 55.00,
        "labor_cost": 70.00
    },
    {
        "code": "CONC-007",
        "category": CostCategory.CONCRETE,
        "description": "Concrete sealing/caulking",
        "unit": "LF",
        "unit_cost": 3.50,
        "material_cost": 1.50,
        "labor_cost": 2.00
    },
    {
        "code": "CONC-008",
        "category": CostCategory.CONCRETE,
        "description": "Reinforced concrete pad (with rebar)",
        "unit": "SF",
        "unit_cost": 15.00,
        "material_cost": 8.00,
        "labor_cost": 7.00
    },
    {
        "code": "CONC-009",
        "category": CostCategory.CONCRETE,
        "description": "Concrete saw cutting",
        "unit": "LF",
        "unit_cost": 6.00,
        "material_cost": 2.00,
        "labor_cost": 4.00
    },
    {
        "code": "CONC-010",
        "category": CostCategory.CONCRETE,
        "description": "Concrete removal and disposal",
        "unit": "CY",
        "unit_cost": 85.00,
        "material_cost": 0.00,
        "labor_cost": 85.00
    },
    
    # CONDUIT (COND-001 to COND-015)
    {
        "code": "COND-001",
        "category": CostCategory.CONDUIT,
        "description": "1-inch PVC conduit",
        "unit": "LF",
        "unit_cost": 3.25,
        "material_cost": 1.50,
        "labor_cost": 1.75
    },
    {
        "code": "COND-002",
        "category": CostCategory.CONDUIT,
        "description": "2-inch PVC conduit",
        "unit": "LF",
        "unit_cost": 4.50,
        "material_cost": 2.25,
        "labor_cost": 2.25
    },
    {
        "code": "COND-003",
        "category": CostCategory.CONDUIT,
        "description": "3-inch PVC conduit",
        "unit": "LF",
        "unit_cost": 6.75,
        "material_cost": 3.50,
        "labor_cost": 3.25
    },
    {
        "code": "COND-004",
        "category": CostCategory.CONDUIT,
        "description": "4-inch PVC conduit",
        "unit": "LF",
        "unit_cost": 9.00,
        "material_cost": 5.00,
        "labor_cost": 4.00
    },
    {
        "code": "COND-005",
        "category": CostCategory.CONDUIT,
        "description": "1-inch rigid metal conduit (RMC)",
        "unit": "LF",
        "unit_cost": 8.50,
        "material_cost": 5.00,
        "labor_cost": 3.50
    },
    {
        "code": "COND-006",
        "category": CostCategory.CONDUIT,
        "description": "2-inch rigid metal conduit (RMC)",
        "unit": "LF",
        "unit_cost": 12.00,
        "material_cost": 7.50,
        "labor_cost": 4.50
    },
    {
        "code": "COND-007",
        "category": CostCategory.CONDUIT,
        "description": "3-inch rigid metal conduit (RMC)",
        "unit": "LF",
        "unit_cost": 18.00,
        "material_cost": 11.00,
        "labor_cost": 7.00
    },
    {
        "code": "COND-008",
        "category": CostCategory.CONDUIT,
        "description": "4-inch rigid metal conduit (RMC)",
        "unit": "LF",
        "unit_cost": 24.00,
        "material_cost": 15.00,
        "labor_cost": 9.00
    },
    {
        "code": "COND-009",
        "category": CostCategory.CONDUIT,
        "description": "Conduit fittings and connectors",
        "unit": "EA",
        "unit_cost": 12.00,
        "material_cost": 6.00,
        "labor_cost": 6.00
    },
    {
        "code": "COND-010",
        "category": CostCategory.CONDUIT,
        "description": "Conduit elbows (90-degree)",
        "unit": "EA",
        "unit_cost": 18.00,
        "material_cost": 10.00,
        "labor_cost": 8.00
    },
    {
        "code": "COND-011",
        "category": CostCategory.CONDUIT,
        "description": "Junction boxes (large)",
        "unit": "EA",
        "unit_cost": 85.00,
        "material_cost": 45.00,
        "labor_cost": 40.00
    },
    {
        "code": "COND-012",
        "category": CostCategory.CONDUIT,
        "description": "Pull boxes (NEMA 3R)",
        "unit": "EA",
        "unit_cost": 150.00,
        "material_cost": 85.00,
        "labor_cost": 65.00
    },
    {
        "code": "COND-013",
        "category": CostCategory.CONDUIT,
        "description": "Expansion fittings",
        "unit": "EA",
        "unit_cost": 45.00,
        "material_cost": 25.00,
        "labor_cost": 20.00
    },
    {
        "code": "COND-014",
        "category": CostCategory.CONDUIT,
        "description": "Conduit supports/hangers",
        "unit": "EA",
        "unit_cost": 8.00,
        "material_cost": 4.00,
        "labor_cost": 4.00
    },
    {
        "code": "COND-015",
        "category": CostCategory.CONDUIT,
        "description": "Conduit sealing compound",
        "unit": "EA",
        "unit_cost": 15.00,
        "material_cost": 8.00,
        "labor_cost": 7.00
    },
    
    # WIRE (WIRE-001 to WIRE-012)
    {
        "code": "WIRE-001",
        "category": CostCategory.WIRE,
        "description": "#6 AWG copper wire (THHN/THWN)",
        "unit": "LF",
        "unit_cost": 2.50,
        "material_cost": 1.80,
        "labor_cost": 0.70
    },
    {
        "code": "WIRE-002",
        "category": CostCategory.WIRE,
        "description": "#4 AWG copper wire (THHN/THWN)",
        "unit": "LF",
        "unit_cost": 3.50,
        "material_cost": 2.50,
        "labor_cost": 1.00
    },
    {
        "code": "WIRE-003",
        "category": CostCategory.WIRE,
        "description": "#2 AWG copper wire (THHN/THWN)",
        "unit": "LF",
        "unit_cost": 5.00,
        "material_cost": 3.75,
        "labor_cost": 1.25
    },
    {
        "code": "WIRE-004",
        "category": CostCategory.WIRE,
        "description": "#1 AWG copper wire (THHN/THWN)",
        "unit": "LF",
        "unit_cost": 6.50,
        "material_cost": 5.00,
        "labor_cost": 1.50
    },
    {
        "code": "WIRE-005",
        "category": CostCategory.WIRE,
        "description": "1/0 AWG copper wire (THHN/THWN)",
        "unit": "LF",
        "unit_cost": 8.00,
        "material_cost": 6.25,
        "labor_cost": 1.75
    },
    {
        "code": "WIRE-006",
        "category": CostCategory.WIRE,
        "description": "2/0 AWG copper wire (THHN/THWN)",
        "unit": "LF",
        "unit_cost": 10.00,
        "material_cost": 7.85,
        "labor_cost": 2.15
    },
    {
        "code": "WIRE-007",
        "category": CostCategory.WIRE,
        "description": "3/0 AWG copper wire (THHN/THWN)",
        "unit": "LF",
        "unit_cost": 12.50,
        "material_cost": 9.80,
        "labor_cost": 2.70
    },
    {
        "code": "WIRE-008",
        "category": CostCategory.WIRE,
        "description": "4/0 AWG copper wire (THHN/THWN)",
        "unit": "LF",
        "unit_cost": 15.00,
        "material_cost": 11.75,
        "labor_cost": 3.25
    },
    {
        "code": "WIRE-009",
        "category": CostCategory.WIRE,
        "description": "250 kcmil copper wire",
        "unit": "LF",
        "unit_cost": 18.00,
        "material_cost": 14.00,
        "labor_cost": 4.00
    },
    {
        "code": "WIRE-010",
        "category": CostCategory.WIRE,
        "description": "500 kcmil copper wire",
        "unit": "LF",
        "unit_cost": 32.00,
        "material_cost": 26.00,
        "labor_cost": 6.00
    },
    {
        "code": "WIRE-011",
        "category": CostCategory.WIRE,
        "description": "Wire pulling lubricant",
        "unit": "EA",
        "unit_cost": 25.00,
        "material_cost": 18.00,
        "labor_cost": 7.00
    },
    {
        "code": "WIRE-012",
        "category": CostCategory.WIRE,
        "description": "Wire connectors and terminals",
        "unit": "EA",
        "unit_cost": 8.00,
        "material_cost": 5.00,
        "labor_cost": 3.00
    },
    
    # LABOR (LABOR-001 to LABOR-010)
    {
        "code": "LABOR-001",
        "category": CostCategory.LABOR,
        "description": "Licensed electrician (journeyman)",
        "unit": "HR",
        "unit_cost": 95.00,
        "material_cost": 0.00,
        "labor_cost": 95.00
    },
    {
        "code": "LABOR-002",
        "category": CostCategory.LABOR,
        "description": "Master electrician",
        "unit": "HR",
        "unit_cost": 125.00,
        "material_cost": 0.00,
        "labor_cost": 125.00
    },
    {
        "code": "LABOR-003",
        "category": CostCategory.LABOR,
        "description": "Electrician apprentice",
        "unit": "HR",
        "unit_cost": 65.00,
        "material_cost": 0.00,
        "labor_cost": 65.00
    },
    {
        "code": "LABOR-004",
        "category": CostCategory.LABOR,
        "description": "General laborer",
        "unit": "HR",
        "unit_cost": 45.00,
        "material_cost": 0.00,
        "labor_cost": 45.00
    },
    {
        "code": "LABOR-005",
        "category": CostCategory.LABOR,
        "description": "Equipment operator",
        "unit": "HR",
        "unit_cost": 75.00,
        "material_cost": 0.00,
        "labor_cost": 75.00
    },
    {
        "code": "LABOR-006",
        "category": CostCategory.LABOR,
        "description": "Foreman/supervisor",
        "unit": "HR",
        "unit_cost": 110.00,
        "material_cost": 0.00,
        "labor_cost": 110.00
    },
    {
        "code": "LABOR-007",
        "category": CostCategory.LABOR,
        "description": "Concrete finisher",
        "unit": "HR",
        "unit_cost": 70.00,
        "material_cost": 0.00,
        "labor_cost": 70.00
    },
    {
        "code": "LABOR-008",
        "category": CostCategory.LABOR,
        "description": "Excavation laborer",
        "unit": "HR",
        "unit_cost": 55.00,
        "material_cost": 0.00,
        "labor_cost": 55.00
    },
    {
        "code": "LABOR-009",
        "category": CostCategory.LABOR,
        "description": "Traffic control personnel",
        "unit": "HR",
        "unit_cost": 50.00,
        "material_cost": 0.00,
        "labor_cost": 50.00
    },
    {
        "code": "LABOR-010",
        "category": CostCategory.LABOR,
        "description": "Project engineer/PM",
        "unit": "HR",
        "unit_cost": 150.00,
        "material_cost": 0.00,
        "labor_cost": 150.00
    },
    
    # EQUIPMENT (EQUIP-001 to EQUIP-015)
    {
        "code": "EQUIP-001",
        "category": CostCategory.EQUIPMENT,
        "description": "Level 2 charging station (7.2 kW)",
        "unit": "EA",
        "unit_cost": 2500.00,
        "material_cost": 2500.00,
        "labor_cost": 0.00
    },
    {
        "code": "EQUIP-002",
        "category": CostCategory.EQUIPMENT,
        "description": "Level 2 charging station (19.2 kW)",
        "unit": "EA",
        "unit_cost": 4500.00,
        "material_cost": 4500.00,
        "labor_cost": 0.00
    },
    {
        "code": "EQUIP-003",
        "category": CostCategory.EQUIPMENT,
        "description": "DC Fast Charger (50 kW)",
        "unit": "EA",
        "unit_cost": 35000.00,
        "material_cost": 35000.00,
        "labor_cost": 0.00
    },
    {
        "code": "EQUIP-004",
        "category": CostCategory.EQUIPMENT,
        "description": "DC Fast Charger (150 kW)",
        "unit": "EA",
        "unit_cost": 75000.00,
        "material_cost": 75000.00,
        "labor_cost": 0.00
    },
    {
        "code": "EQUIP-005",
        "category": CostCategory.EQUIPMENT,
        "description": "DC Fast Charger (350 kW)",
        "unit": "EA",
        "unit_cost": 125000.00,
        "material_cost": 125000.00,
        "labor_cost": 0.00
    },
    {
        "code": "EQUIP-006",
        "category": CostCategory.EQUIPMENT,
        "description": "Electrical service panel (200A)",
        "unit": "EA",
        "unit_cost": 1200.00,
        "material_cost": 800.00,
        "labor_cost": 400.00
    },
    {
        "code": "EQUIP-007",
        "category": CostCategory.EQUIPMENT,
        "description": "Electrical service panel (400A)",
        "unit": "EA",
        "unit_cost": 2500.00,
        "material_cost": 1800.00,
        "labor_cost": 700.00
    },
    {
        "code": "EQUIP-008",
        "category": CostCategory.EQUIPMENT,
        "description": "Transformer (75 kVA)",
        "unit": "EA",
        "unit_cost": 8500.00,
        "material_cost": 7500.00,
        "labor_cost": 1000.00
    },
    {
        "code": "EQUIP-009",
        "category": CostCategory.EQUIPMENT,
        "description": "Transformer (150 kVA)",
        "unit": "EA",
        "unit_cost": 15000.00,
        "material_cost": 13500.00,
        "labor_cost": 1500.00
    },
    {
        "code": "EQUIP-010",
        "category": CostCategory.EQUIPMENT,
        "description": "Circuit breaker (2-pole, 50A)",
        "unit": "EA",
        "unit_cost": 125.00,
        "material_cost": 85.00,
        "labor_cost": 40.00
    },
    {
        "code": "EQUIP-011",
        "category": CostCategory.EQUIPMENT,
        "description": "Circuit breaker (3-pole, 100A)",
        "unit": "EA",
        "unit_cost": 250.00,
        "material_cost": 175.00,
        "labor_cost": 75.00
    },
    {
        "code": "EQUIP-012",
        "category": CostCategory.EQUIPMENT,
        "description": "Surge protection device",
        "unit": "EA",
        "unit_cost": 450.00,
        "material_cost": 350.00,
        "labor_cost": 100.00
    },
    {
        "code": "EQUIP-013",
        "category": CostCategory.EQUIPMENT,
        "description": "Energy meter (kWh)",
        "unit": "EA",
        "unit_cost": 650.00,
        "material_cost": 500.00,
        "labor_cost": 150.00
    },
    {
        "code": "EQUIP-014",
        "category": CostCategory.EQUIPMENT,
        "description": "Network gateway/controller",
        "unit": "EA",
        "unit_cost": 1200.00,
        "material_cost": 1000.00,
        "labor_cost": 200.00
    },
    {
        "code": "EQUIP-015",
        "category": CostCategory.EQUIPMENT,
        "description": "Backup battery system (optional)",
        "unit": "EA",
        "unit_cost": 5500.00,
        "material_cost": 5000.00,
        "labor_cost": 500.00
    },
    
    # SAFETY (SAFE-001 to SAFE-008)
    {
        "code": "SAFE-001",
        "category": CostCategory.SAFETY,
        "description": "Steel bollards (protective)",
        "unit": "EA",
        "unit_cost": 350.00,
        "material_cost": 250.00,
        "labor_cost": 100.00
    },
    {
        "code": "SAFE-002",
        "category": CostCategory.SAFETY,
        "description": "Wheel stops",
        "unit": "EA",
        "unit_cost": 85.00,
        "material_cost": 50.00,
        "labor_cost": 35.00
    },
    {
        "code": "SAFE-003",
        "category": CostCategory.SAFETY,
        "description": "Safety signage (ADA compliant)",
        "unit": "EA",
        "unit_cost": 75.00,
        "material_cost": 45.00,
        "labor_cost": 30.00
    },
    {
        "code": "SAFE-004",
        "category": CostCategory.SAFETY,
        "description": "Pavement markings (striping)",
        "unit": "LF",
        "unit_cost": 2.50,
        "material_cost": 1.25,
        "labor_cost": 1.25
    },
    {
        "code": "SAFE-005",
        "category": CostCategory.SAFETY,
        "description": "Security lighting",
        "unit": "EA",
        "unit_cost": 450.00,
        "material_cost": 325.00,
        "labor_cost": 125.00
    },
    {
        "code": "SAFE-006",
        "category": CostCategory.SAFETY,
        "description": "Emergency shut-off switch",
        "unit": "EA",
        "unit_cost": 175.00,
        "material_cost": 100.00,
        "labor_cost": 75.00
    },
    {
        "code": "SAFE-007",
        "category": CostCategory.SAFETY,
        "description": "Fire extinguisher cabinet",
        "unit": "EA",
        "unit_cost": 225.00,
        "material_cost": 150.00,
        "labor_cost": 75.00
    },
    {
        "code": "SAFE-008",
        "category": CostCategory.SAFETY,
        "description": "Safety barrier/fencing",
        "unit": "LF",
        "unit_cost": 35.00,
        "material_cost": 22.00,
        "labor_cost": 13.00
    },
    
    # SITE (SITE-001 to SITE-010)
    {
        "code": "SITE-001",
        "category": CostCategory.SITE,
        "description": "Excavation (trenching)",
        "unit": "LF",
        "unit_cost": 12.00,
        "material_cost": 0.00,
        "labor_cost": 12.00
    },
    {
        "code": "SITE-002",
        "category": CostCategory.SITE,
        "description": "Backfill and compaction",
        "unit": "LF",
        "unit_cost": 8.00,
        "material_cost": 2.00,
        "labor_cost": 6.00
    },
    {
        "code": "SITE-003",
        "category": CostCategory.SITE,
        "description": "Rock removal (additional)",
        "unit": "CY",
        "unit_cost": 150.00,
        "material_cost": 0.00,
        "labor_cost": 150.00
    },
    {
        "code": "SITE-004",
        "category": CostCategory.SITE,
        "description": "Site preparation/grading",
        "unit": "SF",
        "unit_cost": 2.50,
        "material_cost": 0.00,
        "labor_cost": 2.50
    },
    {
        "code": "SITE-005",
        "category": CostCategory.SITE,
        "description": "Utility locating service",
        "unit": "EA",
        "unit_cost": 350.00,
        "material_cost": 0.00,
        "labor_cost": 350.00
    },
    {
        "code": "SITE-006",
        "category": CostCategory.SITE,
        "description": "Traffic control setup",
        "unit": "DAY",
        "unit_cost": 450.00,
        "material_cost": 100.00,
        "labor_cost": 350.00
    },
    {
        "code": "SITE-007",
        "category": CostCategory.SITE,
        "description": "Erosion control measures",
        "unit": "EA",
        "unit_cost": 275.00,
        "material_cost": 125.00,
        "labor_cost": 150.00
    },
    {
        "code": "SITE-008",
        "category": CostCategory.SITE,
        "description": "Temporary power setup",
        "unit": "EA",
        "unit_cost": 500.00,
        "material_cost": 200.00,
        "labor_cost": 300.00
    },
    {
        "code": "SITE-009",
        "category": CostCategory.SITE,
        "description": "Site cleanup and disposal",
        "unit": "LOT",
        "unit_cost": 750.00,
        "material_cost": 250.00,
        "labor_cost": 500.00
    },
    {
        "code": "SITE-010",
        "category": CostCategory.SITE,
        "description": "Soil testing and analysis",
        "unit": "EA",
        "unit_cost": 425.00,
        "material_cost": 0.00,
        "labor_cost": 425.00
    },
    
    # RESTORATION (REST-001 to REST-008)
    {
        "code": "REST-001",
        "category": CostCategory.RESTORATION,
        "description": "Asphalt patching",
        "unit": "SF",
        "unit_cost": 8.00,
        "material_cost": 4.00,
        "labor_cost": 4.00
    },
    {
        "code": "REST-002",
        "category": CostCategory.RESTORATION,
        "description": "Full asphalt restoration",
        "unit": "SF",
        "unit_cost": 12.00,
        "material_cost": 6.50,
        "labor_cost": 5.50
    },
    {
        "code": "REST-003",
        "category": CostCategory.RESTORATION,
        "description": "Landscape restoration (grass/sod)",
        "unit": "SF",
        "unit_cost": 3.50,
        "material_cost": 2.00,
        "labor_cost": 1.50
    },
    {
        "code": "REST-004",
        "category": CostCategory.RESTORATION,
        "description": "Sidewalk repair",
        "unit": "SF",
        "unit_cost": 15.00,
        "material_cost": 8.00,
        "labor_cost": 7.00
    },
    {
        "code": "REST-005",
        "category": CostCategory.RESTORATION,
        "description": "Curb and gutter repair",
        "unit": "LF",
        "unit_cost": 45.00,
        "material_cost": 25.00,
        "labor_cost": 20.00
    },
    {
        "code": "REST-006",
        "category": CostCategory.RESTORATION,
        "description": "Driveway apron restoration",
        "unit": "SF",
        "unit_cost": 18.00,
        "material_cost": 10.00,
        "labor_cost": 8.00
    },
    {
        "code": "REST-007",
        "category": CostCategory.RESTORATION,
        "description": "Gravel/crushed stone restoration",
        "unit": "SF",
        "unit_cost": 4.50,
        "material_cost": 2.50,
        "labor_cost": 2.00
    },
    {
        "code": "REST-008",
        "category": CostCategory.RESTORATION,
        "description": "Pavement sealing",
        "unit": "SF",
        "unit_cost": 1.50,
        "material_cost": 0.75,
        "labor_cost": 0.75
    },
    
    # GROUNDING (GRND-001 to GRND-007)
    {
        "code": "GRND-001",
        "category": CostCategory.GROUNDING,
        "description": "Ground rod (8-foot copper)",
        "unit": "EA",
        "unit_cost": 85.00,
        "material_cost": 45.00,
        "labor_cost": 40.00
    },
    {
        "code": "GRND-002",
        "category": CostCategory.GROUNDING,
        "description": "Ground rod (10-foot copper)",
        "unit": "EA",
        "unit_cost": 110.00,
        "material_cost": 60.00,
        "labor_cost": 50.00
    },
    {
        "code": "GRND-003",
        "category": CostCategory.GROUNDING,
        "description": "Ground wire (#6 AWG bare copper)",
        "unit": "LF",
        "unit_cost": 2.25,
        "material_cost": 1.50,
        "labor_cost": 0.75
    },
    {
        "code": "GRND-004",
        "category": CostCategory.GROUNDING,
        "description": "Ground wire (#4 AWG bare copper)",
        "unit": "LF",
        "unit_cost": 3.00,
        "material_cost": 2.00,
        "labor_cost": 1.00
    },
    {
        "code": "GRND-005",
        "category": CostCategory.GROUNDING,
        "description": "Ground clamps and connectors",
        "unit": "EA",
        "unit_cost": 18.00,
        "material_cost": 10.00,
        "labor_cost": 8.00
    },
    {
        "code": "GRND-006",
        "category": CostCategory.GROUNDING,
        "description": "Grounding electrode conductor",
        "unit": "LF",
        "unit_cost": 4.50,
        "material_cost": 3.00,
        "labor_cost": 1.50
    },
    {
        "code": "GRND-007",
        "category": CostCategory.GROUNDING,
        "description": "Ground resistance testing",
        "unit": "EA",
        "unit_cost": 250.00,
        "material_cost": 0.00,
        "labor_cost": 250.00
    },
]


class CostCodeDatabase:
    """In-memory cost code database."""
    
    def __init__(self):
        self.cost_codes = [CostCode(**data) for data in COST_CODES_DATA]
        self._code_index = {cc.code: cc for cc in self.cost_codes}
        self._category_index = {}
        for cc in self.cost_codes:
            if cc.category not in self._category_index:
                self._category_index[cc.category] = []
            self._category_index[cc.category].append(cc)
    
    def get_by_code(self, code: str) -> CostCode:
        """Get a cost code by its code."""
        return self._code_index.get(code)
    
    def get_by_category(self, category: CostCategory) -> List[CostCode]:
        """Get all cost codes in a category."""
        return self._category_index.get(category, [])
    
    def get_all(self) -> List[CostCode]:
        """Get all cost codes."""
        return self.cost_codes
    
    def search(self, query: str) -> List[CostCode]:
        """Search cost codes by description."""
        query_lower = query.lower()
        return [cc for cc in self.cost_codes 
                if query_lower in cc.description.lower() or query_lower in cc.code.lower()]


# Global database instance
cost_code_db = CostCodeDatabase()
