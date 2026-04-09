from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import math

app = FastAPI(
    title="Churn Predictor AI",
    description="API for predicting customer churn risk",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CustomerData(BaseModel):
    customer_id: Optional[str] = None
    tenure_months: Optional[int] = None          # months as customer
    monthly_charges: Optional[float] = None       # monthly spend
    total_charges: Optional[float] = None         # lifetime spend
    num_support_tickets: Optional[int] = None     # support tickets opened
    last_login_days_ago: Optional[int] = None     # days since last login
    contract_type: Optional[str] = None           # "month-to-month", "one-year", "two-year"
    payment_method: Optional[str] = None          # "credit-card", "bank-transfer", "check"
    has_tech_support: Optional[bool] = None
    has_online_backup: Optional[bool] = None
    num_products: Optional[int] = None            # number of products subscribed


class CheckoutRequest(BaseModel):
    plan: str  # "starter", "pro", "enterprise"
    success_url: Optional[str] = "https://example.com/success"
    cancel_url: Optional[str] = "https://example.com/cancel"


def compute_churn_score(data: CustomerData) -> float:
    """
    Stub churn scoring model.
    Returns a probability 0.0 (no risk) to 1.0 (certain churn).
    Weights based on common churn indicators.
    """
    score = 0.3  # baseline

    # Short tenure → higher risk
    if data.tenure_months is not None:
        if data.tenure_months < 6:
            score += 0.2
        elif data.tenure_months < 12:
            score += 0.1
        elif data.tenure_months > 36:
            score -= 0.15

    # High support tickets → higher risk
    if data.num_support_tickets is not None:
        score += min(data.num_support_tickets * 0.05, 0.25)

    # Days since last login → higher risk
    if data.last_login_days_ago is not None:
        if data.last_login_days_ago > 30:
            score += 0.2
        elif data.last_login_days_ago > 14:
            score += 0.1

    # Month-to-month contract → higher risk
    if data.contract_type == "month-to-month":
        score += 0.15
    elif data.contract_type == "two-year":
        score -= 0.15

    # Fewer products → higher risk
    if data.num_products is not None:
        if data.num_products == 1:
            score += 0.1
        elif data.num_products >= 3:
            score -= 0.1

    # Tech support → lower risk
    if data.has_tech_support:
        score -= 0.05

    # Check payment → slight higher risk
    if data.payment_method == "check":
        score += 0.05

    return round(max(0.0, min(1.0, score)), 4)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "churn-predictor-ai", "version": "1.0.0"}


@app.post("/predict-churn")
async def predict_churn(data: CustomerData):
    churn_score = compute_churn_score(data)

    if churn_score >= 0.7:
        risk_level = "high"
        recommendation = "Immediate intervention required. Offer retention discount or personal outreach."
    elif churn_score >= 0.4:
        risk_level = "medium"
        recommendation = "Monitor closely. Consider proactive engagement and product education."
    else:
        risk_level = "low"
        recommendation = "Customer appears healthy. Continue standard engagement."

    return {
        "customer_id": data.customer_id,
        "churn_probability": churn_score,
        "churn_percentage": f"{churn_score * 100:.1f}%",
        "risk_level": risk_level,
        "recommendation": recommendation,
        "model_version": "1.0.0-stub",
        "factors_analyzed": {
            "tenure_months": data.tenure_months,
            "num_support_tickets": data.num_support_tickets,
            "last_login_days_ago": data.last_login_days_ago,
            "contract_type": data.contract_type,
            "num_products": data.num_products,
        }
    }


@app.post("/create-checkout-session")
async def create_checkout_session(req: CheckoutRequest):
    plans = {
        "starter": {
            "name": "Starter Plan",
            "price_usd": 29,
            "predictions_per_month": 500,
            "features": ["500 predictions/month", "API access", "Email support"],
        },
        "pro": {
            "name": "Pro Plan",
            "price_usd": 99,
            "predictions_per_month": 5000,
            "features": ["5,000 predictions/month", "API access", "Priority support", "Webhooks", "CSV bulk upload"],
        },
        "enterprise": {
            "name": "Enterprise Plan",
            "price_usd": 299,
            "predictions_per_month": -1,  # unlimited
            "features": ["Unlimited predictions", "Dedicated account manager", "Custom model training", "SLA guarantee", "SSO"],
        },
    }

    if req.plan not in plans:
        raise HTTPException(status_code=400, detail=f"Invalid plan '{req.plan}'. Choose: starter, pro, enterprise.")

    plan_info = plans[req.plan]

    # Stub response — replace with real Stripe SDK call when STRIPE_SECRET_KEY is configured
    return {
        "session_id": f"cs_stub_{req.plan}_placeholder",
        "checkout_url": f"https://checkout.stripe.com/pay/cs_stub_{req.plan}_placeholder",
        "plan": req.plan,
        "plan_details": plan_info,
        "success_url": req.success_url,
        "cancel_url": req.cancel_url,
        "note": "Stripe integration stub — configure STRIPE_SECRET_KEY env var to activate real checkout",
    }


# Vercel requires the app object to be exported
handler = app
