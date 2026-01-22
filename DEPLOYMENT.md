# Deployment Guide

This guide covers deploying both backend and frontend to production.

## Backend Deployment

### Option 1: Render.com (Recommended)

1. **Create Account**: Sign up at [render.com](https://render.com)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the backend folder

3. **Configure Service**:
   ```
   Name: blogger-backend
   Region: Choose closest to your users
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt && python -m spacy download en_core_web_sm
   Start Command: python app.py
   ```

4. **Add Environment Variables**:
   ```
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/blogger
   JWT_SECRET_KEY=your-production-secret-key-make-it-long-and-random
   GEMINI_API_KEY=your-gemini-api-key
   FLASK_ENV=production
   FLASK_DEBUG=False
   PORT=5000
   HOST=0.0.0.0
   ```

5. **Deploy**: Click "Create Web Service"

6. **Note Your URL**: e.g., `https://blogger-backend.onrender.com`

### Option 2: Railway.app

1. **Create Account**: Sign up at [railway.app](https://railway.app)

2. **New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**:
   - Railway auto-detects Python
   - Add environment variables in Settings
   - Set root directory to `backend`

4. **Deploy**: Automatic on push

### Option 3: Heroku

1. **Install Heroku CLI**:
   ```bash
   # Download from heroku.com/cli
   ```

2. **Create Procfile** in backend folder:
   ```
   web: python app.py
   ```

3. **Deploy**:
   ```bash
   cd backend
   heroku login
   heroku create blogger-backend
   heroku config:set MONGODB_URI=your-mongodb-uri
   heroku config:set JWT_SECRET_KEY=your-secret
   heroku config:set GEMINI_API_KEY=your-gemini-key
   git push heroku main
   ```

---

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Update API URL** in `frontend/src/services/api.js`:
   ```javascript
   const API_URL = 'https://your-backend-url.onrender.com/api';
   ```

2. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

3. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

4. **Configure**:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

5. **Production Deploy**:
   ```bash
   vercel --prod
   ```

### Option 2: Netlify

1. **Update API URL** (same as above)

2. **Create `netlify.toml`** in frontend folder:
   ```toml
   [build]
     command = "npm run build"
     publish = "dist"
   
   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

3. **Deploy**:
   - Go to [netlify.com](https://netlify.com)
   - Drag and drop `dist` folder
   - Or connect GitHub repository

### Option 3: GitHub Pages

1. **Update vite.config.js**:
   ```javascript
   export default defineConfig({
     base: '/blogger/',
     // ... rest of config
   })
   ```

2. **Build**:
   ```bash
   npm run build
   ```

3. **Deploy**:
   ```bash
   # Install gh-pages
   npm install -D gh-pages
   
   # Add to package.json scripts:
   "deploy": "gh-pages -d dist"
   
   # Deploy
   npm run deploy
   ```

---

## MongoDB Atlas Setup

1. **Create Cluster**:
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Create free cluster
   - Choose region closest to your backend

2. **Create Database User**:
   - Database Access → Add New User
   - Username: `blogger_user`
   - Password: Generate secure password
   - User Privileges: Read and write to any database

3. **Whitelist IPs**:
   - Network Access → Add IP Address
   - For production: Add your backend server IP
   - For development: Add `0.0.0.0/0` (allow all)

4. **Get Connection String**:
   - Clusters → Connect → Connect your application
   - Copy connection string
   - Replace `<password>` with your password
   - Format: `mongodb+srv://user:pass@cluster.mongodb.net/blogger`

---

## Google Gemini API Setup

1. **Create Account**: [ai.google.dev](https://ai.google.dev)

2. **Generate API Key**:
   - Go to Google AI Studio
   - Create API key
   - Copy and save securely

3. **Set Billing** (if needed):
   - Check quota limits
   - Monitor usage

4. **Monitor Usage**:
   - Check usage in Google AI Studio dashboard

---

## Post-Deployment Checklist

### Backend
- [ ] Environment variables set correctly
- [ ] MongoDB connection working
- [ ] Gemini API key valid
- [ ] Health endpoint responding: `/api/health`
- [ ] CORS configured for frontend domain
- [ ] Logs monitoring set up

### Frontend
- [ ] API URL updated to production backend
- [ ] Build successful without errors
- [ ] All routes working
- [ ] Authentication flow working
- [ ] Blog generation working end-to-end

### Security
- [ ] JWT secret is strong and unique
- [ ] MongoDB uses strong password
- [ ] Gemini API key secured
- [ ] HTTPS enabled
- [ ] Rate limiting considered (optional)

### Monitoring
- [ ] Backend uptime monitoring
- [ ] Error logging configured
- [ ] Cost monitoring (Gemini usage)
- [ ] Database backup strategy

---

## Environment Variables Reference

### Backend (.env)
```env
# Required
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/blogger
JWT_SECRET_KEY=long-random-secret-key-min-32-chars
GEMINI_API_KEY=your-api-key

# Optional
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
HOST=0.0.0.0
```

### Frontend
Update `src/services/api.js`:
```javascript
const API_URL = 'https://your-backend.onrender.com/api';
```

---

## Troubleshooting

### Backend Issues

**502 Bad Gateway**:
- Check if backend service is running
- Verify PORT environment variable
- Check logs for startup errors

**MongoDB Connection Failed**:
- Verify connection string format
- Check IP whitelist in MongoDB Atlas
- Ensure database user has correct permissions

**Gemini Rate Limit**:
- Check API usage and billing
- Implement request queuing
- Consider caching frequently requested content

### Frontend Issues

**API Calls Failing**:
- Verify API_URL is correct
- Check CORS settings in backend
- Ensure backend is deployed and running

**Build Errors**:
- Clear node_modules: `rm -rf node_modules package-lock.json`
- Reinstall: `npm install`
- Check Node version: 18+

---

## Scaling Considerations

### Cost Optimization
1. **MongoDB**: Use M0 free tier initially, upgrade as needed
2. **Gemini**: Cache common requests, use gemini-2.5-flash for cost-effectiveness
3. **Backend**: Start with free tier, upgrade based on traffic

### Performance
1. **Add caching**: Redis for frequent requests
2. **CDN**: Use for frontend static assets
3. **Database indexing**: Already configured
4. **Rate limiting**: Protect against abuse

### Monitoring
1. **Uptime**: UptimeRobot or Pingdom
2. **Errors**: Sentry or LogRocket
3. **Analytics**: Google Analytics or Plausible

---

## Quick Deploy Commands

```bash
# Backend to Render
# Just push to GitHub, Render deploys automatically

# Frontend to Vercel
cd frontend
vercel --prod

# Frontend to Netlify
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

---

**Need help?** Check the main README.md or create an issue on GitHub.
