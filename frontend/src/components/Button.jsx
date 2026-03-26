export default function Button({ children, type = 'submit', onClick, disabled = false }) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className="btn-red"
    >
      {children}
    </button>
  );
}
