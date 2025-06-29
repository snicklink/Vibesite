#!/bin/bash

# Vibegame Repository Creation and Deployment Script
echo "🚀 Creating Vibesite repository and deploying..."

# Navigate to project directory
cd "/Volumes/T7 BACKUP/Projects_2025_nicht aktuell/CODING/VIBEGAME SITE"

# Authenticate GitHub CLI (if not already done)
echo "📝 Checking GitHub authentication..."
if ! gh auth status &>/dev/null; then
    echo "🔑 Please authenticate with GitHub CLI:"
    echo "Run: gh auth login"
    echo "Then run this script again."
    exit 1
fi

# Create GitHub repository
echo "📂 Creating GitHub repository 'Vibesite'..."
gh repo create Vibesite --public --description "Vibecoding website with full-stack backend and admin panel" --source=. --remote=origin --push

# Check if successful
if [ $? -eq 0 ]; then
    echo "✅ Repository created successfully!"
    echo "🌐 Repository URL: $(gh repo view --web --json url -q .url)"
    
    # Optional: Open repository in browser
    echo "🔗 Opening repository in browser..."
    gh repo view --web
    
    echo ""
    echo "🎉 Next steps:"
    echo "1. Go to vercel.com/dashboard"
    echo "2. Click 'New Project'"
    echo "3. Import your 'Vibesite' repository"
    echo "4. Deploy!"
    echo ""
    echo "🔑 Don't forget to set JWT_SECRET in Vercel environment variables!"
else
    echo "❌ Failed to create repository. Please check your authentication and try again."
fi