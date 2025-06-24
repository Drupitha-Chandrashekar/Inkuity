import React from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <>
      <style>{`
        /* Container & form reset */
        body, html {
          margin: 0;
          padding: 0;
          background-color: #0a0f4c;
          font-family: 'Segoe UI', sans-serif;
          height: 100%;
        }
        .login-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #000000, #0a0f4c);
          position: relative;
          overflow: hidden;
        }
        .login-form {
          background: rgba(0, 0, 0, 0.7);
          padding: 2rem 2.5rem;
          border-radius: 12px;
          box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
          width: 100%;
          max-width: 400px;
          color: #eee;
          z-index: 2;
        }
        .login-form h2 {
          text-align: center;
          margin-bottom: 1.5rem;
          font-size: 2rem;
          background: linear-gradient(to right, #38bdf8, #9333ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          letter-spacing: 1px;
        }
        /* Input fields */
        .login-form input {
          width: 100%;
          padding: 0.8rem 1rem;
          margin-bottom: 1rem;
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 6px;
          color: #fff;
          font-size: 1rem;
        }
        .login-form input::placeholder {
          color: rgba(255, 255, 255, 0.6);
        }
        .login-form input:focus {
          outline: none;
          border-color: #38bdf8;
          box-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
          background: rgba(255, 255, 255, 0.15);
        }
        /* Submit button */
        .login-form button {
          width: 100%;
          padding: 0.8rem 1rem;
          background: linear-gradient(45deg, #3b82f6, #9333ea);
          border: none;
          border-radius: 8px;
          color: white;
          font-size: 1rem;
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
        }
        .login-form button:hover {
          transform: translateY(-2px);
          box-shadow: 0 0 15px rgba(147, 51, 234, 0.5);
        }

        /* Floating decorative squares (matching Signup) */
        .floating-square {
          position: absolute;
          width: 50px;
          height: 50px;
          background: rgba(59, 130, 246, 0.1);
          border: 1px solid #38bdf8;
          border-radius: 8px;
          animation: floatSquare 6s infinite ease-in-out;
          z-index: 1;
        }
        .square1 { top: 10%; left: 20%; animation-delay: 0s; }
        .square2 { top: 25%; left: 75%; animation-delay: 2s; }
        .square3 { top: 65%; left: 30%; animation-delay: 4s; }
        .square4 { top: 80%; left: 80%; animation-delay: 1s; }

        @keyframes floatSquare {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(15deg); }
        }
      `}</style>

      <div className="login-container">
        {/* Floating decorative squares */}
        <div className="floating-square square1" />
        <div className="floating-square square2" />
        <div className="floating-square square3" />
        <div className="floating-square square4" />

        <form onSubmit={handleLogin} className="login-form">
          <h2>Login</h2>
          <input type="email" placeholder="Email" required />
          <input type="password" placeholder="Password" required />
          <button type="submit">Login</button>
        </form>
      </div>
    </>
  );
}

export default Login;
