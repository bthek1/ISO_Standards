# Frontend Deployment Configuration

## AWS Infrastructure Setup ✅

### S3 Bucket
- **Bucket Name**: `iso-standards-frontend`
- **Region**: `ap-southeast-2` (Sydney)
- **Versioning**: Enabled
- **Website Hosting**: Enabled with SPA routing (index.html for 404s)
- **Public Access**: Enabled (via CloudFront)

### CloudFront Distribution
- **Distribution ID**: `E2494N0PGM4KTG`
- **Domain Name**: `d1pjttps83iyey.cloudfront.net`
- **HTTPS**: Enabled (redirect from HTTP)
- **Caching**:
  - Index.html: No cache (always fresh)
  - JS/CSS: 1 year cache (fingerprinted assets)
  - Other files: 1 day cache

### GitHub Actions OIDC Integration
- **Role ARN**: `arn:aws:iam::762233760445:role/github-actions-role`
- **Trust Policy**: Limited to main branch deployments
- **Permissions**: S3 sync, CloudFront invalidation

## Deployment Workflow

### Automatic Deployments
Triggered on:
- Push to `main` branch in `Frontend/` directory
- Manual workflow dispatch

### Steps
1. Build React app with Vite
2. Authenticate to AWS via OIDC (no static credentials)
3. Sync build output to S3
4. Invalidate CloudFront cache
5. Deploy completed

## DNS Configuration (Manual Step)

You need to add a CNAME record to your DNS provider:

```
Host: iso
Type: CNAME
Value: d1pjttps83iyey.cloudfront.net
```

For `iso.benedictthekkel.com.au`, add this DNS record at your domain registrar.

### Note on HTTPS/SSL
After adding the CNAME:
1. CloudFront will automatically handle SSL/TLS
2. Consider requesting AWS to create an ACM certificate for iso.benedictthekkel.com.au
3. Update CloudFront distribution to use custom domain

## Manual Deployment

For immediate deployment without waiting for GitHub:

```bash
cd Frontend
npm run build
aws s3 sync dist/ s3://iso-standards-frontend --delete --profile ben-sso
aws cloudfront create-invalidation --distribution-id E2494N0PGM4KTG --paths "/*" --profile ben-sso
```

## Testing

1. **CloudFront URL**: https://d1pjttps83iyey.cloudfront.net
2. **Custom Domain** (once DNS configured): https://iso.benedictthekkel.com.au

## Monitoring

View S3 bucket:
```bash
aws s3 ls iso-standards-frontend --profile ben-sso
aws s3 ls s3://iso-standards-frontend --recursive --profile ben-sso
```

View CloudFront distribution:
```bash
aws cloudfront get-distribution --id E2494N0PGM4KTG --profile ben-sso
```

View invalidations:
```bash
aws cloudfront list-invalidations --distribution-id E2494N0PGM4KTG --profile ben-sso
```

## Cost Estimate

- **S3 Storage**: ~$1-5/month (minimal for static files)
- **CloudFront Data Transfer**: ~$5-50/month (depending on traffic)
- **IAM**: Free
- **Total**: Approximately $10-60/month for typical usage

## Next Steps

1. ✅ S3 bucket created
2. ✅ CloudFront distribution created
3. ✅ GitHub Actions workflow created
4. ✅ IAM role and policies created
5. ⏳ **TODO**: Add DNS CNAME record to domain registrar
6. ⏳ **TODO**: Request SSL certificate (optional, but recommended)
7. ⏳ **TODO**: Push to main branch to trigger first deployment

## Rollback

To rollback to a previous version:

```bash
# List available versions
aws s3api list-object-versions --bucket iso-standards-frontend --profile ben-sso

# Restore specific version
aws s3api get-object --bucket iso-standards-frontend --key index.html --version-id <VERSION_ID> index.html --profile ben-sso
aws s3 cp index.html s3://iso-standards-frontend/ --profile ben-sso

# Invalidate CloudFront
aws cloudfront create-invalidation --distribution-id E2494N0PGM4KTG --paths "/*" --profile ben-sso
```

---

**Deployment ID**: E2494N0PGM4KTG
**Setup Date**: 2025-11-30
**Status**: ✅ Ready for deployment
