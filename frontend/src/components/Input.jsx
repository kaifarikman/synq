export default function Input({ name, type, placeholder, required, style, maxLength }) {
  return (
    <input
      name={name}
      type={type}
      placeholder={placeholder}
      required={required}
      style={style}
      maxLength={maxLength}
      className="input-field"
    />
  );
}