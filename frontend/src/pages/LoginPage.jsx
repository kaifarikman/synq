import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import FormCard from '../components/FormCard';
import Input from '../components/Input';
import Button from '../components/Button';
import { useAuth } from '../hooks/useAuth';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const formData = new FormData(e.target);
    const email = formData.get('email');
    const password = formData.get('password');

    try {
      const result = await login(email, password);
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.message || 'Ошибка входа');
      }
    } catch (err) {
      setError('Ошибка подключения к серверу');
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormCard
      title="С возвращением!"
      footer={<>Ещё нет аккаунта? <Link to="/register">Регистрация</Link></>}
    >
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleLogin}>
        <Input name="email" type="email" placeholder="Введите email" required />
        <Input name="password" type="password" placeholder="Введите пароль" required />
        <Button disabled={loading}>
          {loading ? 'Вход...' : 'Войти'}
        </Button>
      </form>
    </FormCard>
  );
}