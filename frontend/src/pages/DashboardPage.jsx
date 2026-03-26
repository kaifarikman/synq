import { Link, useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import { useAuth } from '../hooks/useAuth';
import './DashboardPage.css';

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate('/', { replace: true });
  };

  return (
    <div className="profile-page-clean">
      <div className="profile-grid-clean">
        <div className="glass-card">
          <h2>Аккаунт</h2>
          <p>{user ? user.username : 'Пользователь авторизован'}</p>
          <p>{user ? user.email : 'Email недоступен'}</p>
          <Button type="button" onClick={handleLogout}>
            Выйти
          </Button>
        </div>

        <div className="glass-card">
          <h1 className="form-title">Dashboard</h1>
          <p>Это защищённая страница. Здесь можно продолжить работу после логина.</p>
          <Button type="button" onClick={() => navigate('/profile')}>
            Открыть профиль
          </Button>
        </div>

        <div className="glass-card">
          <h2>Навигация</h2>
          <p>
            <Link to="/profile">Мой профиль</Link>
          </p>
          <p>
            <Link to="/">На логин</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
