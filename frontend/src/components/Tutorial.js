import React, { useState, useEffect } from 'react';
import './Tutorial.css';

const Tutorial = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [hasSeenTutorial, setHasSeenTutorial] = useState(false);

  useEffect(() => {
    // Check if user has seen the tutorial before
    const seen = localStorage.getItem('hasSeenTutorial');
    if (!seen) {
      setTimeout(() => setIsVisible(true), 1000);
    } else {
      setHasSeenTutorial(true);
    }
  }, []);

  const steps = [
    {
      title: "Welcome to Uruguay Climate Change! 🌍",
      description: "Your comprehensive platform for climate data analysis and AI-powered insights.",
      icon: "👋",
      highlight: null
    },
    {
      title: "Interactive Learning Cards 📚",
      description: "Click on any card with emojis to expand and learn about climate data, AI methods, and why it all matters!",
      icon: "🎯",
      highlight: ".info-card"
    },
    {
      title: "Explore Climate Data 📊",
      description: "View historical temperature and precipitation trends through interactive charts. Hover over data points for details!",
      icon: "📈",
      highlight: ".chart-container"
    },
    {
      title: "AI-Powered Predictions 🔮",
      description: "Navigate to the Predictions page to see our machine learning models forecast future climate patterns.",
      icon: "🤖",
      highlight: null
    },
    {
      title: "Statistical Insights 📐",
      description: "Check the Statistics page for detailed metrics, trends, and key climate indicators.",
      icon: "📊",
      highlight: null
    },
    {
      title: "Machine Learning Models 🧠",
      description: "Explore our LSTM and Prophet models on the AI Models page to understand how we make predictions.",
      icon: "🔬",
      highlight: null
    },
    {
      title: "Gemini AI Insights ✨",
      description: "Get AI-generated analysis and recommendations from Google's Gemini on the AI Insights page.",
      icon: "💡",
      highlight: null
    },
    {
      title: "You're All Set! 🎉",
      description: "Start exploring climate data and making informed decisions. You can restart this tutorial anytime from the help button.",
      icon: "🚀",
      highlight: null
    }
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleClose();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleClose = () => {
    setIsVisible(false);
    localStorage.setItem('hasSeenTutorial', 'true');
    setHasSeenTutorial(true);
  };

  const handleSkip = () => {
    handleClose();
  };

  const restartTutorial = () => {
    setCurrentStep(0);
    setIsVisible(true);
  };

  if (!isVisible && hasSeenTutorial) {
    return (
      <button className="tutorial-restart-btn" onClick={restartTutorial} title="Restart Tutorial">
        ❓
      </button>
    );
  }

  if (!isVisible) return null;

  const step = steps[currentStep];

  return (
    <>
      <div className="tutorial-overlay" onClick={handleClose} />
      <div className="tutorial-modal">
        <button className="tutorial-close" onClick={handleClose}>×</button>
        
        <div className="tutorial-content">
          <div className="tutorial-icon">{step.icon}</div>
          <h2 className="tutorial-title">{step.title}</h2>
          <p className="tutorial-description">{step.description}</p>
          
          <div className="tutorial-progress">
            {steps.map((_, index) => (
              <div
                key={index}
                className={`progress-dot ${index === currentStep ? 'active' : ''} ${index < currentStep ? 'completed' : ''}`}
              />
            ))}
          </div>

          <div className="tutorial-actions">
            <button
              className="tutorial-btn secondary"
              onClick={handleSkip}
            >
              Skip Tutorial
            </button>
            
            <div className="tutorial-nav">
              {currentStep > 0 && (
                <button
                  className="tutorial-btn"
                  onClick={handlePrevious}
                >
                  ← Previous
                </button>
              )}
              
              <button
                className="tutorial-btn primary"
                onClick={handleNext}
              >
                {currentStep === steps.length - 1 ? "Get Started! 🚀" : "Next →"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Tutorial;

