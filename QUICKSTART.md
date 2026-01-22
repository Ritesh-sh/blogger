# Quick Start Guide

Get your AI Blog Generator up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8 or higher
- [ ] Node.js 18 or higher
- [ ] MongoDB Atlas account (free tier)
- [ ] Google Gemini API key

## Step-by-Step Setup

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_sm

# Create environment file
copy .env.example .env
```

**Edit `.env` file** with your credentials:
```env
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET_KEY=any_random_string_min_32_characters
GEMINI_API_KEY=your_gemini_api_key
```

**Start backend**:
```bash
python app.py
```

✅ Backend should be running on http://localhost:5000

### 2. Frontend Setup (2 minutes)

Open a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend should be running on http://localhost:5173

### 3. Test the Application

1. Open http://localhost:5173 in your browser
2. Click "Sign Up" and create an account
3. Go to "Generate" page
4. Enter a website URL (e.g., https://en.wikipedia.org/wiki/Artificial_intelligence)
5. Click "Preview" to see extracted content
6. Click "Generate Blog" and wait 30-60 seconds
7. View your generated blog!

## Getting Your API Keys

### MongoDB Atlas (Free)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a free cluster (M0)
4. Create database user
5. Add IP whitelist: `0.0.0.0/0` (for development)
6. Get connection string from "Connect" button
7. Replace `<password>` with your database user password

### Google Gemini API Key

1. Go to https://ai.google.dev
2. Sign in with your Google account
3. Go to "Get API Key" section
4. Create new API key
5. Copy the key

**Cost estimate**: ~$0.01-0.02 per blog post with GPT-3.5-turbo

## Common Issues & Solutions

### Issue: "Module not found" error in backend
**Solution**: Make sure virtual environment is activated and requirements are installed
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Cannot connect to MongoDB"
**Solution**: 
- Check your MONGODB_URI format
- Ensure IP whitelist includes `0.0.0.0/0`
- Verify database user credentials

### Issue: "Gemini API error"
**Solution**:
- Verify API key is correct in `.env`
- Check you have credits/billing set up
- Try using `gpt-3.5-turbo` instead of `gpt-4`

### Issue: Frontend can't connect to backend
**Solution**:
- Verify backend is running on port 5000
- Check `API_URL` in `frontend/src/services/api.js`
- Ensure CORS is enabled in backend

### Issue: KeyBERT model download fails
**Solution**:
```bash
pip install --upgrade sentence-transformers
pip install --upgrade keybert
```

## Next Steps

1. **Customize**: Edit prompts in `backend/services/prompt_builder.py`
2. **Deploy**: Follow instructions in `DEPLOYMENT.md`
3. **Extend**: Add more features like:
   - Custom prompt templates
   - Multiple LLM providers
   - Blog scheduling
   - Export to WordPress

## Need Help?

- Check `README.md` for detailed documentation
- Review `API_DOCUMENTATION.md` for API details
- See `DEPLOYMENT.md` for production deployment

## Example URLs to Test

Try these URLs for blog generation:
- https://en.wikipedia.org/wiki/Machine_learning
- https://en.wikipedia.org/wiki/Web_development
- https://www.python.org/about/
- https://reactjs.org/docs/getting-started.html

---

**Happy blogging! 🎉**
