#!/bin/bash
set -e

echo "========================================="
echo "Testing Development Settings"
echo "========================================="
export DJANGO_ENV=development
export SECRET_KEY=test-dev-key
cd /home/bthek1/ISO_Standards/Backend
uv run python manage.py check
echo "✅ Development settings check passed!"

echo ""
echo "========================================="
echo "Testing Test Settings"
echo "========================================="
export DJANGO_ENV=test
export SECRET_KEY=test-test-key
uv run python manage.py check
echo "✅ Test settings check passed!"

echo ""
echo "========================================="
echo "Testing Production Settings (Dry Run)"
echo "========================================="
export DJANGO_ENV=production
export SECRET_KEY=test-prod-key-minimum-50-characters-long-for-security
export ALLOWED_HOSTS=example.com,www.example.com
export DB_PASSWORD=test-password
uv run python manage.py check --deploy
echo "✅ Production settings check passed!"

echo ""
echo "========================================="
echo "All environment tests passed!"
echo "========================================="
