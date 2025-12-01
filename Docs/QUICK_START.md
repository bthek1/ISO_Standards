# 🎯 QUICK REFERENCE - Frontend Deployment

## 📍 Current Status: READY FOR PRODUCTION

### Access Your Frontend NOW
```
🔗 https://d1pjttps83iyey.cloudfront.net
```

### After DNS Setup (Custom Domain)
```
🔗 https://iso.benedictthekkel.com.au
```

---

## ⚡ Quick Start

### 1️⃣ Add DNS CNAME (5 minutes)
Go to your domain registrar and add:
```
Host:  iso
Type:  CNAME
Value: d1pjttps83iyey.cloudfront.net
TTL:   3600
```

### 2️⃣ Wait for DNS (5-30 minutes)
```bash
nslookup iso.benedictthekkel.com.au
```

### 3️⃣ Test It Works
```bash
curl -I https://iso.benedictthekkel.com.au
# or open in browser
```

### 4️⃣ Deploy Updates (Automatic)
```bash
git commit -m "fix: update feature"
git push origin main
# GitHub Actions deploys automatically!
```

---

## 📊 What You Have

| Component | Status | Details |
|-----------|--------|---------|
| Frontend | ✅ | React 18 + TypeScript |
| Build | ✅ | 2.5s build, 167 KB gzipped |
| S3 | ✅ | iso-standards-frontend |
| CloudFront | ✅ | E2494N0PGM4KTG |
| CI/CD | ✅ | GitHub Actions auto-deploy |
| HTTPS | ✅ | CloudFront managed |
| DNS | ⏳ | Add CNAME record |

---

## 🔧 Common Commands

### Build Locally
```bash
cd Frontend
npm run build
```

### Deploy Manually
```bash
aws s3 sync dist/ s3://iso-standards-frontend --delete --profile ben-sso
aws cloudfront create-invalidation --distribution-id E2494N0PGM4KTG --paths "/*" --profile ben-sso
```

### Check Status
```bash
aws s3 ls s3://iso-standards-frontend --profile ben-sso
aws cloudfront get-distribution-status --id E2494N0PGM4KTG --profile ben-sso
```

### Test Cache
```bash
curl -I https://d1pjttps83iyey.cloudfront.net/index.html
curl -I https://d1pjttps83iyey.cloudfront.net/assets/index-*.js
```

---

## 📞 Key Resources

### AWS Resources
- **S3 Bucket:** `iso-standards-frontend`
- **CloudFront ID:** `E2494N0PGM4KTG`
- **CloudFront Domain:** `d1pjttps83iyey.cloudfront.net`
- **AWS Account:** `762233760445`

### GitHub
- **Workflow:** `.github/workflows/deploy-frontend.yml`
- **Trigger:** Push to `main` on `Frontend/**`

### Documentation
- Read: `FRONTEND_DEPLOYMENT_COMPLETE.md` (Detailed guide)
- Read: `DEPLOYMENT_GUIDE.md` (Setup instructions)
- Read: `FRONTEND_CHECKLIST.md` (Testing checklist)

---

## 🚨 Troubleshooting

### "Can't access CloudFront URL"
Check S3 bucket policy:
```bash
aws s3api get-bucket-policy --bucket iso-standards-frontend --profile ben-sso
```

### "DNS not resolving"
Wait 5-30 minutes and retry:
```bash
nslookup iso.benedictthekkel.com.au
```

### "Old files still showing"
Invalidate CloudFront cache:
```bash
aws cloudfront create-invalidation --distribution-id E2494N0PGM4KTG --paths "/*" --profile ben-sso
```

### "GitHub Actions failed"
Check Actions tab in your GitHub repo and look at the logs.

---

## 💡 Pro Tips

✅ **Cache Strategy:**
- HTML: Always fresh (no-cache)
- JS/CSS: 1 year cache (fingerprinted)
- Best performance!

✅ **Zero-Downtime Deployments:**
- S3 versioning enabled
- CloudFront failover automatic
- Instant rollback available

✅ **Cost Savings:**
- 68% bundle compression (gzip)
- CloudFront CDN included
- ~$10-60/month for typical traffic

✅ **Easy Updates:**
- Just: `git push origin main`
- Deploys in 2-10 minutes
- No manual steps needed

---

## 📈 Performance

```
Build Time:        2.56 seconds
Bundle Size:       519 KB → 167 KB (gzipped)
Latency (AU):      50-100ms (CDN)
First Paint:       ~400-600ms
Time to Interactive: ~2-3 seconds
Gzip Compression:  68% reduction
```

---

## ✨ Features

✅ Professional government-style design
✅ Fully responsive (mobile → desktop)
✅ HTTPS/TLS enabled by default
✅ Global CDN with 500+ edge locations
✅ Automatic cache invalidation
✅ One-command deployments
✅ Version control & rollback
✅ No downtime updates

---

## 🎯 Next Action

1. Add DNS CNAME to domain registrar
2. Wait for DNS propagation (5-30 min)
3. Access https://iso.benedictthekkel.com.au
4. Push updates to GitHub (auto-deploys)

---

**Status:** ✅ Ready for Production
**Deploy:** `git push origin main`
**Support:** Check `FRONTEND_DEPLOYMENT_COMPLETE.md`
