export default function FormCard({ title, children, footer }) {
  return (
    <div className="form-card">
      <h1 className="form-title">{title}</h1>
      {children}
      {footer && <div className="form-footer">{footer}</div>}
    </div>
  );
}