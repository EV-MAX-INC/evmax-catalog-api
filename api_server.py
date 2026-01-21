from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

app = FastAPI(title='EV MAX Catalog API', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

def get_db():
    db_url = os.getenv('DATABASE_URL', '')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    if db_url: 
        import urllib.parse as up
        up.uses_netloc. append('postgresql')
        url = up.urlparse(db_url)
        return psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            cursor_factory=RealDictCursor
        )
    else:
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=5432,
            database='evmax_catalog',
            user='evmax_user',
            password='SecurePassword2026! ',
            cursor_factory=RealDictCursor
        )

class QuoteRequest(BaseModel):
    product_sku: str
    quantity: int
    tier: str = 'standard'
    season: str = 'summer'

@app.get('/')
def root():
    return {
        'service': 'EV MAX Catalog API',
        'status': 'operational',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    }

@app.get('/health')
def health():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        return {'status': 'degraded', 'database': f'error: {str(e)}'}

@app.get('/api/v1/products')
def get_products():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE is_active = TRUE ORDER BY category, name')
        products = cur.fetchall()
        cur.close()
        conn.close()
        return {'count': len(products), 'products': products}
    except Exception as e:
        raise HTTPException(500, f'Database error: {str(e)}')

@app.get('/api/v1/products/{sku}')
def get_product(sku: str):
    try:
        conn = get_db()
        cur = conn. cursor()
        cur.execute('SELECT * FROM products WHERE sku = %s AND is_active = TRUE', (sku,))
        product = cur.fetchone()
        cur.close()
        conn.close()
        if not product:
            raise HTTPException(404, f'Product {sku} not found')
        return product
    except HTTPException: 
        raise
    except Exception as e:
        raise HTTPException(500, f'Database error: {str(e)}')

@app.post('/api/v1/quotes/calculate')
def calculate_quote(req: QuoteRequest):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE sku = %s AND is_active = TRUE', (req.product_sku,))
        product = cur.fetchone()
        cur.close()
        conn.close()
        
        if not product:
            raise HTTPException(404, f'Product {req.product_sku} not found')
        
        tiers = product['pricing_tiers']
        price = tiers. get(req.tier, tiers. get('standard'))
        
        discount = 0
        if req.quantity >= 50:
            discount = 0.20
        elif req.quantity >= 25:
            discount = 0.15
        elif req.quantity >= 10:
            discount = 0.10
        elif req.quantity >= 5:
            discount = 0.05
        
        seasonal = {'winter': 1. 10, 'spring': 0.95, 'fall': 0.95, 'summer': 1.0}. get(req.season, 1.0)
        
        final_price = price * seasonal * (1 - discount)
        total = final_price * req.quantity
        margin = ((final_price - product['base_cost']) / final_price) * 100
        
        return {
            'product_sku': req.product_sku,
            'product_name': product['name'],
            'quantity': req.quantity,
            'unit_price': float(price),
            'subtotal': float(price * req.quantity),
            'volume_discount_pct': discount * 100,
            'seasonal_adjustment_pct': (seasonal - 1) * 100,
            'final_unit_price': round(final_price, 2),
            'total': round(total, 2),
            'gross_margin_pct': round(margin, 1)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f'Error:  {str(e)}')
