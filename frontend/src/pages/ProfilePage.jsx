import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Input from '../components/Input';
import { useAuth } from '../hooks/useAuth';
import { profileAPI } from '../services/profileApi';
import './ProfilePage.css';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState(null);
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
        setProfile(response.data);
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
      setProfile(response.data);
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
    return <div>Загрузка профиля...</div>;
  }

  return (
    <div className="profile-edit-container">
      <div className="glass-card edit-card">
        <div className="edit-header">
          <div className="avatar-upload-section">
            <div className="avatar-circle-large">
              <span>Фото профиля</span>
            </div>
          </div>

          <div className="main-info-grid">
            <div className="input-group-row">
              <label>Имя:</label>
              <input
                name="full_name"
                type="text"
                placeholder="Данные"
                className="blue-input"
                value={form.full_name}
                onChange={handleChange}
              />
            </div>
            <div className="input-group-row">
              <label>Почта:</label>
              <input
                type="email"
                placeholder="Данные"
                className="blue-input"
                value={user?.email || ''}
                readOnly
              />
            </div>
            <div className="input-group-row">
              <label>UUID:</label>
              <input
                type="text"
                placeholder="UUID"
                className="blue-input"
                value={profile?.uuid || ''}
                readOnly
              />
            </div>
            <div className="input-group-row">
              <label>User ID:</label>
              <input
                type="text"
                placeholder="ID"
                className="blue-input"
                value={String(profile?.user_id || '')}
                readOnly
              />
            </div>
          </div>
        </div>

        <hr className="edit-divider" />

        <form onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}
          {success && <div className="form-footer">{success}</div>}

          <div className="additional-info-section">
            <h3 className="section-title">Дополнительная информация</h3>
            <div className="full-width-field">
              <label>О себе:</label>
              <textarea
                name="bio"
                rows="4"
                className="standard-input"
                value={form.bio}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="edit-footer-actions">
            <button
              type="button"
              className="btn-cancel-text"
              onClick={() => navigate('/dashboard')}
            >
              Отмена
            </button>
            <button type="submit" className="btn-save-main" disabled={saving}>
              {saving ? 'Сохранение...' : 'Сохранить'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
