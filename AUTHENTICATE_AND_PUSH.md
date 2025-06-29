# 🔑 Authentication & Push Instructions

## The token you used doesn't have push permissions. Here's how to fix it:

### Step 1: Re-authenticate with GitHub CLI
```bash
cd "/Volumes/T7 BACKUP/Projects_2025_nicht aktuell/CODING/VIBEGAME SITE"
gh auth login
```

**When prompted:**
1. Choose "GitHub.com"
2. Choose "HTTPS" 
3. Choose "Login with a web browser"
4. Copy the one-time code
5. Press Enter to open browser
6. Paste code and authorize
7. **IMPORTANT**: Make sure to grant full repository access

### Step 2: Push to GitHub
```bash
git remote set-url origin https://github.com/snicklink/Vibesite.git
git push -u origin main
```

### Step 3: Verify Upload
Go to https://github.com/snicklink/Vibesite and refresh - you should see all your files!

### Step 4: Deploy to Vercel
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import "snicklink/Vibesite"
4. Click "Deploy"
5. Set environment variable: `JWT_SECRET` = `VibeCoding2025SuperSecretKey123!`

## Alternative: Manual Upload
If authentication continues to fail:
1. Download your project as ZIP
2. Go to https://github.com/snicklink/Vibesite
3. Click "uploading an existing file" link
4. Drag all files from your project
5. Commit directly to main branch

## Your live URLs will be:
- **Website**: https://vibesite.vercel.app
- **Admin**: https://vibesite.vercel.app/admin

🚀 Almost there!