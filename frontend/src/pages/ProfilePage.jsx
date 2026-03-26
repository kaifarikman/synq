import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Input from '../components/Input';
import { useAuth } from '../hooks/useAuth';
import { profileAPI } from '../services/profileApi';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { logout } = useAuth();
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
    <div className="form-card">
      <h1 className="form-title">Мой профиль</h1>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="form-footer">{success}</div>}
      {profile && (
        <form onSubmit={handleSubmit}>
          <Input
            name="full_name"
            type="text"
            placeholder="Полное имя"
            value={form.full_name}
            onChange={handleChange}
          />
          <Input
            name="bio"
            type="text"
            placeholder="О себе"
            value={form.bio}
            onChange={handleChange}
          />
          <Input
            name="uuid"
            type="text"
            placeholder="UUID"
            value={profile.uuid}
            readOnly
          />
          <Button disabled={saving}>
            {saving ? 'Сохранение...' : 'Сохранить'}
          </Button>
        </form>
      )}
      <Button type="button" onClick={() => navigate('/dashboard')}>
        Назад
      </Button>
    </div>
  );
}
