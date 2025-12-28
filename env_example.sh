# EAIFCH Environment Configuration
# Copy this file to .env and update with your values
# DO NOT commit .env file to version control

# =======================
# Application Settings
# =======================
APP_NAME=EAIFCH
APP_VERSION=1.1.0
ENV=development  # development, staging, production
DEBUG=true
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# =======================
# API Server Settings
# =======================
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=false  # Set to true only in development

# API Security
SECRET_KEY=your-secret-key-here-change-this-in-production
API_KEY_HEADER=X-API-Key
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# =======================
# Database Settings
# =======================
# PostgreSQL
DATABASE_URL=postgresql://eaifch:eaifch_password@localhost:5432/eaifch_db
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_POOL_TIMEOUT=30

# SQLite (alternative for development)
# DATABASE_URL=sqlite:///./eaifch.db

# =======================
# Redis Cache Settings
# =======================
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600  # Cache time-to-live in seconds
CACHE_ENABLED=true

# =======================
# Authentication & Security
# =======================
# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# OAuth (if using external auth)
OAUTH_CLIENT_ID=
OAUTH_CLIENT_SECRET=
OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback

# =======================
# Email Settings (Optional)
# =======================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-specific-password
SMTP_FROM=noreply@eaifch.org
SMTP_USE_TLS=true

# =======================
# File Storage
# =======================
# Local storage
UPLOAD_DIR=./data/uploads
MAX_UPLOAD_SIZE_MB=50

# S3 (if using cloud storage)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=eaifch-data
AWS_REGION=us-east-1

# =======================
# Monitoring & Analytics
# =======================
# Sentry (error tracking)
SENTRY_DSN=
SENTRY_ENVIRONMENT=development

# Prometheus
PROMETHEUS_ENABLED=true
METRICS_PORT=9090

# Google Analytics
GA_TRACKING_ID=

# =======================
# External Services
# =======================
# OpenAI API (for advanced NLP features)
OPENAI_API_KEY=

# Hugging Face (for ML models)
HUGGINGFACE_TOKEN=

# Google Cloud Vision (for image analysis)
GOOGLE_APPLICATION_CREDENTIALS=./credentials/gcp-service-account.json

# =======================
# Cultural Heritage APIs
# =======================
# Europeana API
EUROPEANA_API_KEY=

# UNESCO API
UNESCO_API_KEY=

# ICOM Integration
ICOM_API_KEY=

# =======================
# Compliance & Regulations
# =======================
# GDPR Settings
GDPR_ENABLED=true
DATA_RETENTION_DAYS=365
COOKIE_CONSENT_REQUIRED=true

# EU AI Act Compliance
EU_AI_ACT_MODE=strict  # strict, moderate, lenient

# =======================
# Feature Flags
# =======================
FEATURE_RUST_ENGINE=false
FEATURE_ML_BIAS_DETECTION=true
FEATURE_REAL_TIME_ASSESSMENT=true
FEATURE_BATCH_PROCESSING=true
FEATURE_API_V2=false
FEATURE_EXPERIMENTAL=false

# =======================
# Dashboard Settings
# =======================
DASHBOARD_URL=http://localhost:3000
DASHBOARD_REFRESH_INTERVAL=30  # seconds

# =======================
# Testing & Development
# =======================
# Test Database
TEST_DATABASE_URL=sqlite:///./test_eaifch.db

# Development Tools
PROFILING_ENABLED=false
SQL_ECHO=false  # Set to true to see all SQL queries

# Mock External Services (for testing)
MOCK_EXTERNAL_APIs=false

# =======================
# Backup & Maintenance
# =======================
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *  # Cron format: daily at 2 AM
BACKUP_RETENTION_DAYS=30
BACKUP_DESTINATION=./backups

# Database maintenance
AUTO_VACUUM=true
MAINTENANCE_WINDOW=02:00-04:00

# =======================
# Localization
# =======================
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,fr,es,de,ar,zh
TIMEZONE=UTC

# =======================
# Performance & Optimization
# =======================
# Worker settings
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
CELERY_WORKERS=4

# Caching strategy
CACHE_STRATEGY=redis  # redis, memory, none
ENABLE_COMPRESSION=true

# Query optimization
QUERY_TIMEOUT_SECONDS=30
MAX_PAGE_SIZE=100

# =======================
# Logging
# =======================
LOG_FORMAT=json  # json, text
LOG_FILE=./logs/eaifch.log
LOG_ROTATION=daily
LOG_RETENTION_DAYS=30

# Separate log files
ERROR_LOG_FILE=./logs/error.log
ACCESS_LOG_FILE=./logs/access.log
AUDIT_LOG_FILE=./logs/audit.log

# =======================
# Documentation
# =======================
DOCS_ENABLED=true
DOCS_URL=/docs
REDOC_URL=/redoc
OPENAPI_URL=/openapi.json

# =======================
# Custom Settings
# =======================
# Add your custom configuration here
CUSTOM_TAXONOMY_PATH=
CUSTOM_PRINCIPLES_ENABLED=false
INSTITUTION_NAME=
INSTITUTION_LOGO_URL=

# =======================
# Notes
# =======================
# - Always use strong, unique passwords in production
# - Keep this file secret and never commit to version control
# - Rotate secrets regularly
# - Use environment-specific .env files (.env.development, .env.production)
# - Consider using a secrets management service (AWS Secrets Manager, HashiCorp Vault)
