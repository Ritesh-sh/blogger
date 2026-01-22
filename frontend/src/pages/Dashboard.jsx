import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import '../styles/Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState({
    totalBlogs: 0,
    todayBlogs: 0
  });

  return (
    <div className="dashboard-container">
      <div className="dashboard-hero">
        <div className="hero-content">
          <h1 className="dashboard-title">
            Welcome to <span className="gradient-text">AI Blog Generator</span>
          </h1>
          <p className="dashboard-subtitle">
            Transform any website into high-quality, SEO-optimized blog posts powered by Google Gemini AI
          </p>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="quick-actions">
          <Link to="/generate" className="action-card action-primary">
            <div className="action-icon-wrapper">
              <div className="action-icon">
                <svg width="32" height="32" viewBox="0 0 20 20" fill="none">
                  <path d="M10 3L12 8H17L13 11L14.5 16L10 13L5.5 16L7 11L3 8H8L10 3Z" stroke="currentColor" strokeWidth="2" fill="currentColor"/>
                </svg>
              </div>
            </div>
            <div className="action-content">
              <h2>Generate New Blog</h2>
              <p>Create amazing content from any URL in seconds</p>
            </div>
            <div className="action-arrow">
              <svg width="24" height="24" viewBox="0 0 20 20" fill="none">
                <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          </Link>

          <Link to="/history" className="action-card action-secondary">
            <div className="action-icon-wrapper">
              <div className="action-icon">
                <svg width="32" height="32" viewBox="0 0 20 20" fill="none">
                  <path d="M3 4H17C17.55 4 18 4.45 18 5V15C18 15.55 17.55 16 17 16H3C2.45 16 2 15.55 2 15V5C2 4.45 2.45 4 3 4Z" stroke="currentColor" strokeWidth="2"/>
                  <path d="M2 8H18" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
            </div>
            <div className="action-content">
              <h2>View History</h2>
              <p>Access all your previously generated blogs</p>
            </div>
            <div className="action-arrow">
              <svg width="24" height="24" viewBox="0 0 20 20" fill="none">
                <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          </Link>
        </div>

        <div className="features-section">
          <div className="section-header">
            <h3>How It Works</h3>
            <p>Three simple steps to amazing content</p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-number">1</div>
              <div className="feature-icon">🌐</div>
              <h4>Provide URL</h4>
              <p>Enter any website URL you want to create a blog about</p>
            </div>

            <div className="feature-card">
              <div className="feature-number">2</div>
              <div className="feature-icon">🤖</div>
              <h4>AI Analysis</h4>
              <p>Our AI extracts key topics and keywords automatically using advanced NLP</p>
            </div>

            <div className="feature-card">
              <div className="feature-number">3</div>
              <div className="feature-icon">✨</div>
              <h4>Get Your Blog</h4>
              <p>Receive a complete, SEO-optimized blog post ready to publish</p>
            </div>
          </div>
        </div>

        <div className="stats-section">
          <div className="stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-content">
              <div className="stat-value">30s</div>
              <div className="stat-label">Average Generation Time</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">💎</div>
            <div className="stat-content">
              <div className="stat-value">100%</div>
              <div className="stat-label">SEO Optimized</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🎯</div>
            <div className="stat-content">
              <div className="stat-value">$0.001</div>
              <div className="stat-label">Cost Per Blog</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🚀</div>
            <div className="stat-content">
              <div className="stat-value">10x</div>
              <div className="stat-label">Faster Than Manual</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
