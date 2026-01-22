import { Link } from 'react-router-dom';
import '../styles/Navbar.css';

function Navbar({ onLogout }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-logo">
          🤖 AI Blog Generator
        </Link>
        <div className="navbar-links">
          <Link to="/dashboard" className="navbar-link">Dashboard</Link>
          <Link to="/generate" className="navbar-link">Generate</Link>
          <Link to="/history" className="navbar-link">History</Link>
          <button onClick={onLogout} className="navbar-logout">Logout</button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
