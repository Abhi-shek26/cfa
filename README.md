
# 📈 Stock Technical Analysis API

A high-performance, containerized backend built using FastAPI, designed to deliver real-time stock technical indicators via a tiered subscription model. This project was created as a backend developer assignment for **Kalpi Capital**.

---

## 🚀 Features

- ✅ FastAPI backend with Swagger/OpenAPI docs  
- 🔐 API key-based authentication & tiered authorization  
- 📊 Calculates technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands)  
- ⚡ Efficient Parquet-based stock data access  
- 🐘 PostgreSQL-backed user and subscription system  
- 🐳 Docker + Docker Compose deployment ready  
- 🔁 Optional Redis caching for performance (Premium Tier)  
- 📉 Rate limiting per user tier  

---

## 🏗️ System Architecture

```
+--------------+      +-------------+      +-----------------+
|  User Client | ---> |  FastAPI    | ---> | Parquet File    |
|  (Browser)   | <--- |  Backend    | ---> | PostgreSQL DB   |
+--------------+      +-------------+      +-----------------+
                            |
                         (Redis) - Optional Caching
```

- **User Client**: Web client or cURL  
- **FastAPI**: Processes requests, enforces auth, computes indicators  
- **Parquet File**: Stores OHLC stock data (~3 years)  
- **PostgreSQL**: Tracks users, API keys, usage quotas  
- **Redis** *(optional)*: Caches repeated responses (Premium)

---

## 🛠️ Tech Stack

| Area            | Tool/Tech         |
|-----------------|------------------|
| Backend         | FastAPI (Python) |
| Data Handling   | Pandas, pandas-ta |
| Database        | PostgreSQL        |
| Caching         | Redis *(optional)* |
| Deployment      | Docker, Docker Compose |
| Auth Mechanism  | API Keys          |
| API Docs        | Swagger UI        |

---

## 🎯 Subscription Model

| Tier     | Indicators            | Data Range       | Daily Limit |
|----------|------------------------|------------------|-------------|
| Free     | SMA, EMA               | Last 3 months    | 50 requests |
| Pro      | SMA, EMA, RSI, MACD    | Last 1 year      | 500 requests |
| Premium  | All (incl. Bollinger)  | Full 3 years     | Unlimited   |

---

## 🧪 API Endpoints

| Route                              | Access       | Description                         |
|-----------------------------------|--------------|-------------------------------------|
| `/indicators/sma/{symbol}`        | Free+        | Simple Moving Average               |
| `/indicators/ema/{symbol}`        | Free+        | Exponential Moving Average          |
| `/indicators/rsi/{symbol}`        | Pro+         | Relative Strength Index             |
| `/indicators/macd/{symbol}`       | Pro+         | MACD Indicator                      |
| `/indicators/bollinger/{symbol}`  | Premium only | Bollinger Bands                     |

> 🔍 Docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Setup Instructions

### 1. Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

### 2. Clone & Configure

```bash
git clone https://github.com/Abhi-shek26/cfa
cd cfa
```

### 3. Create `.env`

```env
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=stock_analysis_db
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
STOCK_DATA_PATH="stocks_ohlc_data.parquet"
```

### 4. Start the App

```bash
docker-compose up --build
```

### 5. Access the API

- API: [http://localhost:8000](http://localhost:8000)  
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testing Strategy

We used both manual and programmatic strategies to ensure functionality and reliability.

### ✅ Manual Tests

- Tested all endpoints via Swagger UI with valid and invalid API keys.
- Verified tier-based restrictions:
  - Free users restricted from premium/pro indicators.
  - Pro users blocked from Bollinger Bands.
- Simulated rate-limiting logic using looped requests.

### ✅ Indicator Validation

- Compared indicator outputs against Pandas-TA reference calculations for known stocks like `AAPL` and `TSLA`.

### 🔮 Future Testing

- Introduce `pytest`-based unit + integration test suite.
- Use mocked PostgreSQL + Redis containers for CI testing.

---

## 🔒 Security & Scalability

- 🔐 API Key verification per request  
- ⚖️ Tier enforcement with clear `401`, `403`, and `429` status codes  
- 🔁 Caching for repeated requests (Premium)  
- 📈 Horizontally scalable with containerized deployment  

---
