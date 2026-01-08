#!/usr/bin/env python3
"""
Quick test script for BiteBalance functionality
"""

import os
from dotenv import load_dotenv
from src.referee import AIReferee
from src.models import SteeringMode

def test_basic_functionality():
    """Test basic AI referee functionality"""
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No GEMINI_API_KEY found in .env file")
        return False
    
    print("🧪 Testing BiteBalance AI Referee...")
    
    # Sample menu
    test_menu = """
    1. Caesar Salad - $12 - Romaine lettuce, parmesan, croutons, caesar dressing
    2. Bacon Cheeseburger - $16 - Beef patty, bacon, cheese, fries
    3. Grilled Salmon - $22 - Atlantic salmon, quinoa, steamed vegetables
    4. Chocolate Lava Cake - $8 - Warm chocolate cake with vanilla ice cream
    """
    
    referee = AIReferee(api_key)
    
    # Test Zen Mode
    print("\n🧘‍♂️ Testing Zen Mode...")
    zen_decision = referee.make_decision(test_menu, SteeringMode.ZEN)
    print(f"Winner: {zen_decision['winner']}")
    print(f"Health: {zen_decision['health_score']}/10, Taste: {zen_decision['taste_score']}/10")
    
    # Test Gremlin Mode
    print("\n😈 Testing Gremlin Mode...")
    gremlin_decision = referee.make_decision(test_menu, SteeringMode.GREMLIN)
    print(f"Winner: {gremlin_decision['winner']}")
    print(f"Health: {gremlin_decision['health_score']}/10, Taste: {gremlin_decision['taste_score']}/10")
    
    print("\n✅ Basic functionality test completed!")
    return True

if __name__ == "__main__":
    test_basic_functionality()