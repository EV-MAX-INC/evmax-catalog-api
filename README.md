# EV MAX Catalog API

EV MAX Catalog System v2.0 - Product catalog and quote generation API for precast concrete products

## Features

- **Product CRUD Operations**: Create, Read, Update, Delete products
- **Quote Calculation**: Advanced quote generation with:
  - Volume discounts (5-20% based on quantity)
  - Seasonal pricing adjustments
  - Customer tier pricing (standard, premium, enterprise)
  - Automatic margin calculation
- **Database Models**: Products, Cost Codes, and Compliance Standards
- **Health Check Endpoint**: Monitor API and database status
- **Swagger Documentation**: Interactive API documentation at `/docs`
- **CORS Support**: Cross-origin resource sharing enabled
- **Docker Support**: Complete Docker Compose setup with PostgreSQL

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust relational database with JSONB support
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server
- **Docker**: Containerized deployment

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/EV-MAX-INC/evmax-catalog-api.git
cd evmax-catalog-api
```

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Start the services:
```bash
docker-compose up -d
```

4. Access the API:
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Health Check
- `GET /health` - Check API and database health

### Products
- `GET /products/` - List all products (with pagination)
- `GET /products/{product_id}` - Get a specific product
- `POST /products/` - Create a new product
- `PUT /products/{product_id}` - Update a product
- `DELETE /products/{product_id}` - Delete a product
- `POST /products/quote` - Calculate a quote with discounts

### Quote Calculation

Generate quotes with advanced pricing:

```json
POST /products/quote
{
  "product_id": 1,
  "quantity": 100,
  "season": "winter",
  "tier": "premium"
}
```

Response includes:
- Base and final unit prices
- Volume discount percentage (5-20%)
- Seasonal adjustment
- Tier discount
- Total price
- Margin calculation

## Database Schema

### Products Table
- `id`: Primary key
- `sku`: Unique product identifier
- `category`: Product category
- `name`: Product name
- `base_cost`: Base cost
- `base_price`: Base selling price
- `pricing_tiers`: JSONB field for custom volume pricing
- `material_specs`: JSONB field for material specifications
- `compliance_codes`: Compliance standard codes

### Cost Codes Table
- `id`: Primary key
- `code`: Unique cost code
- `description`: Cost code description
- `category`: Cost category
- `base_rate`: Base rate

### Compliance Standards Table
- `id`: Primary key
- `code`: Unique compliance code
- `name`: Standard name
- `description`: Detailed description
- `issuing_body`: Issuing organization
- `effective_date`: When standard becomes effective

## Configuration

Environment variables (`.env` file):

```bash
DATABASE_URL=postgresql://postgres:password@db:5432/evmax_catalog
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=evmax_catalog
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Volume Discount Tiers

Default volume discounts:
- 10+ units: 5%
- 50+ units: 7%
- 100+ units: 10%
- 250+ units: 12%
- 500+ units: 15%
- 1000+ units: 20%

## Seasonal Pricing

- **Winter**: +10% (high demand)
- **Spring**: +5% (moderate demand)
- **Summer**: -5% (off-peak discount)
- **Fall**: 0% (standard pricing)

## Customer Tiers

- **Standard**: No additional discount
- **Premium**: 5% discount
- **Enterprise**: 10% discount

## License

Copyright © 2026 EV MAX INC. All rights reserved.
