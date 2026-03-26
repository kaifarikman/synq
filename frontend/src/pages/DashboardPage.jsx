import { Link } from 'react-router-dom';
import Button from '../components/Button';
import { useAuth } from '../hooks/useAuth';

export default function DashboardPage() {
  const { user, logout } = useAuth();

  return (
    <div className="form-card">
      <h1 className="form-title">Защищённая страница</h1>
      <p>{user ? `Вы вошли как ${user.username}` : 'Пользователь авторизован'}</p>
      <p>
        <Link to="/profile">Мой профиль</Link>
      </p>
      <Button type="button" onClick={logout}>
        Выйти
      </Button>
    </div>
  );
}
