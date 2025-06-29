# 🎮 Vibegame Website - Professional CMS Solution

**A proper, industry-standard content management solution using Sveltia CMS.**

## ✨ What This Is

A professional static website with **Sveltia CMS** - the modern, lightweight successor to Netlify CMS. This follows 2024 best practices for static site content management.

## 🚀 How It Works

1. **Content stored in Git** - Your projects are markdown files in `_projects/` folder
2. **Professional Admin Panel** - Modern, fast, Git-based CMS interface
3. **Automatic Deployment** - Changes trigger automatic rebuilds on Vercel
4. **Zero Maintenance** - No databases, no servers, just works

## 📋 Setup Instructions

### 1. Enable GitHub OAuth (One-time setup)

1. Go to [GitHub Settings > Developer settings > OAuth Apps](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: `Vibegame CMS`
   - **Homepage URL**: `https://vibesite-wheat.vercel.app`
   - **Authorization callback URL**: `https://vibesite-wheat.vercel.app/admin/`
4. Click "Register application"
5. Copy the **Client ID** and **Client Secret**

### 2. Add Environment Variables in Vercel

1. Go to [Vercel Dashboard > vibesite-wheat > Settings > Environment Variables](https://vercel.com/dashboard)
2. Add these variables:
   - `GITHUB_CLIENT_ID`: Your GitHub OAuth Client ID
   - `GITHUB_CLIENT_SECRET`: Your GitHub OAuth Client Secret

### 3. Access Your Admin Panel

- **Admin URL**: `https://vibesite-wheat.vercel.app/admin/`
- **Login**: Use your GitHub account
- **Permissions**: You need write access to the repository

## 🎯 Managing Content

### Adding New Projects
1. Go to admin panel
2. Click "Projects" → "New Project"  
3. Fill in details:
   - **Title**: Project name
   - **Description**: Short description
   - **Image**: Upload or select image
   - **Project URL**: Link to your game
   - **Category**: Spiele, Apps, Experimentell, Systeme
   - **Color**: Hex color for styling
   - **Featured**: Show in hero section
   - **New**: Show "Neu" badge
   - **Order**: Sort order (lower = first)

### Editing Projects
1. Go to admin panel
2. Click on any project to edit
3. Make changes and save
4. Changes deploy automatically

### Managing Images
- Upload images through the CMS
- Images are stored in `/images/` folder
- Automatic optimization and CDN delivery

## 🔧 Technical Details

### File Structure
```
/
├── _projects/              # Content (markdown files)
│   ├── bratwurst-bomber.md
│   └── ...
├── admin/                  # CMS admin panel
│   ├── index.html
│   └── config.yml
├── images/                 # Static images
├── index.html              # Main website
├── styles.css              # Styling
└── vibecoding.html         # About page
```

### How Content Updates Work
1. Edit content in admin panel
2. CMS creates pull request or commits directly
3. Vercel detects changes and rebuilds site
4. New content appears automatically

### Benefits
- ✅ **Professional**: Industry-standard Git-based CMS
- ✅ **Fast**: 500KB CMS vs 1.5MB+ alternatives
- ✅ **Reliable**: No databases to break
- ✅ **Scalable**: CDN-delivered, globally fast
- ✅ **Secure**: OAuth authentication, Git permissions
- ✅ **Modern**: 2024 best practices

## 🎯 Perfect Balance

This solution hits the sweet spot between:
- ❌ Too Simple: Hardcoded content
- ✅ **Just Right**: Professional CMS that works
- ❌ Too Complex: Custom backends that break

**This is how professionals do it in 2024.** 🎖️