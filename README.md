# Churn Predictor AI — Backend

FastAPI backend for customer churn prediction.

## Endpoints

### GET /health
Returns service health status.

### POST /predict-churn
Accepts customer data and returns churn risk score.

**Request body:**
```json
{
  "customer_id": "cust_001",
  "tenure_months": 3,
  "monthly_charges": 79.99,
  "num_support_tickets": 4,
  "last_login_days_ago": 21,
  "contract_type": "month-to-month",
  "num_products": 1
}
```

### POST /create-checkout-session
Initiates Stripe checkout for a plan (starter/pro/enterprise).

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `STRIPE_SECRET_KEY` | Stripe secret key for checkout | Optional (stub works without it) |

## Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deploy to Vercel

```bash
npx vercel --prod
```
