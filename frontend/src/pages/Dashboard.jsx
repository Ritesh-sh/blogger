import { Link } from 'react-router-dom';
import '../styles/Dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <h1>Welcome to AI Blog Generator</h1>
        <p className="dashboard-subtitle">
          Transform any website into a high-quality, SEO-optimized blog post
        </p>

        <div className="dashboard-cards">
          <Link to="/generate" className="dashboard-card">
            <div className="card-icon">✨</div>
            <h2>Generate Blog</h2>
            <p>Create a new blog post from any website URL</p>
          </Link>

          <Link to="/history" className="dashboard-card">
            <div className="card-icon">📚</div>
            <h2>View History</h2>
            <p>Access all your previously generated blogs</p>
          </Link>
        </div>

        <div className="dashboard-features">
          <h3>How It Works</h3>
          <div className="features-grid">
            <div className="feature-item">
              <span className="feature-number">1</span>
              <div>
                <h4>Provide URL</h4>
                <p>Enter any website URL you want to create a blog about</p>
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-number">2</span>
              <div>
                <h4>AI Analysis</h4>
                <p>Our AI extracts key topics and keywords automatically</p>
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-number">3</span>
              <div>
                <h4>Generate Blog</h4>
                <p>Get a complete, SEO-optimized blog post in seconds</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
