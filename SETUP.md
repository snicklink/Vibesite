# 🚀 Quick Setup Guide

## Current Status
- ✅ Website is live: `https://vibesite-wheat.vercel.app`
- ⚠️ Admin needs GitHub OAuth setup (5 minutes)

## Option 1: Test Mode (Works Immediately)
**Test the CMS interface without GitHub:**
- Visit: `https://vibesite-wheat.vercel.app/admin-test.html`
- This lets you see the CMS interface and test functionality
- Note: Changes won't save to Git (test mode only)

## Option 2: Full Setup (5 minutes)

### Step 1: Create GitHub OAuth App
1. Go to https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: `Vibegame CMS`
   - **Homepage URL**: `https://vibesite-wheat.vercel.app`
   - **Authorization callback URL**: `https://vibesite-wheat.vercel.app/admin/`
4. Click "Register application"
5. Copy the **Client ID** and **Client Secret**

### Step 2: Add to Vercel
1. Go to https://vercel.com/dashboard
2. Find your project → Settings → Environment Variables
3. Add:
   - **Name**: `GITHUB_CLIENT_ID` **Value**: (your client ID)
   - **Name**: `GITHUB_CLIENT_SECRET` **Value**: (your client secret)
4. Click "Save"

### Step 3: Access Admin
- Visit: `https://vibesite-wheat.vercel.app/admin/`
- Login with your GitHub account
- Start managing content!

## Authentication Error Fix
If you see "Authentication aborted undefined":
1. Check that environment variables are set in Vercel
2. Make sure OAuth callback URL matches exactly: `https://vibesite-wheat.vercel.app/admin/`
3. Redeploy the site after adding environment variables

## Contact
If you need help with setup, the issue is likely:
- Missing environment variables in Vercel
- Incorrect OAuth callback URL
- Need to redeploy after adding environment variables