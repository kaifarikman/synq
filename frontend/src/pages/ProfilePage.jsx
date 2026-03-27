import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { profileAPI } from '../services/profileApi';
import './ProfilePage.css';

function getInitials(username) {
  if (!username) {
    return 'U';
  }

  return username.slice(0, 2).toUpperCase();
}

export default function ProfilePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const [form, setForm] = useState({
    full_name: '',
    bio: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    let active = true;

    async function loadProfile() {
      const response = await profileAPI.getMyProfile();

      if (!active) {
        return;
      }

      if (response.success) {
        setForm({
          full_name: response.data.full_name || '',
          bio: response.data.bio || '',
        });
        setLoading(false);
        return;
      }

      if (response.status === 401) {
        await logout();
        navigate('/', { replace: true });
        return;
      }

      setError(response.detail || 'Не удалось загрузить профиль');
      setLoading(false);
    }

    loadProfile();

    return () => {
      active = false;
    };
  }, [logout, navigate]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');
    setSaving(true);

    const response = await profileAPI.updateMyProfile({
      full_name: form.full_name || null,
      bio: form.bio || null,
    });

    if (response.success) {
      setForm({
        full_name: response.data.full_name || '',
        bio: response.data.bio || '',
      });
      setSuccess('Профиль сохранён');
      setSaving(false);
      return;
    }

    if (response.status === 401) {
      await logout();
      navigate('/', { replace: true });
      return;
    }

    setError(response.detail || 'Не удалось сохранить профиль');
    setSaving(false);
  };

  if (loading) {
    return <div className="profile-loading">Загрузка профиля...</div>;
  }

  return (
    <div className="profile-edit-container">
      <form className="glass-card edit-card" onSubmit={handleSubmit}>
        <div className="edit-header">
          <div className="avatar-upload-section">
            <div className="avatar-circle-large">
              <span>{getInitials(user?.username)}</span>
            </div>
            <p className="avatar-helper">Аватар пока не редактируется</p>
          </div>

          <div className="main-info-grid">
            <div className="input-group-row">
              <label htmlFor="full_name">Полное имя:</label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                value={form.full_name}
                onChange={handleChange}
                placeholder="Введите полное имя"
                className="blue-input"
              />
            </div>
            <div className="input-group-row">
              <label htmlFor="email">Почта:</label>
              <input
                id="email"
                type="email"
                value={user?.email || ''}
                className="readonly-input"
                readOnly
              />
            </div>
            <div className="input-group-row">
              <label htmlFor="username">Логин:</label>
              <input
                id="username"
                type="text"
                value={user?.username || ''}
                className="readonly-input"
                readOnly
              />
            </div>
          </div>
        </div>

        <hr className="edit-divider" />

        <div className="additional-info-section">
          <h3 className="section-title">Дополнительная информация</h3>
          {error && <div className="error-message profile-error">{error}</div>}
          {success && <div className="profile-success">{success}</div>}
          <div className="full-width-field">
            <label htmlFor="bio">О себе:</label>
            <textarea
              id="bio"
              name="bio"
              rows="4"
              value={form.bio}
              onChange={handleChange}
              className="standard-input"
              placeholder="Расскажите немного о себе"
            />
          </div>
          <p className="profile-note">
            Сейчас backend поддерживает редактирование полей профиля `full_name`
            и `bio`. Остальные данные отображаются как часть аккаунта.
          </p>
        </div>

        <div className="edit-footer-actions">
          <button
            className="btn-cancel-text"
            type="button"
            onClick={() => navigate('/dashboard')}
          >
            Назад
          </button>
          <button className="btn-save-main" type="submit" disabled={saving}>
            {saving ? 'Сохранение...' : 'Сохранить'}
          </button>
        </div>
      </form>
    </div>
  );
}
