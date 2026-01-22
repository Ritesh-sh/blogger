import { Link, useLocation } from 'react-router-dom';
import '../styles/Navbar.css';

function Navbar({ onLogout }) {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-logo">
          <span className="logo-icon">✍️</span>
          <span className="logo-text">AI Blog Generator</span>
        </Link>
        <div className="navbar-links">
          <Link 
            to="/dashboard" 
            className={`navbar-link ${isActive('/dashboard') ? 'active' : ''}`}
          >
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M3 10L10 3L17 10V17C17 17.55 16.55 18 16 18H4C3.45 18 3 17.55 3 17V10Z" stroke="currentColor" strokeWidth="2"/>
            </svg>
            Dashboard
          </Link>
          <Link 
            to="/generate" 
            className={`navbar-link ${isActive('/generate') ? 'active' : ''}`}
          >
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="7" stroke="currentColor" strokeWidth="2"/>
              <path d="M10 7V13M7 10H13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            Generate
          </Link>
          <Link 
            to="/history" 
            className={`navbar-link ${isActive('/history') ? 'active' : ''}`}
          >
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M3 4H17C17.55 4 18 4.45 18 5V15C18 15.55 17.55 16 17 16H3C2.45 16 2 15.55 2 15V5C2 4.45 2.45 4 3 4Z" stroke="currentColor" strokeWidth="2"/>
              <path d="M2 8H18" stroke="currentColor" strokeWidth="2"/>
            </svg>
            History
          </Link>
          <button onClick={onLogout} className="navbar-logout">
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M13 3H16C16.55 3 17 3.45 17 4V16C17 16.55 16.55 17 16 17H13" stroke="currentColor" strokeWidth="2"/>
              <path d="M8 14L12 10L8 6M12 10H3" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
