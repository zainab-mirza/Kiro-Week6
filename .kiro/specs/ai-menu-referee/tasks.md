# Implementation Plan: AI Menu Referee

## Overview

Implementation of BiteBalance - an AI-powered menu recommendation system using Streamlit for the frontend and Google Gemini API for intelligent menu analysis. The system uses agent steering to balance health and taste preferences.

## Tasks

- [-] 1. Set up project structure and dependencies
  - Create main application file and directory structure
  - Install required packages (streamlit, google-generativeai, python-dotenv)
  - Set up environment configuration for API keys
  - _Requirements: 6.1, 6.4_

- [ ] 2. Implement core data models and types
  - [ ] 2.1 Create MenuItem and ScoredItem dataclasses
    - Define data structures for menu items and scoring results
    - _Requirements: 7.1, 3.1_
  
  - [ ] 2.2 Create SteringMode enum and AnalysisResult dataclass
    - Define mode enumeration and API response structure
    - _Requirements: 1.1, 6.4_

- [ ] 3. Build menu parsing functionality
  - [ ] 3.1 Implement MenuParser class
    - Write text parsing logic to extract menu items from raw input
    - Handle various menu formats and clean item names
    - _Requirements: 2.2, 7.2, 7.3_
  
  - [ ]* 3.2 Write property test for menu parsing
    - **Property 3: Menu Parsing Completeness**
    - **Validates: Requirements 2.2, 7.1**

- [ ] 4. Create Gemini API integration
  - [ ] 4.1 Implement GeminiClient class
    - Set up API client with proper authentication
    - Create prompt formatting for different steering modes
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [ ] 4.2 Add error handling and response parsing
    - Handle API timeouts, rate limits, and malformed responses
    - Parse structured output from Gemini API
    - _Requirements: 6.5, 6.4_
  
  - [ ]* 4.3 Write property tests for API integration
    - **Property 11: Prompt Mode Injection**
    - **Property 14: Structured Output Format**
    - **Validates: Requirements 6.1, 6.4**

- [ ] 5. Implement scoring engine
  - [ ] 5.1 Create ScoringEngine class
    - Implement mode-based weight calculations
    - Apply Zen and Gremlin mode formulas
    - _Requirements: 3.2, 3.3, 3.4_
  
  - [ ]* 5.2 Write property tests for scoring formulas
    - **Property 7: Zen Mode Scoring Formula**
    - **Property 8: Gremlin Mode Scoring Formula**
    - **Property 9: Winner Selection Correctness**
    - **Validates: Requirements 3.2, 3.3, 3.4**

- [ ] 6. Build Streamlit user interface
  - [ ] 6.1 Create main app layout and mode selector
    - Implement three-zone layout (header, input, results)
    - Add sliding toggle for Zen/Gremlin modes with icons
    - _Requirements: 1.1, 1.2, 1.3, 5.2_
  
  - [ ] 6.2 Implement menu input area
    - Add text area for menu dump with placeholder text
    - Create referee button with loading animation
    - _Requirements: 2.1, 2.3, 5.5_
  
  - [ ] 6.3 Create results display components
    - Build winner card, trade-off meters, and reasoning display
    - Add visual styling with green/orange color scheme
    - _Requirements: 4.1, 4.2, 4.3, 5.1_

- [ ]* 6.4 Write property tests for UI components
  - **Property 1: Mode Selection State Consistency**
  - **Property 2: Session State Persistence**
  - **Property 4: UI Feedback Responsiveness**
  - **Validates: Requirements 1.4, 1.5, 5.5**

- [ ] 7. Integrate all components and add error handling
  - [ ] 7.1 Wire together parsing, scoring, and API components
    - Connect menu input to parsing to API to results display
    - Implement end-to-end workflow
    - _Requirements: 2.4, 3.5, 4.5_
  
  - [ ] 7.2 Add comprehensive error handling
    - Handle parsing failures, API errors, and invalid inputs
    - Display user-friendly error messages
    - _Requirements: 2.5, 6.5, 7.4_

- [ ]* 7.3 Write integration tests
  - Test complete user workflows from input to results
  - **Property 5: Error Handling Consistency**
  - **Property 15: API Error Resilience**
  - **Validates: Requirements 2.5, 6.5**

- [ ] 8. Final testing and deployment setup
  - [ ] 8.1 Create requirements.txt and setup instructions
    - Document all dependencies and environment setup
    - Create sample .env file template
    - _Requirements: 6.1_
  
  - [ ] 8.2 Add example menus and usage documentation
    - Create sample restaurant menus for testing
    - Write user guide for the application
    - _Requirements: 7.2_

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Focus on core functionality first, then comprehensive testing