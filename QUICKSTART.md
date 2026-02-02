# Quick Start Guide - EV MAX Catalog API

## Installation & Startup

### Method 1: Python Direct
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload

# Access at http://localhost:8000
```

### Method 2: Docker
```bash
# Build and run
docker build -t evmax-catalog-api .
docker run -p 8000:8000 evmax-catalog-api
```

### Method 3: Docker Compose
```bash
# Start with PostgreSQL
docker-compose up
```

## Quick Test

```bash
# Health check
curl http://localhost:8000/health

# List cost codes
curl http://localhost:8000/cost-codes/

# Calculate a bid
curl -X POST http://localhost:8000/bids/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Test Project",
    "charging_type": "L2",
    "num_ports": 4,
    "excavation_length": 150
  }'
```

## Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | API status |
| `/cost-codes/` | GET | List all cost codes |
| `/cost-codes/{code}` | GET | Get specific code |
| `/bom/generate` | POST | Generate BOM |
| `/bids/calculate` | POST | Calculate bid |
| `/roi/analyze` | POST | ROI analysis |
| `/benchmarks/compare` | POST | Compare competitors |
| `/docs` | GET | Interactive docs |

## Project Structure

```
evmax-catalog-api/
├── app/              # Application code
│   ├── main.py       # FastAPI app
│   ├── config.py     # Settings
│   ├── data/         # Cost codes
│   ├── models/       # Data models
│   ├── routers/      # API endpoints
│   └── services/     # Business logic
├── tests/            # Test suite
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

## Configuration

Edit `.env` file or set environment variables:
- `MATERIAL_MARKUP=0.10` (10%)
- `OVERHEAD_RATE=0.18` (18%)
- `GA_EXCAVATION_CONTINGENCY=0.15` (15%)
- `TARGET_PROFIT_MARGIN=0.27` (27%)
- `ROI_ANALYSIS_YEARS=10`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v
```

## Documentation

- **README.md** - Full documentation
- **EXAMPLES.md** - Detailed usage examples
- **SUMMARY.md** - Implementation summary
- **http://localhost:8000/docs** - Interactive API docs

## Support

For more information, see the complete documentation files.
