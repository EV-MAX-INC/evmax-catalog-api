CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    base_cost DECIMAL(10,2) NOT NULL,
    base_price DECIMAL(10,2) NOT NULL,
    pricing_tiers JSONB NOT NULL DEFAULT '{}',
    material_specs JSONB DEFAULT '{}',
    compliance_codes TEXT[] DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO products (sku, category, name, description, base_cost, base_price, pricing_tiers, material_specs, compliance_codes) VALUES
('EVMAX-EV-36X24-L2-SGL', 'EV_CHARGING_FOUNDATION', 'Level 2 Single Post Foundation', 'Pre-engineered foundation for single Level 2 EV charging station', 592.59, 800.00, '{"standard": 800.00, "priority": 830.63, "emergency": 888.89}', '{"concrete_psi": 6000, "rebar":  "#5 @ 8in o.c."}', '{ACI318,NEC625,ADA309}'),
('EVMAX-EP-36X48-STD', 'EQUIPMENT_PAD', 'Standard Equipment Pad', 'Versatile precast pad for medium equipment', 72.59, 98.00, '{"standard": 98.00, "priority": 101.63, "emergency": 108.89}', '{"concrete_psi": 4000}', '{ACI318,ASTM C150}'),
('EVMAX-TX-90X106-UTL', 'TRANSFORMER_PAD', 'Transformer Pad Large', 'Heavy-duty pad for three-phase transformers up to 500 kVA', 1200.00, 1620.00, '{"standard": 1620.00, "priority":  1680.00, "emergency": 1800.00}', '{"concrete_psi": 6000}', '{IEEE C57.12.28,NEC250}')
ON CONFLICT (sku) DO NOTHING;
