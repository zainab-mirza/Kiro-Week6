import streamlit as st
import os
from dotenv import load_dotenv
from src.executive_dashboard import ExecutiveDashboard
from src.decision_engine import DecisionIntelligenceEngine
from src.models import AllergyFilter

# Load environment variables
load_dotenv()

# Page config for executive dashboard
st.set_page_config(
    page_title="BiteBalance - Decision Intelligence Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Main executive dashboard application"""
    
    # Apply professional styling
    ExecutiveDashboard.render_professional_css()
    
    # Initialize decision engine
    decision_engine = DecisionIntelligenceEngine()
    
    # Executive Header
    ExecutiveDashboard.render_professional_header()
    
    # Dual-Axis Steering System
    nutrition_axis, budget_axis = ExecutiveDashboard.render_dual_axis_steering()
    
    st.markdown("---")
    
    # Hard Constraints
    allergy_filters, time_constraint = ExecutiveDashboard.render_hard_constraints()
    
    st.markdown("---")
    
    # Menu Input Section
    st.markdown("### 📋 Executive Menu Analysis")
    st.markdown("*Paste restaurant menu or grocery options for comprehensive decision intelligence*")
    
    sample_menu = """1. Grilled Atlantic Salmon - $28 - Wild-caught salmon, quinoa pilaf, seasonal vegetables
2. Wagyu Beef Burger - $24 - Premium wagyu patty, truffle aioli, artisan bun, hand-cut fries
3. Mediterranean Bowl - $16 - Quinoa, chickpeas, feta, olives, cucumber, tahini dressing
4. Lobster Risotto - $32 - Maine lobster, arborio rice, white wine, parmesan, herbs
5. Caesar Salad - $14 - Romaine hearts, house-made croutons, parmesan, anchovy dressing
6. Chocolate Lava Cake - $12 - Warm chocolate cake, vanilla bean ice cream, berry coulis"""
    
    menu_text = st.text_area(
        "Menu Items",
        height=200,
        placeholder=f"Example executive menu:\n\n{sample_menu}",
        help="Paste menu items with names, prices, and descriptions for optimal analysis"
    )
    
    # Executive Analysis Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🎯 EXECUTE DECISION INTELLIGENCE ANALYSIS",
            type="primary",
            use_container_width=True
        )
    
    # Process Executive Decision
    if analyze_button and menu_text.strip():
        with st.spinner("🧠 Executing multi-dimensional decision intelligence analysis..."):
            
            # Perform comprehensive analysis
            analysis = decision_engine.analyze_menu(
                menu_text=menu_text,
                nutrition_axis=nutrition_axis,
                budget_axis=budget_axis,
                constraints=allergy_filters,
                time_constraint=time_constraint
            )
        
        st.markdown("---")
        
        # Render Executive Decision Cards
        ExecutiveDashboard.render_decision_cards(analysis)
        
        st.markdown("---")
        
        # Render Trade-off Radar Chart
        if analysis['winner']['health_score'] > 0:
            ExecutiveDashboard.render_trade_off_radar(analysis['winner'])
        
        st.markdown("---")
        
        # Render Veto Log
        if analysis['vetoed_items']:
            ExecutiveDashboard.render_veto_log(analysis['vetoed_items'], analysis['veto_reasons'])
            st.markdown("---")
        
        # Executive Summary
        ExecutiveDashboard.render_executive_summary(analysis)
        
        # Performance Metrics
        st.markdown("### 📊 Decision Intelligence Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Options Analyzed", 
                analysis['total_options'],
                delta=f"{analysis['safe_options']} viable"
            )
        
        with col2:
            st.metric(
                "Decision Confidence",
                f"{analysis['winner']['confidence']}%",
                delta=f"{analysis['alignment_score']}% alignment"
            )
        
        with col3:
            st.metric(
                "Constraints Applied",
                len(analysis['active_constraints']),
                delta=f"{len(analysis['vetoed_items'])} vetoed"
            )
        
        with col4:
            risk_color = "normal" if "Low" in analysis['risk_level'] else "inverse"
            st.metric(
                "Risk Assessment",
                analysis['risk_level'].split(' - ')[0],
                delta=analysis['risk_level'].split(' - ')[1] if ' - ' in analysis['risk_level'] else ""
            )
        
        # Professional Insights
        if analysis['winner']['confidence'] > 80:
            st.success("🎯 **High-Confidence Decision**: Strong alignment with your preferences and constraints.")
        elif analysis['winner']['confidence'] > 60:
            st.info("⚖️ **Balanced Decision**: Reasonable trade-offs across multiple dimensions.")
        else:
            st.warning("🤔 **Complex Trade-off**: Consider adjusting preferences or exploring additional options.")
    
    elif analyze_button and not menu_text.strip():
        st.error("Please provide menu items for executive analysis.")
    
    # Footer with professional branding
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.9em; padding: 20px;">
        <strong>BiteBalance Decision Intelligence Dashboard</strong><br>
        Professional-grade meal optimization for executive decision making
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()