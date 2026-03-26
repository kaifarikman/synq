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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

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

      setError(response.detail || 'Не удалось загрузить профиль');
      setLoading(false);
    }

    loadProfile();

    return () => {
      active = false;
    };
  }, [logout, navigate]);

  if (loading) {
    return <div>Загрузка профиля...</div>;
  }

  return (
    <div className="form-card">
      <h1 className="form-title">Мой профиль</h1>
      {error && <div className="error-message">{error}</div>}
      {profile && (
        <form>
          <Input
            name="full_name"
            type="text"
            placeholder="Полное имя"
            value={profile.full_name || ''}
            readOnly
          />
          <Input
            name="bio"
            type="text"
            placeholder="О себе"
            value={profile.bio || ''}
            readOnly
          />
          <Input
            name="uuid"
            type="text"
            placeholder="UUID"
            value={profile.uuid}
            readOnly
          />
        </form>
      )}
      <Button type="button" onClick={() => navigate('/dashboard')}>
        Назад
      </Button>
    </div>
  );
}
