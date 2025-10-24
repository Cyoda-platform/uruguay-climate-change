"""Google Gemini AI integration for climate insights."""

import os
import json
from typing import Dict, List, Any
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeminiClimateAnalyst:
    """Generate AI-powered insights using Google Gemini."""

    def __init__(self, api_key: str = None):
        """
        Initialize Gemini AI client.

        Args:
            api_key: Google API key. If None, reads from GEMINI_API_KEY env var
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")

        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=self.api_key)
        # Use models/gemini-2.5-flash - the models/ prefix is required!
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    def generate_climate_summary(self, climate_data: Dict[str, Any]) -> str:
        """
        Generate a comprehensive climate summary.

        Args:
            climate_data: Dictionary with climate statistics

        Returns:
            AI-generated summary
        """
        prompt = f"""
        As a climate scientist, analyze the following climate data for Uruguay and provide a comprehensive summary:

        Data:
        {json.dumps(climate_data, indent=2)}

        Please provide:
        1. A clear overview of current climate conditions
        2. Key trends and patterns observed
        3. Notable changes compared to historical averages
        4. Potential implications for the region

        Keep the summary concise (3-4 paragraphs) and scientifically accurate.
        """

        response = self.model.generate_content(prompt)
        return response.text

    def generate_ml_insights(self, ml_results: Dict[str, Any]) -> str:
        """
        Generate insights from ML model predictions.

        Args:
            ml_results: Dictionary with ML prediction results

        Returns:
            AI-generated insights
        """
        prompt = f"""
        As a data scientist specializing in climate analysis, analyze these machine learning predictions:

        ML Results:
        {json.dumps(ml_results, indent=2)}

        Please provide:
        1. Interpretation of the forecast trends
        2. Confidence level assessment
        3. Key patterns identified by the models
        4. What these predictions mean for Uruguay's climate

        Be concise and actionable (2-3 paragraphs).
        """

        response = self.model.generate_content(prompt)
        return response.text

    def generate_anomaly_report(self, anomalies: List[Dict[str, Any]]) -> str:
        """
        Generate report on detected climate anomalies.

        Args:
            anomalies: List of detected anomalies

        Returns:
            AI-generated anomaly report
        """
        prompt = f"""
        As a climate analyst, review these detected climate anomalies for Uruguay:

        Anomalies Detected:
        {json.dumps(anomalies, indent=2)}

        Please provide:
        1. Severity assessment of these anomalies
        2. Possible causes or contributing factors
        3. Historical context (are these unprecedented?)
        4. Potential impacts on environment and agriculture

        Format as a brief report (3-4 paragraphs).
        """

        response = self.model.generate_content(prompt)
        return response.text

    def generate_recommendations(self, analysis_summary: Dict[str, Any]) -> str:
        """
        Generate actionable recommendations based on climate analysis.

        Args:
            analysis_summary: Comprehensive climate analysis data

        Returns:
            AI-generated recommendations
        """
        prompt = f"""
        Based on this climate analysis for Uruguay, provide actionable recommendations:

        Analysis:
        {json.dumps(analysis_summary, indent=2)}

        Please provide recommendations for:
        1. Government and policymakers
        2. Agricultural sector
        3. General public and communities
        4. Climate adaptation strategies

        Format as clear, actionable bullet points under each category.
        """

        response = self.model.generate_content(prompt)
        return response.text

    def generate_comparative_analysis(self, current_data: Dict, historical_data: Dict) -> str:
        """
        Compare current conditions with historical patterns.

        Args:
            current_data: Current climate metrics
            historical_data: Historical climate metrics

        Returns:
            AI-generated comparative analysis
        """
        prompt = f"""
        Compare current climate conditions with historical patterns for Uruguay:

        Current Conditions:
        {json.dumps(current_data, indent=2)}

        Historical Averages:
        {json.dumps(historical_data, indent=2)}

        Provide:
        1. Key differences between current and historical conditions
        2. Magnitude of changes (are they significant?)
        3. Trend direction (improving, worsening, stable)
        4. What this tells us about climate change in the region

        Be specific with numbers and trends (2-3 paragraphs).
        """

        response = self.model.generate_content(prompt)
        return response.text

    def generate_seasonal_forecast_narrative(self, seasonal_data: Dict[str, Any]) -> str:
        """
        Create narrative for seasonal forecasts.

        Args:
            seasonal_data: Seasonal prediction data

        Returns:
            AI-generated narrative
        """
        prompt = f"""
        Create an engaging narrative about the upcoming seasonal forecast for Uruguay:

        Seasonal Forecast:
        {json.dumps(seasonal_data, indent=2)}

        Write a narrative that:
        1. Explains what to expect in the coming months
        2. Highlights any unusual patterns or concerns
        3. Provides context for different sectors (agriculture, tourism, etc.)
        4. Offers practical advice based on the forecast

        Write in an accessible style for general audiences (2-3 paragraphs).
        """

        response = self.model.generate_content(prompt)
        return response.text

    def generate_executive_summary(self, full_analysis: Dict[str, Any]) -> str:
        """
        Generate executive summary of entire climate analysis.

        Args:
            full_analysis: Complete climate analysis results

        Returns:
            AI-generated executive summary
        """
        prompt = f"""
        Create an executive summary of this comprehensive climate analysis for Uruguay:

        Complete Analysis:
        {json.dumps(full_analysis, indent=2)}

        Provide a concise executive summary with:
        1. Key findings (top 3-5 bullet points)
        2. Critical concerns requiring immediate attention
        3. Positive trends or opportunities
        4. Overall climate outlook

        Target audience: Decision-makers and stakeholders. Keep it under 200 words.
        """

        response = self.model.generate_content(prompt)
        return response.text
