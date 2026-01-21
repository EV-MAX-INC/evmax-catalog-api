"""
Sample data script for EV MAX Catalog API
This script demonstrates how to create sample products with the API
"""

sample_products = [
    {
        "sku": "CONC-BEAM-001",
        "name": "Prestressed Concrete Beam - Standard",
        "category": "Structural",
        "base_cost": 450.00,
        "base_price": 675.00,
        "pricing_tiers": {
            "tier1": {"min_quantity": 10, "discount_percent": 5},
            "tier2": {"min_quantity": 50, "discount_percent": 10},
            "tier3": {"min_quantity": 100, "discount_percent": 15}
        },
        "material_specs": {
            "material": "Prestressed Concrete",
            "length_m": 12.0,
            "width_m": 0.6,
            "height_m": 0.8,
            "weight_kg": 2400,
            "concrete_grade": "C40/50",
            "steel_grade": "B500B"
        },
        "compliance_codes": "ASTM C1012,EN 206,ACI 318"
    },
    {
        "sku": "CONC-WALL-002",
        "name": "Precast Concrete Wall Panel",
        "category": "Architectural",
        "base_cost": 280.00,
        "base_price": 420.00,
        "pricing_tiers": {
            "tier1": {"min_quantity": 20, "discount_percent": 7},
            "tier2": {"min_quantity": 100, "discount_percent": 12},
            "tier3": {"min_quantity": 250, "discount_percent": 18}
        },
        "material_specs": {
            "material": "Precast Concrete",
            "length_m": 3.0,
            "width_m": 0.15,
            "height_m": 6.0,
            "weight_kg": 1800,
            "concrete_grade": "C30/37",
            "finish": "Smooth"
        },
        "compliance_codes": "ASTM C90,EN 206,BS 8110"
    },
    {
        "sku": "CONC-SLAB-003",
        "name": "Hollow Core Slab - Heavy Duty",
        "category": "Flooring",
        "base_cost": 320.00,
        "base_price": 480.00,
        "pricing_tiers": {
            "tier1": {"min_quantity": 15, "discount_percent": 6},
            "tier2": {"min_quantity": 75, "discount_percent": 11},
            "tier3": {"min_quantity": 150, "discount_percent": 16}
        },
        "material_specs": {
            "material": "Prestressed Concrete",
            "length_m": 10.0,
            "width_m": 1.2,
            "height_m": 0.3,
            "weight_kg": 900,
            "concrete_grade": "C35/45",
            "load_capacity_kn": 15.0
        },
        "compliance_codes": "ASTM C1577,EN 1168,PCI MNL-124"
    }
]

sample_cost_codes = [
    {
        "code": "LAB-001",
        "description": "Skilled Labor - Concrete Work",
        "category": "Labor",
        "base_rate": 45.00
    },
    {
        "code": "MAT-001",
        "description": "High-Grade Concrete Mix",
        "category": "Material",
        "base_rate": 120.00
    },
    {
        "code": "EQP-001",
        "description": "Crane Rental - Heavy Lift",
        "category": "Equipment",
        "base_rate": 250.00
    }
]

sample_compliance_standards = [
    {
        "code": "ASTM-C1012",
        "name": "Standard Test Method for Length Change of Hydraulic-Cement Mortars Exposed to a Sulfate Solution",
        "description": "Test method for measuring length change of mortar specimens",
        "issuing_body": "ASTM International"
    },
    {
        "code": "EN-206",
        "name": "Concrete - Specification, performance, production and conformity",
        "description": "European standard for concrete specification",
        "issuing_body": "European Committee for Standardization"
    },
    {
        "code": "ACI-318",
        "name": "Building Code Requirements for Structural Concrete",
        "description": "Structural concrete design and construction requirements",
        "issuing_body": "American Concrete Institute"
    }
]

if __name__ == "__main__":
    print("Sample Data for EV MAX Catalog API")
    print("="*60)
    print(f"\n{len(sample_products)} Products")
    print(f"{len(sample_cost_codes)} Cost Codes")
    print(f"{len(sample_compliance_standards)} Compliance Standards")
    print("\nUse these with POST endpoints to populate the database.")
