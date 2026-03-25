const API_BASE_URL = 'http://localhost:3000/api/v1';
let registeredUser = null;

export const authAPI = {
  register: async (userData) => {
    console.log('Registration request:', userData);
    await new Promise(resolve => setTimeout(resolve, 1000));

    if (!userData.username || !userData.email || !userData.password) {
      return {
        success: false,
        status: 400,
        detail: 'Невалидные входные данные'
      };
    }

    if (!userData.email.includes('@')) {
      return {
        success: false,
        status: 400,
        detail: 'Введите корректный email'
      };
    }

    if (userData.password.length < 6) {
      return {
        success: false,
        status: 400,
        detail: 'Пароль должен содержать минимум 6 символов'
      };
    }

    if (userData.username.length < 3) {
      return {
        success: false,
        status: 400,
        detail: 'Имя пользователя должно содержать минимум 3 символа'
      };
    }

    if (registeredUser && registeredUser.email === userData.email) {
      return {
        success: false,
        status: 409,
        detail: 'Пользователь с таким email уже существует'
      };
    }

    if (registeredUser && registeredUser.username === userData.username) {
      return {
        success: false,
        status: 409,
        detail: 'Пользователь с таким именем уже существует'
      };
    }

    const newUser = {
      id: Math.floor(Math.random() * 1000),
      email: userData.email,
      username: userData.username,
      password: userData.password,
      profile: {
        id: Math.floor(Math.random() * 1000),
        uuid: crypto.randomUUID()
      }
    };

    registeredUser = newUser;

    return {
      success: true,
      status: 201,
      data: {
        user: {
          id: newUser.id,
          email: newUser.email,
          username: newUser.username
        },
        profile: newUser.profile
      }
    };
  },

  login: async (email, password) => {
    console.log('Login request:', { email, password });
    await new Promise(resolve => setTimeout(resolve, 1000));

    if (!email || !password) {
      return {
        success: false,
        status: 400,
        detail: 'Невалидный формат запроса'
      };
    }

    if (!registeredUser) {
      return {
        success: false,
        status: 401,
        detail: 'Неверный email или пароль'
      };
    }

    if (registeredUser.email !== email || registeredUser.password !== password) {
      return {
        success: false,
        status: 401,
        detail: 'Неверный email или пароль'
      };
    }

    const accessToken = 'mock-jwt-token-' + Date.now();
    localStorage.setItem('accessToken', accessToken);

    return {
      success: true,
      status: 200,
      data: {
        accessToken: accessToken,
        tokenType: 'Bearer'
      }
    };
  },

  logout: async () => {
    console.log('Logout request');
    await new Promise(resolve => setTimeout(resolve, 500));

    const token = localStorage.getItem('accessToken');

    if (!token) {
      return {
        success: false,
        status: 401,
        detail: 'Токен отсутствует или недействителен'
      };
    }

    localStorage.removeItem('accessToken');

    return {
      success: true,
      status: 204,
      data: null
    };
  },

  getCurrentUser: async () => {
    console.log('Get current user request');
    await new Promise(resolve => setTimeout(resolve, 500));

    const token = localStorage.getItem('accessToken');

    if (!token) {
      return {
        success: false,
        status: 401,
        detail: 'Токен отсутствует или недействителен'
      };
    }

    if (!registeredUser) {
      return {
        success: false,
        status: 401,
        detail: 'Пользователь не найден'
      };
    }

    return {
      success: true,
      status: 200,
      data: {
        id: registeredUser.id,
        email: registeredUser.email,
        username: registeredUser.username,
        profile: registeredUser.profile
      }
    };
  }
};