# API Usage Examples

This document provides practical examples for using the EV MAX Catalog API.

## Starting the API

### Using Python directly
```bash
uvicorn app.main:app --reload
```

### Using Docker Compose (with PostgreSQL)
```bash
docker-compose up
```

The API will be available at `http://localhost:8000`

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example API Calls

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
    "status": "healthy",
    "api_version": "1.0.0",
    "cost_codes_loaded": 95,
    "categories": 9,
    "configuration": {
        "material_markup": "10.0%",
        "overhead_rate": "18.0%",
        "ga_excavation_contingency": "15.0%",
        "target_profit_margin": "27.0%",
        "roi_analysis_years": 10
    }
}
```

### 2. List All Cost Codes

```bash
curl http://localhost:8000/cost-codes/
```

### 3. Get Cost Codes by Category

```bash
curl http://localhost:8000/cost-codes/?category=Concrete
```

### 4. Get Specific Cost Code

```bash
curl http://localhost:8000/cost-codes/CONC-001
```

Response:
```json
{
    "code": "CONC-001",
    "category": "Concrete",
    "description": "4-inch concrete pad",
    "unit": "SF",
    "unit_cost": 8.5,
    "material_cost": 4.25,
    "labor_cost": 4.25
}
```

### 5. Search Cost Codes

```bash
curl "http://localhost:8000/cost-codes/search?q=copper"
```

### 6. Generate Bill of Materials (BOM)

#### L2 Charging Station BOM
```bash
curl -X POST http://localhost:8000/bom/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Downtown Plaza L2",
    "charging_type": "L2",
    "num_ports": 4,
    "site_conditions": "Urban parking lot",
    "excavation_length": 150
  }'
```

#### DC Fast Charging Station BOM
```bash
curl -X POST http://localhost:8000/bom/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Highway Rest Stop DC Fast",
    "charging_type": "DC_FAST",
    "num_ports": 2,
    "site_conditions": "Highway location",
    "excavation_length": 200
  }'
```

### 7. Calculate Project Bid

```bash
curl -X POST http://localhost:8000/bids/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Downtown Station A",
    "charging_type": "L2",
    "num_ports": 4,
    "excavation_length": 150
  }'
```

Response:
```json
{
    "project_name": "Downtown Station A",
    "charging_type": "L2",
    "num_ports": 4,
    "material_cost": 16267.5,
    "labor_cost": 12032.5,
    "subtotal": 28300.0,
    "material_markup": 0.1,
    "material_markup_amount": 1626.75,
    "overhead_rate": 0.18,
    "overhead_amount": 5094.0,
    "excavation_contingency": 0.15,
    "excavation_contingency_amount": 4245.0,
    "profit_margin": 0.27,
    "profit_amount": 10601.75,
    "total_cost": 49867.50,
    "cost_per_port": 12466.88
}
```

### 8. Analyze ROI (Return on Investment)

#### With Default Parameters
```bash
curl -X POST http://localhost:8000/roi/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Downtown Station A",
    "charging_type": "L2",
    "num_ports": 4,
    "excavation_length": 150
  }'
```

#### With Custom Revenue Parameters
```bash
curl -X POST "http://localhost:8000/roi/analyze?annual_revenue_per_port=6000&annual_operating_cost_per_port=1000" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Premium Location",
    "charging_type": "L2",
    "num_ports": 6,
    "excavation_length": 200
  }'
```

Response:
```json
{
    "project_name": "Downtown Station A",
    "initial_investment": 49867.50,
    "annual_revenue_per_port": 5000.0,
    "total_annual_revenue": 20000.0,
    "annual_operating_cost": 3200.0,
    "annual_net_income": 16800.0,
    "payback_period_years": 2.97,
    "roi_percentage": 33.69,
    "ten_year_net_profit": 118132.50,
    "ten_year_roi_percentage": 236.89
}
```

### 9. Compare with Competitors (Benchmarks)

```bash
curl -X POST http://localhost:8000/benchmarks/compare \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Market Analysis Project",
    "charging_type": "L2",
    "num_ports": 4,
    "excavation_length": 150
  }'
```

Response:
```json
{
    "project_name": "Market Analysis Project",
    "charging_type": "L2",
    "num_ports": 4,
    "evmax_cost_per_port": 12466.88,
    "evmax_total_cost": 49867.50,
    "keystone_cost_per_port": 12000.0,
    "keystone_total_cost": 48000.0,
    "gges_cost_per_port": 13500.0,
    "gges_total_cost": 54000.0,
    "evmax_vs_keystone_savings": -1867.50,
    "evmax_vs_gges_savings": 4132.50,
    "evmax_vs_keystone_percentage": -3.89,
    "evmax_vs_gges_percentage": 7.65
}
```

### 10. Get Industry Averages

```bash
curl http://localhost:8000/benchmarks/industry-averages
```

Response:
```json
{
    "l2_cost_per_port_keystone": 12000.0,
    "l2_cost_per_port_gges": 13500.0,
    "dc_fast_cost_per_port_keystone": 55000.0,
    "dc_fast_cost_per_port_gges": 60000.0,
    "industry_average_l2": 12750.0,
    "industry_average_dc_fast": 57500.0
}
```

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Calculate a bid
project = {
    "project_name": "My EV Station",
    "charging_type": "L2",
    "num_ports": 6,
    "excavation_length": 200
}

# Get BOM
bom_response = requests.post(f"{BASE_URL}/bom/generate", json=project)
bom = bom_response.json()
print(f"BOM Items: {len(bom)}")

# Calculate bid
bid_response = requests.post(f"{BASE_URL}/bids/calculate", json=project)
bid = bid_response.json()
print(f"Total Cost: ${bid['total_cost']:,.2f}")
print(f"Cost per Port: ${bid['cost_per_port']:,.2f}")

# Analyze ROI
roi_response = requests.post(
    f"{BASE_URL}/roi/analyze",
    json=project,
    params={
        "annual_revenue_per_port": 5500,
        "annual_operating_cost_per_port": 900
    }
)
roi = roi_response.json()
print(f"Payback Period: {roi['payback_period_years']:.2f} years")
print(f"10-Year ROI: {roi['ten_year_roi_percentage']:.2f}%")
```

## Cost Categories Reference

The API includes 95 cost codes across 9 categories:

1. **Concrete** (CONC-001 to CONC-010): Pads, footings, encasement
2. **Conduit** (COND-001 to COND-015): PVC and metal conduit, fittings
3. **Wire** (WIRE-001 to WIRE-012): Copper wire, various gauges
4. **Labor** (LABOR-001 to LABOR-010): Electricians, laborers, supervisors
5. **Equipment** (EQUIP-001 to EQUIP-015): Chargers, panels, transformers
6. **Safety** (SAFE-001 to SAFE-008): Bollards, signage, lighting
7. **Site** (SITE-001 to SITE-010): Excavation, grading, utilities
8. **Restoration** (REST-001 to REST-008): Asphalt, landscaping, pavement
9. **Grounding** (GRND-001 to GRND-007): Ground rods, wire, testing

## Business Logic

### Pricing Calculation Formula

```
Base Cost = Material Cost + Labor Cost

Material Markup (10%) = Material Cost × 0.10
Overhead (18%) = Base Cost × 0.18
GA Excavation Contingency (15%) = Base Cost × 0.15

Cost Before Profit = Base Cost + Material Markup + Overhead + Contingency
Profit (27%) = Cost Before Profit × 0.27

Total Cost = Cost Before Profit + Profit
Cost Per Port = Total Cost / Number of Ports
```

### ROI Calculation Formula

```
Annual Net Income = (Annual Revenue per Port × Number of Ports) - Annual Operating Cost

Payback Period (years) = Initial Investment / Annual Net Income
Annual ROI % = (Annual Net Income / Initial Investment) × 100

10-Year Net Profit = (Annual Net Income × 10) - Initial Investment
10-Year ROI % = (10-Year Net Profit / Initial Investment) × 100
```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run specific test categories:
```bash
pytest tests/test_api.py -v
pytest tests/test_services.py -v
pytest tests/test_data.py -v
```

## Deployment

### Production Considerations

1. **Environment Variables**: Update `.env` with production values
2. **Database**: Configure PostgreSQL connection
3. **CORS**: Restrict allowed origins in production
4. **Rate Limiting**: Consider adding rate limiting middleware
5. **Authentication**: Add API key or OAuth2 authentication
6. **Monitoring**: Set up logging and monitoring
7. **SSL/TLS**: Use HTTPS in production

### Docker Deployment

```bash
# Build the image
docker build -t evmax-catalog-api .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  evmax-catalog-api
```

## Support

For issues or questions, please refer to the main README.md or contact the development team.
