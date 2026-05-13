# 💰 Fintech Templates

## Payment Gateway Template

### Features
- Stripe integration
- Multiple payment methods (Card, Bank, Wallet)
- Transaction history
- Refund handling
- Webhook handling
- PCI compliance

### API Endpoints
```
POST /payments/create       # Create payment
POST /payments/confirm    # Confirm payment
GET  /payments/:id        # Get payment status
POST /payments/refund     # Refund payment
GET  /transactions       # List transactions
```

---

## Wallet Template

### Features
- User wallets
- Balance management
- Top-up/withdraw
- Transfer between users
- Transaction limits
- KYC integration

### API Endpoints
```
POST /wallets/create      # Create wallet
GET  /wallets/:id       # Get balance
POST /wallets/topup     # Add funds
POST /wallets/withdraw # Withdraw funds
POST /wallets/transfer # Transfer to user
```

---

## Banking API Template

### Features
- Account management
- Transaction logging
- Statement generation
- ACH transfers
- Wire transfers
- Account verification

### API Endpoints
```
POST /accounts/create     # Create account
GET  /accounts/:id      # Get account
POST /accounts/transfer # Transfer
GET  /statements       # Get statement
```

---

## Invoice Template

### Features
- Create invoices
- Send to customers
- Payment tracking
- Recurring invoices
- Tax calculation

---

## Use

```python
from templates import create_fintech_project

project = create_fintech_project(
    name="payment-gateway",
    template="payment-gateway",
    features=["stripe", "webhooks"],
)
```