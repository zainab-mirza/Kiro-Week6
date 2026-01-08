import streamlit as st
import re
from enum import Enum

# Simple enums for the app
class SteeringMode(Enum):
    ZEN = "Zen Mode"
    GREMLIN = "Gremlin Mode"

# Page config
st.set_page_config(
    page_title="🥗 BiteBalance - Smart Food Referee",
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
    
    .option-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .winner-option {
        border-color: #10B981;
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    }
    
    .alternative-option {
        border-color: #f97316;
        background: linear-gradient(135deg, #fff7ed, #fed7aa);
    }
    
    .score-bar {
        background-color: #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
        margin: 5px 0;
        height: 8px;
    }
    
    .health-fill {
        background-color: #10B981;
        height: 8px;
        border-radius: 10px;
    }
    
    .taste-fill {
        background-color: #F97316;
        height: 8px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def generate_food_options(food_input, steering_mode):
    """Generate different preparation options for the mentioned food"""
    
    food_lower = food_input.lower()
    
    # Food-specific option generation
    if 'burger' in food_lower:
        options = [
            {
                'name': 'Grilled Chicken Burger (No Cheese)',
                'description': 'Lean grilled chicken breast, lettuce, tomato, whole wheat bun',
                'health_score': 8,
                'taste_score': 6,
                'calories': '320 cal',
                'modifications': ['No mayo', 'Extra vegetables', 'Whole wheat bun']
            },
            {
                'name': 'Turkey Burger with Light Cheese',
                'description': 'Ground turkey patty, reduced-fat cheese, avocado, multigrain bun',
                'health_score': 7,
                'taste_score': 7,
                'calories': '380 cal',
                'modifications': ['Light cheese', 'Add avocado', 'Side salad instead of fries']
            },
            {
                'name': 'Classic Beef Burger with Cheese',
                'description': 'Beef patty, full cheese, bacon, regular bun with fries',
                'health_score': 4,
                'taste_score': 9,
                'calories': '650 cal',
                'modifications': ['Extra bacon', 'Loaded fries', 'Full-fat cheese']
            }
        ]
    
    elif 'pizza' in food_lower:
        options = [
            {
                'name': 'Thin Crust Veggie Pizza',
                'description': 'Thin whole wheat crust, light cheese, lots of vegetables',
                'health_score': 7,
                'taste_score': 6,
                'calories': '220 cal/slice',
                'modifications': ['Extra vegetables', 'Light cheese', 'Thin crust']
            },
            {
                'name': 'Margherita Pizza (Regular)',
                'description': 'Regular crust, mozzarella, fresh basil, tomato sauce',
                'health_score': 5,
                'taste_score': 8,
                'calories': '280 cal/slice',
                'modifications': ['Fresh mozzarella', 'Basil', 'Regular portion']
            },
            {
                'name': 'Meat Lovers Deep Dish',
                'description': 'Thick crust, extra cheese, pepperoni, sausage, bacon',
                'health_score': 3,
                'taste_score': 9,
                'calories': '420 cal/slice',
                'modifications': ['Extra meat', 'Extra cheese', 'Thick crust']
            }
        ]
    
    elif 'pasta' in food_lower:
        options = [
            {
                'name': 'Zucchini Noodles with Marinara',
                'description': 'Spiralized zucchini, fresh marinara sauce, lean ground turkey',
                'health_score': 9,
                'taste_score': 5,
                'calories': '180 cal',
                'modifications': ['Zucchini noodles', 'Lean protein', 'Fresh herbs']
            },
            {
                'name': 'Whole Wheat Pasta Primavera',
                'description': 'Whole wheat pasta, mixed vegetables, light olive oil',
                'health_score': 7,
                'taste_score': 7,
                'calories': '320 cal',
                'modifications': ['Whole wheat pasta', 'Extra vegetables', 'Light sauce']
            },
            {
                'name': 'Fettuccine Alfredo',
                'description': 'Regular pasta, heavy cream sauce, parmesan cheese',
                'health_score': 3,
                'taste_score': 9,
                'calories': '520 cal',
                'modifications': ['Extra cream', 'Extra cheese', 'Garlic bread']
            }
        ]
    
    elif 'salad' in food_lower:
        options = [
            {
                'name': 'Power Greens Salad',
                'description': 'Kale, spinach, quinoa, grilled chicken, lemon vinaigrette',
                'health_score': 10,
                'taste_score': 6,
                'calories': '280 cal',
                'modifications': ['Extra protein', 'Nuts and seeds', 'Light dressing']
            },
            {
                'name': 'Mediterranean Salad',
                'description': 'Mixed greens, feta, olives, chickpeas, olive oil dressing',
                'health_score': 8,
                'taste_score': 8,
                'calories': '350 cal',
                'modifications': ['Feta cheese', 'Olive oil dressing', 'Chickpeas']
            },
            {
                'name': 'Caesar Salad with Croutons',
                'description': 'Romaine lettuce, caesar dressing, croutons, parmesan',
                'health_score': 5,
                'taste_score': 8,
                'calories': '420 cal',
                'modifications': ['Extra dressing', 'Croutons', 'Bacon bits']
            }
        ]
    
    elif 'sandwich' in food_lower:
        options = [
            {
                'name': 'Grilled Chicken & Avocado Wrap',
                'description': 'Whole wheat tortilla, grilled chicken, avocado, vegetables',
                'health_score': 8,
                'taste_score': 7,
                'calories': '320 cal',
                'modifications': ['Whole wheat wrap', 'Extra vegetables', 'Light spread']
            },
            {
                'name': 'Turkey Club Sandwich',
                'description': 'Multigrain bread, turkey, light mayo, lettuce, tomato',
                'health_score': 6,
                'taste_score': 7,
                'calories': '380 cal',
                'modifications': ['Multigrain bread', 'Light mayo', 'Extra vegetables']
            },
            {
                'name': 'BLT with Extra Bacon',
                'description': 'White bread, bacon, lettuce, tomato, full mayo',
                'health_score': 4,
                'taste_score': 8,
                'calories': '480 cal',
                'modifications': ['Extra bacon', 'Full mayo', 'White bread']
            }
        ]
    
    else:
        # Generic healthy vs indulgent options
        options = [
            {
                'name': f'Healthy {food_input.title()} Option',
                'description': 'Prepared with minimal oil, extra vegetables, lean protein',
                'health_score': 8,
                'taste_score': 6,
                'calories': 'Lower cal',
                'modifications': ['Grilled not fried', 'Extra vegetables', 'Light seasoning']
            },
            {
                'name': f'Balanced {food_input.title()} Option',
                'description': 'Moderate preparation with some indulgent elements',
                'health_score': 6,
                'taste_score': 7,
                'calories': 'Moderate cal',
                'modifications': ['Balanced preparation', 'Some cheese/sauce', 'Regular portion']
            },
            {
                'name': f'Indulgent {food_input.title()} Option',
                'description': 'Rich preparation with cheese, sauce, and full flavor',
                'health_score': 4,
                'taste_score': 9,
                'calories': 'Higher cal',
                'modifications': ['Extra cheese', 'Rich sauce', 'Large portion']
            }
        ]
    
    # Sort options based on steering mode
    if steering_mode == SteeringMode.ZEN:
        options.sort(key=lambda x: x['health_score'], reverse=True)
        winner_reason = "Prioritizing nutritional value and health benefits"
        alternative_reason = "Higher taste but compromises health goals"
    else:
        options.sort(key=lambda x: x['taste_score'], reverse=True)
        winner_reason = "Maximizing flavor satisfaction and indulgence"
        alternative_reason = "Healthier but less satisfying for cheat day"
    
    return options, winner_reason, alternative_reason

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🥗 BiteBalance</h1>
        <h3>Smart Food Referee</h3>
        <p><em>Tell me what you want to eat, I'll show you the best way to have it!</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🧠 **Smart Referee** - Just tell me what food you're craving, and I'll suggest the best options!")
    
    # Steering Mode Selector
    st.markdown("### 🎯 Your Goal Today")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        mode_value = st.select_slider(
            "What's your priority?",
            options=["Zen Mode", "Gremlin Mode"],
            value="Zen Mode",
            format_func=lambda x: f"🧘‍♂️ Health First" if x == "Zen Mode" else f"😈 Taste First"
        )
    
    steering_mode = SteeringMode.ZEN if mode_value == "Zen Mode" else SteeringMode.GREMLIN
    
    # Context Indicator
    if steering_mode == SteeringMode.ZEN:
        st.markdown("""
        <div class="zen-mode">
            🧘‍♂️ <strong>Health First Mode</strong><br>
            <em>I'll find the healthiest way to enjoy your craving</em>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="gremlin-mode">
            😈 <strong>Taste First Mode</strong><br>
            <em>I'll maximize your flavor satisfaction</em>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Food Input
    st.markdown("### 🍽️ What are you craving?")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        food_input = st.text_input(
            "Just type what you want to eat:",
            placeholder="e.g., burger, pizza, pasta, salad, sandwich...",
            help="Tell me any food you're thinking about!"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        analyze_button = st.button("🎯 GET OPTIONS", type="primary", use_container_width=True)
    
    # Process Food Input
    if analyze_button and food_input.strip():
        with st.spinner(f"🤔 Finding the best ways to enjoy {food_input}..."):
            options, winner_reason, alternative_reason = generate_food_options(food_input, steering_mode)
        
        st.markdown("---")
        st.markdown(f"### 🏆 Best Ways to Enjoy {food_input.title()}")
        
        # Winner Option
        winner = options[0]
        
        # Create winner card using Streamlit components
        st.markdown("#### 🥇 RECOMMENDED OPTION")
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{winner['name']}**")
                st.write(winner['description'])
            
            with col2:
                st.metric("Calories", winner['calories'])
        
        # Score bars using Streamlit
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Health Score**")
            st.progress(winner['health_score'] / 10)
            st.write(f"{winner['health_score']}/10")
        
        with col2:
            st.write("**Taste Score**")
            st.progress(winner['taste_score'] / 10)
            st.write(f"{winner['taste_score']}/10")
        
        # Smart modifications
        st.success("💡 **Smart Modifications:**")
        for mod in winner['modifications']:
            st.write(f"• {mod}")
        
        st.markdown("---")
        
        # Alternative Options
        st.markdown("#### 🔄 Other Options")
        
        for i, option in enumerate(options[1:], 1):
            rank_emoji = "🥈" if i == 1 else "🥉"
            
            with st.expander(f"{rank_emoji} {option['name']} - {option['calories']}"):
                st.write(option['description'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Health: {option['health_score']}/10")
                    st.progress(option['health_score'] / 10)
                
                with col2:
                    st.write(f"Taste: {option['taste_score']}/10")
                    st.progress(option['taste_score'] / 10)
        
        # Referee's Reasoning
        st.markdown("#### 🧠 Why I Chose This")
        
        mode_icon = "🧘‍♂️" if steering_mode == SteeringMode.ZEN else "😈"
        mode_name = "Health First" if steering_mode == SteeringMode.ZEN else "Taste First"
        
        st.info(f"{mode_icon} **{mode_name} Referee Says:** {winner_reason}. The {winner['name']} gives you the best balance for your current goal while still satisfying your {food_input} craving!")
        
        # Quick Action Tips
        st.markdown("#### ⚡ Quick Tips")
        
        if steering_mode == SteeringMode.ZEN:
            st.success("🥗 **Health Hack:** Ask for extra vegetables, choose grilled over fried, and request dressing/sauce on the side!")
        else:
            st.success("😋 **Flavor Boost:** Don't hold back on the good stuff - extra cheese, sauce, and sides make it worth it!")
    
    elif analyze_button and not food_input.strip():
        st.error("Please tell me what food you're craving!")
    
    # Example suggestions
    if not food_input:
        st.markdown("### 💡 Try asking about:")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🍔 Burger", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("🍕 Pizza", use_container_width=True):
                st.rerun()
        
        with col3:
            if st.button("🍝 Pasta", use_container_width=True):
                st.rerun()
        
        with col4:
            if st.button("🥗 Salad", use_container_width=True):
                st.rerun()

if __name__ == "__main__":
    main()