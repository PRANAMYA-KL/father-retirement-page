# Deployment Guide

## How to Deploy Your Father's Retirement Website

### Prerequisites
- GitHub account
- Code pushed to GitHub repository
- Deployment platform account (Render/Railway/Heroku)

## Option 1: Render (Recommended)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"

### Step 2: Connect Repository
1. Connect your GitHub account
2. Select `father-retirement-page` repository
3. Click "Connect"

### Step 3: Configure Deployment
- **Name**: `father-retirement-page`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Free

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for deployment (2-5 minutes)
3. Get your live URL (e.g., `https://father-retirement-page.onrender.com`)

## Option 2: Railway

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"

### Step 2: Deploy
1. Select your repository
2. Railway auto-detects Python app
3. Deploys automatically
4. Get your live URL

## Option 3: Heroku

### Step 1: Install Heroku CLI
```bash
# Download from heroku.com
```

### Step 2: Login and Deploy
```bash
heroku login
heroku create father-retirement-page
git push heroku main
```

## Making Updates

### After Making Changes:
1. Edit files locally
2. Test: `python app.py`
3. Commit: `git add . && git commit -m "Update message"`
4. Push: `git push origin main`
5. Platform auto-redeploys

### Example Update Process:
```bash
# Edit files
# Test locally
python app.py

# Commit and push
git add .
git commit -m "Updated website design"
git push origin main

# Wait 1-3 minutes for auto-redeployment
```

## Troubleshooting

### Common Issues:
1. **Build fails**: Check `requirements.txt` has all dependencies
2. **App crashes**: Check `Procfile` has correct start command
3. **Static files not loading**: Ensure file paths are correct

### Useful Commands:
```bash
# Check deployment status
git status
git log --oneline

# Force push if needed
git push -f origin main

# Check remote
git remote -v
```

## Important Files

- `app.py`: Main Flask application
- `requirements.txt`: Python dependencies
- `Procfile`: Start command for deployment
- `runtime.txt`: Python version
- `static/style.css`: Styling
- `templates/index.html`: Main webpage

## Support

If deployment fails:
1. Check platform logs
2. Verify all files are committed
3. Ensure dependencies are correct
4. Contact platform support

---

**Your website will be live and accessible to everyone worldwide!** 🌐 