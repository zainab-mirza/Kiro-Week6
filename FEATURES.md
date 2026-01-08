# 🥗 BiteBalance - Feature Overview

## 🎯 Core Concept
**Agent Steering**: The AI completely changes its personality and decision criteria based on your selected mode, creating genuinely different recommendations.

## 🧘‍♂️ Zen Mode (Pure Discipline)
- **Focus**: Health, longevity, macros
- **Prioritizes**: High protein, low calorie, whole ingredients
- **Rejects**: Fried foods, sugar-heavy items, processed foods
- **Scoring**: 80% health weight, 20% taste weight
- **Color**: Emerald Green (#10B981)

## 😈 Gremlin Mode (Full Cheat Day)
- **Focus**: Taste, indulgence, satisfaction
- **Prioritizes**: Signature dishes, rich sauces, crave-able textures
- **Rejects**: Boring salads, plain preparations
- **Scoring**: 10% health weight, 90% taste weight
- **Color**: Flame Orange (#F97316)

## 🎨 Visual Design

### Split-Personality Interface
- **Gradient Header**: Green to Orange representing the spectrum
- **Mode Indicators**: Clear visual feedback for current mode
- **Dynamic Colors**: UI elements change based on selected mode
- **Score Bars**: Visual representation of health vs taste trade-offs

### Layout Structure
1. **Steering Header** (20%): Mode selection and context
2. **Input Zone** (40%): Menu input and controls
3. **Arbiter's Verdict** (40%): Results and analysis

## 🧠 AI Intelligence Features

### Smart Menu Analysis
- Parses various menu formats automatically
- Extracts prices, descriptions, and ingredients
- Handles both restaurant menus and grocery lists

### Scoring System
- **Health Score** (1-10): Nutrition, ingredients, preparation method
- **Taste Score** (1-10): Flavor profile, satisfaction potential
- **Final Score**: Weighted combination based on steering mode

### Decision Reasoning
- Explains why specific items were chosen
- Mentions rejected alternatives and reasoning
- Provides modification tips for the selected mode

## 💰 Advanced Features

### Budget Constraints
- Optional price filtering
- Three-way optimization: Health vs Taste vs Cost
- Smart budget-aware recommendations

### Quality Assessment
- Decision quality ratings
- Mode alignment scoring
- Recommendation confidence levels

## 🛠️ Technical Architecture

### Modular Design
```
src/
├── models.py         # Data structures and enums
├── referee.py        # AI decision logic
└── ui_components.py  # Reusable UI elements
```

### Error Handling
- API failure recovery
- Menu parsing fallbacks
- User-friendly error messages

### Performance
- Efficient API usage
- Responsive UI updates
- Minimal loading times

## 📊 Example Scenarios

### Zen Mode Results
**Menu**: Caesar Salad, Bacon Burger, Grilled Salmon, Chocolate Cake
**Winner**: Grilled Salmon
**Reasoning**: "High protein, omega-3s, minimal processing. Rejected the bacon burger due to high saturated fat."

### Gremlin Mode Results
**Same Menu**
**Winner**: Bacon Burger
**Reasoning**: "Ultimate comfort food with rich flavors and satisfying textures. Rejected the salmon as too 'healthy' for cheat day."

## 🎯 Use Cases

### Restaurant Dining
- Quick decision making from complex menus
- Balance health goals with social dining
- Discover new dishes aligned with your current mindset

### Grocery Shopping
- Meal planning assistance
- Ingredient selection guidance
- Budget-conscious healthy choices

### Meal Prep
- Weekly menu optimization
- Batch cooking decisions
- Nutritional balance planning

## 🚀 Competitive Advantages

1. **True Agent Steering**: Not just filtering, but complete AI personality change
2. **Visual Trade-off Analysis**: Clear understanding of health vs taste decisions
3. **Budget Integration**: Three-dimensional optimization
4. **Explanation AI**: Transparent reasoning for every decision
5. **Dual Personality**: Serves both health-conscious and indulgent mindsets

## 📈 Potential Enhancements

- **Learning System**: Remember user preferences over time
- **Dietary Restrictions**: Allergies, vegetarian, keto, etc.
- **Cuisine Preferences**: Cultural and regional food preferences
- **Social Features**: Share decisions with friends
- **Nutrition Database**: Detailed macro and micronutrient analysis
- **Meal Planning**: Multi-day optimization
- **Restaurant Integration**: Direct menu API connections