# 🚀 Frontend Deployment Checklist

## ✅ Completed Setup

- [x] React 18 + TypeScript + Vite frontend built
- [x] Material-UI theme with professional government styling
- [x] Production build verified (152 KB gzipped)
- [x] S3 bucket created (`iso-standards-frontend`, ap-southeast-2)
- [x] CloudFront distribution created (`E2494N0PGM4KTG`)
- [x] GitHub Actions workflow configured (`.github/workflows/deploy-frontend.yml`)
- [x] IAM role created with OIDC authentication
- [x] S3 and CloudFront permissions attached

## ⏳ Remaining Steps (In Order)

### 1. DNS Configuration (5 minutes)
**Status**: ⏳ Pending

Go to your domain registrar and add this record:

```
Subdomain: iso
Type: CNAME
Value: d1pjttps83iyey.cloudfront.net
TTL: 3600
```

Common registrars:
- GoDaddy: https://www.godaddy.com/help/add-a-cname-record-19236
- Route53 (AWS): https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-cloudfront-distribution.html
- Namecheap: https://www.namecheap.com/support/knowledgebase/article.aspx/9646/2237/how-do-i-set-up-a-cname-record
- Other: Search "[registrar name] add CNAME record"

### 2. Verify DNS (2 minutes)
**Status**: ⏳ After step 1

```bash
# Wait 5-10 minutes for DNS propagation
nslookup iso.benedictthekkel.com.au

# Should show:
# Non-authoritative answer:
# iso.benedictthekkel.com.au  canonical name = d1pjttps83iyey.cloudfront.net.
```

### 3. Test Deployment (1 minute)
**Status**: ⏳ After DNS verified

```bash
cd /home/bthek1/ISO_Standards/Frontend

# Build locally
npm run build

# Deploy to S3
aws s3 sync dist/ s3://iso-standards-frontend --delete --profile ben-sso

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id E2494N0PGM4KTG \
  --paths "/*" \
  --profile ben-sso
```

### 4. Verify Access (1 minute)
**Status**: ⏳ After deployment

```bash
# Test CloudFront domain (should work immediately)
curl -I https://d1pjttps83iyey.cloudfront.net

# Test custom domain (after DNS propagation)
curl -I https://iso.benedictthekkel.com.au

# Open in browser
# https://iso.benedictthekkel.com.au
```

## 🎯 Immediate Next Actions

### For Immediate Access (5 minutes)
1. ✅ Everything is ready to deploy
2. Run manual deployment commands above
3. Access via CloudFront URL: `https://d1pjttps83iyey.cloudfront.net`

### For Production Domain (10+ minutes)
1. Add DNS CNAME record to domain registrar
2. Wait 5-30 minutes for DNS propagation
3. Access via custom domain: `https://iso.benedictthekkel.com.au`

### For Automatic Deployments (Ongoing)
1. After DNS is set up, subsequent pushes to main will auto-deploy
2. No manual steps needed after first deployment
3. Changes go live in 2-10 minutes

## 📦 What Gets Deployed

```
Frontend/dist/          → S3: iso-standards-frontend/
├── index.html          (no-cache: max-age=0)
├── assets/
│   ├── main-XXXX.js    (1-year cache: max-age=31536000)
│   ├── main-XXXX.css   (1-year cache: max-age=31536000)
│   └── ...
└── ...
```

## 🔗 Key URLs

| URL | Purpose | Status |
|-----|---------|--------|
| `https://d1pjttps83iyey.cloudfront.net` | CloudFront Domain | ✅ Live Now |
| `https://iso.benedictthekkel.com.au` | Custom Domain | ⏳ After DNS Setup |
| `s3://iso-standards-frontend` | S3 Bucket | ✅ Configured |
| `E2494N0PGM4KTG` | CloudFront Distribution | ✅ Active |

## 🎬 Quick Command Reference

### Manual Deployment
```bash
cd /home/bthek1/ISO_Standards/Frontend
npm run build
aws s3 sync dist/ s3://iso-standards-frontend --delete --profile ben-sso
aws cloudfront create-invalidation --distribution-id E2494N0PGM4KTG --paths "/*" --profile ben-sso
```

### Check Deployment Status
```bash
# Check S3
aws s3 ls s3://iso-standards-frontend --profile ben-sso

# Check CloudFront
aws cloudfront get-distribution-status --id E2494N0PGM4KTG --profile ben-sso

# Check GitHub Actions logs
# Go to: https://github.com/[your-repo]/actions
```

### Monitor Cache
```bash
curl -I https://d1pjttps83iyey.cloudfront.net/index.html
curl -I https://d1pjttps83iyey.cloudfront.net/assets/main.js
```

## 📋 Deployment Architecture

```
┌─ Frontend Code ─┐
│   (main branch) │
└────────┬────────┘
         │ git push
         ▼
┌──────────────────────┐
│  GitHub Actions      │
│  (Build & Deploy)    │
└────────┬─────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌──────┐  ┌────────────┐
│ S3   │  │ CloudFront │
│(CDN) │◄─┤   (CDN)    │
└──────┘  └────┬───────┘
              │
              ▼
    ┌─────────────────────┐
    │ iso.benedictthekkel │
    │  .com.au (CNAME)    │
    └─────────────────────┘
```

## 🎓 Learning Resources

- [CloudFront Distribution Setup](https://docs.aws.amazon.com/cloudfront/latest/developerguide/distribution-web-creating.html)
- [S3 Website Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [React Vite Deployment](https://vitejs.dev/guide/static-deploy.html)

## ✨ Key Features

✅ **Performance**
- CloudFront CDN with edge locations worldwide
- 1-year caching for static assets
- HTML files always fresh (no-cache)

✅ **Reliability**
- S3 versioning for rollback
- CloudFront failover
- GitHub Actions logging

✅ **Security**
- HTTPS/TLS encryption
- OIDC authentication (no stored secrets)
- Least-privilege IAM roles

✅ **Automation**
- Auto-deploy on main branch push
- Cache invalidation automatic
- Build happens in <2 minutes

## 🚨 If Something Goes Wrong

**Can't access CloudFront domain?**
```bash
# Check S3 bucket policy
aws s3api get-bucket-policy --bucket iso-standards-frontend --profile ben-sso

# Check CloudFront is deployed
aws cloudfront get-distribution-status --id E2494N0PGM4KTG --profile ben-sso
```

**DNS not resolving?**
```bash
# Check DNS record
nslookup iso.benedictthekkel.com.au

# Check CNAME is pointing correctly
# Should resolve to: d1pjttps83iyey.cloudfront.net
```

**Deployment failed in GitHub?**
1. Check Actions tab on GitHub repo
2. Click failed run
3. Expand "Deploy to S3" step to see error
4. Most common: IAM permissions issue

**Files showing old content?**
```bash
# Manual invalidation
aws cloudfront create-invalidation \
  --distribution-id E2494N0PGM4KTG \
  --paths "/*" \
  --profile ben-sso
```

---

**Last Updated**: 2025-11-30
**Maintainer**: GitHub Copilot
**Status**: ✅ Ready for Production
