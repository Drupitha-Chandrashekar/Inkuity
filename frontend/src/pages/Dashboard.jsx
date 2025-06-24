import React from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  return (
    <>
      <style>{`
        .dashboard-container {
          min-height: 100vh;
          padding: 2rem 1.5rem;
          background: linear-gradient(135deg, #000000, #0a0f4c);
          color: #e0e7ff;
          font-family: 'Segoe UI', sans-serif;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          position: relative;
          overflow: hidden;
          text-align: center;
        }
        .welcome-text {
          font-size: 1.9rem;
          max-width: 700px;
          margin-bottom: 3rem;
          line-height: 1.4;
          font-weight: 600;
          background: linear-gradient(90deg, #38bdf8, #8b5cf6);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          filter: drop-shadow(0 0 6px #38bdf8cc);
        }
        .btn-container {
          display: flex;
          gap: 2.5rem;
          flex-wrap: wrap;
          justify-content: center;
          width: 100%;
          max-width: 600px;
        }
        .btn {
          background: linear-gradient(45deg, #3b82f6, #9333ea);
          color: white;
          font-size: 1.3rem;
          font-weight: 700;
          padding: 1rem 2.5rem;
          border: none;
          border-radius: 12px;
          cursor: pointer;
          position: relative;
          overflow: hidden;
          box-shadow: 0 0 15px #9333ea88;
          transition: box-shadow 0.3s ease, transform 0.3s ease;
          flex: 1 1 250px;
          max-width: 280px;
        }
        .btn:focus {
          outline: none;
          box-shadow: 0 0 25px #3b82f6aa;
        }
        .btn:hover {
          transform: scale(1.1);
          box-shadow:
            0 0 15px #9333ea,
            0 0 25px #3b82f6,
            0 0 40px #9333ea,
            0 0 60px #3b82f6;
        }
        .btn .glow-effect {
          position: absolute;
          top: -25%;
          left: -25%;
          width: 150%;
          height: 150%;
          pointer-events: none;
          background: radial-gradient(circle at center, rgba(255,255,255,0.15) 0%, transparent 70%);
          opacity: 0;
          transition: opacity 0.4s ease;
          animation: pulseGlow 3s infinite ease-in-out;
          border-radius: 12px;
          filter: drop-shadow(0 0 10px #7c3aed88);
          mix-blend-mode: screen;
          z-index: 0;
        }
        .btn:hover .glow-effect {
          opacity: 1;
        }
        @keyframes pulseGlow {
          0%, 100% {
            transform: scale(1);
            opacity: 0.2;
          }
          50% {
            transform: scale(1.15);
            opacity: 0.5;
          }
        }
        .floating-circle {
          position: absolute;
          border-radius: 50%;
          background: rgba(147, 51, 234, 0.2);
          box-shadow: 0 0 15px #9333ea66;
          animation: floatUpDown 6s ease-in-out infinite;
          filter: blur(2px);
          z-index: 1;
        }
        .circle1 {
          width: 120px;
          height: 120px;
          bottom: 15%;
          left: 10%;
          animation-delay: 0s;
        }
        .circle2 {
          width: 180px;
          height: 180px;
          top: 25%;
          right: 15%;
          animation-delay: 3s;
        }
        @keyframes floatUpDown {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-30px); }
        }
        .floating-square {
          position: absolute;
          width: 40px;
          height: 40px;
          background: rgba(59, 130, 246, 0.15);
          border: 1px solid #38bdf8;
          border-radius: 8px;
          animation: floatSquare 6s infinite ease-in-out;
          z-index: 1;
        }
        .square1 { top: 10%; left: 20%; animation-delay: 0s; }
        .square2 { top: 60%; left: 75%; animation-delay: 2s; }
        .square3 { top: 70%; left: 30%; animation-delay: 4s; }
        .square4 { top: 85%; left: 80%; animation-delay: 1s; }
        @keyframes floatSquare {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-15px) rotate(15deg); }
        }
      `}</style>

      <div className="dashboard-container">
        {/* Floating decorative elements */}
        <div className="floating-circle circle1" />
        <div className="floating-circle circle2" />
        <div className="floating-square square1" />
        <div className="floating-square square2" />
        <div className="floating-square square3" />
        <div className="floating-square square4" />

        {/* Welcome message with emojis */}
        <p className="welcome-text">
          Try out your first <strong>🤖 AI-powered image generation 🎨</strong> or instantly <strong>🛡️ detect art theft 🔍</strong> with cutting-edge technology!
        </p>

        {/* Buttons with emojis */}
        <div className="btn-container">
          <button onClick={() => navigate('/sketch-to-image')} className="btn">
            🖌️ Generate Image
            <span className="glow-effect" />
          </button>
          <button onClick={() => navigate('/art-theft-detection')} className="btn">
            🔒 Detect Art Theft
            <span className="glow-effect" />
          </button>
        </div>
      </div>
    </>
  );
}

export default Dashboard;
