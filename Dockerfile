FROM python:3.12-slim

LABEL maintainer="Miles <your@email.com>"
LABEL description="JDM Legacy — Japanese Car Catalog"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose port
EXPOSE 5000

# Run with gunicorn (production-grade WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "run:app"]
