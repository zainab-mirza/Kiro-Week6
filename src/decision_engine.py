import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Tuple, Any
from .models import SteeringMode, AllergyFilter, AllergyChecker

class DecisionIntelligenceEngine:
    """Professional decision intelligence engine for executive-level analysis"""
    
    def __init__(self):
        self.health_keywords = ['salad', 'grilled', 'steamed', 'quinoa', 'salmon', 'chicken breast', 'vegetables', 'fruit', 'lean', 'organic']
        self.taste_keywords = ['burger', 'pizza', 'chocolate', 'cheese', 'bacon', 'fried', 'cake', 'ice cream', 'sauce', 'crispy', 'truffle']
        self.premium_keywords = ['wagyu', 'truffle', 'lobster', 'caviar', 'aged', 'artisan', 'premium', 'organic', 'imported']
        self.speed_keywords = ['quick', 'fast', 'ready', 'instant', 'express', 'wrap', 'sandwich']
    
    def analyze_menu(self, menu_text: str, nutrition_focus: float, budget_focus: float, 
                    allergy_filters: List[AllergyFilter], budget_limit: float = None) -> Dict[str, Any]:
        """
        Comprehensive menu analysis with executive-level decision intelligence
        
        Args:
            nutrition_focus: 0-100 scale (0=Indulgence, 100=Health)
            budget_focus: 0-100 scale (0=Economy, 100=Premium)
            allergy_filters: Hard constraints
            budget_limit: Maximum price constraint
        """
        
        # Parse and filter menu items
        raw_items = self._parse_menu(menu_text)
        if not raw_items:
            return self._empty_analysis()
        
        # Apply hard constraints
        safe_items, vetoed_items = self._apply_constraints(raw_items, allergy_filters, budget_limit)
        
        if not safe_items:
            return self._no_safe_options(vetoed_items, allergy_filters)
        
        # Score all safe items across multiple dimensions
        scored_items = self._score_items(safe_items)
        
        # Generate three distinct recommendations
        recommendations = self._generate_recommendations(scored_items, nutrition_focus, budget_focus)
        
        # Create decision intelligence output
        return {
            'recommendations': recommendations,
            'vetoed_items': vetoed_items,
            'total_analyzed': len(raw_items),
            'constraints_applied': len(allergy_filters),
            'steering_config': {
                'nutrition_focus': nutrition_focus,
                'budget_focus': budget_focus
            }
        }
    
    def _parse_menu(self, menu_text: str) -> List[str]:
        """Parse menu text into clean items"""
        items = []
        for line in menu_text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                items.append(line)
        return items
    
    def _apply_constraints(self, items: List[str], allergy_filters: List[AllergyFilter], 
                          budget_limit: float = None) -> Tuple[List[str], List[Dict]]:
        """Apply hard constraints and return safe items + veto log"""
        safe_items = []
        vetoed_items = []
        
        for item in items:
            veto_reasons = []
            
            # Check allergy constraints
            for allergy_filter in allergy_filters:
                if AllergyChecker.violates_filter(item, allergy_filter):
                    veto_reasons.append(f"Violates {allergy_filter.value} constraint")
            
            # Check budget constraint
            if budget_limit:
                price = self._extract_price(item)
                if price and price > budget_limit:
                    veto_reasons.append(f"Exceeds budget limit (${price} > ${budget_limit})")
            
            if veto_reasons:
                vetoed_items.append({
                    'item': self._clean_item_name(item),
                    'reasons': veto_reasons
                })
            else:
                safe_items.append(item)
        
        return safe_items, vetoed_items
    
    def _score_items(self, items: List[str]) -> List[Dict]:
        """Score items across all dimensions"""
        scored_items = []
        
        for item in items:
            item_lower = item.lower()
            
            # Multi-dimensional scoring
            health_score = min(10, max(1, self._calculate_keyword_score(item_lower, self.health_keywords, base=4)))
            taste_score = min(10, max(1, self._calculate_keyword_score(item_lower, self.taste_keywords, base=4)))
            premium_score = min(10, max(1, self._calculate_keyword_score(item_lower, self.premium_keywords, base=3)))
            speed_score = min(10, max(1, self._calculate_keyword_score(item_lower, self.speed_keywords, base=5)))
            
            # Satiety estimation (based on item characteristics)
            satiety_score = self._estimate_satiety(item_lower)
            
            scored_items.append({
                'item': item,
                'clean_name': self._clean_item_name(item),
                'price': self._extract_price(item),
                'scores': {
                    'health': health_score,
                    'taste': taste_score,
                    'premium': premium_score,
                    'speed': speed_score,
                    'satiety': satiety_score
                }
            })
        
        return scored_items
    
    def _calculate_keyword_score(self, text: str, keywords: List[str], base: int = 3) -> int:
        """Calculate score based on keyword matches"""
        matches = sum(2 for keyword in keywords if keyword in text)
        return base + matches
    
    def _estimate_satiety(self, item_text: str) -> int:
        """Estimate satiety based on item characteristics"""
        satiety_indicators = ['protein', 'meat', 'pasta', 'rice', 'bread', 'burger', 'steak']
        light_indicators = ['salad', 'soup', 'appetizer', 'side']
        
        if any(indicator in item_text for indicator in satiety_indicators):
            return 8
        elif any(indicator in item_text for indicator in light_indicators):
            return 4
        else:
            return 6
    
    def _generate_recommendations(self, scored_items: List[Dict], nutrition_focus: float, 
                                budget_focus: float) -> List[Dict]:
        """Generate three distinct recommendations optimized for different priorities"""
        
        if len(scored_items) < 3:
            # Handle case with fewer than 3 items
            return self._handle_limited_items(scored_items, nutrition_focus, budget_focus)
        
        recommendations = []
        
        # Recommendation 1: Optimized for current steering
        primary = self._find_optimal_choice(scored_items, nutrition_focus, budget_focus)
        recommendations.append(self._create_recommendation(primary, "Primary Choice", nutrition_focus, budget_focus))
        
        # Recommendation 2: Health-optimized alternative
        health_optimal = self._find_health_optimal(scored_items, exclude=[primary])
        recommendations.append(self._create_recommendation(health_optimal, "Health Optimized", 90, budget_focus))
        
        # Recommendation 3: Taste-optimized alternative
        taste_optimal = self._find_taste_optimal(scored_items, exclude=[primary, health_optimal])
        recommendations.append(self._create_recommendation(taste_optimal, "Indulgence Choice", 10, budget_focus))
        
        return recommendations
    
    def _find_optimal_choice(self, items: List[Dict], nutrition_focus: float, budget_focus: float) -> Dict:
        """Find optimal choice based on current steering configuration"""
        best_item = None
        best_score = -1
        
        for item in items:
            scores = item['scores']
            
            # Calculate weighted score based on steering
            health_weight = nutrition_focus / 100
            taste_weight = 1 - health_weight
            premium_weight = budget_focus / 100
            economy_weight = 1 - premium_weight
            
            # Composite scoring
            primary_score = (scores['health'] * health_weight) + (scores['taste'] * taste_weight)
            budget_score = (scores['premium'] * premium_weight) + ((10 - scores['premium']) * economy_weight)
            
            final_score = (primary_score * 0.7) + (budget_score * 0.2) + (scores['satiety'] * 0.1)
            
            if final_score > best_score:
                best_score = final_score
                best_item = item
        
        return best_item
    
    def _find_health_optimal(self, items: List[Dict], exclude: List[Dict] = None) -> Dict:
        """Find health-optimized choice"""
        exclude = exclude or []
        exclude_names = [item['clean_name'] for item in exclude]
        
        best_item = None
        best_health = -1
        
        for item in items:
            if item['clean_name'] in exclude_names:
                continue
            
            if item['scores']['health'] > best_health:
                best_health = item['scores']['health']
                best_item = item
        
        return best_item or items[0]  # Fallback
    
    def _find_taste_optimal(self, items: List[Dict], exclude: List[Dict] = None) -> Dict:
        """Find taste-optimized choice"""
        exclude = exclude or []
        exclude_names = [item['clean_name'] for item in exclude]
        
        best_item = None
        best_taste = -1
        
        for item in items:
            if item['clean_name'] in exclude_names:
                continue
            
            if item['scores']['taste'] > best_taste:
                best_taste = item['scores']['taste']
                best_item = item
        
        return best_item or items[0]  # Fallback
    
    def _create_recommendation(self, item: Dict, category: str, nutrition_focus: float, 
                             budget_focus: float) -> Dict:
        """Create a professional recommendation with confidence metrics"""
        if not item:
            return self._empty_recommendation(category)
        
        scores = item['scores']
        
        # Calculate confidence based on score alignment with preferences
        health_alignment = scores['health'] / 10 if nutrition_focus > 50 else (10 - scores['health']) / 10
        taste_alignment = scores['taste'] / 10 if nutrition_focus < 50 else (10 - scores['taste']) / 10
        confidence = int((health_alignment + taste_alignment) * 50)
        
        # Generate trade-off analysis
        trade_offs = self._analyze_trade_offs(scores, nutrition_focus)
        
        return {
            'name': item['clean_name'],
            'category': category,
            'scores': scores,
            'confidence': confidence,
            'price': item.get('price'),
            'trade_offs': trade_offs,
            'reasoning': self._generate_reasoning(item, category, nutrition_focus, budget_focus)
        }
    
    def _analyze_trade_offs(self, scores: Dict, nutrition_focus: float) -> str:
        """Generate trade-off analysis"""
        if nutrition_focus > 70:
            return f"Prioritized health ({scores['health']}/10) over indulgence ({scores['taste']}/10)"
        elif nutrition_focus < 30:
            return f"Prioritized taste satisfaction ({scores['taste']}/10) over nutrition ({scores['health']}/10)"
        else:
            return f"Balanced approach: Health {scores['health']}/10, Taste {scores['taste']}/10"
    
    def _generate_reasoning(self, item: Dict, category: str, nutrition_focus: float, 
                          budget_focus: float) -> str:
        """Generate executive-level reasoning"""
        scores = item['scores']
        name = item['clean_name']
        
        if category == "Primary Choice":
            return f"Optimal alignment with your preferences. Delivers {scores['health']}/10 nutritional value and {scores['taste']}/10 satisfaction rating."
        elif category == "Health Optimized":
            return f"Maximum nutritional density at {scores['health']}/10. Ideal for long-term wellness objectives."
        else:  # Indulgence Choice
            return f"Peak satisfaction experience at {scores['taste']}/10. Perfect for reward-based dining."
    
    def create_radar_chart(self, recommendation: Dict) -> go.Figure:
        """Create professional radar chart for trade-off visualization"""
        scores = recommendation['scores']
        
        categories = ['Health', 'Taste', 'Premium', 'Speed', 'Satiety']
        values = [scores['health'], scores['taste'], scores['premium'], scores['speed'], scores['satiety']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=recommendation['name'],
            line_color='#10B981',
            fillcolor='rgba(16, 185, 129, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        return fig
    
    def _extract_price(self, item: str) -> float:
        """Extract price from item text"""
        import re
        price_match = re.search(r'\$(\d+(?:\.\d{2})?)', item)
        return float(price_match.group(1)) if price_match else None
    
    def _clean_item_name(self, item: str) -> str:
        """Clean item name for display"""
        clean = item.split('-')[0].strip()
        if clean and clean[0].isdigit() and '.' in clean[:5]:
            clean = clean.split('.', 1)[1].strip()
        return clean or item
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            'recommendations': [],
            'vetoed_items': [],
            'total_analyzed': 0,
            'constraints_applied': 0,
            'steering_config': {'nutrition_focus': 50, 'budget_focus': 50}
        }
    
    def _no_safe_options(self, vetoed_items: List[Dict], allergy_filters: List[AllergyFilter]) -> Dict:
        """Handle case with no safe options"""
        return {
            'recommendations': [],
            'vetoed_items': vetoed_items,
            'total_analyzed': len(vetoed_items),
            'constraints_applied': len(allergy_filters),
            'error': "All menu items were vetoed due to safety constraints"
        }
    
    def _handle_limited_items(self, items: List[Dict], nutrition_focus: float, budget_focus: float) -> List[Dict]:
        """Handle case with limited items"""
        recommendations = []
        for i, item in enumerate(items):
            category = ["Primary Choice", "Alternative", "Backup"][i] if i < 3 else "Option"
            recommendations.append(self._create_recommendation(item, category, nutrition_focus, budget_focus))
        return recommendations
    
    def _empty_recommendation(self, category: str) -> Dict:
        """Create empty recommendation"""
        return {
            'name': 'No suitable option',
            'category': category,
            'scores': {'health': 0, 'taste': 0, 'premium': 0, 'speed': 0, 'satiety': 0},
            'confidence': 0,
            'price': None,
            'trade_offs': 'Insufficient options available',
            'reasoning': 'Unable to generate recommendation due to constraints'
        }