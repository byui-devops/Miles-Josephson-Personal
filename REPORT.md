# JDM Legacy — Final Project Report
### ITM 300 | Cloud Computing | Idaho Falls Campus
**Submitted by:** Miles  
**Date:** April 2026  
**Supervisor:** [Professor Name]

---

## 1. Project Description & Problem Statement

The automotive enthusiast community lacks a centralized, visually compelling digital reference for Japanese Domestic Market (JDM) vehicles across all eras. Existing resources are fragmented — scattered across wikis, forum threads, and manufacturer sites — with no unified interface that contextualizes these machines historically. This project addresses that gap.

**JDM Legacy** is a full-stack web application built on Flask and PostgreSQL that catalogs Japanese performance vehicles across three distinct eras:

- **Past** — Pre-2000 icons such as the Nissan Skyline GT-R R32, Toyota Supra MK4, and Honda NSX that defined an era of Japanese engineering dominance
- **Present** — Current production models including the Toyota GR Yaris, Honda Civic Type R FL5, and Lexus LFA that carry the JDM torch forward
- **Future** — Upcoming concepts and confirmed releases such as the Nissan Hyper Force, Honda Prelude revival, and Mazda Iconic SP that preview the next generation of Japanese performance

Each vehicle entry includes manufacturer, model name, production year, horsepower rating, era classification, a full description, and a flag indicating availability in Forza Horizon 6. The application exposes a RESTful JSON API and serves a cinematic dark-themed frontend with era filtering, Forza-only filtering, and a detail modal for each vehicle.

The project was themed around two personal milestones: an upcoming 10-day tourist trip to Japan and the anticipated release of Forza Horizon 6 — both of which made Japanese automotive culture a fitting and personally meaningful subject.

---

## 2. Architecture Overview

The application follows a three-tier architecture fully provisioned on AWS:

```
Browser → EC2 (Flask + Gunicorn in Docker) → RDS (PostgreSQL)
```

**Backend:** Python 3.12 with Flask 3.0, Flask-SQLAlchemy, and Gunicorn as the WSGI server. The application factory pattern (`create_app()`) enables clean test isolation using an in-memory SQLite database during CI, while PostgreSQL is used in production.

**Database:** AWS RDS PostgreSQL 16. The `cars` table stores all vehicle records. On first boot the application seeds 14 vehicles across the three eras automatically via SQLAlchemy.

**Frontend:** Vanilla HTML/CSS/JavaScript served by Flask's template engine. The UI features a cinematic dark aesthetic with Bebas Neue display typography, era-based color coding (red for past, gold for present, blue for future), animated hero section, and a card grid with modal detail views. All data is fetched client-side from the `/api/cars` endpoint.

**Infrastructure as Code:** Terraform provisions all AWS resources — EC2 instance (t2.micro), RDS PostgreSQL (db.t3.micro), and two security groups. Terraform state is stored remotely in an S3 bucket. The EC2 user-data script installs Docker and runs the application container on boot.

**CI/CD:** Two GitHub Actions pipelines:
- **Build pipeline** — triggers on every push to `main`: runs pytest (unit + integration tests), builds the Docker image, and pushes to Docker Hub tagged with the commit SHA and `latest`
- **Release pipeline** — triggers on git tag push (e.g. `v1.0.0`): re-runs tests, pushes a versioned Docker image, then runs `terraform apply` to provision/update infrastructure and deploy the new image

---

## 3. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the frontend SPA |
| GET | `/api/health` | Health check — returns `{"status":"ok"}` |
| GET | `/api/cars` | List all cars. Supports `?era=past\|present\|future` and `?forza=true\|false` query params |
| GET | `/api/cars/<id>` | Get a single car by ID |
| POST | `/api/cars` | Create a new car entry (JSON body) |

---

## 4. Application URL (EC2)

> **Replace this with your actual EC2 public IP or DNS after running `terraform apply`**

```
http://<EC2_PUBLIC_IP>:5000
```

The EC2 public IP and DNS are output automatically at the end of the Terraform apply step in the release pipeline:

```
Outputs:
ec2_public_ip  = "x.x.x.x"
ec2_public_dns = "ec2-x-x-x-x.compute-1.amazonaws.com"
app_url        = "http://x.x.x.x:5000"
```

---

## 5. Screenshot

> **Insert screenshot here** — open `http://<EC2_PUBLIC_IP>:5000` in your browser after deployment and capture the full page showing the hero section and car grid.

Suggested screenshots to include:
1. Full hero section with animated title and era counters
2. Car grid filtered to "PAST" era showing R32, Supra MK4, NSX cards
3. Modal open on the Nissan Skyline GT-R R32 showing full detail view
4. GitHub Actions showing green build and release pipeline runs
5. Docker Hub repository showing pushed image tags

---

## 6. Codebase URL

```
https://github.com/<your-username>/jdm-legacy
```

Repository structure:
```
jdm-legacy/
├── app/
│   ├── __init__.py          # App factory, DB init, seed data
│   ├── models.py            # Car SQLAlchemy model
│   ├── routes.py            # Flask Blueprint + API endpoints
│   ├── templates/
│   │   └── index.html       # Frontend SPA
│   └── static/
│       ├── css/style.css    # Cinematic dark theme
│       └── js/app.js        # Fetch, filter, modal logic
├── tests/
│   ├── conftest.py
│   └── test_app.py          # 20 unit + integration tests
├── terraform/
│   ├── main.tf              # EC2, RDS, Security Groups
│   ├── variables.tf
│   └── outputs.tf
├── .github/workflows/
│   ├── build.yml            # Build pipeline
│   └── release.yml          # Release pipeline (includes Terraform)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── .gitignore
```

---

## 7. Docker Hub Image URL

```
https://hub.docker.com/r/<your-username>/jdm-legacy
```

**Pull command:**
```bash
docker pull <your-username>/jdm-legacy:latest
```

**Run locally against a local Postgres instance:**
```bash
docker run -p 5000:5000 \
  -e DATABASE_URL="postgresql://jdmuser:jdmpass@host.docker.internal:5432/jdmlegacy" \
  <your-username>/jdm-legacy:latest
```

Image tags published:
- `latest` — always points to the most recent successful build
- `<git-sha>` — pinned to every build pipeline run
- `v1.0.0`, `v1.1.0`, etc. — pinned to every release pipeline tag

---

## 8. Lessons Learned

**Testing against SQLite vs PostgreSQL in CI**
The application uses PostgreSQL in production but SQLite in-memory for tests. This required careful attention to SQLAlchemy compatibility — for example, PostgreSQL-specific column types would break SQLite tests. Using the standard `String`, `Integer`, `Boolean`, and `Text` column types across the board kept the test suite portable without needing a running Postgres container in every CI run.

**Terraform state and the S3 backend**
One of the most important lessons was setting up remote state in S3 before running any `terraform apply`. Running apply twice with local state causes Terraform to try to create duplicate resources. The S3 backend with state locking (via DynamoDB) prevents this. This mirrors what we did in ITM 300 Skills Lab 9 and reinforced why remote state is non-negotiable in any real environment.

**Secrets management in GitHub Actions**
All sensitive values — AWS credentials, Docker Hub token, and the RDS password — are stored as GitHub Actions secrets and injected as environment variables at runtime. No secrets appear anywhere in the codebase or are ever committed to version control. This is a professional practice that would be required in any production environment.

**The release pipeline dependency chain**
Structuring the release pipeline so that `infrastructure` depends on `build-and-push`, which depends on `test`, enforced a correct promotion gate: code that fails tests never reaches Docker Hub, and infrastructure is never provisioned with an untested image. This sequential dependency modeling was one of the most valuable architectural decisions in the project.

**Docker networking between EC2 and RDS**
The EC2 user-data script runs the Docker container with the `DATABASE_URL` environment variable set to the RDS endpoint address that Terraform outputs. Because the RDS security group only allows inbound PostgreSQL connections from the EC2 security group (not from the public internet), the database is properly isolated. This is a pattern directly applicable to production cloud deployments.

**Gunicorn vs Flask dev server**
The Dockerfile uses Gunicorn as the WSGI server rather than Flask's built-in development server. Flask's dev server is single-threaded and not suitable for production. Gunicorn with two workers handles concurrent requests properly and is the industry standard for Flask deployments in containers.

**Personal reflection**
Building a project around a personal interest — Japanese cars in the context of an upcoming Japan trip and Forza Horizon 6 — made the engineering decisions feel meaningful rather than abstract. Choosing which cars to seed into the database, designing the era classification system, and building the filtering UI were genuinely engaging problems that reinforced every cloud infrastructure concept covered in ITM 300.

---

*Report submitted in partial fulfillment of ITM 300 — Cloud Computing*  
*Idaho Falls Campus | Spring 2026*
