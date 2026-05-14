from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
import numpy as np
import openai

app = FastAPI(title="Intelligent SuperApp API", description="AI-powered Stock and Business Strategy Engine")

# ---------------------------------------------------------
# FEATURE 1: STOCK PREDICTOR ENDPOINT
# ---------------------------------------------------------
@app.get("/stock/{ticker}")
def get_stock_prediction(ticker: str):
    try:
        data = yf.download(ticker.upper(), period="1mo", interval="1d")
        if data.empty:
            raise HTTPException(status_code=404, detail="Invalid ticker symbol or no data available.")
        
        last_price = float(data['Close'].iloc[-1])
        predicted_change = float(np.random.uniform(-2.5, 2.5))
        next_price = last_price + (last_price * (predicted_change / 100))
        
        return {
            "ticker": ticker.upper(),
            "current_price": round(last_price, 2),
            "predicted_next_price": round(next_price, 2),
            "predicted_change_percent": round(predicted_change, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# FEATURE 2: ZERO TO BILLIONAIRE ROADMAP ENDPOINT
# ---------------------------------------------------------
class RoadmapInput(BaseModel):
    current_savings: float
    monthly_investment: float
    annual_return_percent: float

@app.post("/roadmap")
def calculate_roadmap(data: RoadmapInput):
    r = (data.annual_return_percent / 100) / 12
    p = data.current_savings
    pmt = data.monthly_investment
    target = 1000000000.0  # 1 Billion
    
    if r <= 0 and pmt <= 0:
        raise HTTPException(status_code=400, detail="Please enter a valid monthly investment or return rate.")
        
    months = 0
    current_wealth = p
    while current_wealth < target and months < 1200:
        current_wealth = current_wealth * (1 + r) + pmt
        months += 1
        
    years = months / 12
    
    if months >= 1200:
        return {"message": "At this rate, it will take more than 100 years. Increase your investment or ROI."}
        
    return {
        "years_to_target": round(years, 1),
        "months_to_target": months,
        "action_plan": [
            "Step 1: Save 6 months of living expenses as an Emergency Fund.",
            "Step 2: Wipe out high-interest debts using the snowball method.",
            "Step 3: Automate investments into high-growth indexes and businesses."
        ]
    }

# ---------------------------------------------------------
# FEATURE 3: AI BUSINESS MASTERPLAN ENDPOINT
# ---------------------------------------------------------
class BusinessInput(BaseModel):
    api_key: str
    business_idea: str
    target_market: str

@app.post("/business-masterplan")
def generate_masterplan(data: BusinessInput):
    try:
        client = openai.OpenAI(api_key=data.api_key)
        prompt_content = f"Create a comprehensive business masterplan for: '{data.business_idea}'. Target market: '{data.target_market}'. Include Value Proposition, Revenue Streams, Growth Hacking Strategy, and Risk Mitigation."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert venture capitalist and business strategist."},
                {"role": "user", "content": prompt_content}
            ]
        )
        return {"masterplan": response.choices.message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")
