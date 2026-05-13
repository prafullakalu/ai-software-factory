# 🚀 SaaS Templates

## Auth Template

### Features
- Email/password authentication
- Social login (Google, GitHub, Apple)
- JWT tokens
- Refresh tokens
- Password reset
- Email verification
- 2FA (optional)

---

## Dashboard Template

### Features
- Analytics charts
- User management
- Settings
- Activity logs
- Data tables
- Export data

---

## Billing Template

### Features
- Subscription plans
- Usage-based billing
- Invoice generation
- Payment methods
- Upgrade/downgrade
- Cancellation

---

## Multi-tenant Template

### Features
- Workspace management
- Team invitations
- Role-based access
- Permissions
- Audit logs

---

## API Template

### Features
- RESTful API
- GraphQL option
- Rate limiting
- API versioning
- Documentation
- Rate: 1k req/min

---

## Use

```python
from templates import create_saas_project

project = create_saas_project(
    name="my-saas",
    template="saas-auth",
    features=["auth", "billing", "dashboard"],
)
```