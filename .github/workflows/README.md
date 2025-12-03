# GitHub Actions Workflows

This directory contains CI/CD workflows for the ISO Standards project.

## Workflows Overview

### 🔄 CI - All Tests (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**What it does:**
- Runs backend tests (Python 3.13, PostgreSQL 16)
- Runs frontend tests (Node.js 20)
- Linting and type checking for both
- Generates and uploads coverage reports

**Status:** Required for PR merges

---

### 🧪 Backend Tests (`test-backend.yml`)

**Triggers:**
- Push to `main` or `develop` (Backend changes only)
- Pull requests (Backend changes only)
- Manual workflow dispatch

**Test Matrix:**
- Python: 3.13
- Database: PostgreSQL 16

**Steps:**
1. Install dependencies with `uv`
2. Run Ruff linting
3. Run Black formatting check
4. Run mypy type checking
5. Run database migrations
6. Execute pytest with coverage
7. Upload coverage to Codecov

**Environment:**
- Uses in-memory PostgreSQL service
- Test settings (`config.settings.test`)

---

### 🎨 Frontend Tests (`test-frontend.yml`)

**Triggers:**
- Push to `main` or `develop` (Frontend changes only)
- Pull requests (Frontend changes only)
- Manual workflow dispatch

**Test Matrix:**
- Node.js: 20, 22

**Steps:**
1. Install dependencies with `npm ci`
2. TypeScript type checking
3. ESLint linting
4. Run Vitest tests with coverage
5. Build production bundle
6. Upload coverage to Codecov

---

### 🚀 Deploy Frontend (`deploy-frontend.yml`)

**Triggers:**
- Push to `main` (Frontend changes only)
- Manual workflow dispatch

**Jobs:**
1. **Test:** Runs all frontend tests
2. **Build & Deploy:** Deploys to AWS S3 + CloudFront

**Deployment Steps:**
1. Run tests (type-check, lint, unit tests)
2. Build production bundle
3. Configure AWS credentials (OIDC)
4. Sync to S3 bucket
5. Invalidate CloudFront cache

**AWS Resources:**
- S3 Bucket: `iso-standards-frontend`
- CloudFront Distribution: `E2494N0PGM4KTG`
- Region: `ap-southeast-2`
- IAM Role: `github-actions-role`

**URL:** https://d1pjttps83iyey.cloudfront.net

---

## Required Secrets

### GitHub Secrets

| Secret | Description | Used In |
|--------|-------------|---------|
| `CODECOV_TOKEN` | Codecov upload token | All test workflows |

### AWS Configuration

The deployment uses **OIDC** (OpenID Connect) for authentication - no AWS access keys needed!

**Required AWS Resources:**
- IAM Role: `arn:aws:iam::762233760445:role/github-actions-role`
- Trust relationship configured for GitHub Actions
- S3 bucket with public read access
- CloudFront distribution

---

## Running Workflows Locally

### Backend Tests

```bash
cd Backend

# Install dependencies
uv venv
source .venv/bin/activate
uv pip install -e .

# Create test .env
cat > .env << EOF
DJANGO_ENV=test
DJANGO_SETTINGS_MODULE=config.settings.test
SECRET_KEY=test-secret-key
DEBUG=False
EOF

# Run tests
pytest --cov=. --cov-report=term

# Linting
ruff check .
black --check .
```

### Frontend Tests

```bash
cd Frontend

# Install dependencies
npm ci

# Run tests
npm run test:coverage

# Type check
npm run type-check

# Lint
npm run lint

# Build
npm run build
```

---

## Workflow Status Badges

Add these to your README:

```markdown
[![CI Status](https://github.com/bthek1/ISO_Standards/actions/workflows/ci.yml/badge.svg)](https://github.com/bthek1/ISO_Standards/actions/workflows/ci.yml)
[![Backend Tests](https://github.com/bthek1/ISO_Standards/actions/workflows/test-backend.yml/badge.svg)](https://github.com/bthek1/ISO_Standards/actions/workflows/test-backend.yml)
[![Frontend Tests](https://github.com/bthek1/ISO_Standards/actions/workflows/test-frontend.yml/badge.svg)](https://github.com/bthek1/ISO_Standards/actions/workflows/test-frontend.yml)
[![Deploy Frontend](https://github.com/bthek1/ISO_Standards/actions/workflows/deploy-frontend.yml/badge.svg)](https://github.com/bthek1/ISO_Standards/actions/workflows/deploy-frontend.yml)
```

---

## Troubleshooting

### Backend Tests Failing

**Issue:** PostgreSQL connection errors
- Check that the service is healthy in workflow logs
- Verify DATABASE_URL format
- Ensure migrations run successfully

**Issue:** Import errors
- Verify all dependencies are in `pyproject.toml`
- Check Python version compatibility

### Frontend Tests Failing

**Issue:** Type errors
- Run `npm run type-check` locally
- Check TypeScript version compatibility

**Issue:** Build failures
- Verify all environment variables are set
- Check Vite configuration

### Deployment Failing

**Issue:** AWS authentication errors
- Verify IAM role ARN is correct
- Check OIDC trust relationship
- Ensure role has S3 and CloudFront permissions

**Issue:** S3 sync errors
- Verify bucket name and region
- Check IAM permissions for S3 operations

---

## Best Practices

1. **Always run tests before pushing:**
   ```bash
   # Backend
   cd Backend && pytest

   # Frontend
   cd Frontend && npm test
   ```

2. **Use conventional commits** for automatic changelog generation

3. **Keep workflows DRY** - use composite actions for repeated steps

4. **Monitor workflow costs** - GitHub Actions minutes usage

5. **Security:**
   - Never commit secrets
   - Use OIDC for AWS (no long-lived credentials)
   - Rotate tokens regularly

---

## Future Enhancements

- [ ] Add backend deployment workflow
- [ ] Implement semantic versioning
- [ ] Add performance testing
- [ ] Set up staging environment
- [ ] Add E2E tests with Playwright
- [ ] Implement blue-green deployment
- [ ] Add security scanning (Snyk, Dependabot)
