import streamlit as st
import re
from enum import Enum

# Simple enums for the app
class SteeringMode(Enum):
    ZEN = "Zen Mode"
    GREMLIN = "Gremlin Mode"

class AllergyFilter(Enum):
    NUTS = "🥜 No Nuts"
    GLUTEN = "🌾 Gluten-Free"
    DAIRY = "🥛 Dairy-Free"
    VEGAN = "🌱 Vegan"

# Page config
st.set_page_config(
    page_title="🥗 BiteBalance - The AI Menu Referee",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(90deg, #10B981 0%, #F97316 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    
    .zen-mode {
        background-color: #10B981;
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
    
    .gremlin-mode {
        background-color: #F97316;
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
    
    .winner-card {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .score-bar {
        background-color: #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
        height: 20px;
    }
    
    .health-fill {
        background-color: #10B981;
        height: 20px;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .taste-fill {
        background-color: #F97316;
        height: 20px;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

def analyze_menu_simple(menu_text, steering_mode, allergy_filters):
    """Simple menu analysis without external dependencies"""
    
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
    
    # Filter out items based on allergies
    safe_items = []
    vetoed_items = []
    
    allergy_keywords = {
        AllergyFilter.NUTS: ['nut', 'almond', 'peanut', 'walnut', 'pecan'],
        AllergyFilter.GLUTEN: ['wheat', 'bread', 'pasta', 'flour', 'gluten', 'bun'],
        AllergyFilter.DAIRY: ['milk', 'cheese', 'butter', 'cream', 'yogurt'],
        AllergyFilter.VEGAN: ['meat', 'chicken', 'beef', 'pork', 'fish', 'salmon']
    }
    
    for item in items:
        is_safe = True
        for allergy in allergy_filters:
            keywords = allergy_keywords.get(allergy, [])
            if any(keyword in item.lower() for keyword in keywords):
                is_safe = False
                vetoed_items.append(clean_item_name(item))
                break
        
        if is_safe:
            safe_items.append(item)
    
    if not safe_items:
        return {
            "winner": "No safe options available",
            "health_score": 1,
            "taste_score": 1,
            "verdict": "All menu items were vetoed due to your safety constraints.",
            "modification": "Consider adjusting your allergy filters.",
            "parallel_choice": "Same result in both modes",
            "parallel_explanation": "Safety constraints override all preferences.",
            "vetoed_items": vetoed_items
        }
    
    # Simple scoring
    health_keywords = ['salad', 'grilled', 'steamed', 'quinoa', 'salmon', 'vegetables', 'fruit', 'lean']
    taste_keywords = ['burger', 'pizza', 'chocolate', 'cheese', 'bacon', 'fried', 'cake', 'sauce', 'crispy']
    
    best_item = safe_items[0]
    best_score = 0
    
    for item in safe_items:
        item_lower = item.lower()
        health_score = min(10, max(1, sum(2 for kw in health_keywords if kw in item_lower) + 3))
        taste_score = min(10, max(1, sum(2 for kw in taste_keywords if kw in item_lower) + 3))
        
        # Apply steering mode weights
        if steering_mode == SteeringMode.ZEN:
            final_score = (health_score * 0.8) + (taste_score * 0.2)
        else:
            final_score = (health_score * 0.1) + (taste_score * 0.9)
        
        if final_score > best_score:
            best_score = final_score
            best_item = item
    
    # Find parallel choice (opposite mode)
    parallel_item = safe_items[0]
    parallel_score = 0
    
    for item in safe_items:
        item_lower = item.lower()
        health_score = min(10, max(1, sum(2 for kw in health_keywords if kw in item_lower) + 3))
        taste_score = min(10, max(1, sum(2 for kw in taste_keywords if kw in item_lower) + 3))
        
        # Opposite mode weights
        if steering_mode == SteeringMode.ZEN:
            final_score = (health_score * 0.1) + (taste_score * 0.9)  # Gremlin weights
        else:
            final_score = (health_score * 0.8) + (taste_score * 0.2)  # Zen weights
        
        if final_score > parallel_score:
            parallel_score = final_score
            parallel_item = item
    
    winner_name = clean_item_name(best_item)
    parallel_name = clean_item_name(parallel_item)
    
    # Calculate final scores for display
    winner_lower = best_item.lower()
    final_health = min(10, max(1, sum(2 for kw in health_keywords if kw in winner_lower) + 3))
    final_taste = min(10, max(1, sum(2 for kw in taste_keywords if kw in winner_lower) + 3))
    
    # Generate responses based on mode
    if steering_mode == SteeringMode.ZEN:
        verdict = f"Selected {winner_name} for optimal nutritional value and clean preparation. I rejected {parallel_name} as it prioritizes indulgence over health goals."
        modification = "Ask for extra vegetables and request preparation without added oils for maximum nutritional benefit."
        parallel_explanation = f"In Gremlin mode, I would choose {parallel_name} for maximum flavor satisfaction over nutritional concerns."
    else:
        verdict = f"Chose {winner_name} for maximum flavor satisfaction and indulgence! I rejected {parallel_name} as too health-focused for a proper cheat day."
        modification = "Add extra cheese or sauce, and don't forget an indulgent side that maximizes your taste experience!"
        parallel_explanation = f"In Zen mode, I would choose {parallel_name} for nutritional optimization over pure taste pleasure."
    
    if vetoed_items:
        verdict += f" I also vetoed {len(vetoed_items)} items due to your safety constraints."
    
    return {
        "winner": winner_name,
        "health_score": final_health,
        "taste_score": final_taste,
        "verdict": verdict,
        "modification": modification,
        "parallel_choice": parallel_name,
        "parallel_explanation": parallel_explanation,
        "vetoed_items": vetoed_items
    }

def clean_item_name(item):
    """Clean up item name for display"""
    clean = item.split('-')[0].strip()
    if clean and clean[0].isdigit() and '.' in clean[:5]:
        clean = clean.split('.', 1)[1].strip()
    return clean or item

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🥗 BiteBalance</h1>
        <h3>The AI Menu Referee</h3>
        <p><em>Arbitrating the conflict between health goals and flavor cravings</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("🆓 **Free Version** - Using intelligent mock AI for instant results! No API key required.")
    
    # Steering Mode Selector
    st.markdown("### 🎯 Mode Master")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        mode_value = st.select_slider(
            "Choose your referee mode:",
            options=["Zen Mode", "Gremlin Mode"],
            value="Zen Mode",
            format_func=lambda x: f"🧘‍♂️ {x}" if x == "Zen Mode" else f"😈 {x}"
        )
    
    steering_mode = SteeringMode.ZEN if mode_value == "Zen Mode" else SteeringMode.GREMLIN
    
    # Context Indicator
    if steering_mode == SteeringMode.ZEN:
        st.markdown("""
        <div class="zen-mode">
            🧘‍♂️ <strong>Pure Discipline Mode</strong><br>
            <em>Referee is prioritizing Longevity & Macros</em>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="gremlin-mode">
            😈 <strong>Full Cheat Day Mode</strong><br>
            <em>Referee is prioritizing Umami & Dopamine</em>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Allergy Filters
    st.markdown("### 🛡️ Hard Veto Filters (Safety Constraints)")
    st.markdown("*These are absolute constraints - the referee will veto any dish that violates them*")
    
    col1, col2, col3, col4 = st.columns(4)
    active_filters = []
    
    with col1:
        if st.checkbox("🥜 No Nuts", key="nuts_filter"):
            active_filters.append(AllergyFilter.NUTS)
    
    with col2:
        if st.checkbox("🌾 Gluten-Free", key="gluten_filter"):
            active_filters.append(AllergyFilter.GLUTEN)
    
    with col3:
        if st.checkbox("🥛 Dairy-Free", key="dairy_filter"):
            active_filters.append(AllergyFilter.DAIRY)
    
    with col4:
        if st.checkbox("🌱 Vegan", key="vegan_filter"):
            active_filters.append(AllergyFilter.VEGAN)
    
    if active_filters:
        filter_names = [f.value for f in active_filters]
        st.info(f"Active constraints: {', '.join(filter_names)}")
    
    st.markdown("---")
    
    # Menu Input
    st.markdown("### 📋 Menu Dump")
    
    sample_menu = """1. Caesar Salad - $12 - Romaine lettuce, parmesan, croutons, caesar dressing
2. Bacon Cheeseburger - $16 - Beef patty, bacon, cheese, fries
3. Grilled Salmon - $22 - Atlantic salmon, quinoa, steamed vegetables
4. Chocolate Lava Cake - $8 - Warm chocolate cake with vanilla ice cream
5. Chicken Wrap - $14 - Grilled chicken, vegetables, whole wheat tortilla"""
    
    menu_text = st.text_area(
        "Paste the menu from the restaurant website or your grocery list here...",
        height=200,
        placeholder=f"Example:\n\n{sample_menu}"
    )
    
    # Referee Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        referee_button = st.button("🏆 GET REFEREE DECISION", type="primary", use_container_width=True)
    
    # Process Decision
    if referee_button and menu_text.strip():
        with st.spinner("🤔 Analyzing trade-offs across parallel universes..."):
            decision = analyze_menu_simple(menu_text, steering_mode, active_filters)
        
        st.markdown("---")
        st.markdown("### 🏆 The Arbiter's Verdict")
        
        # Winner Card
        st.markdown(f"""
        <div class="winner-card">
            <h2>🥇 WINNER</h2>
            <h1>{decision['winner']}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Parallel Universe
        if decision.get('parallel_choice') and decision['parallel_choice'] != decision['winner']:
            st.markdown("#### 🌌 The Road Not Taken")
            opposite_mode = "Gremlin" if steering_mode == SteeringMode.ZEN else "Zen"
            opposite_icon = "🔥" if steering_mode == SteeringMode.ZEN else "⚖️"
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(107, 114, 128, 0.3), rgba(156, 163, 175, 0.2));
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #6B7280;
                margin: 15px 0;
                opacity: 0.7;
            ">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 1.2em; margin-right: 8px;">{opposite_icon}</span>
                    <strong>In {opposite_mode} Mode, I would have chosen:</strong>
                </div>
                <h3 style="margin: 5px 0; color: #374151;">{decision['parallel_choice']}</h3>
                <p style="margin: 5px 0; font-style: italic; color: #6B7280;">
                    {decision['parallel_explanation']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Trade-off Analysis
        st.markdown("#### ⚖️ Trade-off Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Health Score**")
            health_percentage = (decision['health_score'] / 10) * 100
            st.markdown(f"""
            <div class="score-bar">
                <div class="health-fill" style="width: {health_percentage}%"></div>
            </div>
            <p style="text-align: center;">{decision['health_score']}/10</p>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Taste/Crave Score**")
            taste_percentage = (decision['taste_score'] / 10) * 100
            st.markdown(f"""
            <div class="score-bar">
                <div class="taste-fill" style="width: {taste_percentage}%"></div>
            </div>
            <p style="text-align: center;">{decision['taste_score']}/10</p>
            """, unsafe_allow_html=True)
        
        # Referee's Logic
        st.markdown("#### 🧠 The Referee's Logic")
        st.info(decision['verdict'])
        
        # Modification Tip
        st.markdown("#### 💡 Pro Tip")
        st.success(decision['modification'])
        
        # Show vetoed items if any
        if decision.get('vetoed_items'):
            st.markdown("#### 🚫 Items Vetoed for Safety")
            for item in decision['vetoed_items']:
                st.error(f"❌ {item}")
        
    elif referee_button and not menu_text.strip():
        st.error("Please paste a menu or grocery list first!")

if __name__ == "__main__":
    main()