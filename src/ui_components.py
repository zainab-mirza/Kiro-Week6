import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Tuple
from .models import AllergyFilter, DualAxisCalculator, DecisionIntelligence, RefereeChoice

class UIComponents:
    """Reusable UI components for the BiteBalance app"""
    
    @staticmethod
    def render_header():
        """Render the main app header"""
        st.markdown("""
        <div class="main-header">
            <h1>🥗 BiteBalance</h1>
            <h3>The AI Menu Referee</h3>
            <p><em>Arbitrating the conflict between health goals and flavor cravings</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_mode_selector() -> SteeringMode:
        """Render the steering mode selector"""
        st.markdown("### 🎯 Mode Master")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            mode_value = st.select_slider(
                "Choose your referee mode:",
                options=["Zen Mode", "Gremlin Mode"],
                value="Zen Mode",
                format_func=lambda x: f"🧘‍♂️ {x}" if x == "Zen Mode" else f"😈 {x}"
            )
        
        mode = SteeringMode.ZEN if mode_value == "Zen Mode" else SteeringMode.GREMLIN
        UIComponents._render_mode_context(mode)
        
        return mode
    
    @staticmethod
    def _render_mode_context(mode: SteeringMode):
        """Render the context indicator for the selected mode"""
        mode_info = ScoreCalculator.get_mode_description(mode)
        
        if mode == SteeringMode.ZEN:
            st.markdown(f"""
            <div class="zen-mode">
                {mode_info['icon']} <strong>{mode_info['title']}</strong><br>
                <em>{mode_info['description']}</em>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="gremlin-mode">
                {mode_info['icon']} <strong>{mode_info['title']}</strong><br>
                <em>{mode_info['description']}</em>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_allergy_filters() -> List[AllergyFilter]:
        """Render the Hard Veto allergy filter chips"""
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
        
        return active_filters
    @staticmethod
    def render_budget_selector() -> float:
        """Render the budget constraint selector"""
        st.markdown("### 💰 Budget Constraint (Optional)")
        enable_budget = st.checkbox("Set budget limit")
        budget_limit = None
        
        if enable_budget:
            budget_limit = st.slider("Maximum price per item ($)", 5, 50, 25)
            st.info(f"Only considering items under ${budget_limit}")
        
        return budget_limit
    
    @staticmethod
    def render_menu_input() -> str:
        """Render the menu input area"""
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
        
        return menu_text
    
    @staticmethod
    def render_referee_button() -> bool:
        """Render the main referee decision button"""
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            return st.button("🏆 GET REFEREE DECISION", type="primary", use_container_width=True)
    
    @staticmethod
    def render_decision_results(decision: Dict[str, Any], current_mode: SteeringMode):
        """Render the complete decision results with parallel universe"""
        st.markdown("---")
        st.markdown("### 🏆 The Arbiter's Verdict")
        
        # Winner Card with Referee Avatar
        UIComponents._render_winner_card_with_avatar(decision, current_mode)
        
        # Parallel Universe Comparison
        if decision.get('parallel_choice'):
            UIComponents._render_parallel_universe(decision, current_mode)
        
        # Trade-off Analysis
        UIComponents._render_score_analysis(decision)
        
        # Referee Logic and Tips
        UIComponents._render_decision_explanation(decision, current_mode)
    
    @staticmethod
    def _render_winner_card_with_avatar(decision: Dict[str, Any], mode: SteeringMode):
        """Render the winner card with referee personality avatar"""
        mode_info = ScoreCalculator.get_mode_description(mode)
        
        st.markdown(f"""
        <div class="winner-card" style="background: linear-gradient(135deg, {mode_info['color']}, {mode_info['bg_color']});">
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                <div style="font-size: 2em; margin-right: 15px;">{mode_info['icon']}</div>
                <div>
                    <h2 style="margin: 0;">🥇 WINNER</h2>
                    <small style="opacity: 0.8;">{mode_info['title']} Referee</small>
                </div>
            </div>
            <h1 style="margin: 10px 0;">{decision['winner']}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_parallel_universe(decision: Dict[str, Any], current_mode: SteeringMode):
        """Render the parallel universe comparison"""
        opposite_mode = "Gremlin" if current_mode == SteeringMode.ZEN else "Zen"
        opposite_icon = "🔥" if current_mode == SteeringMode.ZEN else "⚖️"
        
        st.markdown("#### 🌌 The Road Not Taken")
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
                {decision.get('parallel_explanation', 'Alternative choice based on different priorities')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_score_analysis(decision: Dict[str, Any]):
        """Render the score bars and analysis"""
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
    
    @staticmethod
    def _render_decision_explanation(decision: Dict[str, Any], mode: SteeringMode):
        """Render the AI's reasoning and tips with personality"""
        mode_info = ScoreCalculator.get_mode_description(mode)
        
        # Referee's Logic with personality styling
        st.markdown("#### 🧠 The Referee's Logic")
        
        verdict_style = f"""
        <div style="
            background-color: {mode_info['bg_color']}20;
            border-left: 4px solid {mode_info['color']};
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 1.5em; margin-right: 10px;">{mode_info['icon']}</span>
                <strong>{mode_info['title']} Referee Says:</strong>
            </div>
            <p style="margin: 0;">{decision['verdict']}</p>
        </div>
        """
        st.markdown(verdict_style, unsafe_allow_html=True)
        
        # Show vetoed items if any
        if decision.get('vetoed_items'):
            st.markdown("#### 🚫 Items Vetoed for Safety")
            for item in decision['vetoed_items']:
                st.error(f"❌ {item}")
        
        # Modification Tip
        st.markdown("#### 💡 Pro Tip")
        st.success(decision['modification'])
    
    @staticmethod
    def render_custom_css():
        """Render all custom CSS styles"""
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
            
            .stSelectbox > div > div {
                background-color: #f8fafc;
            }
            
            .stButton > button {
                background: linear-gradient(90deg, #10B981, #F97316);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
        </style>
        """, unsafe_allow_html=True)