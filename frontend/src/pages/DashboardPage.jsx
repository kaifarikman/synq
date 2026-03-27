import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { profileAPI } from '../services/profileApi';
import './DashboardPage.css';

function getInitials(username) {
  if (!username) {
    return 'U';
  }

  return username.slice(0, 2).toUpperCase();
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadProfile() {
      const response = await profileAPI.getMyProfile();

      if (!active) {
        return;
      }

      if (response.success) {
        setProfile(response.data);
        setLoading(false);
        return;
      }

      if (response.status === 401) {
        await logout();
        navigate('/', { replace: true });
        return;
      }

      setLoading(false);
    }

    loadProfile();

    return () => {
      active = false;
    };
  }, [logout, navigate]);

  const completionFields = [
    user?.username,
    user?.email,
    profile?.full_name,
    profile?.bio,
  ];
  const filledFields = completionFields.filter(Boolean).length;
  const completion = Math.round((filledFields / completionFields.length) * 100);

  const handleLogout = async () => {
    await logout();
    navigate('/', { replace: true });
  };

  return (
    <div className="profile-page-clean">
      <div className="profile-grid-clean">
        <aside className="glass-card">
          <div className="avatar-placeholder-lg dashboard-avatar">
            {getInitials(user?.username)}
          </div>
          <h2 className="dashboard-name">{user?.username || 'Пользователь'}</h2>
          <p className="dashboard-email">{user?.email || 'Email не найден'}</p>
          <button className="btn-red" type="button" onClick={logout}>
            Выйти
          </button>
        </aside>

        <main className="glass-card dashboard-main-card">
          <div className="dashboard-heading-row">
            <div>
              <p className="dashboard-kicker">SYNQ</p>
              <h1 className="dashboard-title">Личный кабинет</h1>
            </div>
            <Link className="btn-light dashboard-inline-link" to="/profile">
              Редактировать профиль
            </Link>
          </div>

          <p className="dashboard-copy">
            {loading
              ? 'Подтягиваем данные профиля...'
              : 'Здесь собраны основные данные аккаунта и быстрый доступ к профилю.'}
          </p>

          <hr className="card-divider" />

          <section className="dashboard-section">
            <div className="progress-header">
              <span>Заполненность профиля</span>
              <strong>{completion}%</strong>
            </div>
            <div className="progress-bar-container">
              <div
                className="progress-bar-fill"
                style={{ width: `${completion}%` }}
              />
            </div>
          </section>

          <section className="dashboard-summary-grid">
            <div className="glass-card dashboard-summary-card">
              <h3>Основное</h3>
              <p>
                <strong>Логин:</strong> {user?.username || 'Не указан'}
              </p>
              <p>
                <strong>Email:</strong> {user?.email || 'Не указан'}
              </p>
            </div>
            <div className="glass-card dashboard-summary-card">
              <h3>Профиль</h3>
              <p>
                <strong>Полное имя:</strong>{' '}
                {profile?.full_name || 'Пока не заполнено'}
              </p>
              <p>
                <strong>О себе:</strong> {profile?.bio || 'Пока не заполнено'}
              </p>
            </div>
          </section>
        </main>

        <aside className="glass-card">
          <h3 className="dashboard-side-title">Быстрые действия</h3>
          <Link className="btn-light dashboard-side-link" to="/profile">
            Открыть мой профиль
          </Link>
          <button
            className="btn-outline-blue"
            type="button"
            onClick={() => navigate('/profile')}
          >
            Заполнить данные
          </button>
          <hr className="card-divider" />
          <div className="dashboard-note">
            Чем полнее профиль, тем проще дальше расширять функциональность кабинета.
          </div>
        </aside>
      </div>
    </div>
  );
}
