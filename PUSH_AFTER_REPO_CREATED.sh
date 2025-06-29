#!/bin/bash

echo "🚀 Pushing Vibesite to GitHub..."

cd "/Volumes/T7 BACKUP/Projects_2025_nicht aktuell/CODING/VIBEGAME SITE"

# Push to GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Repository: https://github.com/snicklink/Vibesite"
    echo ""
    echo "🎉 Next: Deploy to Vercel!"
    echo "1. Go to vercel.com/dashboard"
    echo "2. Click 'New Project'"
    echo "3. Import 'snicklink/Vibesite'"
    echo "4. Set JWT_SECRET environment variable"
    echo ""
    echo "🔗 Opening repository..."
    open "https://github.com/snicklink/Vibesite"
else
    echo "❌ Push failed. Make sure you created the repository first!"
fi