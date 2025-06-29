# 📤 Push to GitHub Instructions

## After creating the "Vibesite" repository on GitHub:

### 1. Copy the repository URL
After creating the repo, GitHub will show you the repository URL. It will look like:
`https://github.com/YOUR_USERNAME/Vibesite.git`

### 2. Run these commands in Terminal:

```bash
# Navigate to project directory
cd "/Volumes/T7 BACKUP/Projects_2025_nicht aktuell/CODING/VIBEGAME SITE"

# Add GitHub as remote origin (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/Vibesite.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 3. Verify Upload
Go back to your GitHub repository page and refresh - you should see all your files!

### 4. Deploy to Vercel
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import from GitHub → Select "Vibesite"
4. Click "Deploy"

### 5. Set Environment Variables in Vercel
- Go to your project settings in Vercel
- Environment Variables section
- Add: `JWT_SECRET` = `VibeCoding2025SuperSecretKey123!`

## Your live URLs will be:
- **Website**: `https://vibesite.vercel.app`
- **Admin Panel**: `https://vibesite.vercel.app/admin`

## Ready to go! 🚀