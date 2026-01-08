#!/usr/bin/env python3
"""
Test script for BiteBalance Executive Dashboard
"""

from src.decision_engine import DecisionIntelligenceEngine
from src.models import AllergyFilter

def test_executive_functionality():
    """Test the executive decision intelligence engine"""
    
    print("🏆 Testing BiteBalance Executive Decision Intelligence...")
    print("=" * 60)
    
    # Initialize engine
    engine = DecisionIntelligenceEngine()
    
    # Test menu
    test_menu = """
    1. Grilled Atlantic Salmon - $28 - Wild-caught salmon, quinoa pilaf, seasonal vegetables
    2. Wagyu Beef Burger - $24 - Premium wagyu patty, truffle aioli, artisan bun, hand-cut fries
    3. Mediterranean Bowl - $16 - Quinoa, chickpeas, feta, olives, cucumber, tahini dressing
    4. Lobster Risotto - $32 - Maine lobster, arborio rice, white wine, parmesan, herbs
    5. Caesar Salad - $14 - Romaine hearts, house-made croutons, parmesan, anchovy dressing
    6. Chocolate Lava Cake - $12 - Warm chocolate cake, vanilla bean ice cream, berry coulis
    """
    
    # Test Health-Focused Analysis (Nutrition=20, Budget=50)
    print("\n🧘‍♂️ Testing Health-Focused Analysis...")
    health_analysis = engine.analyze_menu(
        menu_text=test_menu,
        nutrition_axis=20,  # Health focused
        budget_axis=50,     # Mid-range budget
        constraints=[],
        time_constraint=False
    )
    
    print(f"Winner: {health_analysis['winner']['name']}")
    print(f"Health Score: {health_analysis['winner']['health_score']}/10")
    print(f"Confidence: {health_analysis['winner']['confidence']}%")
    print(f"Reasoning: {health_analysis['reasoning'][:100]}...")
    
    # Test Indulgence-Focused Analysis (Nutrition=80, Budget=70)
    print("\n😈 Testing Indulgence-Focused Analysis...")
    indulgence_analysis = engine.analyze_menu(
        menu_text=test_menu,
        nutrition_axis=80,  # Indulgence focused
        budget_axis=70,     # Premium budget
        constraints=[],
        time_constraint=False
    )
    
    print(f"Winner: {indulgence_analysis['winner']['name']}")
    print(f"Taste Score: {indulgence_analysis['winner']['taste_score']}/10")
    print(f"Confidence: {indulgence_analysis['winner']['confidence']}%")
    print(f"Reasoning: {indulgence_analysis['reasoning'][:100]}...")
    
    # Test Constraint Enforcement
    print("\n🛡️ Testing Constraint Enforcement...")
    constrained_analysis = engine.analyze_menu(
        menu_text=test_menu,
        nutrition_axis=50,
        budget_axis=50,
        constraints=[AllergyFilter.DAIRY],  # No dairy
        time_constraint=False
    )
    
    print(f"Winner: {constrained_analysis['winner']['name']}")
    print(f"Vetoed Items: {len(constrained_analysis['vetoed_items'])}")
    if constrained_analysis['vetoed_items']:
        print(f"First Veto: {constrained_analysis['vetoed_items'][0]} - {constrained_analysis['veto_reasons'][0]}")
    
    # Test Decision Intelligence Metrics
    print("\n📊 Decision Intelligence Metrics:")
    print(f"Total Options: {health_analysis['total_options']}")
    print(f"Safe Options: {health_analysis['safe_options']}")
    print(f"Risk Level: {health_analysis['risk_level']}")
    print(f"Alignment Score: {health_analysis['alignment_score']}%")
    
    print("\n✅ Executive Dashboard Test Completed Successfully!")
    print("\n🚀 Ready for National Stage Competition!")
    
    return True

if __name__ == "__main__":
    test_executive_functionality()