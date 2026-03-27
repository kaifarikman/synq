const ProfilePage = ({ onSave, onCancel }) => {
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
            <div className="input-group-row"><label>Имя:</label><input type="text" placeholder="Данные" className="blue-input" /></div>
            <div className="input-group-row"><label>Номер телефона:</label><input type="text" placeholder="Данные" className="blue-input" /></div>
            <div className="input-group-row"><label>Фамилия:</label><input type="text" placeholder="Данные" className="blue-input" /></div>
            <div className="input-group-row"><label>Почта:</label><input type="email" placeholder="Данные" className="blue-input" /></div>
            <div className="input-group-row"><label>Отчество:</label><input type="text" placeholder="Данные" className="blue-input" /></div>
            <div className="input-group-row"><label>Ник в Telegram:</label><input type="text" placeholder="Данные" className="blue-input" /></div>
          </div>
        </div>

        <hr className="edit-divider" />

        <div className="additional-info-section">
          <h3 className="section-title">Дополнительная информация</h3>
          <div className="full-width-field">
            <label>Место работы:</label>
            <input type="text" className="standard-input" />
          </div>
          <div className="full-width-field">
            <label>О себе:</label>
            <textarea rows="2" className="standard-input"></textarea>
          </div>
          <div className="resume-row">
            <label>Резюме:</label>
            <button className="btn-upload-light">Загрузить</button>
          </div>
        </div>

        <div className="edit-footer-actions">
          <button className="btn-cancel-text" onClick={onCancel}>Отмена</button>
          <button className="btn-save-main" onClick={onSave}>Сохранить</button>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;