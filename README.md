# EV MAX Catalog API v2.0

Product catalog and quote generation API for precast concrete products.

## Features
- 🚀 RESTful API with FastAPI
- 🗄️ PostgreSQL database
- 💰 Real-time quote generation
- 📊 Tiered pricing (Standard, Priority, Emergency)
- 🎯 Volume discounts (5%, 10%, 15%, 20%)
- 🌦️ Seasonal pricing adjustments

## Product Categories
- EV Charging Foundations
- Equipment Pads
- Transformer Pads
- Hollowcore Slabs

## API Endpoints

### Health Check
\\\
GET /health
\\\

### Products
\\\
GET /api/v1/products
GET /api/v1/products/{sku}
\\\

### Quote Generation
\\\
POST /api/v1/quotes/calculate
{
  "product_sku":  "EVMAX-EV-36X24-L2-SGL",
  "quantity": 10,
  "tier": "priority",
  "season": "winter"
}
\\\

## Quick Start

\\\ash
pip install -r requirements.txt
uvicorn api_server: app --reload
\\\

Visit http://localhost:8000/docs for interactive API documentation. 

## Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

## Technology Stack
- FastAPI 0.109.0
- PostgreSQL
- Python 3.11+
- Uvicorn ASGI server

---

© 2026 EV MAX INC - Product Catalog System
