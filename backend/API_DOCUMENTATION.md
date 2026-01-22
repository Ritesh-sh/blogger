# Backend API Endpoints

Base URL: `http://localhost:5000/api`

## Authentication

### POST /auth/signup
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (201):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00"
  },
  "access_token": "jwt_token_here"
}
```

**Errors:**
- 400: Missing fields or invalid email
- 409: User already exists

---

### POST /auth/login
Login to existing account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00"
  },
  "access_token": "jwt_token_here"
}
```

**Errors:**
- 400: Missing fields
- 401: Invalid credentials

---

### GET /auth/me
Get current authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Errors:**
- 401: Invalid or missing token
- 404: User not found

---

## Blog Generation

### POST /blog/generate
Generate a blog post from a website URL.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "url": "https://example.com/article",
  "length": 1000,
  "tone": "professional",
  "include_cta": true
}
```

**Parameters:**
- `url` (required): Website URL to extract content from
- `length` (optional): Blog length in words (500-3000, default: 1000)
- `tone` (optional): Writing tone (professional/casual/technical/persuasive/educational, default: professional)
- `include_cta` (optional): Include call-to-action (boolean, default: true)

**Response (200):**
```json
{
  "message": "Blog generated successfully",
  "blog": {
    "id": "blog_id",
    "content": "# Blog Title\n\nBlog content here...",
    "title": "Blog Title",
    "meta_description": "SEO meta description",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "word_count": 1000,
    "reading_time": 5,
    "website_url": "https://example.com/article",
    "topic_analysis": {
      "intent": "informational",
      "category": "technology",
      "topic_summary": "Content about AI and ML"
    }
  }
}
```

**Errors:**
- 400: Invalid URL, missing fields, or content extraction failed
- 401: Unauthorized
- 500: Blog generation failed

---

### GET /blog/history
Get user's blog generation history.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `limit` (optional): Number of entries (1-50, default: 10)
- `skip` (optional): Number to skip for pagination (default: 0)

**Response (200):**
```json
{
  "history": [
    {
      "id": "blog_id",
      "user_id": "user_id",
      "website_url": "https://example.com",
      "keywords": ["keyword1", "keyword2"],
      "generated_blog": "Blog content...",
      "blog_config": {
        "length": 1000,
        "tone": "professional",
        "include_cta": true
      },
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 25,
  "limit": 10,
  "skip": 0
}
```

**Errors:**
- 401: Unauthorized
- 500: Server error

---

### GET /blog/history/:id
Get a specific blog entry by ID.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "blog": {
    "id": "blog_id",
    "user_id": "user_id",
    "website_url": "https://example.com",
    "keywords": ["keyword1", "keyword2"],
    "generated_blog": "Blog content...",
    "blog_config": {
      "length": 1000,
      "tone": "professional",
      "include_cta": true
    },
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Errors:**
- 401: Unauthorized
- 404: Blog not found
- 500: Server error

---

### POST /blog/preview
Preview content extraction without generating blog.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "url": "https://example.com/article"
}
```

**Response (200):**
```json
{
  "preview": {
    "title": "Article Title",
    "description": "Meta description",
    "summary": "First 300 characters...",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "word_count": 1500,
    "url": "https://example.com/article"
  }
}
```

**Errors:**
- 400: Invalid URL or content extraction failed
- 401: Unauthorized

---

## Health Check

### GET /api/health
Check API health status.

**Response (200):**
```json
{
  "status": "healthy",
  "message": "Blog Generator API is running"
}
```

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Error Type",
  "message": "Detailed error message"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `409`: Conflict
- `500`: Internal Server Error
