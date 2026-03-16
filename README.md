# VentureLens AI

AI-powered platform for validating startup ideas using real market data and large language models.

VentureLens analyzes market demand, competition signals, and trends using Google Trends
and generates structured business insights with AI.

The platform helps founders evaluate startup ideas before building products.

---

![VentureLens AI](https://img.shields.io/badge/VentureLens-AI-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker)

---

# Overview

Launching a startup without validating demand is risky.

VentureLens AI combines:

• real market trend data  
• AI reasoning via LLMs  
• structured scoring models  

to generate a **startup validation report**.

Users can analyze startup ideas and receive insights such as:

- market demand signals
- competitive landscape
- opportunity scoring
- AI-generated strategic insights

---

# Key Features

### AI Startup Analysis
- 7-dimension AI evaluation system
- structured reasoning using LLMs
- automated opportunity scoring

### Market Intelligence
- Google Trends demand analysis
- keyword demand comparison
- trend signal detection

### Insight Dashboard
- interactive analytics dashboard
- Chart.js visualizations
- structured analysis output

### Product Features
- Google OAuth authentication
- analysis history
- delete analysis history
- export analysis report to PDF
- user feedback system

### Production Setup
- Railway deployment
- Docker containerization
- static files optimization
- production Django settings

### Compliance
- Privacy Policy page
- Terms of Service page

---

# AI Analysis Dimensions

Each startup idea is evaluated across multiple dimensions:

1. Market Demand
2. Competition Landscape
3. Problem-Solution Fit
4. Market Timing
5. Monetization Potential
6. Scalability
7. Execution Feasibility

These signals are combined into a **viability score**.

---

# AI Analysis Pipeline

1. User submits startup idea
2. System extracts relevant keywords
3. Google Trends data is collected
4. Market demand signals are analyzed
5. LLM generates structured insights
6. Multi-factor scoring engine evaluates viability
7. Results displayed in the dashboard

---

# Architecture Overview

venturelens/
├── venturelens_project/
│ ├── settings/
│ │ ├── base.py
│ │ ├── development.py
│ │ └── production.py
│
├── apps/
│ ├── core/
│ │ ├── authentication
│ │ ├── landing pages
│ │ └── user management
│
│ ├── analysis/
│ │ ├── ai_service.py
│ │ ├── trends_service.py
│ │ ├── scoring_service.py
│ │ └── analysis_orchestrator.py
│
│ └── dashboard/
│ └── analysis results UI
│
├── static/
├── templates/
├── docker-compose.yml
└── manage.py


---

# Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Django 5.x + Python 3.12 |
| Database | PostgreSQL + psycopg2 |
| AI / LLM | Groq API (Llama 3.3 70B) |
| Market Data | Google Trends via pytrends |
| Frontend | TailwindCSS + HTMX + Alpine.js |
| Charts | Chart.js |
| Auth | Google OAuth |
| Deployment | Railway |
| Container | Docker + Gunicorn + Nginx |

---

# Quick Start (Local Development)

```bash
git clone https://github.com/yourusername/venturelens-ai.git
cd venturelens-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

python manage.py migrate
python manage.py runserver

SECRET_KEY=your-django-secret-key
DEBUG=True

DATABASE_URL=postgresql://user:pass@localhost:5432/venturelens

GROQ_API_KEY=your-groq-api-key
OPENAI_API_KEY=your-openai-key
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_SECRET=your-secret

