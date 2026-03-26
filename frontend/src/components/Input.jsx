export default function Input({
  name,
  type,
  placeholder,
  required,
  style,
  maxLength,
  value,
  onChange,
  readOnly = false
}) {
  return (
    <input
      name={name}
      type={type}
      placeholder={placeholder}
      required={required}
      style={style}
      maxLength={maxLength}
      value={value}
      onChange={onChange}
      readOnly={readOnly}
      className="input-field"
    />
  );
}
