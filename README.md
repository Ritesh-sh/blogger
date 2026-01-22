# AI Blog Generator

A production-ready, lightweight AI system that generates SEO-optimized blog posts from website URLs using NLP and LLM technology.

## 🚀 Features

- **Smart Content Extraction**: Extracts meaningful content from any website URL
- **NLP Keyword Extraction**: Uses KeyBERT for local keyword extraction (no LLM cost)
- **AI Blog Generation**: Creates high-quality, original blog posts using Google Gemini API
- **SEO Optimization**: Automatic meta descriptions, headings, and keyword optimization
- **User Authentication**: JWT-based secure authentication
- **History Management**: Stores and retrieves all generated blogs
- **Clean UI**: Modern React frontend with intuitive design

## 📁 Project Structure

```
blogger/
├── backend/                  # Python Flask Backend
│   ├── app.py               # Main application entry
│   ├── config.py            # Configuration management
│   ├── requirements.txt     # Python dependencies
│   ├── routes/
│   │   ├── auth.py         # Authentication endpoints
│   │   └── blog.py         # Blog generation endpoints
│   ├── services/
│   │   ├── url_validator.py        # URL validation
│   │   ├── content_extractor.py    # Web content extraction
│   │   ├── text_cleaner.py         # Text cleaning
│   │   ├── keyword_extractor.py    # NLP keyword extraction
│   │   ├── topic_analyzer.py       # Topic & intent analysis
│   │   ├── prompt_builder.py       # LLM prompt construction
│   │   ├── blog_generator.py       # LLM API integration
│   │   └── seo_postprocessor.py    # SEO enhancements
│   ├── models/
│   │   ├── user.py          # User model
│   │   └── blog_history.py  # Blog history model
│   └── utils/
│       ├── logger.py        # Logging utility
│       └── db.py           # Database connection
│
└── frontend/                # React + Vite Frontend
    ├── src/
    │   ├── components/      # Reusable components
    │   ├── pages/          # Page components
    │   ├── services/       # API integration
    │   └── styles/         # CSS styles
    ├── package.json
    └── vite.config.js
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MongoDB Atlas
- **Authentication**: JWT + bcrypt
- **NLP**: KeyBERT, Sentence Transformers
- **Web Scraping**: Trafilatura, BeautifulSoup
- **LLM**: Google Gemini API (gemini-2.5-flash)

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: Plain CSS

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- MongoDB Atlas account
- Google Gemini API key

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
cd blogger
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (required for NLP)
python -m spacy download en_core_web_sm

# Create .env file
copy .env.example .env
# Edit .env with your credentials
```

### 3. Configure Environment Variables

Edit `backend/.env`:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/blogger
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
GEMINI_API_KEY=your-gemini-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
HOST=0.0.0.0
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
venv\Scripts\activate  # Windows
python app.py
```
Backend runs on: http://localhost:5000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

## 📖 API Documentation

### Authentication Endpoints

#### POST /api/auth/signup
Create a new user account.
```json
Request:
{
  "email": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "message": "User created successfully",
  "user": { "id": "...", "email": "..." },
  "access_token": "jwt-token"
}
```

#### POST /api/auth/login
Login to existing account.
```json
Request:
{
  "email": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "message": "Login successful",
  "user": { "id": "...", "email": "..." },
  "access_token": "jwt-token"
}
```

#### GET /api/auth/me
Get current user (requires authentication).
```
Headers: Authorization: Bearer <token>
Response:
{
  "user": { "id": "...", "email": "...", "created_at": "..." }
}
```

### Blog Endpoints

#### POST /api/blog/generate
Generate a blog post from URL (requires authentication).
```json
Request:
{
  "url": "https://example.com/article",
  "length": 1000,
  "tone": "professional",
  "include_cta": true
}

Response:
{
  "message": "Blog generated successfully",
  "blog": {
    "id": "...",
    "content": "...",
    "title": "...",
    "meta_description": "...",
    "keywords": [...],
    "word_count": 1000,
    "reading_time": 5
  }
}
```

#### GET /api/blog/history
Get blog generation history.
```
Query Parameters:
- limit (default: 10)
- skip (default: 0)

Response:
{
  "history": [...],
  "total": 25,
  "limit": 10,
  "skip": 0
}
```

#### GET /api/blog/history/:id
Get specific blog by ID.

#### POST /api/blog/preview
Preview content without generating blog.
```json
Request:
{
  "url": "https://example.com/article"
}

Response:
{
  "preview": {
    "title": "...",
    "keywords": [...],
    "summary": "...",
    "word_count": 500
  }
}
```

## 🏗️ Deployment

### Backend Deployment (Render/Railway)

1. **Prepare for deployment**:
   - Ensure all dependencies are in requirements.txt
   - Set environment variables in hosting platform
   - Use production MongoDB Atlas cluster

2. **Render.com Setup**:
   - Create new Web Service
   - Connect GitHub repository
   - Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - Start command: `python app.py`
   - Add environment variables

3. **Railway.app Setup**:
   - Create new project from GitHub
   - Add environment variables
   - Deploy automatically on push

### Frontend Deployment (Vercel/Netlify)

1. **Update API URL**:
   Edit `frontend/src/services/api.js`:
   ```javascript
   const API_URL = 'https://your-backend-url.com/api';
   ```

2. **Build for production**:
   ```bash
   cd frontend
   npm run build
   ```

3. **Vercel Deployment**:
   ```bash
   npm install -g vercel
   vercel
   ```

4. **Netlify Deployment**:
   - Drag and drop `dist` folder to Netlify
   - Or connect GitHub repository

### Environment Variables for Production

Backend:
- `MONGODB_URI`: Production MongoDB connection string
- `JWT_SECRET_KEY`: Strong secret key
- `GEMINI_API_KEY`: Google Gemini API key
- `FLASK_ENV`: production
- `FLASK_DEBUG`: False

## 🔧 Configuration Options

### Blog Generation Settings (config.py)
```python
MIN_BLOG_LENGTH = 500      # Minimum words
MAX_BLOG_LENGTH = 3000     # Maximum words
DEFAULT_BLOG_LENGTH = 1000 # Default words
```

### Tone Options
- `professional`: Business and formal content
- `casual`: Friendly and conversational
- `technical`: Expert-level technical writing
- `persuasive`: Marketing and sales content
- `educational`: Teaching and tutorial style

## 📊 System Architecture

```
User Request
    ↓
Frontend (React)
    ↓
API Layer (Flask)
    ↓
┌─────────────────────────┐
│  Content Pipeline       │
│  1. URL Validation      │
│  2. Content Extraction  │
│  3. Text Cleaning       │
│  4. Keyword Extraction  │  ← KeyBERT (Local NLP)
│  5. Topic Analysis      │
│  6. Prompt Building     │
│7. LLM Generation      │  ← Google Gemini API
│  8. SEO Processing      │
│  9. Database Storage    │  ← MongoDB
└─────────────────────────┘
    ↓
Response to User
```

## 💡 Usage Tips

1. **Best Results**:
   - Use URLs with substantial content (500+ words)
   - Choose tone matching your audience
   - Review preview before generating

2. **Cost Optimization**:
   - Shorter blogs cost less (fewer tokens)
   - Preview feature is free (no LLM call)
   - Reuse generated blogs when possible

3. **SEO Best Practices**:
   - Generated blogs include proper headings
   - Keywords are naturally integrated
   - Meta descriptions are auto-generated

## 🐛 Troubleshooting

### Backend Issues

**MongoDB Connection Error**:
```
Solution: Check MONGODB_URI in .env file
Verify MongoDB Atlas IP whitelist settings
```

**Gemini API Error**:
```
Solution: Verify GEMINI_API_KEY is correct
Check API quota and billing status
```

**KeyBERT Model Error**:
```
Solution: Install sentence-transformers
pip install sentence-transformers
```

### Frontend Issues

**API Connection Failed**:
```
Solution: Verify backend is running on port 5000
Check CORS settings in backend
Update API_URL in services/api.js
```

**Build Errors**:
```
Solution: Delete node_modules and package-lock.json
Run: npm install
```

## 📝 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Google for Gemini API
- KeyBERT for keyword extraction
- Trafilatura for content extraction
- Flask and React communities

---

**Built with ❤️ for creating amazing blog content**
