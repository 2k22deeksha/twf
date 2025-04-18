# Warehouse Delivery Cost Calculator API

A REST API to calculate the minimum delivery cost for warehouse products to a customer location (L1), with deployment options for Rancher and local testing.

## Features
- Calculates optimal delivery routes for orders
- Supports deployment via Docker/Rancher
- Free-tier compatible (Render/Cloud Run)

## Technologies
- **Backend**: Python/Flask
- **Deployment**: Docker, Rancher
- **Testing**: Postman

---

## API Usage with Postman

### Sample Request
**URL**: https://twf-r06k.onrender.com/calculate-cost 
**Headers**:
- `Content-Type: application/json`
- POST request

**Request Body**:
```json
{
  "A": 1,
  "B": 2,
  "C": 1,
  "D": 5,
  "G": 2,
  "H": 1,
  "I": 1
}

o/p:
{
    "min_cost": 634.0
}


FYI: free instance will spin down with inactivity, which can delay requests by 50 seconds or more
