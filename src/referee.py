import google.generativeai as genai
import json
import re
from typing import Optional, Dict, Any
from .models import SteeringMode, RefereeDecision, PromptBuilder

class AIReferee:
    """The core AI referee that makes menu decisions"""
    
    def __init__(self, api_key: str):
        """Initialize the AI referee with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def make_decision(self, menu_text: str, mode: SteeringMode, budget_limit: Optional[float] = None) -> Dict[str, Any]:
        """Make a referee decision based on menu and steering mode"""
        
        # Build the system prompt
        system_prompt = PromptBuilder.build_system_prompt(mode, budget_limit)
        
        try:
            # Generate AI response
            full_prompt = f"{system_prompt}\n\nMENU:\n{menu_text}"
            response = self.model.generate_content(full_prompt)
            
            # Parse the JSON response
            return self._parse_response(response.text)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response and extract JSON"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            
            if json_match:
                result = json.loads(json_match.group())
                
                # Validate required fields
                required_fields = ['winner', 'health_score', 'taste_score', 'verdict', 'modification']
                if all(field in result for field in required_fields):
                    return result
                else:
                    return self._create_fallback_response(response_text)
            else:
                return self._create_fallback_response(response_text)
                
        except json.JSONDecodeError:
            return self._create_fallback_response(response_text)
    
    def _create_fallback_response(self, response_text: str) -> Dict[str, Any]:
        """Create a fallback response when JSON parsing fails"""
        return {
            "winner": "Unable to parse menu properly",
            "health_score": 5,
            "taste_score": 5,
            "verdict": "The AI had trouble parsing this menu format. Try listing items more clearly with names and descriptions.",
            "modification": "Format your menu with clear item names, prices (optional), and brief descriptions."
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response"""
        return {
            "winner": "Error occurred",
            "health_score": 0,
            "taste_score": 0,
            "verdict": f"API Error: {error_message}",
            "modification": "Please check your API key and internet connection, then try again."
        }

class DecisionAnalyzer:
    """Analyzes and validates referee decisions"""
    
    @staticmethod
    def validate_scores(decision: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clamp scores to 1-10 range"""
        decision['health_score'] = max(1, min(10, decision.get('health_score', 5)))
        decision['taste_score'] = max(1, min(10, decision.get('taste_score', 5)))
        return decision
    
    @staticmethod
    def calculate_mode_alignment(decision: Dict[str, Any], mode: SteeringMode) -> float:
        """Calculate how well the decision aligns with the steering mode"""
        health_score = decision['health_score']
        taste_score = decision['taste_score']
        
        if mode == SteeringMode.ZEN:
            # In Zen mode, we want high health scores
            return health_score / 10.0
        else:
            # In Gremlin mode, we want high taste scores
            return taste_score / 10.0
    
    @staticmethod
    def get_decision_quality(decision: Dict[str, Any]) -> str:
        """Assess the quality of the decision"""
        health_score = decision['health_score']
        taste_score = decision['taste_score']
        
        total_score = health_score + taste_score
        
        if total_score >= 16:
            return "Excellent choice! 🌟"
        elif total_score >= 12:
            return "Good balance ✅"
        elif total_score >= 8:
            return "Decent option 👍"
        else:
            return "Could be better 🤔"