import React from 'react';
import { Link } from 'react-router-dom';

function Landing() {
  return (
    <>
      <style>{`
        body, html {
          margin: 0;
          padding: 0;
          font-family: 'Segoe UI', sans-serif;
          background-color: black;
        }

        html {
          scroll-behavior: smooth;
        }

        .landing-container {
          height: 100vh;
          width: 100%;
          overflow: hidden;
          scroll-behavior: smooth;
          position: relative;
        }

        .animated-bg {
          background: linear-gradient(135deg, #000000, #0a0f4c);
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
        }

        .animated-bg::before {
          content: '';
          position: absolute;
          width: 100%;
          height: 100%;
          background-image:
            radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px);
          background-size: 50px 50px;
          animation: moveGrid 40s linear infinite;
          z-index: 1;
          opacity: 0.4;
        }

        @keyframes moveGrid {
          0% {
            background-position: 0 0, 0 0, 0 0;
          }
          100% {
            background-position: 100px 100px, 100px 0, 0 100px;
          }
        }
          

        .floating-emoji {
          position: absolute;
          font-size: 2rem;
          opacity: 0.6;
          animation: floatEmoji 5s ease-in-out infinite;
        }

        .emoji1 { top: 10%; left: 15%; animation-delay: 0s; }
        .emoji2 { top: 20%; left: 80%; animation-delay: 1s; }
        .emoji3 { top: 75%; left: 10%; animation-delay: 2s; }
        .emoji4 { top: 85%; left: 70%; animation-delay: 3s; }
        .emoji5 { top: 50%; left: 90%; animation-delay: 4s; }
        .emoji6 { top: 30%; left: 40%; animation-delay: 2.5s; }

        @keyframes floatEmoji {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-15px); }
        }

        .landing-content {
          z-index: 2;
          text-align: center;
          padding: 2rem;
          max-width: 800px;
        }

      .landing-content h1 {
  font-size: 3rem;
  font-weight: 900;
  letter-spacing: 1.5px;
  background: linear-gradient(90deg, #00f0ff, #7f00ff, #00f0ff);
  background-size: 200% auto;
  color: transparent;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shineText 5s linear infinite, pulseGlow 2.5s ease-in-out infinite;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.2), 0 0 20px rgba(128, 0, 255, 0.4);
}

@keyframes shineText {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}

@keyframes pulseGlow {
  0%, 100% {
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.2), 0 0 20px rgba(128, 0, 255, 0.4);
  }
  50% {
    text-shadow: 0 0 25px rgba(0, 255, 255, 0.4), 0 0 40px rgba(128, 0, 255, 0.6);
  }
}


        .subheading {
          font-size: 1.3rem;
          color: #4ade80;
          margin-bottom: 1rem;
          font-weight: 600;
        }

        .description {
          font-size: 1.1rem;
          color: #cbd5e1;
          margin-bottom: 3rem;
          line-height: 1.7;
        }

        .landing-buttons {
          display: flex;
          gap: 1rem;
          justify-content: center;
          flex-wrap: wrap;
        }

        .btn {
          padding: 0.8rem 1.5rem;
          font-size: 1rem;
          border: none;
          border-radius: 8px;
          background: linear-gradient(45deg, #3b82f6, #9333ea);
          color: white;
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 0 15px rgba(147, 51, 234, 0.5);
        }
      `}</style>

      <div className="landing-container">
        <div className="animated-bg">
          {/* Floating Emojis for AI, Pencil, Brush, Art Theme */}
          <div className="floating-emoji emoji1">🤖</div>
          <div className="floating-emoji emoji2">✏️</div>
          <div className="floating-emoji emoji3">🎨</div>
          <div className="floating-emoji emoji4">🧠</div>
          <div className="floating-emoji emoji5">🖌️</div>
          <div className="floating-emoji emoji6">🖼️</div>

          <div className="landing-content">
            <h1>Welcome to Doodle-to-Realistic Image Generator and Art Theft Detection App</h1>
            <div className="subheading">🎨 Sketch ✏️ → Reality 🌆 | 🛡️ Shield Your Art</div>

            <p className="description">
              Step into the world of Artificial Intelligence-powered creativity.<br />
              Upload your rough sketches and watch them transform into high-definition art using state-of-the-art AI models.<br />
              Safeguard your artistic vision from unauthorized use with smart theft detection.
            </p>

            <div className="landing-buttons">
              <Link to="/signup"><button className="btn">Sign Up</button></Link>
              <Link to="/login"><button className="btn">Log In</button></Link>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Landing;
