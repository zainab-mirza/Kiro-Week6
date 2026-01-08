# Requirements Document

## Introduction

BiteBalance is an AI-powered menu recommendation system that acts as a "referee" between health goals and flavor cravings. The system uses Agent Steering to dynamically adjust recommendation priorities based on user-selected modes, helping users make informed food choices from restaurant menus or grocery lists.

## Glossary

- **System**: The BiteBalance application
- **Referee**: The AI component that analyzes and recommends menu items
- **Steering_Mode**: User-selected preference mode (Zen or Gremlin)
- **Menu_Dump**: Raw text input containing menu items or grocery lists
- **Health_Score**: Numerical rating (1-10) for nutritional value
- **Taste_Score**: Numerical rating (1-10) for flavor appeal
- **Final_Score**: Calculated recommendation score based on steering weights
- **Trade_Off_Meter**: Visual representation of health vs taste scoring
- **Winner_Card**: Display component showing the top recommended item

## Requirements

### Requirement 1: Mode Selection Interface

**User Story:** As a user, I want to select between health-focused and taste-focused modes, so that I can get recommendations aligned with my current priorities.

#### Acceptance Criteria

1. THE System SHALL display a central sliding toggle for mode selection
2. WHEN Zen Mode is selected, THE System SHALL show a lotus icon and "Pure Discipline" label in green
3. WHEN Gremlin Mode is selected, THE System SHALL show a devil icon and "Full Cheat Day" label in orange/red
4. WHEN a mode is selected, THE System SHALL update the context indicator text accordingly
5. THE System SHALL persist the selected mode throughout the session

### Requirement 2: Menu Input Processing

**User Story:** As a user, I want to paste restaurant menus or grocery lists, so that I can get recommendations from available options.

#### Acceptance Criteria

1. THE System SHALL provide a clean text area for menu input
2. WHEN menu text is pasted, THE System SHALL parse it into structured menu items
3. WHEN the Referee button is clicked, THE System SHALL display a "thinking" animation
4. THE System SHALL handle various menu formats and extract item names
5. IF parsing fails, THEN THE System SHALL display a helpful error message

### Requirement 3: AI Scoring and Recommendation Engine

**User Story:** As a user, I want the AI to score menu items based on my selected mode, so that I receive personalized recommendations.

#### Acceptance Criteria

1. THE Referee SHALL assign Health_Score and Taste_Score (1-10) to each menu item
2. WHEN Zen Mode is active, THE Referee SHALL calculate Final_Score as (Health_Score × 0.8) + (Taste_Score × 0.2)
3. WHEN Gremlin Mode is active, THE Referee SHALL calculate Final_Score as (Health_Score × 0.1) + (Taste_Score × 0.9)
4. THE Referee SHALL select the item with the highest Final_Score as the winner
5. THE Referee SHALL generate justification explaining the selection reasoning

### Requirement 4: Results Display and Visualization

**User Story:** As a user, I want to see the recommended item with clear scoring and reasoning, so that I understand why it was chosen.

#### Acceptance Criteria

1. THE System SHALL display the winning item in a highlighted Winner_Card
2. THE System SHALL show Trade_Off_Meter with separate health and taste progress bars
3. THE System SHALL display the Referee's logic explaining the choice
4. THE System SHALL mention at least one rejected item in the explanation
5. THE System SHALL provide a modification tip to improve the dish for the selected mode

### Requirement 5: Visual Design and User Experience

**User Story:** As a user, I want an intuitive interface with clear visual feedback, so that I can easily navigate between health and indulgence priorities.

#### Acceptance Criteria

1. THE System SHALL use a split-personality color palette with emerald green and flame orange
2. THE System SHALL organize the interface into three zones: Steering Header (20%), Input Zone (40%), and Results (40%)
3. WHEN results are generated, THE System SHALL reveal the verdict section smoothly
4. THE System SHALL maintain consistent visual hierarchy and contrast
5. THE System SHALL provide immediate visual feedback for all user interactions

### Requirement 6: LLM Integration and Prompt Engineering

**User Story:** As a system administrator, I want consistent AI behavior across different modes, so that recommendations are reliable and explainable.

#### Acceptance Criteria

1. THE System SHALL inject the current Steering_Mode into the LLM prompt
2. WHEN in Zen Mode, THE Referee SHALL prioritize high protein, low calorie, and whole ingredients
3. WHEN in Gremlin Mode, THE Referee SHALL prioritize signature dishes, rich sauces, and crave-able textures
4. THE Referee SHALL return structured output with Winner, Health_Score, Taste_Score, Verdict, and Modification
5. THE System SHALL handle LLM API errors gracefully with user-friendly messages

### Requirement 7: Menu Item Analysis and Parsing

**User Story:** As a user, I want the system to understand various menu formats, so that I can use it with different restaurants and grocery stores.

#### Acceptance Criteria

1. THE Parser SHALL extract individual menu items from unstructured text
2. THE Parser SHALL handle common menu formats including prices, descriptions, and categories
3. THE Parser SHALL identify dish names even when mixed with other text
4. WHEN menu items cannot be parsed, THE System SHALL request clearer input
5. THE Parser SHALL maintain item context and descriptions for accurate scoring