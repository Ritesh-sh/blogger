import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { blogAPI } from '../services/api';
import '../styles/Generator.css';

function Generator() {
  const [url, setUrl] = useState('');
  const [length, setLength] = useState(1000);
  const [tone, setTone] = useState('professional');
  const [includeCta, setIncludeCta] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const navigate = useNavigate();

  const handlePreview = async () => {
    if (!url) return;
    
    setLoadingPreview(true);
    setError('');
    
    try {
      const data = await blogAPI.previewContent(url);
      setPreview(data.preview);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to preview content');
    } finally {
      setLoadingPreview(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await blogAPI.generateBlog(url, length, tone, includeCta);
      // Navigate to the generated blog view
      navigate(`/blog/${data.blog.id}`);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to generate blog. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generator-container">
      <div className="generator-content">
        <h1>Generate Blog Post</h1>
        <p className="generator-subtitle">
          Enter a website URL to create an SEO-optimized blog post
        </p>

        <form onSubmit={handleSubmit} className="generator-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="url">Website URL *</label>
            <div className="url-input-group">
              <input
                type="url"
                id="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
                placeholder="https://example.com/article"
              />
              <button
                type="button"
                onClick={handlePreview}
                className="preview-button"
                disabled={!url || loadingPreview}
              >
                {loadingPreview ? 'Loading...' : 'Preview'}
              </button>
            </div>
          </div>

          {preview && (
            <div className="preview-card">
              <h3>Content Preview</h3>
              <p><strong>Title:</strong> {preview.title}</p>
              <p><strong>Word Count:</strong> {preview.word_count}</p>
              <p><strong>Keywords:</strong> {preview.keywords.join(', ')}</p>
              <p><strong>Summary:</strong> {preview.summary}</p>
            </div>
          )}

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="length">Blog Length (words)</label>
              <input
                type="number"
                id="length"
                value={length}
                onChange={(e) => setLength(Number(e.target.value))}
                min={500}
                max={3000}
                step={100}
              />
              <small>{length} words</small>
            </div>

            <div className="form-group">
              <label htmlFor="tone">Tone</label>
              <select
                id="tone"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
              >
                <option value="professional">Professional</option>
                <option value="casual">Casual</option>
                <option value="technical">Technical</option>
                <option value="persuasive">Persuasive</option>
                <option value="educational">Educational</option>
              </select>
            </div>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={includeCta}
                onChange={(e) => setIncludeCta(e.target.checked)}
              />
              Include Call-to-Action (CTA)
            </label>
          </div>

          <button
            type="submit"
            className="generate-button"
            disabled={loading || !url}
          >
            {loading ? '🤖 Generating Blog...' : '✨ Generate Blog'}
          </button>

          {loading && (
            <div className="loading-message">
              <p>This may take 30-60 seconds. Please wait...</p>
              <p>Extracting content → Analyzing keywords → Generating blog</p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default Generator;
