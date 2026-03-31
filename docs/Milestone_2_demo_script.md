# Milestone 2 Demo Script – MenuBuddy

## 1. Setup Commands

Create and activate a virtual environment if needed:

```bash
python -m venv .venv
```
### Windows
```bash
.venv\Scripts\activate
```
### macOS/Linux
```bash
source .venv/bin/activate
```
Install required packages
```bash
pip install -r requirements.txt
```
## 2. Run Command
```bash
python main.py
```
## Demo Input(Step-by-Step)
When prompted:
```bash
Import menu (1=URL, 2=Image):
```
Enter
```bash
1
```
Then input the URL: 
```bash
https://www.menuwithprice.com/menu/olive-garden/
```
Backup URL:
```bash
https://www.menuwithprice.com/menu/wendys/
```

## 4. Demo Questions
#### Quesiton 1:
```bash
What soups are available?
```
**Expected Outcomes**:
```bash
*   ToGo Soup, Salad & Breadstick Entrée Dinner [1]
*   ToGo Soup, Salad & Breadstick Entrée Lunch [1]
*   ToGo Homemade Chicken and Gnocchi Soup [3]
*   ToGo Homemade Pasta e Fagioli Soup [3]
*   ToGo Homemade Zuppa Toscana Soup [3]
*   ToGo Homemade Minestrone Soup [3]
```
#### Quesiton 2:
```bash
What desserts are on the menu?
```
**Expected Outcomes**:
```bash
The following desserts are on the menu:
*   Chocolate Lasagna - $12.29 [1]
*   Warm Italian Doughnuts - $11.49 [1]
*   Sicilian Cheesecake - $11.99 [1]
*   Strawberry Cream Cake - $12.29 [1]
*   Black Tie Mousse Cake - $12.49 [1]
*   Tiramisu - $11.99 [1]
*   Apple Bites - $1.29 [2]
*   Classic chocolate Frosty - $0.99 [4]
*   Classic Vanilla Frosty - $0.99 [4]
*   Chocolate Chunk Cookies - $2.18 [4]
*   Sugar Cookies - $2.18 [4]
```
#### Quesiton 3:
```bash
What seafood options are available?
```
**Expected Outcomes**:
```bash
The seafood options available are:
*   Herb-Grilled Salmon - $30.29 [1]
*   Seafood Alfredo - $28.79 [3]
*   Shrimp Alfredo - $27.79 [3]
*   Shrimp Scampi Lunch - $15.49 [4]
*   Crispy Panko Fish Sandwich - $6.16 [5]
```
#### Quesiton 4:
```bash
What is the price of Shrimp Alfredo?
```
**Expected Outcomes**:
```bash
Shrimp Alfredo is $27.79 [2].
```
#### Quesiton 5:
```bash
Recommend 2 pasta dishes
```
**Expected Outcomes**:
```bash
Here are two pasta dish recommendations:
*   Chicken Marsala Fettuccine - $27.29 [1]
*   Fettuccine Alfredo - $20.99 [4]
```
## 5. Refusal Case 
#### Quesiton 6:
```bash
Does the Chicken Alfredo contain peanuts?
```
**Expected Outcomes**:
```bash
The provided context lists Chicken Alfredo for $26.49 [2]. However, the context does not contain information regarding ingredients or allergens, such as peanuts, for any menu item. Therefore, I cannot determine if the Chicken Alfredo contains peanuts based on the given information.
```

## 6. Expected System Behavior 
For each query:
1. Retrieve relevant menu items
2. Build context block
3. Generate grounded answer
4. Validate answer
5. Output answer with verdict

Output format:
```bash
--- ANSWER (STATUS: VERIFIED - OK) ---
[Grounded Answer]
------------------------------
```
## 7. Demo Success Criteria 
- Menu loads successfully from URL
- Questions return grounded answers
- Answers include citations
- UI works properly 
- No hallucinated items
- Refusal works correctly for missing data
- System runs without crashing
