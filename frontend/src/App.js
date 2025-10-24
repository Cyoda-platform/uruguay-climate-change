import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Predictions from './pages/Predictions';
import Statistics from './pages/Statistics';
import MachineLearning from './pages/MachineLearning';
import AIInsights from './pages/AIInsights';
import Alerts from './pages/Alerts';
import GeminiCyoda from './pages/GeminiCyoda';
import Tutorial from './components/Tutorial';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Tutorial />
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">🌍 Uruguay Climate Change</h1>
            <ul className="nav-links">
              <li>
                <Link to="/">Dashboard</Link>
              </li>
              <li>
                <Link to="/predictions">Predictions</Link>
              </li>
              <li>
                <Link to="/statistics">Statistics</Link>
              </li>
              <li>
                <Link to="/ml">AI Models</Link>
              </li>
              <li>
                <Link to="/insights">AI Insights</Link>
              </li>
              {/* <li>
                <Link to="/alerts">🚨 Alerts</Link>
              </li> */}
              <li>
                <Link to="/gemini-cyoda">🤖 Gemini</Link>
              </li>
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/statistics" element={<Statistics />} />
            <Route path="/ml" element={<MachineLearning />} />
            <Route path="/insights" element={<AIInsights />} />
            {/* <Route path="/alerts" element={<Alerts />} /> */}
            <Route path="/gemini-cyoda" element={<GeminiCyoda />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
