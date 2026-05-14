from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pydantic

app = FastAPI(
    title="Intelligent Super App Backend",
    description="World-class ultra-fast AI Financial Engine",
    version="1.0.0"
)

# CORS settings to connect with your mobile app frontend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for Business Plan Inputs
class BusinessIdea(pydantic.BaseModel):
    idea: str
    budget: float
    target_market: str

@app.get("/")
def home():
    return {"message": "Welcome to the World's No.1 Intelligent Super App API Backend!"}

# 1. Ultra-Fast Stock Market API Module
@app.get("/api/stock/{ticker}")
def get_stock_prediction(ticker: str):
    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period="1mo")
        
        if hist.empty:
            raise HTTPException(status_code=404, detail="Stock ticker not found")
            
        current_price = float(hist['Close'].iloc[-1])
        avg_price = float(hist['Close'].mean())
        trend = "Bullish (Market likely to move up)" if current_price > avg_price else "Bearish (Market looks weak)"
        
        return {
            "ticker": ticker.upper(),
            "current_price": round(current_price, 2),
            "moving_average_30d": round(avg_price, 2),
            "ai_trend_indicator": trend,
            "message": "Stock data processed in milliseconds!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Zero to Billionaire Mathematical API Module
@app.get("/api/billionaire")
def calculate_roadmap(savings: float = 0, monthly: float = 500, rate: float = 15, years: int = 25):
    P = savings
    PMT = monthly
    r = rate / 100
    n = 12
    t = years
    
    total_months = n * t
    future_value = P * ((1 + r/n)**total_months) + PMT * (((1 + r/n)**total_months - 1) / (r/n)) * (1 + r/n)
    target = 1000000000
    is_billionaire = future_value >= target
    shortfall = max(0.0, target - future_value)
    
    return {
        "total_wealth_generated": round(future_value, 2),
        "target_reached": is_billionaire,
        "amount_needed_to_hit_billion": round(shortfall, 2),
        "strategy_tip": "If target not reached, increase monthly business investment or boost your annual return rate."
    }

# 3. AI Business Masterplan Generator API Module
@app.post("/api/business-masterplan")
def generate_masterplan(data: BusinessIdea):
    if not data.idea.strip():
        raise HTTPException(status_code=400, detail="Business idea cannot be empty")
        
    marketing = data.budget * 0.35
    operations = data.budget * 0.45
    buffer = data.budget * 0.20
    projected_revenue_y1 = data.budget * 2.5
    
    return {
        "business_name_or_idea": data.idea,
        "target_audience_region": data.target_market,
        "financial_budget_breakdown": {
            "marketing_and_growth_35pct": round(marketing, 2),
            "operations_and_product_45pct": round(operations, 2),
            "safety_buffer_cash_20pct": round(buffer, 2)
        },
        "year_1_gross_revenue_projection": round(projected_revenue_y1, 2),
        "growth_hacking_strategy": "Leverage organic viral content (TikTok/Shorts), Micro-influencer partnerships, and aggressive SEO to minimize CAC.",
        "execution_steps": [
            "Launch a Minimum Viable Product (MVP) within 30 days to test the market.",
            "Secure intellectual property and local startup compliance before scaling.",
            "Reinvest 80% of Year 1 profits into scaling operations or compounding financial assets."
        ]
    }
