# Production Configuration

## Environment Setup

### Backend (.env)
```bash
# API Keys
HUGGINGFACE_API_TOKEN=your_token_here
OPENAI_API_KEY=your_key_here

# Mode
DEMO_MODE=0  # Set to 0 for production
ENVIRONMENT=production

# Database (PostgreSQL recommended for production)
DATABASE_URL=postgresql://user:password@localhost:5432/finagent

# Security
JWT_SECRET_KEY=generate-a-secure-random-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Storage (AWS S3 or Azure Blob)
STORAGE_TYPE=s3
S3_BUCKET=finagent-files
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# OCR
TESSERACT_PATH=/usr/bin/tesseract

# IBM Orchestrate (Optional)
IBM_ORCH_API_KEY=your_secure_key
```

### Frontend (.env.production)
```bash
VITE_API_URL=https://api.yourdomain.com
```

## Docker Deployment

### Build Images
```bash
# Backend
docker build -t finagent-backend:latest -f docker/Dockerfile.backend .

# Frontend
docker build -t finagent-frontend:latest -f docker/Dockerfile.frontend .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

## Cloud Deployment Options

### 1. AWS (Recommended)
- **Backend**: AWS ECS/Fargate or EC2
- **Frontend**: AWS S3 + CloudFront
- **Database**: AWS RDS (PostgreSQL)
- **Storage**: AWS S3
- **Cost**: ~$50-100/month for small workload

### 2. Azure
- **Backend**: Azure App Service or Container Instances
- **Frontend**: Azure Static Web Apps
- **Database**: Azure Database for PostgreSQL
- **Storage**: Azure Blob Storage
- **Cost**: ~$50-100/month

### 3. Google Cloud
- **Backend**: Cloud Run or GKE
- **Frontend**: Firebase Hosting or Cloud Storage
- **Database**: Cloud SQL (PostgreSQL)
- **Storage**: Cloud Storage
- **Cost**: ~$40-80/month

### 4. Railway/Render (Quick Deploy)
- **One-click deployment** for both frontend & backend
- Built-in PostgreSQL
- Cost: ~$20-40/month
- **Easiest for hackathon demo**

## Security Checklist

- [ ] Change all default passwords and secret keys
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS for production domain only
- [ ] Set up rate limiting
- [ ] Enable authentication and authorization
- [ ] Configure backup and disaster recovery
- [ ] Set up monitoring and alerts
- [ ] Review and harden database security
- [ ] Enable logging and audit trails
- [ ] Configure firewall rules

## Performance Optimization

### Backend
- Enable Gunicorn/Uvicorn workers (4-8 workers)
- Use Redis for caching
- Configure database connection pooling
- Enable gzip compression

### Frontend
- Build optimized production bundle
- Enable CDN for static assets
- Configure caching headers
- Lazy load routes and components

## Monitoring

### Recommended Tools
- **Application Performance**: New Relic, Datadog, or Application Insights
- **Logs**: Logstash, CloudWatch, or Azure Monitor
- **Uptime**: Pingdom, UptimeRobot
- **Errors**: Sentry

## CI/CD Pipeline

### GitHub Actions (Recommended)
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and deploy backend
        run: |
          # Add your deployment commands
      - name: Build and deploy frontend
        run: |
          # Add your deployment commands
```

## Database Migration

### From SQLite (dev) to PostgreSQL (prod)
```bash
# Export data
pg_dump sqlite:///./finagent.db > backup.sql

# Import to PostgreSQL
psql $DATABASE_URL < backup.sql
```

## Scaling Strategy

### Phase 1: Single Server (0-100 users)
- 1 backend instance
- Static frontend (CDN)
- Managed database

### Phase 2: Horizontal Scaling (100-1000 users)
- Multiple backend instances (load balanced)
- Redis cache
- Async task queue (Celery)

### Phase 3: Microservices (1000+ users)
- Separate services per agent
- API Gateway
- Message queue (RabbitMQ/SQS)
- Auto-scaling

## Cost Estimates

### Small Deployment (10-50 users)
- Hosting: $30-50/month
- Database: $15-25/month
- Storage: $5-10/month
- **Total**: ~$50-85/month

### Medium Deployment (100-500 users)
- Hosting: $100-200/month
- Database: $50-100/month
- Storage: $20-40/month
- CDN: $10-20/month
- **Total**: ~$180-360/month

### Large Deployment (1000+ users)
- Hosting: $500-1000/month
- Database: $200-400/month
- Storage: $100-200/month
- CDN: $50-100/month
- Monitoring: $50-100/month
- **Total**: ~$900-1800/month
