import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Generator from './pages/Generator';
import History from './pages/History';
import BlogView from './pages/BlogView';
import Navbar from './components/Navbar';
import './styles/App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const handleLogin = (token) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      {isAuthenticated && <Navbar onLogout={handleLogout} />}
      <Routes>
        <Route 
          path="/" 
          element={!isAuthenticated ? <Landing /> : <Navigate to="/dashboard" />} 
        />
        <Route 
          path="/login" 
          element={!isAuthenticated ? <Login onLogin={handleLogin} /> : <Navigate to="/dashboard" />} 
        />
        <Route 
          path="/signup" 
          element={!isAuthenticated ? <Signup onLogin={handleLogin} /> : <Navigate to="/dashboard" />} 
        />
        <Route 
          path="/dashboard" 
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/" />} 
        />
        <Route 
          path="/generate" 
          element={isAuthenticated ? <Generator /> : <Navigate to="/" />} 
        />
        <Route 
          path="/history" 
          element={isAuthenticated ? <History /> : <Navigate to="/" />} 
        />
        <Route 
          path="/blog/:id" 
          element={isAuthenticated ? <BlogView /> : <Navigate to="/" />} 
        />
      </Routes>
    </Router>
  );
}

export default App;
