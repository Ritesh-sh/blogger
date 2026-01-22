import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { blogAPI } from '../services/api';
import '../styles/History.css';

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const [total, setTotal] = useState(0);
  const limit = 10;

  useEffect(() => {
    fetchHistory();
  }, [page]);

  const fetchHistory = async () => {
    setLoading(true);
    setError('');

    try {
      const data = await blogAPI.getHistory(limit, page * limit);
      setHistory(data.history);
      setTotal(data.total);
    } catch (err) {
      setError('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading && history.length === 0) {
    return <div className="loading">Loading history...</div>;
  }

  return (
    <div className="history-container">
      <div className="history-content">
        <div className="history-header">
          <h1>Blog History</h1>
          <p>Total blogs generated: {total}</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        {history.length === 0 ? (
          <div className="empty-state">
            <p>No blogs generated yet</p>
            <Link to="/generate" className="empty-state-button">
              Generate Your First Blog
            </Link>
          </div>
        ) : (
          <>
            <div className="history-list">
              {history.map((blog) => (
                <Link
                  to={`/blog/${blog.id}`}
                  key={blog.id}
                  className="history-item"
                >
                  <div className="history-item-header">
                    <h3>{blog.website_url}</h3>
                    <span className="history-date">
                      {formatDate(blog.created_at)}
                    </span>
                  </div>
                  <div className="history-item-meta">
                    <span>Keywords: {blog.keywords.slice(0, 3).join(', ')}</span>
                    <span>•</span>
                    <span>
                      {blog.generated_blog.split(' ').length} words
                    </span>
                  </div>
                </Link>
              ))}
            </div>

            {total > limit && (
              <div className="pagination">
                <button
                  onClick={() => setPage(Math.max(0, page - 1))}
                  disabled={page === 0}
                  className="pagination-button"
                >
                  Previous
                </button>
                <span className="pagination-info">
                  Page {page + 1} of {Math.ceil(total / limit)}
                </span>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={(page + 1) * limit >= total}
                  className="pagination-button"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default History;
