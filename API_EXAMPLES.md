# API Usage Examples

This document provides examples of how to use the EV MAX Catalog API.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. CORS is enabled for specified origins.

## Examples

### 1. Health Check

Check if the API is running and database is connected:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "database": "healthy",
  "timestamp": "2026-01-21T07:25:00.000000"
}
```

### 2. Create a Product

```bash
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "CONC-BEAM-001",
    "name": "Prestressed Concrete Beam - Standard",
    "category": "Structural",
    "base_cost": 450.00,
    "base_price": 675.00,
    "pricing_tiers": {
      "tier1": {"min_quantity": 10, "discount_percent": 5},
      "tier2": {"min_quantity": 50, "discount_percent": 10}
    },
    "material_specs": {
      "material": "Prestressed Concrete",
      "length_m": 12.0,
      "weight_kg": 2400
    },
    "compliance_codes": "ASTM C1012,EN 206,ACI 318"
  }'
```

### 3. Get All Products

```bash
curl http://localhost:8000/products/
```

With pagination:
```bash
curl "http://localhost:8000/products/?skip=0&limit=10"
```

### 4. Get a Single Product

```bash
curl http://localhost:8000/products/1
```

### 5. Update a Product

```bash
curl -X PUT http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "base_price": 700.00
  }'
```

### 6. Delete a Product

```bash
curl -X DELETE http://localhost:8000/products/1
```

### 7. Calculate a Quote

Calculate a quote with volume discount, seasonal pricing, and tier discount:

```bash
curl -X POST http://localhost:8000/products/quote \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 100,
    "season": "winter",
    "tier": "premium"
  }'
```

Response:
```json
{
  "product_id": 1,
  "product_name": "Prestressed Concrete Beam - Standard",
  "sku": "CONC-BEAM-001",
  "quantity": 100,
  "base_price": 675.00,
  "unit_price": 640.13,
  "volume_discount_percent": 10.0,
  "seasonal_adjustment_percent": 10.0,
  "tier_adjustment_percent": 5.0,
  "subtotal": 67500.00,
  "total_price": 64012.50,
  "margin_percent": 29.69,
  "margin_amount": 19012.50
}
```

## Quote Calculation Details

### Volume Discounts (5-20%)

- 10+ units: 5%
- 50+ units: 7%
- 100+ units: 10%
- 250+ units: 12%
- 500+ units: 15%
- 1000+ units: 20%

### Seasonal Pricing

- **Winter**: +10% (high demand)
- **Spring**: +5% (moderate demand)
- **Summer**: -5% (off-peak discount)
- **Fall**: 0% (standard pricing)

### Customer Tiers

- **Standard**: No additional discount
- **Premium**: 5% discount
- **Enterprise**: 10% discount

## OpenAPI Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Python Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a product
product_data = {
    "sku": "CONC-BEAM-001",
    "name": "Prestressed Concrete Beam",
    "category": "Structural",
    "base_cost": 450.00,
    "base_price": 675.00
}
response = requests.post(f"{BASE_URL}/products/", json=product_data)
product = response.json()
print(f"Created product: {product['id']}")

# Get quote
quote_data = {
    "product_id": product['id'],
    "quantity": 100,
    "season": "winter",
    "tier": "premium"
}
response = requests.post(f"{BASE_URL}/products/quote", json=quote_data)
quote = response.json()
print(f"Total price: ${quote['total_price']}")
print(f"Margin: {quote['margin_percent']}%")
```
