from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum

class SteeringMode(Enum):
    ZEN = "Zen Mode"
    GREMLIN = "Gremlin Mode"

class SteeringAxis(Enum):
    NUTRITION_INDULGENCE = "nutrition_indulgence"
    BUDGET_PREMIUM = "budget_premium"

class AllergyFilter(Enum):
    NUTS = "🥜 No Nuts"
    GLUTEN = "🌾 Gluten-Free" 
    DAIRY = "🥛 Dairy-Free"
    VEGAN = "🌱 Vegan"
    QUICK = "⚡ Under 20 mins"

@dataclass
class DecisionMetrics:
    """5-dimensional analysis metrics"""
    health: int  # 1-10
    taste: int   # 1-10  
    satiety: int # 1-10
    price: int   # 1-10 (10 = expensive)
    speed: int   # 1-10 (10 = very fast)

@dataclass
class RefereeChoice:
    """Professional referee recommendation"""
    name: str
    metrics: DecisionMetrics
    confidence: float  # 0-100%
    trade_off_summary: str
    reasoning: str
    category: str  # "optimizer", "alternative", "compromise"

@dataclass
class DecisionIntelligence:
    """Complete decision analysis output"""
    optimizer: RefereeChoice
    alternative: RefereeChoice  
    compromise: RefereeChoice
    vetoed_items: List[Dict[str, str]]  # {"name": str, "reason": str}
    constraint_summary: str
    methodology_note: str

@dataclass
class MenuItem:
    """Represents a single menu item"""
    name: str
    price: Optional[float] = None
    description: str = ""
    health_score: int = 0
    taste_score: int = 0
    final_score: float = 0.0

@dataclass
class RefereeDecision:
    """The AI referee's final decision with parallel universe comparison"""
    winner: str
    health_score: int
    taste_score: int
    verdict: str
    modification: str
    parallel_choice: str = ""
    parallel_explanation: str = ""
    vetoed_items: List[str] = None
    active_filters: List[str] = None

class DualAxisCalculator:
    """Handles dual-axis steering calculations"""
    
    @staticmethod
    def calculate_weighted_score(metrics: DecisionMetrics, nutrition_focus: int, budget_focus: int) -> float:
        """Calculate final score based on dual-axis steering"""
        # Normalize inputs (0-100 to 0-1)
        nutrition_weight = nutrition_focus / 100.0
        budget_weight = budget_focus / 100.0
        
        # Health component (nutrition axis)
        health_component = metrics.health * nutrition_weight
        indulgence_component = metrics.taste * (1 - nutrition_weight)
        
        # Budget component (budget axis) 
        # Higher budget_focus = willing to pay more = price matters less
        budget_component = (10 - metrics.price) * budget_weight
        value_component = metrics.price * (1 - budget_weight)
        
        # Combine with satiety and speed as base factors
        base_score = (metrics.satiety + metrics.speed) / 2
        
        final_score = (
            (health_component + indulgence_component) * 0.4 +
            (budget_component + value_component) * 0.3 +
            base_score * 0.3
        )
        
        return final_score
    
    @staticmethod
    def get_axis_description(nutrition_focus: int, budget_focus: int) -> Dict[str, str]:
        """Get descriptions for current axis positions"""
        
        # Nutrition axis descriptions
        if nutrition_focus <= 20:
            nutrition_desc = "Clinical Nutrition"
            nutrition_color = "#059669"
        elif nutrition_focus <= 40:
            nutrition_desc = "Health Conscious"
            nutrition_color = "#10B981"
        elif nutrition_focus <= 60:
            nutrition_desc = "Moderate Balance"
            nutrition_color = "#6B7280"
        elif nutrition_focus <= 80:
            nutrition_desc = "Comfort Seeking"
            nutrition_color = "#F59E0B"
        else:
            nutrition_desc = "Pure Hedonism"
            nutrition_color = "#EF4444"
        
        # Budget axis descriptions
        if budget_focus <= 20:
            budget_desc = "Economy Focus"
            budget_color = "#6B7280"
        elif budget_focus <= 40:
            budget_desc = "Budget Conscious"
            budget_color = "#10B981"
        elif budget_focus <= 60:
            budget_desc = "Standard Range"
            budget_color = "#3B82F6"
        elif budget_focus <= 80:
            budget_desc = "Premium Willing"
            budget_color = "#8B5CF6"
        else:
            budget_desc = "Fine Dining"
            budget_color = "#F59E0B"
        
        return {
            "nutrition_desc": nutrition_desc,
            "nutrition_color": nutrition_color,
            "budget_desc": budget_desc,
            "budget_color": budget_color
        }

class ProfessionalAnalyzer:
    """Professional-grade menu analysis engine"""
    
    @staticmethod
    def analyze_menu_item(item_text: str) -> DecisionMetrics:
        """Analyze a menu item and return 5D metrics"""
        item_lower = item_text.lower()
        
        # Health analysis (1-10)
        health_keywords = ['salad', 'grilled', 'steamed', 'quinoa', 'salmon', 'lean', 'vegetables', 'fruit', 'whole grain']
        unhealthy_keywords = ['fried', 'deep', 'butter', 'cream', 'sugar', 'processed']
        
        health_score = 5  # baseline
        health_score += sum(1 for kw in health_keywords if kw in item_lower)
        health_score -= sum(1 for kw in unhealthy_keywords if kw in item_lower)
        health_score = max(1, min(10, health_score))
        
        # Taste analysis (1-10)
        taste_keywords = ['cheese', 'bacon', 'chocolate', 'sauce', 'crispy', 'rich', 'decadent', 'signature']
        bland_keywords = ['plain', 'steamed', 'boiled']
        
        taste_score = 5  # baseline
        taste_score += sum(1 for kw in taste_keywords if kw in item_lower)
        taste_score -= sum(1 for kw in bland_keywords if kw in item_lower)
        taste_score = max(1, min(10, taste_score))
        
        # Satiety analysis (1-10)
        filling_keywords = ['protein', 'meat', 'pasta', 'rice', 'bread', 'burger', 'large']
        light_keywords = ['salad', 'soup', 'appetizer', 'small']
        
        satiety_score = 5  # baseline
        satiety_score += sum(1 for kw in filling_keywords if kw in item_lower)
        satiety_score -= sum(1 for kw in light_keywords if kw in item_lower)
        satiety_score = max(1, min(10, satiety_score))
        
        # Price analysis (1-10, where 10 = expensive)
        expensive_keywords = ['lobster', 'truffle', 'wagyu', 'premium', 'organic', 'artisan']
        cheap_keywords = ['basic', 'simple', 'classic']
        
        price_score = 5  # baseline
        price_score += sum(2 for kw in expensive_keywords if kw in item_lower)
        price_score -= sum(1 for kw in cheap_keywords if kw in item_lower)
        price_score = max(1, min(10, price_score))
        
        # Speed analysis (1-10, where 10 = very fast)
        fast_keywords = ['sandwich', 'wrap', 'salad', 'ready', 'quick']
        slow_keywords = ['braised', 'slow', 'roasted', 'baked']
        
        speed_score = 5  # baseline
        speed_score += sum(1 for kw in fast_keywords if kw in item_lower)
        speed_score -= sum(1 for kw in slow_keywords if kw in item_lower)
        speed_score = max(1, min(10, speed_score))
        
        return DecisionMetrics(
            health=health_score,
            taste=taste_score,
            satiety=satiety_score,
            price=price_score,
            speed=speed_score
        )

class PromptBuilder:
    """Builds AI prompts based on steering mode"""
    
    @staticmethod
    def build_system_prompt(mode: SteeringMode, budget_limit: Optional[float] = None) -> str:
        """Build the system prompt for the AI referee"""
        
        base_prompt = "You are the BiteBalance Referee. Your job is to select the perfect meal from a menu based on a specific user 'Steering Mode.'"
        
        if mode == SteeringMode.ZEN:
            mode_prompt = """
            ZEN MODE: You are a strict health coach. Prioritize high protein, low calorie, and whole ingredients. 
            Veto anything fried or sugar-heavy. Look for grilled, steamed, or raw preparations.
            
            Analyze the menu and select the healthiest option that still has decent taste appeal.
            """
        else:
            mode_prompt = """
            GREMLIN MODE: You are a foodie on a mission to find the tastiest meal. 
            Prioritize signature dishes, rich sauces, and 'crave-able' textures. 
            Veto boring salads and plain preparations.
            
            Analyze the menu and select the most delicious, indulgent option.
            """
        
        output_format = """
        You must return your decision in this exact JSON format:
        {
            "winner": "Dish Name",
            "health_score": 8,
            "taste_score": 6,
            "verdict": "Brief explanation of how you balanced the trade-off. Mention at least one item you REJECTED because it didn't fit the mode.",
            "modification": "One tip to make the dish even better for the selected mode."
        }
        """
        
        budget_constraint = ""
        if budget_limit:
            budget_constraint = f"\n\nBUDGET CONSTRAINT: Only consider items under ${budget_limit}."
        
        return f"{base_prompt}\n{mode_prompt}\n{output_format}{budget_constraint}"

class AllergyChecker:
    """Checks menu items against allergy filters"""
    
    ALLERGY_KEYWORDS = {
        AllergyFilter.NUTS: ['nut', 'almond', 'peanut', 'walnut', 'pecan', 'cashew', 'pistachio'],
        AllergyFilter.GLUTEN: ['wheat', 'bread', 'pasta', 'flour', 'gluten', 'bun', 'crust'],
        AllergyFilter.DAIRY: ['milk', 'cheese', 'butter', 'cream', 'yogurt', 'dairy'],
        AllergyFilter.VEGAN: ['meat', 'chicken', 'beef', 'pork', 'fish', 'salmon', 'cheese', 'milk', 'egg']
    }
    
    @staticmethod
    def violates_filter(item_text: str, allergy_filter: AllergyFilter) -> bool:
        """Check if an item violates an allergy filter"""
        item_lower = item_text.lower()
        keywords = AllergyChecker.ALLERGY_KEYWORDS[allergy_filter]
        return any(keyword in item_lower for keyword in keywords)
    
    @staticmethod
    def get_safe_items(items: List[str], active_filters: List[AllergyFilter]) -> List[str]:
        """Filter items that are safe given active allergy filters"""
        safe_items = []
        for item in items:
            is_safe = True
            for allergy_filter in active_filters:
                if AllergyChecker.violates_filter(item, allergy_filter):
                    is_safe = False
                    break
            if is_safe:
                safe_items.append(item)
        return safe_items

class ScoreCalculator:
    """Handles scoring logic based on steering mode"""
    
    @staticmethod
    def calculate_final_score(health_score: int, taste_score: int, mode: SteeringMode) -> float:
        """Calculate final score based on steering mode weights"""
        if mode == SteeringMode.ZEN:
            # Zen Mode: 80% health, 20% taste
            return (health_score * 0.8) + (taste_score * 0.2)
        else:  # Gremlin Mode
            # Gremlin Mode: 10% health, 90% taste
            return (health_score * 0.1) + (taste_score * 0.9)
    
    @staticmethod
    def get_mode_description(mode: SteeringMode) -> dict:
        """Get mode-specific descriptions and styling"""
        if mode == SteeringMode.ZEN:
            return {
                "icon": "⚖️",
                "title": "Pure Discipline",
                "description": "Referee is prioritizing Longevity & Macros",
                "color": "#10B981",
                "bg_color": "#3B82F6",
                "focus": "high protein, low calorie, whole ingredients",
                "tone": "clinical"
            }
        else:
            return {
                "icon": "🔥",
                "title": "Full Cheat Day", 
                "description": "Referee is prioritizing Umami & Dopamine",
                "color": "#F97316",
                "bg_color": "#F59E0B",
                "focus": "signature dishes, rich sauces, crave-able textures",
                "tone": "enthusiastic"
            }

class MenuParser:
    """Parses menu text into structured data"""
    
    @staticmethod
    def parse_menu_text(menu_text: str) -> List[str]:
        """Extract menu items from raw text"""
        lines = menu_text.strip().split('\n')
        items = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove numbering if present
                if line[0].isdigit() and '.' in line[:5]:
                    line = line.split('.', 1)[1].strip()
                items.append(line)
        
        return items
    
    @staticmethod
    def extract_price(item_text: str) -> Optional[float]:
        """Extract price from item text if present"""
        import re
        price_match = re.search(r'\$(\d+(?:\.\d{2})?)', item_text)
        if price_match:
            return float(price_match.group(1))
        return None