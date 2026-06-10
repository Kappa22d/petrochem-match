# PetroChem Match — Intelligent B2B Matchmaking for Oil & Gas

![Status](https://img.shields.io/badge/status-MVP-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A professional, production-ready B2B matchmaking platform connecting oil & gas operators, refiners, chemical engineers, specialty chemical suppliers, and consultants. Built with Flask, Supabase, and Tailwind CSS.

## 🎯 Key Features

- **Smart Matching Engine**: AI-assisted compatibility scoring between professionals and organizations
- **Professional Directory**: Search and filter by role, expertise, location, and company size
- **RFQ Hub**: Post and respond to Requests for Quote with full collaboration workflow
- **Engineering Calculators**:
  - ESG/CO2 Savings Estimator
  - Chemical Property Lookup (PubChemPy integration)
  - Unit Converter (SI ↔ Imperial)
- **Secure Authentication**: Supabase Auth with email and magic links
- **Premium UX**: Dark/light mode, mobile-responsive, industry-appropriate design

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11+, Flask |
| **Database** | Supabase (PostgreSQL) |
| **ORM** | SQLAlchemy 2.0 |
| **Frontend** | Jinja2, Tailwind CSS, HTMX |
| **Auth** | Supabase Auth |
| **Forms** | WTForms |
| **Chem Data** | PubChemPy |

## 📋 Project Structure

```
petrochem-match/
├── app/
│   ├── __init__.py                 # App factory
│   ├── config.py                   # Configuration
│   ├── models/                     # SQLAlchemy models
│   │   └── __init__.py
│   ├── blueprints/                 # Route blueprints
│   │   ├── main.py                 # Homepage, landing
│   │   ├── auth.py                 # Auth routes
│   │   ├── profile.py              # Profile management
│   │   ├── directory.py            # Directory & search
│   │   ├── matching.py             # Matching engine
│   │   ├── rfq.py                  # RFQ management
│   │   └── tools.py                # Engineering calculators
│   ├── templates/                  # Jinja2 templates
│   │   ├── base.html               # Base layout
│   │   ├── landing.html            # Homepage
│   │   ├── dashboard.html          # User dashboard
│   │   └── ...
│   ├── static/                     # Static files
│   │   ├── css/
│   │   └── js/
│   └── utils.py                    # Utility functions
├── instance/                       # Instance-specific files
├── migrations/                     # Alembic migrations (optional)
├── tests/                          # Test suite
├── requirements.txt                # Dependencies
├── .env.example                    # Environment template
├── run.py                          # Entry point
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or use Supabase hosted)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/petrochem-match.git
cd petrochem-match
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **Settings → API** and copy:
   - Project URL → `SUPABASE_URL`
   - Anon Key → `SUPABASE_KEY`
   - Service Role Key → `SUPABASE_SERVICE_ROLE_KEY`
3. Create `.env` from `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. Update `.env` with your Supabase credentials and generate a `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### 5. Initialize Database

```bash
# Run migrations (create tables)
flask db upgrade

# Seed sample data
python -c "from app import create_app, db; from app.utils import seed_database; app = create_app(); with app.app_context(): seed_database()"
```

### 6. Run Development Server

```bash
python run.py
```

Visit **http://localhost:5000** in your browser.

## 📚 Supabase Setup (Detailed)

### Create Tables

Run these SQL commands in your Supabase SQL Editor:

```sql
-- Users (managed by Supabase Auth, we'll extend it)
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE,
  full_name TEXT,
  role TEXT CHECK (role IN ('operator', 'engineer', 'supplier', 'consultant')),
  company TEXT,
  bio TEXT,
  location TEXT,
  expertise_tags JSONB DEFAULT '[]',
  years_experience INT,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- RFQs (Requests for Quote)
CREATE TABLE public.rfqs (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  specifications JSONB,
  status TEXT DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'closed')),
  budget_range TEXT,
  anonymous BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Listings (Offers from suppliers)
CREATE TABLE public.listings (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  category TEXT,
  specifications JSONB,
  price_range TEXT,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Matches (Compatibility records)
CREATE TABLE public.matches (
  id BIGSERIAL PRIMARY KEY,
  user_a_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  user_b_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  score NUMERIC(3,2),
  reason TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- Chemicals (for lookup tool)
CREATE TABLE public.chemicals (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  cas_number TEXT,
  formula TEXT,
  molecular_weight NUMERIC,
  properties JSONB,
  created_at TIMESTAMP DEFAULT now()
);
```

## 🔐 Security & Best Practices

- ✅ All secrets in `.env` (never commit)
- ✅ Input validation via WTForms
- ✅ CSRF protection enabled
- ✅ Proper error handling and logging
- ✅ Industry disclaimers on technical pages
- ✅ Rate limiting on search/RFQs (configurable)
- ✅ Supabase Row-Level Security (RLS) ready

## 📱 Deployment

### Deploy to Render

1. Push to GitHub
2. Connect repo to [Render.com](https://render.com)
3. Create Web Service:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn run:app`
   - Environment: Add all `.env` variables
4. Deploy!

### Deploy to Railway

```bash
railway link  # Authenticate
railway up    # Deploy
```

### Deploy to Fly.io

```bash
fly launch
fly deploy
```

## 🧪 Testing

```bash
pytest tests/
pytest --cov=app tests/  # With coverage
```

## 📖 Usage Examples

### Create a User Profile

```python
from app.models import User, Profile
from app import db

user = User(email='engineer@example.com')
db.session.add(user)
db.session.commit()

profile = Profile(
    user_id=user.id,
    full_name='Jane Smith',
    role='engineer',
    company='ChemTech Solutions',
    expertise_tags=['catalysts', 'corrosion', 'CO2-capture'],
    years_experience=8
)
db.session.add(profile)
db.session.commit()
```

### Search Directory

```python
from app.models import Profile

results = Profile.query.filter(
    Profile.role == 'supplier',
    Profile.location.ilike('%Texas%')
).all()
```

## 🎨 Customization

### Modify Color Scheme

Edit `tailwind.config.js` or use Tailwind CDN classes directly in templates.

### Add New Features

1. Create new model in `app/models/`
2. Create new blueprint in `app/blueprints/`
3. Add routes and templates
4. Update migrations (Alembic)

## ⚠️ Legal & Compliance

**Disclaimer**: This platform is for informational purposes only. All technical calculations, chemical recommendations, and business insights should be verified by qualified professionals before operational use.

- GDPR-ready (user data export, deletion)
- Industry-specific compliance hooks
- Privacy policy template included

## 📞 Support & Contributing

For issues, feature requests, or contributions:

1. Open a GitHub Issue
2. Fork and create a feature branch
3. Submit a Pull Request

## 📄 License

MIT License — see LICENSE file for details.

---

**Built for the future of oil & gas chemistry. Connect. Collaborate. Innovate.**
