// Centralized API fetch utility for authenticated requests
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function apiFetch(url, options = {}, navigate) {
  const token = localStorage.getItem('token');
  const headers = {
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
  let method = (options.method || 'GET').toUpperCase();
  let opts = { ...options, headers };
  if (method === 'GET' || method === 'HEAD') {
    // Remove body for GET/HEAD requests
    const { body, ...rest } = opts;
    opts = rest;
  }
  // If url is relative, prepend API_BASE_URL
  const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${url.startsWith('/') ? '' : '/'}${url}`;
  const res = await fetch(fullUrl, opts);
  if (res.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    if (navigate) navigate('/login');
    throw new Error('Unauthorized');
  }
  return res;
} 