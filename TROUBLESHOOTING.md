# Troubleshooting Guide

This guide helps you solve common issues when setting up or running the AI Blog Generator.

---

## 🔧 Installation Issues

### Python Virtual Environment Won't Create

**Error**: `Error: Command '['...\venv\Scripts\python.exe', '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1`

**Solutions**:
1. Try using a specific Python version:
   ```bash
   py -3.9 -m venv venv
   ```

2. Install virtualenv manually:
   ```bash
   pip install virtualenv
   python -m virtualenv venv
   ```

3. Check Python is properly installed:
   ```bash
   python --version
   ```

---

### Requirements Installation Fails

**Error**: `ERROR: Could not find a version that satisfies the requirement...`

**Solutions**:
1. Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```

2. Install problematic packages individually:
   ```bash
   pip install flask
   pip install pymongo
   # ... etc
   ```

3. Check Python version (needs 3.8+):
   ```bash
   python --version
   ```

---

### spaCy Model Download Fails

**Error**: `Can't find model 'en_core_web_sm'`

**Solutions**:
1. Download directly:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. Try alternative method:
   ```bash
   pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
   ```

3. If still failing, spaCy model is optional - the app will work without it

---

### npm Install Fails (Frontend)

**Error**: `npm ERR! code EACCES` or permission errors

**Solutions**:
1. Clear npm cache:
   ```bash
   npm cache clean --force
   ```

2. Delete node_modules and try again:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

3. Use --legacy-peer-deps flag:
   ```bash
   npm install --legacy-peer-deps
   ```

---

## 🗄️ Database Issues

### MongoDB Connection Failed

**Error**: `ServerSelectionTimeoutError: connection refused`

**Solutions**:
1. **Check connection string format**:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/blogger
   ```
   - Ensure no spaces
   - Replace `<password>` with actual password
   - Database name at the end

2. **Verify IP Whitelist**:
   - Go to MongoDB Atlas → Network Access
   - Add `0.0.0.0/0` for development
   - Add your server IP for production

3. **Check database user**:
   - Go to Database Access
   - Ensure user has "Read and write" privileges

4. **Test connection separately**:
   ```python
   from pymongo import MongoClient
   client = MongoClient("your_connection_string")
   print(client.server_info())
   ```

---

### Authentication Failed (MongoDB)

**Error**: `Authentication failed`

**Solutions**:
1. Password contains special characters? URL-encode them:
   - `@` → `%40`
   - `#` → `%23`
   - `$` → `%24`
   - `&` → `%26`

2. Recreate database user:
   - Delete existing user
   - Create new one with simple password
   - Update connection string

---

## 🔑 API Key Issues

### Gemini API Authentication Failed

**Error**: `API_KEY_INVALID` or authentication error

**Solutions**:
1. **Verify API key**:
   - Check it starts with `sk-`
   - No extra spaces or quotes
   - Copy-paste directly from Google AI Studio dashboard

2. **Check `.env` file**:
   ```env
   GEMINI_API_KEY=your-actual-key-here
   ```
   - No quotes around the key
   - No spaces

3. **Ensure `.env` is loaded**:
   ```python
   from dotenv import load_dotenv
   import os
   load_dotenv()
   print(os.getenv('GEMINI_API_KEY'))  # Should print your key
   ```

4. **Check API key is active**:
   - Go to ai.google.dev
   - Check API keys section
   - Verify billing is set up

---

### Gemini Rate Limit Exceeded

**Error**: `Rate limit reached`

**Solutions**:
1. Wait a few minutes and try again
2. Check your usage limits in Google AI Studio
3. Upgrade to paid tier if on free tier
4. Implement request queuing in your code

---

## 🌐 Server Issues

### Backend Won't Start

**Error**: `Address already in use`

**Solution**: Port 5000 is occupied
```bash
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Mac/Linux: Find and kill process
lsof -i :5000
kill -9 <process_id>

# Or use a different port in .env
PORT=5001
```

---

### CORS Error in Frontend

**Error**: `Access to XMLHttpRequest... has been blocked by CORS policy`

**Solutions**:
1. **Verify backend CORS config** in `app.py`:
   ```python
   CORS(app, resources={
       r"/api/*": {
           "origins": ["http://localhost:5173"],
       }
   })
   ```

2. **Check frontend API URL** in `services/api.js`:
   ```javascript
   const API_URL = 'http://localhost:5000/api';
   ```

3. **Ensure backend is running** on correct port

4. **Try starting backend with CORS disabled** (development only):
   ```python
   CORS(app, resources={r"/api/*": {"origins": "*"}})
   ```

---

### Frontend Build Fails

**Error**: Various build errors

**Solutions**:
1. Clear Vite cache:
   ```bash
   rm -rf node_modules/.vite
   npm run dev
   ```

2. Check Node version (needs 18+):
   ```bash
   node --version
   ```

3. Delete and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

---

## 🔐 Authentication Issues

### JWT Token Invalid

**Error**: `401 Unauthorized` or `Token has expired`

**Solutions**:
1. **Token expired**: Tokens last 24 hours - login again

2. **Check JWT secret**: Ensure `JWT_SECRET_KEY` in `.env` is set

3. **Clear localStorage**:
   ```javascript
   localStorage.clear();
   ```
   Then login again

4. **Verify token format** in API calls:
   ```javascript
   headers: {
     'Authorization': `Bearer ${token}`
   }
   ```

---

### Login Always Fails

**Error**: `Invalid email or password` (but credentials are correct)

**Solutions**:
1. **Check database connection**: User might not be saved

2. **Check password hashing**:
   ```python
   import bcrypt
   # Verify bcrypt is installed correctly
   ```

3. **Try creating new user**:
   - Delete existing user from database
   - Sign up again

4. **Check email format**: Must be lowercase in database

---

## 📝 Blog Generation Issues

### Content Extraction Fails

**Error**: `Content extraction failed` or `Insufficient content`

**Solutions**:
1. **Try different URL**: Some sites block scraping

2. **Check URL is reachable**:
   ```bash
   curl -I <your_url>
   ```

3. **Use articles with substantial content** (500+ words)

4. **Try well-known sites first**:
   - Wikipedia articles
   - Medium posts
   - Public blogs

5. **Check website robots.txt**: Site might block scraping

---

### Keyword Extraction Returns Empty

**Error**: No keywords extracted

**Solutions**:
1. **Content too short**: Needs at least 100 words

2. **Check KeyBERT installation**:
   ```bash
   pip install keybert sentence-transformers
   ```

3. **Download transformer models**:
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   ```

4. **Check logs** for specific error messages

---

### Blog Generation Takes Too Long

**Issue**: Generation takes more than 2 minutes

**Solutions**:
1. **Normal for first time**: Models need to load

2. **Reduce blog length**: Try 500 words instead of 3000

3. **Check Gemini API status**: Check Google Cloud status

4. **Use GPT-3.5 instead of GPT-4**:
   ```python
   GEMINI_MODEL = 'gemini-2.5-flash'
   ```

---

### Generated Blog Quality Poor

**Issue**: Blog content not meeting expectations

**Solutions**:
1. **Improve source content**: Use URLs with better content

2. **Adjust prompt** in `prompt_builder.py`

3. **Try different tones**: Professional, casual, technical, etc.

4. **Use GPT-4** instead of GPT-3.5 (costs more):
   ```python
   GEMINI_MODEL = 'gemini-pro'
   ```

5. **Increase blog length**: Longer blogs often have better quality

---

## 💾 Data Issues

### Blog History Not Showing

**Issue**: History page is empty even after generating blogs

**Solutions**:
1. **Check MongoDB connection**: Data might not be saving

2. **Verify user ID matches**:
   ```python
   # Check JWT token contains correct user ID
   ```

3. **Check database manually**:
   - Go to MongoDB Atlas
   - Browse Collections
   - Check `blog_history` collection

4. **Check browser console** for JavaScript errors

---

## 🚀 Deployment Issues

### Render Deployment Fails

**Error**: Build or deployment errors

**Solutions**:
1. **Check build command**:
   ```bash
   pip install -r requirements.txt && python -m spacy download en_core_web_sm
   ```

2. **Verify environment variables** are set in Render dashboard

3. **Check logs** in Render dashboard for specific errors

4. **Ensure requirements.txt includes all dependencies**

5. **Check Python version**: Set to 3.9 or 3.10

---

### Frontend Can't Connect to Deployed Backend

**Issue**: Frontend works locally but not in production

**Solutions**:
1. **Update API_URL** in `services/api.js`:
   ```javascript
   const API_URL = 'https://your-backend.onrender.com/api';
   ```

2. **Check CORS settings** allow your frontend domain

3. **Verify backend is running**: Visit `/api/health` endpoint

4. **Check HTTPS/HTTP**: Both must use HTTPS in production

---

## 🔍 Debugging Tips

### Enable Verbose Logging

In `config.py`:
```python
DEBUG = True
```

In components, add console.log:
```javascript
console.log('API Response:', data);
```

---

### Check Backend Logs

```bash
cd backend
python app.py
# Watch terminal for colored logs
```

---

### Check Frontend Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for errors or warnings
4. Check Network tab for failed requests

---

### Test API Directly

Use cURL or Postman:
```bash
curl http://localhost:5000/api/health
```

---

### Verify Environment Variables

```bash
# Backend
cd backend
venv\Scripts\activate
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('MONGODB_URI'))"
```

---

## 📞 Still Need Help?

1. **Check the logs** - Most errors have helpful messages
2. **Review documentation** - README.md, QUICKSTART.md
3. **Test components individually** - Isolate the problem
4. **Search error messages** - Google the exact error
5. **Check GitHub issues** - Similar problems might be solved
6. **Create a minimal reproduction** - Test with simple inputs

---

## 🆘 Emergency Reset

If everything is broken, start fresh:

```bash
# Backend
cd backend
rm -rf venv
rm .env
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your credentials

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Then start both servers
```

---

**Remember**: Most issues are configuration problems. Double-check your `.env` file and API keys!
