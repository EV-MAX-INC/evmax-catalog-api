# EV-MAX Catalog API

A high-performance SaaS API for managing 83+ construction cost codes with automated bid calculation and ROI analysis features for EV charging infrastructure projects.

## Features

- **Cost Code Management**: Comprehensive catalog of 83+ construction cost codes
- **Automated Bid Calculation**: Intelligent bid generation based on cost codes
- **ROI Analysis**: Financial analysis and return on investment calculations
- **Contextual Heritage Tracking**: Advanced chain tracking for bids and cost codes
- **Heritage Lineage Analysis**: Track dependencies and relationships across the system
- **RESTful API**: Modern FastAPI-based REST API
- **Database Support**: PostgreSQL for production, SQLite for development
- **Data Validation**: Pydantic models for robust data validation
- **Documentation**: Auto-generated API documentation with Swagger UI

## Technology Stack

- **Framework**: FastAPI 0.109+
- **Python**: 3.10+
- **Database**: SQLAlchemy 2.0+ with PostgreSQL/SQLite
- **Validation**: Pydantic 2.5+
- **Server**: Uvicorn (ASGI server)
- **Migrations**: Alembic

## Project Structure

```
evmax-catalog-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database configuration
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── cost_code.py        # Cost code model
│   │   ├── bid.py              # Bid model
│   │   └── contextual_chain.py # Contextual chain models
│   ├── routes/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── cost_codes.py       # Cost code endpoints
│   │   ├── bids.py             # Bid endpoints
│   │   └── contextual_chains.py # Contextual chain endpoints
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── cost_code.py        # Cost code schemas
│   │   ├── bid.py              # Bid schemas
│   │   └── contextual_chain.py # Contextual chain schemas
│   └── services/               # Business logic
│       ├── __init__.py
│       ├── cost_code_service.py
│       ├── bid_service.py
│       └── contextual_service.py
├── examples/                   # Usage examples
│   └── contextual_chain_usage.py
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_api.py
│   └── test_contextual_service.py
├── alembic/                    # Database migrations
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Poetry configuration
└── README.md                   # This file
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL (for production) or SQLite (for development)
- pip or Poetry package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/EV-MAX-INC/evmax-catalog-api.git
cd evmax-catalog-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
Or with Poetry:
```bash
poetry install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Cost Codes
- `GET /api/v1/cost-codes` - List all cost codes
- `GET /api/v1/cost-codes/{id}` - Get a specific cost code
- `POST /api/v1/cost-codes` - Create a new cost code
- `PUT /api/v1/cost-codes/{id}` - Update a cost code
- `DELETE /api/v1/cost-codes/{id}` - Delete a cost code

### Bids
- `GET /api/v1/bids` - List all bids
- `GET /api/v1/bids/{id}` - Get a specific bid
- `POST /api/v1/bids` - Create a new bid
- `POST /api/v1/bids/calculate` - Calculate bid based on cost codes

### ROI Analysis
- `POST /api/v1/analysis/roi` - Calculate ROI for a project

### Contextual Chains
- `POST /api/v1/contextual-chains/nodes` - Create a new contextual chain node
- `GET /api/v1/contextual-chains/nodes/{node_id}/analysis` - Analyze node heritage and metrics
- `GET /api/v1/contextual-chains/bids/{bid_id}/heritage` - Get bid heritage lineage
- `GET /api/v1/contextual-chains/snapshots/{node_id}` - Get complete chain snapshot
- `POST /api/v1/contextual-chains/bids/{bid_id}/contextualize` - Create contextual entry for existing bid

## Contextual Lathering String Heritage System

The Contextual Lathering Engine provides advanced heritage tracking capabilities for bids and cost codes:

### Overview

The system tracks relationships between cost codes, bids, and ROI analyses through a hierarchical chain structure. Each node in the chain maintains:

- **Heritage Lineage**: Complete ancestor tracking
- **Lathering Depth**: Distance from root nodes
- **Chain Metrics**: Comprehensive relationship analysis
- **Circular Dependency Detection**: Prevents invalid chains

### Key Concepts

#### Heritage Tracking
Each node maintains links to all ancestors, allowing you to:
- Trace the complete lineage of any bid or cost code
- Understand dependency relationships
- Analyze impact of changes through the chain

#### Lathering Depth
Nodes are assigned a depth based on their position in the chain:
- **Depth 0**: Root nodes (e.g., base cost codes)
- **Depth 1**: Direct children (e.g., bids using those cost codes)
- **Depth N**: Deeper relationships (e.g., ROI analyses of bids)

#### Chain Metrics
Each node can be analyzed to provide:
- Total ancestor count
- Node type distribution
- Relationship patterns
- Value flow through the chain

### Usage Examples

#### Create a Contextual Chain Node

```bash
curl -X POST http://localhost:8000/api/v1/contextual-chains/nodes \
  -H "Content-Type: application/json" \
  -d '{
    "node_id": "cost-code-123",
    "node_type": "cost_code",
    "parent_nodes": [],
    "metadata": {"description": "Base cost code"}
  }'
```

#### Analyze Node Heritage

```bash
curl http://localhost:8000/api/v1/contextual-chains/nodes/bid-456/analysis
```

Response:
```json
{
  "node_id": "bid-456",
  "lathering_depth": 1,
  "heritage_lineage": ["cost-code-123"],
  "total_ancestors": 1,
  "chain_metrics": {
    "node_type": "bid",
    "is_root": false,
    "is_leaf": true,
    "total_descendants": 0
  }
}
```

#### Get Chain Snapshot

```bash
curl http://localhost:8000/api/v1/contextual-chains/snapshots/cost-code-123?include_metrics=true
```

#### Contextualize an Existing Bid

```bash
curl -X POST http://localhost:8000/api/v1/contextual-chains/bids/123/contextualize
```

### Python Examples

See `examples/contextual_chain_usage.py` for comprehensive usage examples including:
- Creating multi-level chains
- Analyzing heritage lineage
- Generating snapshots
- Detecting circular dependencies

Run the examples:
```bash
python examples/contextual_chain_usage.py
```

### Configuration

Contextual chain behavior can be configured in `.env`:

```env
ENABLE_CONTEXTUAL_TRACKING=True      # Enable/disable tracking
MAX_CHAIN_DEPTH=50                    # Maximum allowed chain depth
CHAIN_SNAPSHOT_TTL=3600               # Snapshot cache TTL (seconds)
ENABLE_CIRCULAR_DEPENDENCY_CHECK=True # Enable cycle detection
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/ tests/
isort app/ tests/
```

### Linting
```bash
flake8 app/ tests/
mypy app/
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

## Configuration

Key configuration options in `.env`:

- `DATABASE_URL`: Database connection string
- `API_HOST`: API server host (default: 0.0.0.0)
- `API_PORT`: API server port (default: 8000)
- `DEBUG`: Enable debug mode (default: True)
- `CORS_ORIGINS`: Allowed CORS origins

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

Proprietary - EV-MAX-INC

## Support

For support, please contact the EV-MAX development team.
