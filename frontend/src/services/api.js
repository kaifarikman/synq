const API_BASE_URL = 'http://localhost:3000/api/v1';
let registeredUser = null;

export const authAPI = {
  register: async (userData) => {
    console.log('Registration request:', userData);

    await new Promise(resolve => setTimeout(resolve, 1000));

    if (!userData.username || !userData.email || !userData.password) {
      return {
        success: false,
        detail: 'Заполните все поля'
      };
    }

    if (!userData.email.includes('@')) {
      return {
        success: false,
        detail: 'Введите корректный email'
      };
    }

    if (userData.password.length < 6) {
      return {
        success: false,
        detail: 'Пароль должен содержать минимум 6 символов'
      };
    }

    if (userData.username.length < 3) {
      return {
        success: false,
        detail: 'Имя пользователя должно содержать минимум 3 символа'
      };
    }

    registeredUser = {
      email: userData.email,
      password: userData.password,
      username: userData.username,
      profile: {
        id: Math.floor(Math.random() * 1000),
        uuid: crypto.randomUUID()
      }
    };

    return {
      success: true,
      user: {
        id: Math.floor(Math.random() * 1000),
        email: userData.email,
        username: userData.username
      },
      profile: registeredUser.profile
    };
  },

  // Вход
  login: async (email, password) => {
    console.log('Login request:', { email, password });

    await new Promise(resolve => setTimeout(resolve, 1000));

    if (!email || !password) {
      return {
        success: false,
        detail: 'Заполните все поля'
      };
    }

    if (registeredUser && registeredUser.email === email && registeredUser.password === password) {
      const accessToken = 'mock-jwt-token-' + Date.now();
      localStorage.setItem('accessToken', accessToken);
      return {
        success: true,
        accessToken: accessToken,
        tokenType: 'Bearer'
      };
    }

    return {
      success: false,
      detail: 'Неверный email или пароль'
    };
  },

  logout: async () => {
    console.log('Logout request');
    await new Promise(resolve => setTimeout(resolve, 500));
    localStorage.removeItem('accessToken');
    return { success: true };
  },

  getCurrentUser: async () => {
    console.log('Get current user request');
    await new Promise(resolve => setTimeout(resolve, 500));

    const token = localStorage.getItem('accessToken');
    if (!token || !registeredUser) {
      return {
        success: false,
        detail: 'Unauthorized'
      };
    }

    return {
      success: true,
      id: 1,
      email: registeredUser.email,
      username: registeredUser.username,
      profile: registeredUser.profile
    };
  }
};