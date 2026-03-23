import { Link } from 'react-router-dom';
import FormCard from '../components/FormCard';
import Input from '../components/Input';
import Button from '../components/Button';

export default function VerifyPage() {
  return (
    <FormCard
      title="Подтверждение"
      footer={<Link to="/verify">Отправить еще раз</Link>}
    >
      <form onSubmit={(e) => e.preventDefault()}>
        <Input
          type="text"
          placeholder="000000"
          required
          maxLength="6"
          style={{ textAlign: 'center', fontSize: '1.5rem', letterSpacing: '10px' }}
        />
        <Button>Подтвердить</Button>
      </form>
    </FormCard>
  );
}