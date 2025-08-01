# Deployment Troubleshooting Guide

## Common Issues and Solutions

### 1. Application Not Loading
If your application shows "Application Error" or doesn't load:

**Check these things:**
- Ensure all files are committed to your Git repository
- Verify the Procfile is correct: `web: gunicorn app:app`
- Check that requirements.txt contains all dependencies
- Make sure runtime.txt specifies a supported Python version

### 2. Render Sleep Behavior (Free Tier)
**"Incoming HTTP request service waking up application compute resource"**

This is **NORMAL** for Render's free tier. Your app sleeps after 15 minutes of inactivity and takes 10-30 seconds to wake up.

**Solutions:**

1. **Wait for wake-up**: Simply wait 10-30 seconds for the app to start
2. **Use keep-alive script**: Run locally to prevent sleep:
   ```bash
   python keep_alive.py https://your-app.onrender.com
   ```
3. **Upgrade to paid plan**: Eliminates sleep behavior
4. **Bookmark the ping URL**: Visit `https://your-app.onrender.com/ping` to wake it up quickly

**Keep-Alive Usage:**
```bash
# Install requests if not already installed
pip install requests

# Run keep-alive (makes requests every 5 minutes)
python keep_alive.py https://your-app.onrender.com

# Or with custom interval (every 10 minutes)
python keep_alive.py https://your-app.onrender.com 600
```

### 3. Testing Your Deployment

**Health Check:**
Visit your deployed URL + `/health` to verify the app is running:
```
https://your-app-name.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Flask app is running successfully",
  "wishes_count": 0,
  "timestamp": 1234567890.123
}
```

**Quick Wake-Up:**
Visit your deployed URL + `/ping` for faster response:
```
https://your-app-name.onrender.com/ping
```

### 4. Common Fixes

**If the app still doesn't work:**

1. **Check Render Logs:**
   - Go to your Render dashboard
   - Click on your service
   - Go to "Logs" tab
   - Look for error messages

2. **Common Error Messages:**
   - `ModuleNotFoundError`: Missing dependency in requirements.txt
   - `Port already in use`: Check if PORT environment variable is set
   - `File not found`: Ensure all files are in the repository

3. **Force Redeploy:**
   - In Render dashboard, go to "Manual Deploy"
   - Click "Deploy latest commit"

### 5. File Structure Requirements

Your repository must contain:
```
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── keep_alive.py (optional)
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── uploads/
└── wishes.json (will be created automatically)
```

### 6. Environment Variables

Render automatically sets:
- `PORT`: The port your app should listen on
- `FLASK_ENV`: Set to "production" in production

### 7. Testing Locally

Before deploying, test locally:
```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` to verify it works.

### 8. Debugging Steps

1. **Check if the app starts:**
   - Visit `/health` endpoint
   - Should return JSON response

2. **Check static files:**
   - CSS should load properly
   - No 404 errors for static files

3. **Check form submission:**
   - Try submitting a wish
   - Check if wishes.json is created/updated

### 9. Render-Specific Notes

- Render uses `gunicorn` as the WSGI server
- Static files are served automatically by Flask
- File uploads work but files may be temporary (consider using cloud storage for production)
- The app runs on the port specified by the `PORT` environment variable
- **Free tier apps sleep after 15 minutes of inactivity**
- **Wake-up time is 10-30 seconds** - this is normal!

### 10. If Still Having Issues

1. Check the Render logs for specific error messages
2. Verify all dependencies are in requirements.txt
3. Ensure the app.py file has the correct configuration
4. Try redeploying from the Render dashboard
5. Contact Render support if the issue persists

## Quick Test Commands

After deployment, test these URLs:
- `https://your-app.onrender.com/` - Main page
- `https://your-app.onrender.com/health` - Health check
- `https://your-app.onrender.com/ping` - Quick wake-up
- `https://your-app.onrender.com/static/style.css` - CSS file

## Sleep Behavior Solutions

| Solution | Pros | Cons |
|----------|------|------|
| Wait 10-30 seconds | Free, simple | Users must wait |
| Keep-alive script | Prevents sleep | Requires running locally |
| Paid plan | No sleep | Costs money |
| Bookmark ping URL | Quick wake-up | Manual action needed | 