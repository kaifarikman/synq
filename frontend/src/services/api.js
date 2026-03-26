const API_ORIGIN =
  import.meta.env.VITE_API_ORIGIN || window.location.origin;
const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api/v1';
const API_BASE_URL = new URL(API_PREFIX, API_ORIGIN)
  .toString()
  .replace(/\/$/, '');

async function request(path, options = {}) {
  const { token, body, ...restOptions } = options;
  const headers = new Headers(restOptions.headers || {});

  if (body !== undefined) {
    headers.set('Content-Type', 'application/json');
  }

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...restOptions,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const rawText = await response.text();
  const payload = rawText ? JSON.parse(rawText) : null;

  if (!response.ok) {
    return {
      success: false,
      status: response.status,
      detail: payload?.detail || 'Ошибка запроса',
      data: payload,
    };
  }

  return {
    success: true,
    status: response.status,
    data: payload,
  };
}

export const authAPI = {
  register(userData) {
    return request('/auth/registry', {
      method: 'POST',
      body: userData,
    });
  },

  confirmEmail(email, code) {
    return request('/auth/confirm_email', {
      method: 'POST',
      body: { email, code },
    });
  },

  async login(email, password) {
    const response = await request('/auth/login', {
      method: 'POST',
      body: { email, password },
    });

    if (response.success && response.data?.access_token) {
      localStorage.setItem('accessToken', response.data.access_token);
    }

    return response;
  },

  async logout() {
    const token = localStorage.getItem('accessToken');

    if (token) {
      localStorage.removeItem('accessToken');
    }

    return {
      success: true,
      status: 204,
      data: null,
    };
  },

  async getCurrentUser() {
    return {
      success: false,
      status: 501,
      detail: 'Endpoint /auth/me ещё не реализован на backend',
      data: null,
    };
  },
};
