# VentureLens AI

AI-powered platform for validating startup ideas using market data and AI insights.

VentureLens analyzes market demand, competition, and trends using Google Trends data
and generates actionable business insights with LLMs.

Built with Django, PostgreSQL, and Groq LLM.

![VentureLens AI](https://img.shields.io/badge/VentureLens-AI-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?style=for-the-badge&logo=django)

---

## Features

- Startup idea validation using real market data
- Google Trends demand analysis
- AI-generated business insights
- Market opportunity scoring
- Keyword comparison
- Interactive charts

---

## Architecture Overview

```
venturelens/
├── venturelens_project/        # Django project config
│   ├── settings/
│   │   ├── base.py             # Shared settings
│   │   ├── development.py      # Dev overrides
│   │   └── production.py       # Prod overrides
│   ├── urls.py
│   └── wsgi.py / asgi.py
│
├── apps/
│   ├── core/                   # Auth, landing, user management
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services/
│   │
│   ├── analysis/               # Core AI analysis engine
│   │   ├── models.py           # StartupAnalysis, ViabilityScore, etc.
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── services/
│   │       ├── ai_service.py       # LLM integration (Groq/OpenAI)
│   │       ├── trends_service.py   # Google Trends (pytrends)
│   │       ├── scoring_service.py  # Viability scoring engine
│   │       └── analysis_orchestrator.py
│   │
│   └── dashboard/              # Results display
│       ├── views.py
│       └── urls.py
│
├── static/
│   ├── css/
│   │   └── tailwind.css        # TailwindCSS compiled
│   ├── js/
│   │   ├── charts.js           # Chart.js configurations
│   │   ├── animations.js       # GSAP / micro-interactions
│   │   └── htmx-extensions.js
│   └── images/
│
├── templates/
│   ├── base.html               # Master layout
│   ├── core/
│   │   └── landing.html        # Landing page
│   ├── analysis/
│   │   └── input.html          # Idea input form
│   ├── dashboard/
│   │   └── results.html        # Full insight dashboard
│   └── partials/
│       ├── navbar.html
│       ├── loading.html
│       └── score_card.html
│
├── .env.example
├── requirements.txt
├── manage.py
└── docker-compose.yml
```

## Quick Start (Windows)

```bash
# 1. Clone and enter directory
cd venturelens

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
copy .env.example .env
# Edit .env with your keys

# 5. Database setup
python manage.py migrate

# 6. Run development server
python manage.py runserver
```

## Environment Variables

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/venturelens
GROQ_API_KEY=your-groq-api-key          # Primary LLM
OPENAI_API_KEY=your-openai-key          # Fallback
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.x + Python 3.12 |
| Database | PostgreSQL + psycopg2 |
| AI/LLM | Groq API (llama-3.3-70b) |
| Trends | pytrends (Google Trends) |
| Frontend | TailwindCSS + HTMX + Alpine.js |
| Charts | Chart.js 4.x |
| Cache | Django Cache (Redis-ready) |
| Deploy | Docker + Gunicorn + Nginx |
