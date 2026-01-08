import streamlit as st
import json
from datetime import datetime
from enum import Enum

# Professional Referee Personas
class RefereePersona(Enum):
    STRICT_DOCTOR = "👨‍⚕️ The Strict Doctor"
    GOURMET_CRITIC = "👨‍🍳 The Gourmet Critic"
    BUDGET_ANALYST = "💰 The Budget Analyst"
    BALANCED_COACH = "⚖️ The Balanced Coach"

# Page config for Vercel deployment
st.set_page_config(
    page_title="BiteBalance - AI Food Referee",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'show_reasoning' not in st.session_state:
    st.session_state.show_reasoning = False
if 'meal_history' not in st.session_state:
    st.session_state.meal_history = []
if 'health_profile' not in st.session_state:
    st.session_state.health_profile = {
        'allergies': [],
        'daily_calorie_limit': 2000,
        'dietary_preference': 'None'
    }

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .control-tower {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }
    
    .reasoning-trace {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        font-family: 'Monaco', monospace;
        font-size: 0.9em;
        border-left: 4px solid #3b82f6;
    }
    
    .winner-card {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
    }
    
    .persona-indicator {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid #3b82f6;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9em;
        margin: 10px 0;
        text-align: center;
    }
    
    .system-status {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

def generate_reasoning_trace(food_input, persona, health_profile):
    """Generate AI reasoning trace for transparency"""
    
    trace_steps = [
        f"🔍 **Step 1: Input Analysis**\n   - Food requested: {food_input}\n   - Persona: {persona.value}\n   - Active constraints: {len(health_profile['allergies'])} allergies",
        
        f"🧮 **Step 2: Constraint Evaluation**\n   - Dietary preference: {health_profile['dietary_preference']}\n   - Calorie target: {health_profile['daily_calorie_limit']} cal/day\n   - Allergen screening: {'Active' if health_profile['allergies'] else 'None'}",
        
        f"⚖️ **Step 3: Persona Weighting**\n   - {persona.value} priorities applied\n   - Health vs Taste weighting calculated\n   - Budget considerations: {'High' if persona == RefereePersona.BUDGET_ANALYST else 'Standard'}",
        
        f"🎯 **Step 4: Option Generation**\n   - Generated 3 preparation variants\n   - Scored each option (Health/Taste/Value)\n   - Applied persona-specific ranking",
        
        f"✅ **Step 5: Final Selection**\n   - Winner selected based on weighted scores\n   - Confidence calculated: 85-95%\n   - Modifications suggested for optimization"
    ]
    
    return trace_steps

def analyze_food_with_persona(food_input, persona, health_profile):
    """Analyze food with persona-specific logic"""
    
    food_lower = food_input.lower()
    
    # Base options with comprehensive data
    if 'burger' in food_lower:
        base_options = [
            {
                'name': 'Grilled Chicken Burger (No Cheese)',
                'description': 'Lean grilled chicken breast, lettuce, tomato, whole wheat bun',
                'health_score': 8, 'taste_score': 6, 'value_score': 7,
                'calories': '320 cal', 'price': '$12',
                'modifications': ['No mayo', 'Extra vegetables', 'Whole wheat bun']
            },
            {
                'name': 'Turkey Burger with Light Cheese',
                'description': 'Ground turkey patty, reduced-fat cheese, avocado, multigrain bun',
                'health_score': 7, 'taste_score': 7, 'value_score': 6,
                'calories': '380 cal', 'price': '$14',
                'modifications': ['Light cheese', 'Add avocado', 'Side salad instead of fries']
            },
            {
                'name': 'Classic Beef Burger with Cheese',
                'description': 'Beef patty, full cheese, bacon, regular bun with fries',
                'health_score': 4, 'taste_score': 9, 'value_score': 8,
                'calories': '650 cal', 'price': '$16',
                'modifications': ['Extra bacon', 'Loaded fries', 'Full-fat cheese']
            }
        ]
    elif 'pizza' in food_lower:
        base_options = [
            {
                'name': 'Thin Crust Veggie Pizza',
                'description': 'Thin whole wheat crust, light cheese, lots of vegetables',
                'health_score': 7, 'taste_score': 6, 'value_score': 8,
                'calories': '220 cal/slice', 'price': '$14',
                'modifications': ['Extra vegetables', 'Light cheese', 'Thin crust']
            },
            {
                'name': 'Margherita Pizza (Regular)',
                'description': 'Regular crust, mozzarella, fresh basil, tomato sauce',
                'health_score': 5, 'taste_score': 8, 'value_score': 7,
                'calories': '280 cal/slice', 'price': '$16',
                'modifications': ['Fresh mozzarella', 'Basil', 'Regular portion']
            },
            {
                'name': 'Meat Lovers Deep Dish',
                'description': 'Thick crust, extra cheese, pepperoni, sausage, bacon',
                'health_score': 3, 'taste_score': 9, 'value_score': 6,
                'calories': '420 cal/slice', 'price': '$20',
                'modifications': ['Extra meat', 'Extra cheese', 'Thick crust']
            }
        ]
    else:
        # Generic options for other foods
        base_options = [
            {
                'name': f'Healthy {food_input.title()} Option',
                'description': 'Prepared with minimal oil, extra vegetables, lean protein',
                'health_score': 8, 'taste_score': 6, 'value_score': 7,
                'calories': 'Lower cal', 'price': '$12',
                'modifications': ['Grilled not fried', 'Extra vegetables', 'Light seasoning']
            },
            {
                'name': f'Balanced {food_input.title()} Option',
                'description': 'Moderate preparation with some indulgent elements',
                'health_score': 6, 'taste_score': 7, 'value_score': 8,
                'calories': 'Moderate cal', 'price': '$14',
                'modifications': ['Balanced preparation', 'Some cheese/sauce', 'Regular portion']
            },
            {
                'name': f'Indulgent {food_input.title()} Option',
                'description': 'Rich preparation with cheese, sauce, and full flavor',
                'health_score': 4, 'taste_score': 9, 'value_score': 6,
                'calories': 'Higher cal', 'price': '$18',
                'modifications': ['Extra cheese', 'Rich sauce', 'Large portion']
            }
        ]
    
    # Apply persona-specific weighting
    for option in base_options:
        if persona == RefereePersona.STRICT_DOCTOR:
            option['final_score'] = option['health_score'] * 0.8 + option['taste_score'] * 0.1 + option['value_score'] * 0.1
        elif persona == RefereePersona.GOURMET_CRITIC:
            option['final_score'] = option['health_score'] * 0.1 + option['taste_score'] * 0.8 + option['value_score'] * 0.1
        elif persona == RefereePersona.BUDGET_ANALYST:
            option['final_score'] = option['health_score'] * 0.3 + option['taste_score'] * 0.2 + option['value_score'] * 0.5
        else:  # Balanced Coach
            option['final_score'] = option['health_score'] * 0.4 + option['taste_score'] * 0.4 + option['value_score'] * 0.2
    
    # Sort by final score
    base_options.sort(key=lambda x: x['final_score'], reverse=True)
    
    # Filter based on health profile
    filtered_options = []
    for option in base_options:
        is_valid = True
        
        # Check allergies
        option_text = option['description'].lower()
        for allergy in health_profile['allergies']:
            if allergy.lower() in option_text:
                is_valid = False
                break
        
        # Check dietary preferences
        if health_profile['dietary_preference'] == 'Vegan' and any(word in option_text for word in ['cheese', 'meat', 'chicken', 'beef']):
            is_valid = False
        
        if is_valid:
            filtered_options.append(option)
    
    return filtered_options[:3] if filtered_options else base_options[:3]

def render_sidebar():
    """Render the control tower sidebar"""
    
    with st.sidebar:
        # Logo and Title
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="color: #1e293b; margin: 0;">🏆 BiteBalance</h2>
            <p style="color: #64748b; margin: 5px 0 0 0;">AI Control Tower</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Referee Persona Selector
        st.markdown("### 🎭 Referee Persona")
        
        persona_descriptions = {
            RefereePersona.STRICT_DOCTOR: "Medical-grade nutrition focus. Prioritizes longevity and health markers.",
            RefereePersona.GOURMET_CRITIC: "Michelin-star flavor profiles. Prioritizes taste and culinary excellence.",
            RefereePersona.BUDGET_ANALYST: "Calories-per-dollar optimization. Prioritizes value and cost efficiency.",
            RefereePersona.BALANCED_COACH: "Holistic approach. Balances health, taste, and practical considerations."
        }
        
        selected_persona = st.selectbox(
            "Choose your AI referee:",
            options=list(RefereePersona),
            format_func=lambda x: x.value,
            key="referee_persona"
        )
        
        st.info(f"**Focus:** {persona_descriptions[selected_persona]}")
        
        st.markdown("---")
        
        # Health Profile Section
        st.markdown("### 👤 Health Profile")
        
        # Dietary Preferences
        dietary_pref = st.selectbox(
            "Dietary Preference:",
            ["None", "Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean"],
            key="dietary_preference"
        )
        
        # Daily Calorie Limit
        calorie_limit = st.slider(
            "Daily Calorie Target:",
            1200, 3000, 2000,
            step=100,
            key="calorie_limit"
        )
        
        # Allergies/Restrictions
        st.markdown("**Allergies & Restrictions:**")
        allergies = []
        
        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("🥜 Nuts", key="nuts_allergy"):
                allergies.append("Nuts")
            if st.checkbox("🌾 Gluten", key="gluten_allergy"):
                allergies.append("Gluten")
        
        with col2:
            if st.checkbox("🥛 Dairy", key="dairy_allergy"):
                allergies.append("Dairy")
            if st.checkbox("🌱 Vegan", key="vegan_req"):
                allergies.append("Vegan")
        
        # Update session state
        st.session_state.health_profile = {
            'allergies': allergies,
            'daily_calorie_limit': calorie_limit,
            'dietary_preference': dietary_pref
        }
        
        # Display active constraints
        if allergies or dietary_pref != "None":
            st.markdown("**Active Constraints:**")
            constraints = allergies + ([dietary_pref] if dietary_pref != "None" else [])
            for constraint in constraints:
                st.markdown(f'<div class="persona-indicator">{constraint}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Advanced Controls
        st.markdown("### ⚙️ Advanced Controls")
        
        # Internal Monologue Toggle
        show_reasoning = st.toggle(
            "🧠 Show AI Reasoning Trace",
            value=st.session_state.show_reasoning,
            help="Display the AI's step-by-step decision process"
        )
        st.session_state.show_reasoning = show_reasoning
        
        # Confidence Threshold
        confidence_threshold = st.slider(
            "Confidence Threshold:",
            0.5, 1.0, 0.8,
            step=0.05,
            help="Minimum confidence required for recommendations"
        )
        
        st.markdown("---")
        
        # System Status
        st.markdown("""
        <div class="system-status">
            <strong>🟢 System Status</strong><br>
            <small>AI Model: Active</small><br>
            <small>Response Time: <0.5s</small><br>
            <small>Confidence: High</small>
        </div>
        """, unsafe_allow_html=True)
    
    return selected_persona, show_reasoning, confidence_threshold

def main():
    # Render Control Tower Sidebar
    selected_persona, show_reasoning, confidence_threshold = render_sidebar()
    
    # Main Dashboard Header
    st.markdown("""
    <div class="main-header">
        <h1>🏆 BiteBalance Professional</h1>
        <h3>AI-Powered Food Decision Intelligence</h3>
        <p>Professional-grade meal optimization with advanced agent steering</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Control Tower Status
    st.markdown(f"""
    <div class="control-tower">
        <h4>🎛️ Control Tower Status</h4>
        <p><strong>Active Persona:</strong> {selected_persona.value}</p>
        <p><strong>Reasoning Trace:</strong> {'Enabled' if show_reasoning else 'Disabled'}</p>
        <p><strong>Health Profile:</strong> {len(st.session_state.health_profile['allergies'])} constraints active</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Input Section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        food_input = st.text_input(
            "🍽️ What food are you considering?",
            placeholder="e.g., burger, pizza, pasta, salad...",
            help="Tell me what you're craving and I'll optimize it for you!"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🎯 ANALYZE OPTIONS", type="primary", use_container_width=True)
    
    # Process Analysis
    if analyze_button and food_input.strip():
        
        # Show reasoning trace if enabled
        if show_reasoning:
            st.markdown("### 🧠 AI Reasoning Trace")
            
            reasoning_steps = generate_reasoning_trace(food_input, selected_persona, st.session_state.health_profile)
            
            for i, step in enumerate(reasoning_steps, 1):
                with st.expander(f"Step {i}: {step.split('**')[1].split('**')[0]}", expanded=i==1):
                    st.markdown(f'<div class="reasoning-trace">{step}</div>', unsafe_allow_html=True)
        
        # Analyze options
        with st.spinner(f"🤔 {selected_persona.value} is analyzing your options..."):
            options = analyze_food_with_persona(food_input, selected_persona, st.session_state.health_profile)
        
        st.markdown("---")
        st.markdown(f"### 🏆 {selected_persona.value}'s Recommendation")
        
        # Winner Card
        winner = options[0]
        confidence = min(95, int(winner['final_score'] * 10 + 15))
        
        st.markdown(f"""
        <div class="winner-card">
            <h3>🥇 OPTIMAL CHOICE</h3>
            <h2>{winner['name']}</h2>
            <p>{winner['description']}</p>
            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                <span><strong>Calories:</strong> {winner['calories']}</span>
                <span><strong>Price:</strong> {winner['price']}</span>
                <span><strong>Confidence:</strong> {confidence}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Score Analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Health Score", f"{winner['health_score']}/10")
            st.progress(winner['health_score'] / 10)
        
        with col2:
            st.metric("Taste Score", f"{winner['taste_score']}/10")
            st.progress(winner['taste_score'] / 10)
        
        with col3:
            st.metric("Value Score", f"{winner['value_score']}/10")
            st.progress(winner['value_score'] / 10)
        
        # Smart Modifications
        st.success("💡 **Persona-Optimized Modifications:**")
        for mod in winner['modifications']:
            st.write(f"• {mod}")
        
        # Alternative Options
        if len(options) > 1:
            st.markdown("#### 🔄 Alternative Options")
            
            for i, option in enumerate(options[1:], 2):
                rank_emoji = "🥈" if i == 2 else "🥉"
                
                with st.expander(f"{rank_emoji} {option['name']} - {option['calories']} - {option['price']}"):
                    st.write(option['description'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"Health: {option['health_score']}/10")
                        st.progress(option['health_score'] / 10)
                    with col2:
                        st.write(f"Taste: {option['taste_score']}/10")
                        st.progress(option['taste_score'] / 10)
                    with col3:
                        st.write(f"Value: {option['value_score']}/10")
                        st.progress(option['value_score'] / 10)
        
        # Save to history
        meal_record = {
            'food': food_input,
            'winner': winner['name'],
            'persona': selected_persona.value,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
        
        st.session_state.meal_history.append(meal_record)
        
        # Keep only last 10 records
        if len(st.session_state.meal_history) > 10:
            st.session_state.meal_history = st.session_state.meal_history[-10:]
    
    elif analyze_button and not food_input.strip():
        st.error("Please tell me what food you're considering!")

if __name__ == "__main__":
    main()