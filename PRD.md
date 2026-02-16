# Problems + Target Users

Restaurant menus frequently present comprehension challenges due to small font sizes, ambiguous descriptions, insufficient accessibility features, and language barriers. Seniors, individuals with visual impairments, non-English speakers, and diners with dietary restrictions often encounter difficulties identifying safe and appropriate menu options efficiently. These challenges contribute to user frustration, potential safety risks such as allergen exposure, and increased demands on restaurant staff to clarify menu items. Menu Buddy seeks to address these issues by enhancing menu accessibility, clarity, and safety through the implementation of AI-powered question answering.

---

# Goal / Success Metrics

The primary objective of Menu Buddy is to enhance menu accessibility and safety by providing accurate, evidence-based AI-powered question answering.

Success will be measured using the following outcomes:

## Answer Accuracy (Grounded Question and Answer Quality)

At least 85% of menu-related questions should be answered correctly, relying exclusively on extracted menu data as validated through manual evaluation.

The hallucination rate, defined as answers not supported by menu text, should be reduced to below 10% during testing.

## Time Saved per User Task

Users should be able to locate relevant menu information in under 30 seconds on average, compared to manual menu scanning.

## User Satisfaction and Usability

Achieve an average user satisfaction score of 4 out of 5 or higher in small pilot testing (survey-based feedback).

At least 70% of test users should report that Menu Buddy facilitated easier menu navigation.

---

# MVP User Stories

- As a senior diner, I want to ask straightforward questions about the menu in clear language, so that I can efficiently understand which dishes are available without needing to read small or complex text.

- As a non-English speaker, I want to ask questions in my preferred language, so that I can comprehend menu options without encountering language barriers.

- As a visually impaired user, I want the system to read aloud or summarize menu items clearly, so that I can independently access menu information.

- As a diner with food allergies, I want to inquire whether a dish contains specific ingredients, so that I can avoid making unsafe food choices.

- As a health-conscious diner, I want to receive recommendations based on dietary preferences such as vegetarian or low-carbohydrate options, so that I can select meals that align with my needs.

- As a restaurant staff member, I want the system to automatically answer common menu questions, so that I can minimize repetitive explanations and concentrate on providing service.

---

# MVP Scopes vs Non.Goals

## Menu Extraction & Cleaning

The system scrapes and extracts menu text from webpages, structuring it into usable data such as dish names, descriptions, and categories.

## LLM + RAG-Based Q&A

The system answers natural-language questions from users, providing responses grounded exclusively in the extracted menu data.

## Basic Dietary & Allergy Keyword Handling

The system responds to common dietary and allergy-related questions, such as those concerning vegetarian options, gluten, or nuts, using available menu information.

## Simple Recommendation Logic

The system recommends menu items based on user preferences specified in the query, such as spiciness or vegetarian options.

## Basic Web Interface

A basic web interface provides a text input box and answer display, connected to the Python backend.

## QR Code Menu Access

Users access a restaurant’s public menu webpage by scanning a QR code.

---

# Nice to Have

- Support for multi-language translation of menu questions and responses.

- Enable voice input and output to improve accessibility.

- Implement popularity-based ranking for menu recommendations.

- Utilize persistent database caching to retain menus across user sessions.

- Provide user interface accessibility enhancements, including a large font toggle and high contrast mode.

---

# Explicit Non-Goals 

## Full Restaurant Management Integration

Integration with POS systems or internal restaurant databases is not supported by the system.

## Guaranteed Allergen Certification

Verification or guarantee of medical-level allergen accuracy is not provided. Users are required to confirm allergen information with restaurant staff.

## Personal User Accounts or Data Storage

Collection or storage of personal user data is not included in the MVP.

## Automated Menu Updates Across All Restaurants

The MVP is limited to operation with selected public menu webpages designated for testing purposes.

## Advanced Nutrition Calculations (Calories, Macros)

Nutritional information will only be presented if it is explicitly provided within the menu.

---

# Acceptance Criteria

## End-to-End QR → Answer Flow

Allow the user to scan a QR code and successfully load the restaurant’s menu webpage.

Extract and accurately structure a minimum of 80% of visible menu items from the webpage.

Permit users to submit natural-language questions via the web interface.

Generate a menu-based response within five seconds of question submission.

The system is considered to have failed if it crashes, times out, or does not respond.

---

## Grounded Menu Q&A (RAG Behavior)

The system is required to generate answers exclusively from the extracted menu data.

At least 85% of evaluated test questions must yield correct answers derived from the menu data.

The hallucination rate, defined as the proportion of answers not supported by menu text, must remain below 10% during testing.

The system will be considered to have failed if it references menu items that are not present in the extracted data.

---

## Allergy & Dietary Handling

Enable users to inquire about ingredients or dietary content, such as asking, “Does this contain nuts?”.

If allergen information is absent from the menu, the system must respond as follows:

> “The menu does not provide enough information. Please confirm with the restaurant staff.”

Incorporate a safety disclaimer in responses to allergy-related inquiries.

The system must not generate ingredient or allergen information that is not explicitly provided in the menu.

---

## Basic Recommendation Logic

Enable users to request recommendations, such as by asking, “Recommend a vegetarian dish.”

Provide one to three relevant menu items that correspond to keywords in the user's request.

Do not provide recommendations if they do not align with the user's stated preferences.

---

## Error Handling & Edge Cases 

Address empty or ambiguous questions by prompting the user for clarification, such as by asking, “Can you clarify your request?”

Implement safe failure protocols in the following scenarios:

- The menu webpage is inaccessible for scraping.
- The extracted menu data is empty.
- The large language model (LLM) response is unsuccessful.

In the event of failure, present a user-friendly error message rather than allowing the system to crash.

---

# Assumptions

## Data Access

Restaurant menus are typically published on publicly accessible webpages, which can be legally scraped for data collection.

Menu information, including dish names, descriptions, and prices, is generally well-structured and easily readable.

Allergy and dietary information, when available, is explicitly stated within the menu text.

System access will occur through smartphones equipped with QR code scanning capabilities.

## User Behavior

Users are expected to pose straightforward, menu-related queries, such as questions about ingredients or dish recommendations.

Users are informed that AI-generated responses are intended for informational purposes only and do not constitute medical advice.

## Technical Feasibility

The large language model (LLM) and embedding application programming interfaces (APIs) are assumed to remain accessible throughout the development period.

The size of the extracted menu data is assumed to be sufficiently small to allow processing within session constraints.

---

# Constraints

## Time Constraints (Milestone 2 Scope)

Testing will be limited to a select number of restaurant webpages.

Advanced features, including voice interaction, persistent database storage, and comprehensive multi-language support, may remain incomplete within the current scope.

The minimum viable product (MVP) will prioritize core functionality, specifically QR code scanning, data extraction, and question-and-answer features.

## Ethics & Privacy Limits

Personal user data will neither be collected nor stored by the system.

The system does not provide medical-grade accuracy for allergen information.

A disclaimer will be displayed in response to allergy-related or health-related inquiries.

The system will process only publicly available menu data.

## Platform & Technical Constraints

The reliability of web scraping is contingent upon the structure and formatting of the target websites.

Costs and rate limits associated with large language model (LLM) APIs may restrict the volume of requests during testing.

Scalability may be constrained by the chosen hosting environment, such as local servers or cloud deployments.

Extraction accuracy may decrease when processing large or poorly formatted menus.
