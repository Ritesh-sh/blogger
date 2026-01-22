import { useNavigate } from 'react-router-dom';
import '../styles/Landing.css';

function Landing() {
  const navigate = useNavigate();

  const features = [
    {
      icon: '🌐',
      title: 'Smart Content Extraction',
      description: 'Extracts meaningful content from any website URL instantly'
    },
    {
      icon: '🤖',
      title: 'AI-Powered Generation',
      description: 'Creates high-quality, SEO-optimized blogs using Google Gemini AI'
    },
    {
      icon: '🔑',
      title: 'NLP Keyword Extraction',
      description: 'Intelligent keyword extraction using advanced NLP algorithms'
    },
    {
      icon: '📊',
      title: 'SEO Optimization',
      description: 'Automatic meta descriptions, headings, and keyword optimization'
    },
    {
      icon: '💾',
      title: 'History Management',
      description: 'Store and retrieve all your generated blogs in one place'
    },
    {
      icon: '⚡',
      title: 'Lightning Fast',
      description: 'Generate professional blogs in seconds, not hours'
    }
  ];

  return (
    <div className="landing-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <span className="badge-text">✨ Powered by Google Gemini AI</span>
          </div>
          
          <h1 className="hero-title">
            Transform Any URL Into
            <span className="gradient-text"> SEO-Optimized Blogs</span>
          </h1>
          
          <p className="hero-description">
            Generate professional, engaging blog posts from any website URL in seconds. 
            Powered by cutting-edge AI and NLP technology for content that ranks.
          </p>

          <div className="hero-buttons">
            <button 
              className="btn-primary btn-get-started"
              onClick={() => navigate('/signup')}
            >
              <span>Get Started Free</span>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            
            <button 
              className="btn-secondary btn-login"
              onClick={() => navigate('/login')}
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 3C6.13401 3 3 6.13401 3 10C3 13.866 6.13401 17 10 17C13.866 17 17 13.866 17 10C17 6.13401 13.866 3 10 3Z" stroke="currentColor" strokeWidth="2"/>
                <path d="M10 7V10L12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span>Login</span>
            </button>
          </div>

          <div className="hero-stats">
            <div className="stat-item">
              <div className="stat-number">10x</div>
              <div className="stat-label">Faster Content</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <div className="stat-number">90%</div>
              <div className="stat-label">Cost Savings</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <div className="stat-number">100%</div>
              <div className="stat-label">SEO Optimized</div>
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="floating-card card-1">
            <div className="card-header">
              <div className="card-dot"></div>
              <div className="card-dot"></div>
              <div className="card-dot"></div>
            </div>
            <div className="card-content">
              <div className="card-line"></div>
              <div className="card-line short"></div>
              <div className="card-line"></div>
            </div>
          </div>
          
          <div className="floating-card card-2">
            <div className="card-icon">🚀</div>
            <div className="card-text">Blog Generated!</div>
          </div>
          
          <div className="floating-card card-3">
            <div className="card-icon">✨</div>
            <div className="card-text">SEO Score: 95%</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          <span className="section-badge">Features</span>
          <h2 className="section-title">Everything You Need to Create Amazing Content</h2>
          <p className="section-description">
            Powerful features designed to help you generate high-quality, SEO-optimized blog posts effortlessly
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <div className="section-header">
          <span className="section-badge">How It Works</span>
          <h2 className="section-title">Generate Blogs in 3 Simple Steps</h2>
        </div>

        <div className="steps-container">
          <div className="step-card">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3 className="step-title">Enter URL</h3>
              <p className="step-description">
                Paste any website URL you want to create content from
              </p>
            </div>
          </div>

          <div className="step-arrow">→</div>

          <div className="step-card">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3 className="step-title">AI Processing</h3>
              <p className="step-description">
                Our AI extracts content, analyzes keywords, and structures the blog
              </p>
            </div>
          </div>

          <div className="step-arrow">→</div>

          <div className="step-card">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3 className="step-title">Get Your Blog</h3>
              <p className="step-description">
                Receive a polished, SEO-optimized blog ready to publish
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2 className="cta-title">Ready to Transform Your Content Creation?</h2>
          <p className="cta-description">
            Join thousands of content creators who are already generating amazing blogs with AI
          </p>
          <button 
            className="btn-primary btn-cta"
            onClick={() => navigate('/signup')}
          >
            Start Creating Now
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
        
        <div className="cta-gradient"></div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <h3 className="footer-logo">AI Blog Generator</h3>
            <p className="footer-tagline">Create amazing content with AI</p>
          </div>
          <div className="footer-links">
            <button onClick={() => navigate('/signup')} className="footer-link">Get Started</button>
            <button onClick={() => navigate('/login')} className="footer-link">Login</button>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2026 AI Blog Generator. Built with ❤️ using Google Gemini AI</p>
        </div>
      </footer>
    </div>
  );
}

export default Landing;
