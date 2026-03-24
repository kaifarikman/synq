export default function Button({ children, type = 'submit', onClick }) {
  return (
    <button
      type={type}
      onClick={onClick}
      className="btn-red"
    >
      {children}
    </button>
  );
}