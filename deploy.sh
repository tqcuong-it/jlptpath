#!/bin/bash
set -e

# Load env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

MSG="${1:-update}"
HUGO="/home/node/.openclaw/workspace/.tools/bin/hugo"

echo "🏗️ Building..."
$HUGO --buildFuture --quiet --minify

echo "🚀 Deploying to Cloudflare Pages..."
npx wrangler pages deploy public --project-name=jlptpath --commit-dirty=true

echo "📦 Pushing to GitHub..."
git add -A
git commit -m "$MSG" 2>/dev/null || true
git push origin master 2>/dev/null || true

echo "✅ Done! https://jlptpath.com"
