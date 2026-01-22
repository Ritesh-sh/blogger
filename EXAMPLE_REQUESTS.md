# Example API Requests

Test these API requests using tools like Postman, cURL, or HTTPie.

## 1. User Signup

```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": "65a1234567890abcdef12345",
    "email": "test@example.com",
    "created_at": "2024-01-15T10:30:00"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 2. User Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## 3. Preview Content (Before Generation)

```bash
curl -X POST http://localhost:5000/api/blog/preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
  }'
```

**Response:**
```json
{
  "preview": {
    "title": "Artificial intelligence - Wikipedia",
    "description": "Artificial intelligence (AI) is intelligence demonstrated by machines...",
    "summary": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to natural intelligence displayed by animals including humans...",
    "keywords": [
      "artificial intelligence",
      "machine learning",
      "neural networks",
      "deep learning",
      "AI systems"
    ],
    "word_count": 4532,
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
  }
}
```

## 4. Generate Blog Post

```bash
curl -X POST http://localhost:5000/api/blog/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Machine_learning",
    "length": 1000,
    "tone": "professional",
    "include_cta": true
  }'
```

**Response:**
```json
{
  "message": "Blog generated successfully",
  "blog": {
    "id": "65a9876543210fedcba98765",
    "content": "# Understanding Machine Learning: A Comprehensive Guide\n\nMachine learning has revolutionized...",
    "title": "Understanding Machine Learning: A Comprehensive Guide",
    "meta_description": "Explore the fundamentals of machine learning, its applications, and how it's transforming industries worldwide.",
    "keywords": [
      "machine learning",
      "artificial intelligence",
      "data science",
      "algorithms",
      "neural networks"
    ],
    "word_count": 1024,
    "reading_time": 5,
    "website_url": "https://en.wikipedia.org/wiki/Machine_learning",
    "topic_analysis": {
      "intent": "educational",
      "category": "technology",
      "topic_summary": "Content covering machine learning, algorithms, and data science"
    }
  }
}
```

## 5. Get Blog History

```bash
curl -X GET "http://localhost:5000/api/blog/history?limit=5&skip=0" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "history": [
    {
      "id": "65a9876543210fedcba98765",
      "user_id": "65a1234567890abcdef12345",
      "website_url": "https://en.wikipedia.org/wiki/Machine_learning",
      "keywords": ["machine learning", "AI", "algorithms"],
      "generated_blog": "# Understanding Machine Learning...",
      "blog_config": {
        "length": 1000,
        "tone": "professional",
        "include_cta": true
      },
      "created_at": "2024-01-15T11:00:00"
    }
  ],
  "total": 1,
  "limit": 5,
  "skip": 0
}
```

## 6. Get Specific Blog

```bash
curl -X GET http://localhost:5000/api/blog/history/65a9876543210fedcba98765 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 7. Get Current User

```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 8. Health Check (No Auth Required)

```bash
curl -X GET http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Blog Generator API is running"
}
```

---

## Using HTTPie (Alternative)

HTTPie has cleaner syntax:

```bash
# Install HTTPie
pip install httpie

# Signup
http POST :5000/api/auth/signup email=test@example.com password=password123

# Login
http POST :5000/api/auth/login email=test@example.com password=password123

# Generate blog (with token)
http POST :5000/api/blog/generate \
  url=https://example.com \
  length:=1000 \
  tone=professional \
  include_cta:=true \
  Authorization:"Bearer YOUR_TOKEN"
```

---

## Using JavaScript (Fetch API)

```javascript
// Signup
const signup = async () => {
  const response = await fetch('http://localhost:5000/api/auth/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'test@example.com',
      password: 'password123'
    })
  });
  const data = await response.json();
  console.log(data);
  return data.access_token;
};

// Generate blog
const generateBlog = async (token) => {
  const response = await fetch('http://localhost:5000/api/blog/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      url: 'https://en.wikipedia.org/wiki/Python_(programming_language)',
      length: 1000,
      tone: 'professional',
      include_cta: true
    })
  });
  const data = await response.json();
  console.log(data);
};

// Usage
const token = await signup();
await generateBlog(token);
```

---

## Using Python Requests

```python
import requests

BASE_URL = 'http://localhost:5000/api'

# Signup
response = requests.post(f'{BASE_URL}/auth/signup', json={
    'email': 'test@example.com',
    'password': 'password123'
})
token = response.json()['access_token']

# Generate blog
response = requests.post(
    f'{BASE_URL}/blog/generate',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'url': 'https://en.wikipedia.org/wiki/Python_(programming_language)',
        'length': 1000,
        'tone': 'professional',
        'include_cta': True
    }
)
blog = response.json()
print(blog['blog']['content'])
```

---

## Postman Collection

Import this JSON into Postman:

```json
{
  "info": {
    "name": "Blog Generator API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Signup",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": {
              "raw": "http://localhost:5000/api/auth/signup",
              "protocol": "http",
              "host": ["localhost"],
              "port": "5000",
              "path": ["api", "auth", "signup"]
            }
          }
        }
      ]
    }
  ]
}
```

Save this as a `.json` file and import into Postman.
