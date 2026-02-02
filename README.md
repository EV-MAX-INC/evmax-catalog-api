# EV-MAX Catalog API

A high-performance SaaS API for managing 83+ construction cost codes with automated bid calculation and ROI analysis features for EV charging infrastructure projects.

## Features

- **Cost Code Management**: Comprehensive catalog of 83+ construction cost codes
- **Automated Bid Calculation**: Intelligent bid generation based on cost codes
- **ROI Analysis**: Financial analysis and return on investment calculations
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
│   │   └── bid.py              # Bid model
│   ├── routes/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── cost_codes.py       # Cost code endpoints
│   │   └── bids.py             # Bid endpoints
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── cost_code.py        # Cost code schemas
│   │   └── bid.py              # Bid schemas
│   └── services/               # Business logic
│       ├── __init__.py
│       ├── cost_code_service.py
│       └── bid_service.py
├── tests/                      # Test suite
│   ├── __init__.py
│   └── test_api.py
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
