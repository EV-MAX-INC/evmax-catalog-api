# EV MAX Catalog API

A SaaS-ready catalog API for managing and serving EV charging station installation cost data.

## Features

- **Cost Code Management**: 83+ cost code line items across 9 categories
  - Concrete (CONC)
  - Conduit (COND)
  - Wire (WIRE)
  - Labor (LABOR)
  - Equipment (EQUIP)
  - Safety (SAFE)
  - Site (SITE)
  - Restoration (REST)
  - Grounding (GRND)

- **Automated Bid Calculation**:
  - 10% material markup
  - 18% overhead calculation
  - 15% GA excavation contingency
  - 27% target profit margin

- **ROI Analysis**:
  - Payback period calculations
  - 10-year financial projections
  - Per-port and project-level pricing

- **Multiple Endpoints**:
  - Cost code lookups by category
  - BOM (Bill of Materials) generation
  - Automated bid calculations
  - ROI and financial projections
  - Benchmark comparisons

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the API:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
evmax-catalog-api/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Data models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── routers/             # API endpoints
│   └── data/                # Cost code data
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Testing

```bash
pytest
```

## License

Proprietary - EV MAX INC
