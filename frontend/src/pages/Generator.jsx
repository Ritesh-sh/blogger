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
      {/* Hero Section */}
      <div className="generator-hero">
        <div className="hero-content">
          <div className="magic-icon">✨</div>
          <h1>Generate Blog Post</h1>
          <p>Transform any web article into an SEO-optimized blog post powered by AI</p>
        </div>
      </div>

      <div className="generator-content">
        <form onSubmit={handleSubmit} className="generator-form">
          {error && (
            <div className="error-message">
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
              </svg>
              {error}
            </div>
          )}

          <div className="form-section">
            <div className="form-group">
              <label htmlFor="url">
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clipRule="evenodd"/>
                </svg>
                Website URL
              </label>
              <div className="url-input-group">
                <input
                  type="url"
                  id="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  required
                  placeholder="https://example.com/article"
                  className="url-input"
                />
                <button
                  type="button"
                  onClick={handlePreview}
                  className="preview-button"
                  disabled={!url || loadingPreview}
                >
                  {loadingPreview ? (
                    <>
                      <span className="spinner"></span>
                      Loading...
                    </>
                  ) : (
                    <>
                      <svg width="18" height="18" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                        <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd"/>
                      </svg>
                      Preview
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {preview && (
            <div className="preview-card">
              <div className="preview-header">
                <svg width="24" height="24" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
                </svg>
                <h3>Content Preview</h3>
              </div>
              <div className="preview-content">
                <div className="preview-item">
                  <span className="preview-label">Title</span>
                  <span className="preview-value">{preview.title}</span>
                </div>
                <div className="preview-item">
                  <span className="preview-label">Word Count</span>
                  <span className="preview-value">{preview.word_count}</span>
                </div>
                <div className="preview-item">
                  <span className="preview-label">Keywords</span>
                  <div className="preview-keywords">
                    {preview.keywords.map((keyword, idx) => (
                      <span key={idx} className="keyword-pill">{keyword}</span>
                    ))}
                  </div>
                </div>
                <div className="preview-item">
                  <span className="preview-label">Summary</span>
                  <span className="preview-value summary">{preview.summary}</span>
                </div>
              </div>
            </div>
          )}

          <div className="form-section">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="length">
                  <svg width="18" height="18" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd"/>
                  </svg>
                  Blog Length
                </label>
                <input
                  type="number"
                  id="length"
                  value={length}
                  onChange={(e) => setLength(Number(e.target.value))}
                  min={500}
                  max={3000}
                  step={100}
                />
                <small className="field-hint">{length} words</small>
              </div>

              <div className="form-group">
                <label htmlFor="tone">
                  <svg width="18" height="18" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
                  </svg>
                  Writing Tone
                </label>
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
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={includeCta}
                  onChange={(e) => setIncludeCta(e.target.checked)}
                />
                <span className="checkbox-custom"></span>
                Include Call-to-Action (CTA)
              </label>
            </div>
          </div>

          <button
            type="submit"
            className="generate-button"
            disabled={loading || !url}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Generating Blog...
              </>
            ) : (
              <>
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd"/>
                </svg>
                Generate Blog
              </>
            )}
          </button>

          {loading && (
            <div className="loading-message">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <p className="loading-text">AI is working its magic... This may take 30-60 seconds</p>
              <div className="loading-steps">
                <div className="loading-step">
                  <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                  </svg>
                  Extracting content
                </div>
                <div className="loading-step">
                  <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                  </svg>
                  Analyzing keywords
                </div>
                <div className="loading-step">
                  <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clipRule="evenodd"/>
                  </svg>
                  Generating blog
                </div>
              </div>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default Generator;
