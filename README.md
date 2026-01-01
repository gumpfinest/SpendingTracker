# SmartSpend - AI-Powered Personal Finance Assistant

A microservices-based personal finance application that helps users understand their spending habits and predicts future savings using AI.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                    │
│                         React + TypeScript                               │
│                    (Port 3000 - UI/Visualization)                       │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY                                    │
│                    Java Spring Boot Backend                              │
│              (Port 8080 - Auth, Business Logic, DB)                     │
└────────────┬────────────────────────────────────────┬───────────────────┘
             │                                        │
             ▼                                        ▼
┌────────────────────────────┐          ┌────────────────────────────────┐
│     DATA SERVICE           │          │        AI AGENT SERVICE        │
│   Python FastAPI           │          │      Python FastAPI            │
│ (Port 8001 - Processing)   │          │  (Port 8002 - AI/ML/Advice)    │
└────────────────────────────┘          └────────────────────────────────┘
```

## Features

- ✅ **User Authentication**: JWT-based secure authentication
- ✅ **Transaction Management**: Add, view, and categorize transactions
- ✅ **AI-Powered Categorization**: Automatic transaction categorization
- ✅ **Budget Tracking**: Set and monitor monthly budgets by category
- ✅ **Spending Analytics**: Visual charts and insights
- ✅ **AI Financial Assistant**: Get personalized financial advice via chat
- ✅ **Spending Forecasts**: ML-powered predictions using linear regression

## Microservices

### 1. Frontend (React + TypeScript) - Port 3000
- Interactive dashboard with Tailwind CSS
- Beautiful charts with Recharts
- JWT-based authentication
- AI chat assistant interface
- Responsive design

### 2. Core Backend (Java Spring Boot) - Port 8080
- RESTful API Gateway
- JWT Authentication with Spring Security
- PostgreSQL/H2 database integration
- Transaction and budget management
- Integration with Python microservices

### 3. Data Service (Python FastAPI) - Port 8001
- Transaction categorization using keyword matching
- Spending analytics with Pandas
- ML-based forecasting with Scikit-learn
- Budget analysis

### 4. AI Agent Service (Python FastAPI) - Port 8002
- Conversational AI using OpenAI (with fallback)
- Financial advice generation
- Spending pattern detection
- Personalized recommendations

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Recharts, Formik |
| API Gateway | Java 17, Spring Boot 3.2, Spring Security, JWT (jjwt), JPA |
| Data Processing | Python 3.11, FastAPI, Pandas, NumPy, Scikit-learn |
| AI Agent | Python 3.11, FastAPI, OpenAI, LangChain |
| Database | PostgreSQL (Docker) / H2 (Development) |
| Containerization | Docker, Docker Compose |

## Getting Started

### Prerequisites
- **Java 17+** - [Download from Adoptium](https://adoptium.net/)
- **Maven 3.8+** - [Download Maven](https://maven.apache.org/download.cgi)
- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 20+** - [Download Node.js](https://nodejs.org/)

### Environment Setup

```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env and add your OpenAI API key (optional - app works without it)
```

### Running on Windows (Without Docker)

Open **4 separate PowerShell terminals** and run the following:

#### Terminal 1: Backend (Java Spring Boot)
```powershell
cd c:\Users\bruno\Documents\CodingProjects\SmartSpendApp\backend
# If you have Maven installed:
mvn spring-boot:run
# Or use the wrapper:
# .\mvnw.cmd spring-boot:run
# Runs on http://localhost:8080
```

#### Terminal 2: Data Service (Python FastAPI)
```powershell
cd c:\Users\bruno\Documents\CodingProjects\SmartSpendApp\data-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
# Runs on http://localhost:8001
```

#### Terminal 3: AI Agent Service (Python FastAPI)
```powershell
cd c:\Users\bruno\Documents\CodingProjects\SmartSpendApp\ai-agent-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Optional: Set OpenAI API key
$env:OPENAI_API_KEY="your-key-here"
uvicorn main:app --reload --port 8002
# Runs on http://localhost:8002
```

#### Terminal 4: Frontend (React)
```powershell
cd c:\Users\bruno\Documents\CodingProjects\SmartSpendApp\frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

### Quick Start Script (Windows)

You can also use the provided start script:
```powershell
cd c:\Users\bruno\Documents\CodingProjects\SmartSpendApp
.\start-all.ps1
```

### Access the Application

After all services are running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **Data Service**: http://localhost:8001
- **AI Agent**: http://localhost:8002

## API Documentation

- **Backend Swagger**: http://localhost:8080/swagger-ui.html
- **Data Service Docs**: http://localhost:8001/docs
- **AI Agent Docs**: http://localhost:8002/docs

## Project Structure

```
SmartSpendApp/
├── backend/                    # Java Spring Boot Backend
│   ├── src/main/java/com/smartspend/
│   │   ├── config/            # Security & WebClient config
│   │   ├── controller/        # REST Controllers
│   │   ├── dto/               # Data Transfer Objects
│   │   ├── entity/            # JPA Entities
│   │   ├── exception/         # Exception handlers
│   │   ├── repository/        # JPA Repositories
│   │   ├── security/          # JWT implementation
│   │   └── service/           # Business logic
│   ├── Dockerfile
│   └── pom.xml
│
├── data-service/              # Python Data Processing
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   └── core/              # Configuration
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── ai-agent-service/          # Python AI Agent
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   └── core/              # Agent & config
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── context/           # Auth context
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── types/             # TypeScript types
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## Data Flow

1. **User Action**: User adds transaction "Starbucks - $5.00"
2. **Storage**: React → Java Backend → Database (saved as "Pending")
3. **Categorization**: Java → Python Data Service → Returns "Food & Dining"
4. **Update**: Java updates transaction with category
5. **Analytics**: User views dashboard → Java aggregates data
6. **Forecasting**: Java → Python Data Service → ML predictions
7. **AI Advice**: Java → AI Agent → Personalized recommendations
8. **Display**: React renders charts and insights

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Transactions
- `GET /api/transactions` - Get all transactions
- `POST /api/transactions` - Create transaction (auto-categorized)
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction

### Budgets
- `GET /api/budgets?month=&year=` - Get budgets for month
- `POST /api/budgets` - Create budget
- `PUT /api/budgets/{id}` - Update budget
- `DELETE /api/budgets/{id}` - Delete budget

### Analytics
- `GET /api/analytics/dashboard` - Dashboard summary
- `GET /api/analytics/forecast` - Spending forecast

### AI
- `POST /api/ai/advice` - Get financial advice
- `POST /api/ai/chat` - Chat with AI assistant
- `GET /api/ai/patterns` - Detect spending patterns

## License

MIT License
