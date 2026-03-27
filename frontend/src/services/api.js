const API_ORIGIN =
  import.meta.env.VITE_API_ORIGIN || window.location.origin;
const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api/v1';
const API_BASE_URL = new URL(API_PREFIX, API_ORIGIN)
  .toString()
  .replace(/\/$/, '');

export function getAccessToken() {
  return localStorage.getItem('accessToken');
}

export async function request(path, options = {}) {
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
  let payload = null;

  if (rawText) {
    try {
      payload = JSON.parse(rawText);
    } catch {
      payload = rawText;
    }
  }

  if (!response.ok) {
    return {
      success: false,
      status: response.status,
      detail:
        (typeof payload === 'object' && payload !== null && payload.detail) ||
        (typeof payload === 'string' && payload) ||
        'Ошибка запроса',
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
    const token = getAccessToken();

    const response = await request('/auth/logout', {
      method: 'POST',
      token,
    });

    localStorage.removeItem('accessToken');

    if (!response.success && response.status !== 401) {
      return response;
    }

    return {
      success: true,
      status: 204,
      data: null,
    };
  },

  getCurrentUser() {
    return request('/auth/me', {
      method: 'GET',
      token: getAccessToken(),
    });
  },
};
