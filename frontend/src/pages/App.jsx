import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './Landing';
import Login from './Login';
import Signup from './Signup';
import Dashboard from './Dashboard';
import SketchToImage from './SketchToImage';
import ArtTheftDetection from './ArtTheftDetection';

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
