import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import FormCard from '../components/FormCard';
import Input from '../components/Input';
import Button from '../components/Button';
import { useAuth } from '../hooks/useAuth';

export default function RegistrationPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const formData = new FormData(e.target);
    const userData = {
      username: formData.get('username'),
      email: formData.get('email'),
      password: formData.get('password'),
    };

    try {
      const result = await register(userData);
      if (result.success) {
        sessionStorage.setItem('pendingRegistrationEmail', userData.email);
        navigate('/verify', {
          state: { email: userData.email },
        });
      } else {
        setError(result.detail || 'Ошибка регистрации');
      }
    } catch {
      setError('Ошибка подключения к серверу');
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormCard
      title="Добро пожаловать!"
      footer={<>Уже есть аккаунт? <Link to="/">Войти</Link></>}
    >
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleRegister}>
        <Input name="username" type="text" placeholder="Имя пользователя" required />
        <Input name="email" type="email" placeholder="Введите email" required />
        <Input name="password" type="password" placeholder="Придумайте пароль" required />
        <Button disabled={loading}>
          {loading ? 'Регистрация...' : 'Зарегистрироваться'}
        </Button>
      </form>
    </FormCard>
  );
}
