# 🚀 Vercel Deployment Guide

## Prerequisites

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Sign up for Vercel** at [vercel.com](https://vercel.com) using GitHub

3. **Push to GitHub** (we'll do this together)

## Deployment Steps

### Step 1: Commit and Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Vibegame website with backend"

# Add your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/vibegame-website.git

# Push to GitHub
git push -u origin master
```

### Step 2: Deploy to Vercel

You have two options:

#### Option A: Auto-deploy via GitHub (Recommended)
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect the configuration
5. Click "Deploy"

#### Option B: Deploy via CLI
```bash
vercel --prod
```

### Step 3: Set Environment Variables

In your Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add these variables:
   - `JWT_SECRET`: A strong secret key for authentication
   
Example:
```
JWT_SECRET=VibeCoding2025SuperSecretKey123!@#
```

### Step 4: Access Your Site

- **Main Website**: `https://your-project.vercel.app`
- **Admin Panel**: `https://your-project.vercel.app/admin`

## Important Notes

⚠️ **Database Limitation**: Vercel uses ephemeral storage, so the SQLite database resets on each deployment. For production, consider:
- Vercel Postgres
- PlanetScale
- Supabase
- MongoDB Atlas

## Project Structure

```
/
├── api/                    # Backend API (serverless functions)
│   ├── server.js          # Main API server
│   ├── admin.html         # Admin interface
│   ├── themes.json        # Theme configuration
│   └── package.json       # API dependencies
├── public/                # Frontend static files
│   ├── index.html         # Main website
│   ├── vibecoding.html    # About page
│   ├── styles.css         # Styles
│   └── images/            # Static images
├── vercel.json            # Vercel configuration
├── package.json           # Root dependencies
└── .env.example           # Environment variables template
```

## API Endpoints

- `GET /` - Main website
- `GET /admin` - Admin panel
- `GET /api/projects` - Get all projects
- `GET /api/themes` - Get available themes
- `POST /api/auth/login` - Admin login
- `POST /api/admin/projects` - Create project (authenticated)

## Default Admin Login

- **Username**: `admin`
- **Password**: `admin123`

🔒 **IMPORTANT**: Change the default password after first deployment!

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check that all dependencies are in `package.json`
2. **API Not Working**: Verify `vercel.json` routes configuration
3. **Database Issues**: Remember that SQLite resets on each deployment
4. **Admin Panel 404**: Ensure `admin.html` is in the `api/` directory

### Logs:
```bash
vercel logs
```

## Next Steps

1. Set up a persistent database (recommended: Vercel Postgres)
2. Configure custom domain
3. Set up monitoring and analytics
4. Add SSL certificates (automatic with Vercel)