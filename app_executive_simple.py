import streamlit as st
import plotly.graph_objects as go
from enum import Enum

# Simple enums
class AllergyFilter(Enum):
    NUTS = "🥜 No Nuts"
    GLUTEN = "🌾 Gluten-Free"
    DAIRY = "🥛 Dairy-Free"
    VEGAN = "🌱 Vegan"

# Page config
st.set_page_config(
    page_title="BiteBalance - Executive Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
    background-color: #f8fafc;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    color: #1f2937;
}

.executive-header {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 30px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.decision-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    height: 300px;
    margin: 10px 0;
}

.winner-card {
    border: 2px solid #10B981;
}

.alternative-card {
    border: 2px solid #6366f1;
}

.compromise-card {
    border: 2px solid #f59e0b;
}

.score-bar {
    background-color: #f3f4f6;
    height: 6px;
    border-radius: 3px;
    margin: 5px 0;
}

.health-fill {
    background-color: #10B981;
    height: 6px;
    border-radius: 3px;
}

.taste-fill {
    background-color: #f97316;
    height: 6px;
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

def analyze_executive_menu(menu_text, nutrition_axis, budget_axis, constraints):
    """Executive-grade menu analysis"""
    
    items = [line.strip() for line in menu_text.split('\n') if line.strip()]
    
    if not items:
        return {
            'winner': {'name': 'No items found', 'health_score': 0, 'taste_score': 0, 'confidence': 0, 'description': 'Please provide menu items'},
            'alternative': {'name': 'No alternatives', 'health_score': 0, 'taste_score': 0, 'confidence': 0, 'description': 'No menu provided'},
            'compromise': {'name': 'No options', 'health_score': 0, 'taste_score': 0, 'confidence': 0, 'description': 'No items to analyze'},
            'vetoed_items': [],
            'veto_reasons': [],
            'reasoning': 'No menu items provided for analysis.',
            'total_options': 0
        }
    
    # Filter items based on constraints
    safe_items = []
    vetoed_items = []
    veto_reasons = []
    
    allergy_keywords = {
        AllergyFilter.NUTS: ['nut', 'almond', 'peanut', 'walnut'],
        AllergyFilter.GLUTEN: ['wheat', 'bread', 'pasta', 'flour', 'gluten'],
        AllergyFilter.DAIRY: ['milk', 'cheese', 'butter', 'cream'],
        AllergyFilter.VEGAN: ['meat', 'chicken', 'beef', 'pork', 'fish']
    }
    
    for item in items:
        is_safe = True
        veto_reason = ""
        
        for constraint in constraints:
            keywords = allergy_keywords.get(constraint, [])
            if any(keyword in item.lower() for keyword in keywords):
                is_safe = False
                veto_reason = f"Violates {constraint.value} constraint"
                break
        
        if is_safe:
            safe_items.append(item)
        else:
            vetoed_items.append(clean_name(item))
            veto_reasons.append(veto_reason)
    
    if not safe_items:
        return {
            'winner': {'name': 'No safe options', 'health_score': 0, 'taste_score': 0, 'confidence': 0, 'description': 'All items vetoed'},
            'alternative': {'name': 'All vetoed', 'health_score': 0, 'taste_score': 0, 'confidence': 0, 'description': 'Constraints too restrictive'},
            'compromise': {'name': 'No viable options', 'health_score': 0, 'taste_score': 0, 'confidence': 0, 'description': 'Adjust constraints'},
            'vetoed_items': vetoed_items,
            'veto_reasons': veto_reasons,
            'reasoning': 'All items excluded due to hard constraints.',
            'total_options': len(items)
        }
    
    # Score items
    scored_items = []
    health_keywords = ['salad', 'grilled', 'steamed', 'quinoa', 'salmon', 'vegetables', 'lean']
    taste_keywords = ['burger', 'pizza', 'chocolate', 'cheese', 'bacon', 'fried', 'sauce']
    premium_keywords = ['truffle', 'wagyu', 'artisan', 'premium', 'organic']
    
    for item in safe_items:
        item_lower = item.lower()
        
        health_score = min(10, max(1, sum(2 for kw in health_keywords if kw in item_lower) + 3))
        taste_score = min(10, max(1, sum(2 for kw in taste_keywords if kw in item_lower) + 3))
        premium_score = min(10, max(1, sum(2 for kw in premium_keywords if kw in item_lower) + 3))
        
        scored_items.append({
            'name': clean_name(item),
            'original': item,
            'health_score': health_score,
            'taste_score': taste_score,
            'premium_score': premium_score,
            'description': extract_description(item)
        })
    
    # Select winner based on dual-axis preferences
    winner = select_best_item(scored_items, nutrition_axis, budget_axis, 'optimal')
    alternative = select_best_item(scored_items, 100 - nutrition_axis, budget_axis, 'alternative')
    compromise = select_best_item(scored_items, 50, 50, 'compromise')
    
    reasoning = f"Selected {winner['name']} based on {get_focus_description(nutrition_axis, budget_axis)}. This decision optimizes for your dual-axis preferences while respecting all safety constraints."
    
    return {
        'winner': winner,
        'alternative': alternative,
        'compromise': compromise,
        'vetoed_items': vetoed_items,
        'veto_reasons': veto_reasons,
        'reasoning': reasoning,
        'total_options': len(items)
    }

def select_best_item(scored_items, nutrition_axis, budget_axis, category):
    """Select best item based on preferences"""
    if not scored_items:
        return {'name': 'No options', 'health_score': 0, 'taste_score': 0, 'confidence': 0, 'description': 'No items available'}
    
    best_item = None
    best_score = -1
    
    for item in scored_items:
        # Calculate weighted score
        health_weight = (100 - nutrition_axis) / 100
        taste_weight = nutrition_axis / 100
        premium_weight = budget_axis / 100
        
        weighted_score = (
            item['health_score'] * health_weight * 0.4 +
            item['taste_score'] * taste_weight * 0.4 +
            item['premium_score'] * premium_weight * 0.2
        )
        
        if weighted_score > best_score:
            best_score = weighted_score
            best_item = item
    
    if best_item:
        best_item['confidence'] = min(95, int(best_score * 10))
    
    return best_item or scored_items[0]

def clean_name(item):
    """Clean item name"""
    clean = item.split('-')[0].strip()
    if clean and clean[0].isdigit() and '.' in clean[:5]:
        clean = clean.split('.', 1)[1].strip()
    return clean or item

def extract_description(item):
    """Extract description from item"""
    parts = item.split('-')
    if len(parts) >= 3:
        return parts[2].strip()
    return "Premium selection"

def get_focus_description(nutrition_axis, budget_axis):
    """Get focus description based on axes"""
    if nutrition_axis <= 40:
        nutrition_focus = "health optimization"
    elif nutrition_axis >= 60:
        nutrition_focus = "indulgence satisfaction"
    else:
        nutrition_focus = "balanced nutrition"
    
    if budget_axis >= 60:
        budget_focus = "premium quality"
    else:
        budget_focus = "value optimization"
    
    return f"{nutrition_focus} with {budget_focus}"

def render_decision_card(item_data, card_type, color):
    """Render a decision card"""
    
    type_labels = {
        'winner': ('OPTIMAL CHOICE', '🏆'),
        'alternative': ('ALTERNATIVE', '🔄'),
        'compromise': ('COMPROMISE', '⚖️')
    }
    
    label, icon = type_labels.get(card_type, ('CHOICE', '📋'))
    
    st.markdown(f"""
    <div class="decision-card {card_type}-card">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="
                background: {color};
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 0.9em;
            ">{label}</div>
            <div style="margin-left: auto; font-size: 1.2em;">{icon}</div>
        </div>
        
        <h3 style="margin: 0 0 10px 0; color: #1f2937;">{item_data['name']}</h3>
        <p style="color: #6b7280; font-size: 0.9em; margin-bottom: 15px;">{item_data['description']}</p>
        
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-size: 0.8em; color: #6b7280;">Health Score</span>
                <span style="font-weight: bold; color: #10B981;">{item_data['health_score']}/10</span>
            </div>
            <div class="score-bar">
                <div class="health-fill" style="width: {item_data['health_score'] * 10}%;"></div>
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-size: 0.8em; color: #6b7280;">Taste Score</span>
                <span style="font-weight: bold; color: #f97316;">{item_data['taste_score']}/10</span>
            </div>
            <div class="score-bar">
                <div class="taste-fill" style="width: {item_data['taste_score'] * 10}%;"></div>
            </div>
        </div>
        
        <div style="
            background: #f8fafc;
            padding: 10px;
            border-radius: 6px;
            text-align: center;
            margin-top: auto;
        ">
            <span style="font-size: 0.8em; color: #6b7280;">Confidence</span><br>
            <span style="font-weight: bold; color: {color}; font-size: 1.1em;">{item_data['confidence']}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_radar_chart(item_data):
    """Render radar chart for trade-off analysis"""
    
    categories = ['Health', 'Taste', 'Satiety', 'Value', 'Speed']
    values = [
        item_data['health_score'],
        item_data['taste_score'],
        item_data.get('satiety_score', 7),
        item_data.get('value_score', 8),
        item_data.get('speed_score', 6)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Selected Choice',
        line_color='#10B981',
        fillcolor='rgba(16, 185, 129, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(size=10),
                gridcolor='#e5e7eb'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#374151')
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def main():
    """Main executive dashboard"""
    
    # Executive Header
    st.markdown("""
    <div class="executive-header">
        <h1 style="margin: 0; font-weight: 300; font-size: 2.5em;">BiteBalance</h1>
        <h3 style="margin: 10px 0 0 0; opacity: 0.8; font-weight: 300;">Decision Intelligence Dashboard</h3>
        <p style="margin: 15px 0 0 0; opacity: 0.7; font-size: 1.1em;">
            Executive-grade meal optimization through multi-dimensional trade-off analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dual-Axis Steering
    st.markdown("### 🎯 Decision Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Nutrition ↔ Indulgence**")
        nutrition_axis = st.select_slider(
            "Primary Axis",
            options=list(range(0, 101, 10)),
            value=50,
            format_func=lambda x: f"Health Focus" if x <= 30 else f"Balanced" if x <= 70 else f"Indulgence",
            key="nutrition_axis"
        )
    
    with col2:
        st.markdown("**Budget ↔ Premium**")
        budget_axis = st.select_slider(
            "Secondary Axis",
            options=list(range(0, 101, 10)),
            value=50,
            format_func=lambda x: f"Economy" if x <= 30 else f"Mid-Range" if x <= 70 else f"Premium",
            key="budget_axis"
        )
    
    st.markdown("---")
    
    # Hard Constraints
    st.markdown("### 🛡️ Hard Constraints")
    st.markdown("*Executive dealbreakers - non-negotiable requirements*")
    
    col1, col2, col3, col4 = st.columns(4)
    active_filters = []
    
    with col1:
        if st.checkbox("🥜 No Nuts", key="nuts_constraint"):
            active_filters.append(AllergyFilter.NUTS)
    
    with col2:
        if st.checkbox("🌾 Gluten-Free", key="gluten_constraint"):
            active_filters.append(AllergyFilter.GLUTEN)
    
    with col3:
        if st.checkbox("🥛 Dairy-Free", key="dairy_constraint"):
            active_filters.append(AllergyFilter.DAIRY)
    
    with col4:
        if st.checkbox("🌱 Vegan", key="vegan_constraint"):
            active_filters.append(AllergyFilter.VEGAN)
    
    if active_filters:
        constraint_names = [f.value for f in active_filters]
        st.info(f"**Active Constraints:** {' • '.join(constraint_names)}")
    
    st.markdown("---")
    
    # Menu Input
    st.markdown("### 📋 Executive Menu Analysis")
    st.markdown("*Paste restaurant menu or grocery options for comprehensive decision intelligence*")
    
    sample_menu = """1. Grilled Atlantic Salmon - $28 - Wild-caught salmon, quinoa pilaf, seasonal vegetables
2. Wagyu Beef Burger - $24 - Premium wagyu patty, truffle aioli, artisan bun, hand-cut fries
3. Mediterranean Bowl - $16 - Quinoa, chickpeas, feta, olives, cucumber, tahini dressing
4. Lobster Risotto - $32 - Maine lobster, arborio rice, white wine, parmesan, herbs
5. Caesar Salad - $14 - Romaine hearts, house-made croutons, parmesan, anchovy dressing"""
    
    menu_text = st.text_area(
        "Menu Items",
        height=200,
        placeholder=f"Example executive menu:\n\n{sample_menu}",
        help="Paste menu items with names, prices, and descriptions for optimal analysis"
    )
    
    # Analysis Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🎯 EXECUTE DECISION INTELLIGENCE ANALYSIS",
            type="primary",
            use_container_width=True
        )
    
    # Process Analysis
    if analyze_button and menu_text.strip():
        with st.spinner("🧠 Executing multi-dimensional decision intelligence analysis..."):
            analysis = analyze_executive_menu(menu_text, nutrition_axis, budget_axis, active_filters)
        
        st.markdown("---")
        
        # Decision Cards
        st.markdown("### 🏆 Executive Decision Matrix")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_decision_card(analysis['winner'], 'winner', '#10B981')
        
        with col2:
            render_decision_card(analysis['alternative'], 'alternative', '#6366f1')
        
        with col3:
            render_decision_card(analysis['compromise'], 'compromise', '#f59e0b')
        
        st.markdown("---")
        
        # Trade-off Radar
        if analysis['winner']['health_score'] > 0:
            st.markdown("### 📊 Multi-Dimensional Trade-off Analysis")
            fig = render_radar_chart(analysis['winner'])
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")
        
        # Veto Log
        if analysis['vetoed_items']:
            st.markdown("### 🚫 Executive Veto Log")
            st.markdown("*Items excluded due to hard constraints*")
            
            for item, reason in zip(analysis['vetoed_items'], analysis['veto_reasons']):
                st.markdown(f"""
                <div style="
                    background: #fef2f2;
                    border-left: 4px solid #ef4444;
                    padding: 12px 16px;
                    margin: 8px 0;
                    border-radius: 0 8px 8px 0;
                ">
                    <strong style="color: #dc2626;">{item}</strong><br>
                    <span style="color: #7f1d1d; font-size: 0.9em;">Reason: {reason}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("---")
        
        # Executive Summary
        st.markdown("### 📋 Executive Summary")
        st.markdown(f"**Decision Rationale:** {analysis['reasoning']}")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Options Analyzed", analysis['total_options'])
        
        with col2:
            st.metric("Decision Confidence", f"{analysis['winner']['confidence']}%")
        
        with col3:
            st.metric("Constraints Applied", len(active_filters))
        
    elif analyze_button and not menu_text.strip():
        st.error("Please provide menu items for executive analysis.")

if __name__ == "__main__":
    main()