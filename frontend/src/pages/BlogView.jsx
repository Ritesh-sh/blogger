import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { blogAPI } from '../services/api';
import '../styles/BlogView.css';

function BlogView() {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetchBlog();
  }, [id]);

  const fetchBlog = async () => {
    setLoading(true);
    setError('');

    try {
      const data = await blogAPI.getBlogById(id);
      setBlog(data.blog);
    } catch (err) {
      setError('Failed to load blog');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(blog.generated_blog);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return <div className="loading">Loading blog...</div>;
  }

  if (error || !blog) {
    return (
      <div className="error-container">
        <p>{error || 'Blog not found'}</p>
        <Link to="/history" className="back-button">Back to History</Link>
      </div>
    );
  }

  const wordCount = blog.generated_blog.split(' ').length;

  return (
    <div className="blog-view-container">
      <div className="blog-view-header">
        <Link to="/history" className="back-link">← Back to History</Link>
        <button onClick={copyToClipboard} className="copy-button">
          {copied ? '✓ Copied!' : '📋 Copy Blog'}
        </button>
      </div>

      <div className="blog-meta">
        <p><strong>Source:</strong> <a href={blog.website_url} target="_blank" rel="noopener noreferrer">{blog.website_url}</a></p>
        <p><strong>Generated:</strong> {formatDate(blog.created_at)}</p>
        <p><strong>Word Count:</strong> {wordCount}</p>
      </div>

      <div className="blog-keywords">
        <strong>Keywords:</strong>
        <div className="keywords-list">
          {blog.keywords.map((keyword, index) => (
            <span key={index} className="keyword-tag">{keyword}</span>
          ))}
        </div>
      </div>

      <div className="blog-content">
        <div dangerouslySetInnerHTML={{ __html: renderMarkdown(blog.generated_blog) }} />
      </div>
    </div>
  );
}

// Simple markdown renderer (you can use a library like marked or react-markdown for better support)
function renderMarkdown(markdown) {
  let html = markdown;
  
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  
  // Italic
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  
  // Line breaks
  html = html.replace(/\n\n/g, '</p><p>');
  html = '<p>' + html + '</p>';
  
  return html;
}

export default BlogView;
