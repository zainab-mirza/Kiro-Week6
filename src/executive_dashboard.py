import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Tuple
from .models import AllergyFilter

class ExecutiveDashboard:
    """Professional Executive Dashboard for Decision Intelligence"""
    
    @staticmethod
    def render_professional_header():
        """Render executive-style header"""
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        ">
            <h1 style="margin: 0; font-weight: 300; font-size: 2.5em;">BiteBalance</h1>
            <h3 style="margin: 10px 0 0 0; opacity: 0.8; font-weight: 300;">Decision Intelligence Dashboard</h3>
            <p style="margin: 15px 0 0 0; opacity: 0.7; font-size: 1.1em;">
                Executive-grade meal optimization through multi-dimensional trade-off analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_dual_axis_steering() -> Tuple[int, int]:
        """Render professional dual-axis steering system"""
        st.markdown("### 🎯 Decision Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Nutrition ↔ Indulgence**")
            nutrition_score = st.select_slider(
                "Primary Axis",
                options=list(range(0, 101, 10)),
                value=50,
                format_func=lambda x: f"Health Focus" if x <= 30 else f"Balanced" if x <= 70 else f"Indulgence",
                key="nutrition_axis"
            )
        
        with col2:
            st.markdown("**Budget ↔ Premium**")
            budget_score = st.select_slider(
                "Secondary Axis", 
                options=list(range(0, 101, 10)),
                value=50,
                format_func=lambda x: f"Economy" if x <= 30 else f"Mid-Range" if x <= 70 else f"Premium",
                key="budget_axis"
            )
        
        # Dynamic background color based on settings
        ExecutiveDashboard._render_dynamic_styling(nutrition_score, budget_score)
        
        return nutrition_score, budget_score
    
    @staticmethod
    def _render_dynamic_styling(nutrition_score: int, budget_score: int):
        """Render dynamic styling based on slider positions"""
        # Calculate dominant color
        if nutrition_score <= 40:
            primary_color = "#10B981"  # Green for health
        elif nutrition_score >= 60:
            primary_color = "#F97316"  # Orange for indulgence
        else:
            primary_color = "#6366F1"  # Blue for balanced
        
        if budget_score >= 70:
            accent_color = "#F59E0B"  # Gold for premium
        else:
            accent_color = primary_color
        
        st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, {primary_color}08 0%, {accent_color}05 100%);
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_hard_constraints() -> Tuple[List[AllergyFilter], bool]:
        """Render professional constraint chips"""
        st.markdown("### 🛡️ Hard Constraints")
        st.markdown("*Executive dealbreakers - non-negotiable requirements*")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        active_filters = []
        
        constraints = [
            (col1, AllergyFilter.NUTS, "🥜 No Nuts"),
            (col2, AllergyFilter.GLUTEN, "🌾 Gluten-Free"),
            (col3, AllergyFilter.DAIRY, "🥛 Dairy-Free"),
            (col4, AllergyFilter.VEGAN, "🌱 Vegan"),
        ]
        
        with col5:
            time_constraint = st.checkbox("⚡ Under 20min", key="time_filter")
        
        for col, filter_type, label in constraints:
            with col:
                if st.checkbox(label, key=f"{filter_type.name.lower()}_constraint"):
                    active_filters.append(filter_type)
        
        if active_filters or time_constraint:
            constraint_names = [f.value for f in active_filters]
            if time_constraint:
                constraint_names.append("⚡ Quick Service")
            
            st.info(f"**Active Constraints:** {' • '.join(constraint_names)}")
        
        return active_filters, time_constraint, time_constraint
    
    @staticmethod
    def render_decision_cards(decisions: Dict[str, Any]) -> None:
        """Render professional decision cards in 3-column layout"""
        st.markdown("### 🏆 Executive Decision Matrix")
        
        col1, col2, col3 = st.columns(3)
        
        # Winner Card
        with col1:
            ExecutiveDashboard._render_winner_card(decisions['winner'])
        
        # Alternative Card
        with col2:
            ExecutiveDashboard._render_alternative_card(decisions['alternative'])
        
        # Compromise Card
        with col3:
            ExecutiveDashboard._render_compromise_card(decisions['compromise'])
    
    @staticmethod
    def _render_winner_card(winner_data: Dict[str, Any]):
        """Render the winner decision card"""
        st.markdown(f"""
        <div style="
            background: white;
            border: 2px solid #10B981;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
            height: 300px;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="
                    background: #10B981;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 0.9em;
                ">OPTIMAL CHOICE</div>
                <div style="margin-left: auto; font-size: 1.2em;">🏆</div>
            </div>
            
            <h3 style="margin: 0 0 10px 0; color: #1f2937;">{winner_data['name']}</h3>
            <p style="color: #6b7280; font-size: 0.9em; margin-bottom: 15px;">{winner_data['description']}</p>
            
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-size: 0.8em; color: #6b7280;">Health Score</span>
                    <span style="font-weight: bold; color: #10B981;">{winner_data['health_score']}/10</span>
                </div>
                <div style="background: #f3f4f6; height: 6px; border-radius: 3px;">
                    <div style="
                        background: #10B981;
                        height: 6px;
                        border-radius: 3px;
                        width: {winner_data['health_score'] * 10}%;
                    "></div>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-size: 0.8em; color: #6b7280;">Taste Score</span>
                    <span style="font-weight: bold; color: #f97316;">{winner_data['taste_score']}/10</span>
                </div>
                <div style="background: #f3f4f6; height: 6px; border-radius: 3px;">
                    <div style="
                        background: #f97316;
                        height: 6px;
                        border-radius: 3px;
                        width: {winner_data['taste_score'] * 10}%;
                    "></div>
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
                <span style="font-weight: bold; color: #10B981; font-size: 1.1em;">{winner_data['confidence']}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_alternative_card(alt_data: Dict[str, Any]):
        """Render the alternative choice card"""
        st.markdown(f"""
        <div style="
            background: white;
            border: 2px solid #6366f1;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.1);
            height: 300px;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="
                    background: #6366f1;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 0.9em;
                ">ALTERNATIVE</div>
                <div style="margin-left: auto; font-size: 1.2em;">🔄</div>
            </div>
            
            <h3 style="margin: 0 0 10px 0; color: #1f2937;">{alt_data['name']}</h3>
            <p style="color: #6b7280; font-size: 0.9em; margin-bottom: 15px;">{alt_data['description']}</p>
            
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-size: 0.8em; color: #6b7280;">Health Score</span>
                    <span style="font-weight: bold; color: #10B981;">{alt_data['health_score']}/10</span>
                </div>
                <div style="background: #f3f4f6; height: 6px; border-radius: 3px;">
                    <div style="
                        background: #10B981;
                        height: 6px;
                        border-radius: 3px;
                        width: {alt_data['health_score'] * 10}%;
                    "></div>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-size: 0.8em; color: #6b7280;">Taste Score</span>
                    <span style="font-weight: bold; color: #f97316;">{alt_data['taste_score']}/10</span>
                </div>
                <div style="background: #f3f4f6; height: 6px; border-radius: 3px;">
                    <div style="
                        background: #f97316;
                        height: 6px;
                        border-radius: 3px;
                        width: {alt_data['taste_score'] * 10}%;
                    "></div>
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
                <span style="font-weight: bold; color: #6366f1; font-size: 1.1em;">{alt_data['confidence']}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_compromise_card(comp_data: Dict[str, Any]):
        """Render the compromise choice card"""
        st.markdown(f"""
        <div style="
            background: white;
            border: 2px solid #f59e0b;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 16px rgba(245, 158, 11, 0.1);
            height: 300px;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="
                    background: #f59e0b;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 0.9em;
                ">COMPROMISE</div>
                <div style="margin-left: auto; font-size: 1.2em;">⚖️</div>
            </div>
            
            <h3 style="margin: 0 0 10px 0; color: #1f2937;">{comp_data['name']}</h3>
            <p style="color: #6b7280; font-size: 0.9em; margin-bottom: 15px;">{comp_data['description']}</p>
            
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-size: 0.8em; color: #6b7280;">Health Score</span>
                    <span style="font-weight: bold; color: #10B981;">{comp_data['health_score']}/10</span>
                </div>
                <div style="background: #f3f4f6; height: 6px; border-radius: 3px;">
                    <div style="
                        background: #10B981;
                        height: 6px;
                        border-radius: 3px;
                        width: {comp_data['health_score'] * 10}%;
                    "></div>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-size: 0.8em; color: #6b7280;">Taste Score</span>
                    <span style="font-weight: bold; color: #f97316;">{comp_data['taste_score']}/10</span>
                </div>
                <div style="background: #f3f4f6; height: 6px; border-radius: 3px;">
                    <div style="
                        background: #f97316;
                        height: 6px;
                        border-radius: 3px;
                        width: {comp_data['taste_score'] * 10}%;
                    "></div>
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
                <span style="font-weight: bold; color: #f59e0b; font-size: 1.1em;">{comp_data['confidence']}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_trade_off_radar(winner_data: Dict[str, Any]) -> None:
        """Render professional radar chart for trade-off analysis"""
        st.markdown("### 📊 Multi-Dimensional Trade-off Analysis")
        
        # Create radar chart
        categories = ['Health', 'Taste', 'Satiety', 'Value', 'Speed']
        values = [
            winner_data['health_score'],
            winner_data['taste_score'], 
            winner_data.get('satiety_score', 7),
            winner_data.get('value_score', 8),
            winner_data.get('speed_score', 6)
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
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_veto_log(vetoed_items: List[str], reasons: List[str]) -> None:
        """Render professional veto log"""
        if not vetoed_items:
            return
            
        st.markdown("### 🚫 Executive Veto Log")
        st.markdown("*Items excluded due to hard constraints*")
        
        for item, reason in zip(vetoed_items, reasons):
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
    
    @staticmethod
    def render_executive_summary(decisions: Dict[str, Any]) -> None:
        """Render executive summary with key insights"""
        st.markdown("### 📋 Executive Summary")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            **Decision Rationale:** {decisions['reasoning']}
            
            **Key Trade-offs:**
            - Sacrificed {decisions['trade_offs']['sacrificed']} to gain {decisions['trade_offs']['gained']}
            - Risk assessment: {decisions['risk_level']}
            - Alignment with preferences: {decisions['alignment_score']}%
            """)
        
        with col2:
            # Key metrics
            st.metric("Decision Confidence", f"{decisions['winner']['confidence']}%")
            st.metric("Options Analyzed", decisions['total_options'])
            st.metric("Constraints Applied", len(decisions.get('active_constraints', [])))
    
    @staticmethod
    def render_professional_css():
        """Render professional executive styling"""
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: #1f2937;
        }
        
        .stSelectbox > div > div {
            background-color: white;
            border: 1px solid #d1d5db;
            border-radius: 8px;
        }
        
        .stCheckbox > label {
            font-size: 0.9em;
            color: #374151;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #1e293b, #334155);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            padding: 0.5rem 2rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .stTextArea > div > div > textarea {
            background-color: white;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
        }
        
        .stInfo {
            background-color: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 8px;
        }
        
        .stSuccess {
            background-color: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 8px;
        }
        
        .stError {
            background-color: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)