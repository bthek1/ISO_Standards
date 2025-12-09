# Frontend Deployment Guide

## 📋 Current Status

✅ **Frontend Setup**: Complete (React 18 + TypeScript + MUI)
✅ **Build Pipeline**: Configured (Vite, npm scripts)
✅ **AWS Infrastructure**: Deployed (S3 + CloudFront + IAM)
✅ **GitHub Actions**: Configured (OIDC-based CI/CD)

## 🎯 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Git Repository (main)                     │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ GitHub Actions   │
                    │  (Build & Push)  │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
         ┌──────────────┐         ┌─────────────────┐
         │ S3 Bucket    │         │ CloudFront CDN  │
         │ (Storage)    │◄────────│ (Distribution)  │
         └──────────────┘         └────────┬────────┘
                                          │
                                          ▼
                              ┌────────────────────────┐
                              │ ISO Custom Domain      │
                              │ iso.benedictthekkel... │
                              └────────────────────────┘
```

## 🔧 Deployment Components

### 1. AWS S3 Bucket

- **Name**: `iso-standards-frontend`
- **Region**: `ap-southeast-2` (Sydney, Australia)
- **Purpose**: Store built frontend files
- **Status**: ✅ Active

### 2. CloudFront Distribution

- **ID**: `E2494N0PGM4KTG`
- **Domain**: `d1pjttps83iyey.cloudfront.net`
- **Purpose**: CDN + HTTPS + SPA routing
- **Status**: ✅ Active

### 3. GitHub Actions Workflow

- **File**: `.github/workflows/deploy-frontend.yml`
- **Trigger**: Push to `main` on `Frontend/**` changes
- **Steps**: Build → Auth → Deploy → Invalidate
- **Status**: ✅ Ready

### 4. IAM Authentication

- **Role**: `github-actions-role`
- **Method**: OIDC (no static credentials)
- **Permissions**: S3 + CloudFront
- **Status**: ✅ Configured

## 🚀 Quick Start

### Option 1: Manual Deployment (Immediate)

```bash
cd /home/bthek1/ISO_Standards/Frontend

# Build the frontend
npm run build

# Deploy to S3
aws s3 sync dist/ s3://iso-standards-frontend --delete --profile ben-sso

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id E2494N0PGM4KTG \
  --paths "/*" \
  --profile ben-sso

echo "✅ Deployment complete!"
echo "📍 Access at: https://d1pjttps83iyey.cloudfront.net"
```

### Option 2: Automated Deployment (Via GitHub)

```bash
# Commit and push to main
git add Frontend/
git commit -m "feat: update frontend"
git push origin main

# GitHub Actions will automatically:
# 1. Build the React app
# 2. Deploy to S3
# 3. Invalidate CloudFront
# 4. Live in ~2 minutes
```

## 📡 DNS Configuration

### Step 1: Add CNAME Record

Add this record to your DNS provider (where `benedictthekkel.com.au` is hosted):

```
Host: iso
Type: CNAME
TTL: 3600 (1 hour)
Value: d1pjttps83iyey.cloudfront.net
```

### Step 2: Verify DNS Propagation

```bash
# Check DNS resolution
nslookup iso.benedictthekkel.com.au

# Should resolve to: d1pjttps83iyey.cloudfront.net
```

### Step 3: Update CloudFront (Optional but Recommended)

For a more professional setup with proper HTTPS certificate:

```bash
# Create ACM certificate for iso.benedictthekkel.com.au
# (Manual step in AWS Console or via CLI)

# Update CloudFront distribution to use custom domain
# This associates the certificate with your domain
```

## 📊 Testing Deployment

### Test 1: Build Verification

```bash
cd /home/bthek1/ISO_Standards/Frontend
npm run build

# Should output:
# ✓ 1234 modules transformed
# dist/index.html     0.45 kB │ gzip: 0.25 kB
# dist/assets/...     XXX kB  │ gzip: XXX kB
```

### Test 2: CloudFront Distribution

```bash
# Check distribution is active
aws cloudfront get-distribution --id E2494N0PGM4KTG --profile ben-sso

# Should show Status: "Deployed"
```

### Test 3: S3 Bucket Contents

```bash
# List deployed files
aws s3 ls s3://iso-standards-frontend --recursive --profile ben-sso

# Should show:
# index.html
# assets/...
```

### Test 4: Access via URL

```bash
# Test CloudFront URL
curl -I https://d1pjttps83iyey.cloudfront.net

# After DNS setup, test custom domain
curl -I https://iso.benedictthekkel.com.au
```

### Test 5: Cache Headers

```bash
# Check HTML (should be no-cache)
curl -I https://d1pjttps83iyey.cloudfront.net/index.html
# Should show: Cache-Control: max-age=0, no-cache, no-store, must-revalidate

# Check assets (should be 1-year cache)
curl -I https://d1pjttps83iyey.cloudfront.net/assets/main.js
# Should show: Cache-Control: max-age=31536000
```

## 🔄 Deployment Workflow

### On Each Push to Main

1. **GitHub Action Triggers**
   - Event: Push to `main` branch on `Frontend/` path

2. **Build Stage** (30-60 seconds)
   - Checkout code
   - Install dependencies
   - Run TypeScript type check
   - Build with Vite
   - Output to `Frontend/dist/`

3. **Authentication** (Instant)
   - Assume `github-actions-role` via OIDC
   - Get temporary AWS credentials

4. **Deploy Stage** (30-60 seconds)
   - Sync files to S3
   - Set cache headers (HTML: no-cache, assets: 1-year)
   - Preserve versions in S3

5. **Invalidation** (10-60 seconds)
   - Create CloudFront invalidation for `/*`
   - Clears edge cache globally
   - Forces CDN to fetch latest from S3

6. **Live** (30 seconds - 5 minutes)
   - All edge locations updated
   - Available at `https://iso.benedictthekkel.com.au`

### Total Time: **2-10 minutes** from push to live

## 📈 Monitoring & Debugging

### View Deployment History

```bash
# Recent S3 versions
aws s3api list-object-versions \
  --bucket iso-standards-frontend \
  --max-items 10 \
  --profile ben-sso

# Recent CloudFront invalidations
aws cloudfront list-invalidations \
  --distribution-id E2494N0PGM4KTG \
  --profile ben-sso
```

### Check GitHub Actions Logs

1. Go to GitHub repository
2. Click "Actions" tab
3. Select "Deploy Frontend to AWS S3 + CloudFront"
4. Click latest run
5. Check each step's output

### CloudFront Metrics

```bash
# Get distribution stats
aws cloudfront get-distribution-statistics \
  --distribution-id E2494N0PGM4KTG \
  --profile ben-sso
```

## 🐛 Troubleshooting

### Issue: CloudFront shows old files

**Solution**: Manually invalidate cache

```bash
aws cloudfront create-invalidation \
  --distribution-id E2494N0PGM4KTG \
  --paths "/*" \
  --profile ben-sso
```

### Issue: 404 on custom domain

**Possible Causes**:

1. DNS CNAME not configured correctly
2. CloudFront distribution not deployed (takes 10-30 min)
3. S3 bucket not public

**Debug Steps**:

```bash
# Verify DNS
nslookup iso.benedictthekkel.com.au

# Check S3 bucket policy
aws s3api get-bucket-policy --bucket iso-standards-frontend --profile ben-sso

# Check CloudFront origin
aws cloudfront get-distribution-config --id E2494N0PGM4KTG --profile ben-sso
```

### Issue: GitHub Actions fails

**Check**:

1. Is OIDC role still attached? `aws iam get-role --role-name github-actions-role`
2. Are permissions still there? `aws iam get-role-policy --role-name github-actions-role --policy-name s3-cloudfront-policy`
3. Check GitHub Actions logs for specific error

### Issue: Files don't cache correctly

**Verify cache headers**:

```bash
curl -I https://d1pjttps83iyey.cloudfront.net/assets/main.js | grep Cache-Control
# Should show: max-age=31536000 (for assets)

curl -I https://d1pjttps83iyey.cloudfront.net/index.html | grep Cache-Control
# Should show: max-age=0, no-cache (for HTML)
```

## 🔒 Security Checklist

✅ **S3 Bucket**

- [x] Versioning enabled (rollback capability)
- [x] Block public access disabled (CloudFront can access)
- [x] Public read policy attached
- [x] HTTPS enforced via CloudFront

✅ **CloudFront**

- [x] HTTPS enabled (redirect HTTP)
- [x] Origin access restricted (S3 only)
- [x] Security headers configured

✅ **GitHub Actions**

- [x] OIDC authentication (no static keys)
- [x] Limited IAM permissions (least privilege)
- [x] Role restricted to main branch

✅ **Credentials**

- [x] AWS credentials use ben-sso profile
- [x] No hardcoded secrets in repo
- [x] No secrets in GitHub Actions logs

## 📝 Cost Optimization

**Current Setup Costs** (Estimated):

- S3: $0.23/GB/month stored → ~$2-5/month
- CloudFront: $0.085/GB transferred → $5-50/month (varies with traffic)
- **Total**: $7-55/month depending on traffic

**To Reduce Costs**:

1. Set S3 lifecycle policies (move old versions to Glacier)
2. Configure CloudFront compression (already enabled)
3. Use CloudFront security policies (prevent expensive edge locations)

## 🎓 Next Steps

1. **Configure DNS** (Manual)

   ```
   Add CNAME: iso → d1pjttps83iyey.cloudfront.net
   ```

2. **Test Deployment** (Optional)

   ```bash
   cd Frontend && npm run build
   aws s3 sync dist/ s3://iso-standards-frontend --delete --profile ben-sso
   ```

3. **Push to Main** (Automatic)

   ```bash
   git commit -m "feat: deploy frontend"
   git push origin main
   ```

4. **Monitor**
   - Check GitHub Actions logs
   - Access <https://iso.benedictthekkel.com.au>
   - Verify cache headers and performance

## 📞 Support

For issues or questions:

1. Check GitHub Actions logs (Actions tab)
2. Review CloudFront distribution in AWS Console
3. Check S3 bucket contents
4. Verify DNS with `nslookup`

---

**Setup Date**: 2025-11-30
**Status**: ✅ Ready for Production
**Last Updated**: [Current Timestamp]
