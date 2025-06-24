// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import SketchToImage from './pages/SketchToImage';
import ArtTheftDetection from './pages/ArtTheftDetection';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/sketch-to-image" element={<SketchToImage />} />
        <Route path="/art-theft-detection" element={<ArtTheftDetection />} />
      </Routes>
    </Router>
  );
}

export default App;
