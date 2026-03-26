import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import FormCard from '../components/FormCard';
import Input from '../components/Input';
import Button from '../components/Button';
import { useAuth } from '../hooks/useAuth';

export default function VerifyPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { confirmEmail } = useAuth();
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const emailFromState = location.state?.email;
    const emailFromStorage = sessionStorage.getItem('pendingRegistrationEmail');
    setEmail(emailFromState || emailFromStorage || '');
  }, [location.state]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const result = await confirmEmail(email, Number(code));
      if (result.success) {
        sessionStorage.removeItem('pendingRegistrationEmail');
        setSuccess('Email подтверждён. Теперь можно войти.');
        navigate('/', {
          replace: true,
          state: { email },
        });
      } else {
        setError(result.detail || 'Ошибка подтверждения email');
      }
    } catch {
      setError('Ошибка подключения к серверу');
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormCard
      title="Подтверждение"
      footer={
        <>
          Нет письма? <Link to="/register">Вернуться к регистрации</Link>
        </>
      }
    >
      {error && <div className="error-message">{error}</div>}
      {success && <div className="form-footer">{success}</div>}
      <form onSubmit={handleSubmit}>
        <Input
          name="email"
          type="email"
          placeholder="Введите email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Input
          name="code"
          type="text"
          placeholder="000000"
          required
          maxLength="6"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          style={{ textAlign: 'center', fontSize: '1.5rem', letterSpacing: '10px' }}
        />
        <Button disabled={loading}>
          {loading ? 'Подтверждение...' : 'Подтвердить'}
        </Button>
      </form>
    </FormCard>
  );
}
