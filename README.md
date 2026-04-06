# JDM Legacy — Final Project Report
### ITM 350 | Cloud Computing | Idaho Falls Campus
**Submitted by:** Miles Josephson  
**Submitted to:** Brother Jensen  
**Date:** April 2026

---

## 1. Detailed Description & Problem Statement

The automotive enthusiast community lacks a centralized, visually compelling digital reference for Japanese Domestic Market (JDM) vehicles across all eras. Existing resources are fragmented — scattered across wikis, forum threads, and manufacturer sites — with no unified interface that contextualizes these machines historically or connects them to modern gaming culture like Forza Horizon 6.

**JDM Legacy** is a full-stack web application built on Flask and PostgreSQL that catalogs Japanese performance vehicles across three distinct eras:

- **Past** — Pre-2000 icons such as the Nissan Skyline GT-R R32, Toyota Supra MK4, Honda NSX, Mazda RX-7 FD, and Mitsubishi Lancer Evolution VI that defined an era of Japanese engineering dominance
- **Present** — Current production models including the Toyota GR Yaris, Nissan GT-R NISMO, Honda Civic Type R FL5, Subaru BRZ tS, and Lexus LFA that carry the JDM torch forward
- **Future** — Upcoming concepts and confirmed releases such as the Nissan Hyper Force, Honda Prelude revival, Mazda Iconic SP, and Toyota GR GT3 Concept that preview the next generation of Japanese performance

Each vehicle entry includes manufacturer, model name, production year, horsepower rating, era classification, a full description, and a flag indicating availability in Forza Horizon 6. The application exposes a RESTful JSON API and serves a cinematic dark-themed frontend with era filtering, Forza-only filtering, and a detail modal for each vehicle.

The project was themed around two personal milestones: an upcoming 10-day trip to Japan in September and the anticipated release of Forza Horizon 6 — both of which made Japanese automotive culture a fitting and personally meaningful subject for a cloud computing project.

### Architecture Overview

The application follows a three-tier architecture fully provisioned on AWS:

```
Browser → EC2 (Flask + Gunicorn in Docker) → RDS (PostgreSQL)
```

- **Backend:** Python 3.12 with Flask 3.0, Flask-SQLAlchemy, and Gunicorn as the WSGI server
- **Database:** AWS RDS PostgreSQL 16 with 14 vehicles seeded across three eras on first boot
- **Frontend:** Vanilla HTML/CSS/JavaScript with a cinematic dark aesthetic, Bebas Neue display typography, and era-based color coding
- **Infrastructure:** Terraform provisions EC2 (t2.micro), RDS (db.t3.micro), and security groups with state stored in S3
- **CI/CD:** Two GitHub Actions pipelines — a build pipeline on every push to main, and a release pipeline triggered by git tags that runs Terraform and deploys to AWS

---

## 2. EC2 Application URL

```
http://98.84.152.232:5000
```

---

## 3. Screenshot of Application Successfully Running

> **[Insert screenshot here]** — Screenshot of JDM Legacy running at http://98.84.152.232:5000 showing the hero section with the animated title "THE SOUL OF JAPANESE PERFORMANCE", the era counter displaying 5 Legends, 5 Icons, and 4 Visions, and the car grid with cards for the Nissan Skyline GT-R R32, Toyota Supra MK4, Honda NSX, and other vehicles.

---

## 4. Codebase URL

```
https://github.com/byui-devops/Miles-Josephson-Personal
```

Repository structure:
```
Miles-Josephson-Personal/
├── .github/workflows/
│   ├── build.yml          # Build pipeline — triggers on push to main
│   └── release.yml        # Release pipeline — triggers on git tag
├── app/
│   ├── __init__.py        # App factory, DB init, seed data
│   ├── models.py          # Car SQLAlchemy model
│   ├── routes.py          # Flask Blueprint + REST API endpoints
│   ├── templates/
│   │   └── index.html     # Frontend SPA
│   └── static/
│       ├── css/style.css  # Cinematic dark theme
│       └── js/app.js      # Fetch, filter, modal logic
├── tests/
│   ├── conftest.py
│   └── test_app.py        # 20 unit + integration tests
├── terraform/
│   ├── main.tf            # EC2, RDS, Security Groups
│   ├── variables.tf
│   └── outputs.tf
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
```

---

## 5. Docker Hub Image URL

```
https://hub.docker.com/r/milesjo01/jdm-legacy
```

**Pull command:**
```bash
docker pull milesjo01/jdm-legacy:latest
```

Image tags published:
- `latest` — always points to the most recent successful build
- `v1.0.0` — pinned to the first production release
- `<git-sha>` — pinned to every individual build pipeline run

---

## 6. Lessons Learned

**Small bugs add up fast**
The most important lesson from this entire project is that the details matter enormously. Throughout the deployment process, small issues created real roadblocks — a Docker Hub secret named `DOCKERHUB_USER` instead of `DOCKERHUB_USERNAME`, a PostgreSQL version number (`16.3`) that AWS Academy did not support, AWS credentials expiring mid-deployment, and project files nested one folder too deep for GitHub Actions to detect the workflows. None of these were conceptually difficult problems, but each one required careful debugging to identify and fix. In a real professional environment these are exactly the kinds of issues that separate engineers who ship from engineers who don't.

**AWS Academy credential expiration is a real constraint**
AWS Academy issues temporary credentials that expire every 4 hours. This meant that any time I stepped away and came back, the credentials in both my local AWS CLI configuration and my GitHub Secrets had expired and needed to be refreshed before anything AWS-related would work. In a production environment this would be handled with IAM roles attached directly to EC2 instances or GitHub's OIDC integration with AWS — permanent, role-based authentication rather than temporary session tokens.

**GitHub branch protection requires a different workflow**
Because the BYUI DevOps organization enforces branch protection on main, every change had to go through a pull request rather than a direct push. This is actually the correct professional workflow — no one pushes directly to main in a real engineering team — but it added steps to every fix. Creating a branch, pushing, opening a PR, merging, then pulling main locally became the rhythm of the project.

**Terraform state management is non-negotiable**
Setting up the S3 backend for Terraform state before running any apply was critical. Without remote state, running the pipeline twice would attempt to create duplicate AWS resources and fail. The S3 backend ensures Terraform always knows the current state of infrastructure regardless of which machine or pipeline runner is executing the commands.

**Docker Compose is invaluable for local development**
Being able to run `docker-compose up --build` and have a fully working Flask + PostgreSQL environment locally — identical to production — made development and debugging significantly faster. Testing locally before pushing to the pipeline saved a lot of pipeline minutes and made it easy to verify the app was working before attempting a full cloud deployment.

**The architecture decisions came together**
Looking back at the full system — GitHub → GitHub Actions → Docker Hub → Terraform → EC2 + RDS — every piece has a clear purpose and connects logically to the next. The build pipeline ensures code quality on every commit. The release pipeline ensures infrastructure and deployment are automated and repeatable. Terraform ensures infrastructure is version-controlled and reproducible. This is the same pattern used in professional cloud engineering teams, and building it end-to-end for a project I actually cared about made every concept from ITM 350 click into place.

---

*Report submitted in partial fulfillment of ITM 350 — Cloud Computing*  
*Idaho Falls Campus | Spring 2026*  
*Submitted to Brother Jensen*
