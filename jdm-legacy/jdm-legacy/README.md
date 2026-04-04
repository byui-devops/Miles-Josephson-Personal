# JDM Legacy 🇯🇵

A full-stack web application cataloging Japanese performance vehicles across three eras — Past, Present, and Future. Built for ITM 300 Cloud Computing.

## Tech Stack

- **Backend:** Python 3.12, Flask 3.0, Flask-SQLAlchemy, Gunicorn
- **Database:** PostgreSQL (AWS RDS in production, SQLite in tests)
- **Infrastructure:** AWS EC2 + RDS via Terraform
- **CI/CD:** GitHub Actions (build + release pipelines)
- **Container:** Docker + Docker Hub

---

## Local Development

### Prerequisites
- Docker + Docker Compose
- Python 3.12+

### Run with Docker Compose (recommended)
```bash
git clone https://github.com/<your-username>/jdm-legacy.git
cd jdm-legacy
docker-compose up --build
```
App available at: http://localhost:5000

### Run without Docker
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set your DATABASE_URL or use the default (requires local Postgres)
export DATABASE_URL=postgresql://jdmuser:jdmpass@localhost:5432/jdmlegacy

python run.py
```

---

## Running Tests
```bash
pip install -r requirements.txt
pytest tests/ -v --cov=app --cov-report=term-missing
```

Tests use an in-memory SQLite database — no running Postgres required.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/cars` | List all cars |
| GET | `/api/cars?era=past` | Filter by era (past/present/future) |
| GET | `/api/cars?forza=true` | Filter Forza HZ6 available cars |
| GET | `/api/cars/<id>` | Get single car |
| POST | `/api/cars` | Create car (JSON body) |

**POST /api/cars body:**
```json
{
  "make": "Nissan",
  "model": "Skyline GT-R R32",
  "year": 1989,
  "era": "past",
  "horsepower": 280,
  "description": "The legendary Godzilla.",
  "forza_available": true,
  "image_url": "https://..."
}
```

---

## Deployment

### GitHub Actions Secrets Required

| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `DB_PASSWORD` | RDS PostgreSQL password |

### Before First Release

1. Create the Terraform S3 state bucket manually:
```bash
aws s3api create-bucket --bucket jdm-legacy-tfstate --region us-east-1
```

2. Push your code to `main` — the **build pipeline** runs automatically.

3. To trigger the **release pipeline** (provisions AWS infrastructure):
```bash
git tag v1.0.0
git push origin v1.0.0
```

Terraform will provision EC2 + RDS and deploy your Docker image. The EC2 public IP is printed in the pipeline output.

---

## Project Structure

```
jdm-legacy/
├── app/
│   ├── __init__.py       # App factory + seed data
│   ├── models.py         # Car model
│   ├── routes.py         # API endpoints
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── tests/
│   ├── conftest.py
│   └── test_app.py       # 20 unit + integration tests
├── terraform/
│   ├── main.tf           # EC2, RDS, Security Groups
│   ├── variables.tf
│   └── outputs.tf
├── .github/workflows/
│   ├── build.yml         # Build pipeline (on push to main)
│   └── release.yml       # Release pipeline (on git tag)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── REPORT.md             # Final project report
```

---

*ITM 300 Cloud Computing — Spring 2026*
