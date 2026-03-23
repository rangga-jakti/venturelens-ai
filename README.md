# VentureLens AI 🔍

> **Stop guessing. Start validating.**
> AI-powered startup idea validation using real market data, LLM reasoning, and structured scoring — before you write a single line of code.

![VentureLens AI](https://img.shields.io/badge/VentureLens-AI-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker)

**Live Demo → [venturelens.up.railway.app](https://venturelens.up.railway.app)**

---

## The Problem

Most startups fail not because of bad execution — but because they build something nobody wants.

Founders spend months (and money) building products based on gut feeling, not data. By the time they realize there's no market, it's too late.

---

## The Solution

VentureLens AI gives you a **data-backed startup validation report in seconds**, combining:

- **Real-time market signals** via Google Trends
- **AI reasoning** powered by LLaMA 3.3 (Groq)
- **Structured multi-factor scoring** across 7 dimensions

---

## Features

### 7-Dimension AI Analysis
Every idea is evaluated across 7 factors and scored 0–100:

| Dimension | What it measures |
|---|---|
| Market Demand | Is there real, growing interest? |
| Competition Landscape | How crowded is the space? |
| Problem-Solution Fit | Does your solution solve the right pain? |
| Market Timing | Is now the right time to build this? |
| Monetization Potential | Can this make money? |
| Scalability | Can it grow without breaking? |
| Execution Feasibility | Can a small team actually build it? |

### Market Intelligence Dashboard
- Interactive radar chart across all 7 dimensions
- Google Trends data with 1M / 3M / 12M / 5Y / 10Y timeframes
- Keyword trend comparison with multiple signals
- Simulated fallback when live data is unavailable

### Competitor Intelligence
- Auto-identifies direct & indirect competitors
- Expandable cards with strengths & weaknesses per competitor
- Similarity scoring (langsung / tidak langsung)

### Business Model Recommendations
- AI-generated monetization strategies ranked by revenue potential
- Expandable preview cards (High / Medium / Low potential badges)

### Full Report Includes
- Problem Statement
- Value Proposition
- Scalability Analysis
- SWOT (Strengths, Weaknesses, Opportunities, Threats)
- Investor Perspective
- AI Recommendation

### Product Features
- Google OAuth login
- Analysis history with delete
- Export to PDF (browser print)
- Shareable public report links
- Thumbs up/down feedback system
- Multi-language support (EN / ID)
- Viability score with animated ring + expandable rationale

### Production-Ready
- Docker containerization
- Railway deployment
- WhiteNoise static file handling
- Production-grade Django configuration
- Privacy Policy & Terms of Service

---

## AI Analysis Pipeline

```
User submits idea
      ↓
Keyword extraction
      ↓
Google Trends data collection
      ↓
Market demand signal analysis
      ↓
LLM generates structured insights (LLaMA 3.3 via Groq)
      ↓
Multi-factor scoring engine
      ↓
Full validation report rendered
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x + Python 3.12 |
| Database | PostgreSQL |
| AI / LLM | LLaMA 3.3-70b (Groq API) |
| Market Data | Google Trends (pytrends) |
| Frontend | TailwindCSS + HTMX + Alpine.js |
| Visualization | Chart.js |
| Authentication | Google OAuth (django-allauth) |
| Deployment | Railway |
| Infrastructure | Docker + Gunicorn + WhiteNoise |

---

## System Architecture

```
venturelens/
├── venturelens_project/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│
├── apps/
│   ├── core/              # auth, landing page, user management
│   ├── analysis/
│   │   ├── ai_service.py
│   │   ├── trends_service.py
│   │   ├── scoring_service.py
│   │   └── analysis_orchestrator.py
│   └── dashboard/         # results UI, history, sharing
│
├── static/
├── templates/
├── docker-compose.yml
└── manage.py
```

---

## Quick Start (Local)

```bash
git clone https://github.com/rangga-jakti/venturelens-ai.git
cd venturelens-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env
# Fill in your environment variables

python manage.py migrate
python manage.py runserver
```

### Environment Variables

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DATABASE_URL=postgresql://user:pass@localhost:5432/venturelens

GROQ_API_KEY=your-groq-api-key

GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_SECRET=your-secret
```

Settings module: `venturelens_project.settings.development`

---

## Use Cases

- Validate a startup idea before building
- Automate early-stage market research
- Test product-market fit hypotheses
- Compare multiple SaaS ideas quickly
- Content niche & audience demand discovery

---

## What This Project Demonstrates

- End-to-end AI-powered SaaS from scratch
- Integrating LLMs into production Django workflows
- Designing data pipelines + multi-factor scoring systems
- Combining real-time external data (Google Trends) with AI reasoning
- Deploying scalable applications using Docker & Railway

---

## Open for Work

Available for freelance and remote opportunities in:

- AI SaaS Development
- LLM Integration & Prompt Engineering
- Data-driven Web Applications

📩 Let's build something impactful together.

---

*Built by Rangga*