import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import os
from dotenv import load_dotenv
from src.models import SteeringMode, AllergyFilter, AllergyChecker
from src.executive_dashboard import ExecutiveDashboard
from src.decision_engine import DecisionIntelligenceEngine

# Load environment variables
load_dotenv()

# Page config for Executive Dashboard
st.set_page_config(
    page_title="BiteBalance - Decision Intelligence Dashboard",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FreeAIReferee:
    """Free AI referee using intelligent mock analysis with parallel universe"""
    
    def __init__(self):
        self.use_mock = True  # Always use mock for free version
    
    def make_decision(self, menu_text, steering_mode, budget_limit=None, allergy_filters=None):
        """Make referee decision with parallel universe analysis"""
        return self._get_enhanced_mock_decision(menu_text, steering_mode, budget_limit, allergy_filters or [])
    
    def _get_enhanced_mock_decision(self, menu_text, steering_mode, budget_limit, allergy_filters):
        """Generate enhanced mock decisions with parallel universe and safety vetoes"""
        
        # Parse menu items
        items = [line.strip() for line in menu_text.split('\n') if line.strip()]
        
        if not items:
            return {
                "winner": "No menu items found",
                "health_score": 5,
                "taste_score": 5,
                "verdict": "Please paste a menu with clear item listings.",
                "modification": "Try formatting like: '1. Dish Name - $Price - Description'",
                "parallel_choice": "",
                "parallel_explanation": "",
                "vetoed_items": []
            }
        
        # Apply allergy filters first (Hard Vetoes)
        safe_items = AllergyChecker.get_safe_items(items, allergy_filters)
        vetoed_items = [item for item in items if item not in safe_items]
        
        if not safe_items:
            return {
                "winner": "No safe options available",
                "health_score": 1,
                "taste_score": 1,
                "verdict": "All menu items were vetoed due to your safety constraints.",
                "modification": "Consider adjusting your allergy filters or finding a different menu.",
                "parallel_choice": "Same result in both modes",
                "parallel_explanation": "Safety constraints override all preferences.",
                "vetoed_items": [self._clean_item_name(item) for item in vetoed_items]
            }
        
        # Analyze safe items for both modes
        zen_choice, zen_scores = self._analyze_items(safe_items, SteeringMode.ZEN)
        gremlin_choice, gremlin_scores = self._analyze_items(safe_items, SteeringMode.GREMLIN)
        
        # Current mode choice
        if steering_mode == SteeringMode.ZEN:
            winner = zen_choice
            winner_scores = zen_scores
            parallel_choice = gremlin_choice
            parallel_mode = "Gremlin"
        else:
            winner = gremlin_choice
            winner_scores = gremlin_scores
            parallel_choice = zen_choice
            parallel_mode = "Zen"
        
        # Generate personality-appropriate responses
        verdict, modification, parallel_explanation = self._generate_responses(
            winner, parallel_choice, steering_mode, allergy_filters, vetoed_items
        )
        
        return {
            "winner": self._clean_item_name(winner),
            "health_score": winner_scores['health'],
            "taste_score": winner_scores['taste'],
            "verdict": verdict,
            "modification": modification,
            "parallel_choice": self._clean_item_name(parallel_choice),
            "parallel_explanation": parallel_explanation,
            "vetoed_items": [self._clean_item_name(item) for item in vetoed_items]
        }
    
    def _analyze_items(self, items, mode):
        """Analyze items and return best choice for given mode"""
        health_keywords = ['salad', 'grilled', 'steamed', 'quinoa', 'salmon', 'chicken breast', 'vegetables', 'fruit', 'lean']
        taste_keywords = ['burger', 'pizza', 'chocolate', 'cheese', 'bacon', 'fried', 'cake', 'ice cream', 'sauce', 'crispy']
        
        best_item = items[0]
        best_score = 0
        best_scores = {'health': 5, 'taste': 5}
        
        for item in items:
            item_lower = item.lower()
            health_score = min(10, max(1, sum(2 for keyword in health_keywords if keyword in item_lower) + 3))
            taste_score = min(10, max(1, sum(2 for keyword in taste_keywords if keyword in item_lower) + 3))
            
            # Apply mode weights
            if mode == SteeringMode.ZEN:
                final_score = (health_score * 0.8) + (taste_score * 0.2)
            else:
                final_score = (health_score * 0.1) + (taste_score * 0.9)
            
            if final_score > best_score:
                best_score = final_score
                best_item = item
                best_scores = {'health': health_score, 'taste': taste_score}
        
        return best_item, best_scores
    
    def _generate_responses(self, winner, parallel_choice, mode, allergy_filters, vetoed_items):
        """Generate personality-appropriate responses"""
        winner_clean = self._clean_item_name(winner)
        parallel_clean = self._clean_item_name(parallel_choice)
        
        # Veto explanation
        veto_text = ""
        if vetoed_items:
            filter_names = [f.value.split()[1] for f in allergy_filters]  # Extract just the constraint name
            veto_text = f" I had to veto {len(vetoed_items)} items due to your {', '.join(filter_names)} constraints."
        
        if mode == SteeringMode.ZEN:
            verdict = f"Selected {winner_clean} for optimal nutrient density and clean preparation methods. I rejected {parallel_clean} as it prioritizes indulgence over health goals.{veto_text} This choice aligns with longevity and metabolic efficiency."
            
            modification = "Request preparation without added oils, ask for extra vegetables, and consider a side of leafy greens for enhanced micronutrient profile."
            
            parallel_explanation = f"In Gremlin mode, I would prioritize sensory satisfaction and comfort food appeal over nutritional optimization."
            
        else:  # Gremlin mode
            verdict = f"Chose {winner_clean} because life demands maximum flavor satisfaction! I rejected {parallel_clean} - too virtuous for a proper cheat day.{veto_text} This choice delivers the dopamine hit you're craving."
            
            modification = "Add extra cheese, request crispy preparation, and don't forget an indulgent side that makes your taste buds sing!"
            
            parallel_explanation = f"In Zen mode, I would focus on boring nutritional metrics instead of pure deliciousness."
        
        return verdict, modification, parallel_explanation
    
    def _clean_item_name(self, item):
        """Clean up item name for display"""
        if not item:
            return "Unknown item"
        
        # Remove numbering
        clean = item.split('-')[0].strip()
        if clean and clean[0].isdigit() and '.' in clean[:5]:
            clean = clean.split('.', 1)[1].strip()
        
        return clean or item

def validate_scores(decision):
    """Validate and clamp scores"""
    decision['health_score'] = max(1, min(10, decision.get('health_score', 5)))
    decision['taste_score'] = max(1, min(10, decision.get('taste_score', 5)))
    return decision

def get_decision_quality(decision):
    """Assess decision quality"""
    total_score = decision['health_score'] + decision['taste_score']
    if total_score >= 16:
        return "Excellent choice! 🌟"
    elif total_score >= 12:
        return "Good balance ✅"
    elif total_score >= 8:
        return "Decent option 👍"
    else:
        return "Could be better 🤔"

# Main App
def main():
    # Apply custom CSS
    UIComponents.render_custom_css()
    
    # Initialize Free AI Referee (no API key needed!)
    referee = FreeAIReferee()
    
    # Header
    UIComponents.render_header()
    
    # Add National Stage notice
    st.success("🏆 **NATIONAL STAGE VERSION** - Now with Parallel Universe Analysis & Safety Constraints!")
    
    # Steering Mode Selector
    steering_mode = UIComponents.render_mode_selector()
    st.markdown("---")
    
    # Hard Veto Filters (NEW!)
    allergy_filters = UIComponents.render_allergy_filters()
    st.markdown("---")
    
    # Budget Selector
    budget_limit = UIComponents.render_budget_selector()
    st.markdown("---")
    
    # Menu Input
    menu_text = UIComponents.render_menu_input()
    
    # Referee Button
    referee_button = UIComponents.render_referee_button()
    
    # Process Decision
    if referee_button and menu_text.strip():
        with st.spinner("🤔 Analyzing trade-offs across parallel universes..."):
            decision = referee.make_decision(menu_text, steering_mode, budget_limit, allergy_filters)
            decision = validate_scores(decision)
        
        # Render Results with Parallel Universe
        UIComponents.render_decision_results(decision, steering_mode)
        
        # Show decision quality
        quality = get_decision_quality(decision)
        st.markdown(f"**Decision Quality:** {quality}")
        
        # Show constraint summary
        if allergy_filters or decision.get('vetoed_items'):
            st.markdown("#### 🛡️ Safety Summary")
            if decision.get('vetoed_items'):
                st.warning(f"Vetoed {len(decision['vetoed_items'])} items for safety")
            if allergy_filters:
                st.info(f"Applied {len(allergy_filters)} safety constraints")
        
    elif referee_button and not menu_text.strip():
        st.error("Please paste a menu or grocery list first!")

if __name__ == "__main__":
    main()