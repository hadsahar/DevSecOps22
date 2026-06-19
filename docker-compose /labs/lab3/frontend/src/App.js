import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [stats, setStats] = useState({});
  const [users, setUsers] = useState([]);
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsRes, usersRes, productsRes, ordersRes] = await Promise.all([
        fetch(`${apiUrl}/api/stats`),
        fetch(`${apiUrl}/api/users?per_page=5`),
        fetch(`${apiUrl}/api/products?per_page=5`),
        fetch(`${apiUrl}/api/orders?per_page=5`)
      ]);

      if (!statsRes.ok || !usersRes.ok || !productsRes.ok || !ordersRes.ok) {
        throw new Error('Failed to fetch data');
      }

      const [statsData, usersData, productsData, ordersData] = await Promise.all([
        statsRes.json(),
        usersRes.json(),
        productsRes.json(),
        ordersRes.json()
      ]);

      setStats(statsData);
      setUsers(usersData.users);
      setProducts(productsData.products);
      setOrders(ordersData.orders);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
          <hr />
          <button className="btn btn-outline-danger" onClick={fetchData}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container">
          <a className="navbar-brand" href="/">
            {process.env.REACT_APP_TITLE || 'Full-Stack Docker App'}
          </a>
          <div className="navbar-nav ms-auto">
            <span className="navbar-text">
              API: {apiUrl}
            </span>
          </div>
        </div>
      </nav>

      <div className="container mt-4">
        <div className="row">
          <div className="col-12">
            <h1 className="text-center mb-4">Dashboard</h1>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="row mb-4">
          <div className="col-md-4">
            <div className="card bg-primary text-white">
              <div className="card-body">
                <h5 className="card-title">Users</h5>
                <h2 className="card-text">{stats.users || 0}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card bg-success text-white">
              <div className="card-body">
                <h5 className="card-title">Products</h5>
                <h2 className="card-text">{stats.products || 0}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card bg-info text-white">
              <div className="card-body">
                <h5 className="card-title">Orders</h5>
                <h2 className="card-text">{stats.orders || 0}</h2>
              </div>
            </div>
          </div>
        </div>

        {/* Data Tables */}
        <div className="row">
          {/* Users Table */}
          <div className="col-lg-4 mb-4">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Recent Users</h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-sm">
                    <thead>
                      <tr>
                        <th>Username</th>
                        <th>Email</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.map(user => (
                        <tr key={user.id}>
                          <td>{user.username}</td>
                          <td>{user.email}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          {/* Products Table */}
          <div className="col-lg-4 mb-4">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Recent Products</h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-sm">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Price</th>
                      </tr>
                    </thead>
                    <tbody>
                      {products.map(product => (
                        <tr key={product.id}>
                          <td>{product.name}</td>
                          <td>${product.price}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          {/* Orders Table */}
          <div className="col-lg-4 mb-4">
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">Recent Orders</h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-sm">
                    <thead>
                      <tr>
                        <th>Order ID</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {orders.map(order => (
                        <tr key={order.id}>
                          <td>{order.order_id}</td>
                          <td>
                            <span className={`badge bg-${
                              order.status === 'delivered' ? 'success' :
                              order.status === 'shipped' ? 'info' :
                              order.status === 'pending' ? 'warning' :
                              'secondary'
                            }`}>
                              {order.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Refresh Button */}
        <div className="row">
          <div className="col-12 text-center">
            <button className="btn btn-primary btn-lg" onClick={fetchData}>
              Refresh Data
            </button>
          </div>
        </div>
      </div>

      <footer className="bg-light text-center py-3 mt-5">
        <div className="container">
          <p className="mb-0">
            Full-Stack Docker Application | Powered by React + Flask + PostgreSQL
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
