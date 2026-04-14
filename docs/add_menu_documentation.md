## Link to Word documents

**Pre**

    https://jaguartamu-my.sharepoint.com/:w:/g/personal/rsanc083_jaguar_tamu_edu/IQBoFUXigcAfRJxEBKXcZGsuAVSyX8B8dYqEXRDrxnn8q6M?e=etSS4d

**Restaurants**

    https://jaguartamu-my.sharepoint.com/:w:/g/personal/rsanc083_jaguar_tamu_edu/IQBfrg3xzLHPQ5setF0pg-t_AVXhDdMyZyPktQezJHBh54k?e=QxCFRJ


## Pre

**Was given an error**

    503 UNAVAILABLE: This model is currently experiencing high demand

Could be because Google GenAI API couldn’t process the request because their servers were overloaded.

**Possible Fixes**

1. Switch to a more stable model

2. Add error handling around pipe.run()

3. Retry until success

**Current Fix**

1. Switched gemini-3.1-flash-lite-preview to gemini-2.5-flash
   
    a. Successful in answering one question (still gave 503 error) but crashed after asking second question

2. Switched gemini-2.5-flash to gemini-2.5-flash-lite

    a. Successful in anwering more than one question, still gave 503 error

# Restaurants 

## Canes

https://www.menuwithprice.com/menu/raising-canes/

| Question | Response | Correct / Incorrect |
| -------- | -------- | -------- |
| What do they have in Raising Canes?  | Raising Cane's offers Tailgates, Combos, Chicken Finger, Coleslaw, Texas Toast, Cane's Sauce, Honey Mustard, Sandwich Only, 21oz. Cane's Sauce, 21oz. Honey Mustard, 32oz. Cane's Sauce, 32oz. Honey Mustard, Freshly Squeezed Lemonade, Fountain Drink, Tea, and Half Tea/Half Lemonade [1, 4]. The Caniac Combo includes 6 Chicken Fingers, Crinkle-Cut Fries, and two of something not specified [1]. Tailgate options include 25 Fingers for $41.99, 50 Fingers for $79.99, 75 Fingers for $118.99, and 100 Fingers for $142.99 [1]. | Correct  |
| Does Raising Cane's have a kids meal?  | Yes, Raising Cane's has a kids meal called "The Kid's Combo" for $6.69 | Correct |


## Panda Express

https://www.menuwithprice.com/menu/panda-express/

| Question | Response | Correct / Incorrect |
| -------- | -------- | -------- |
| What do they have in Panda Express?  | Panda Express offers several meal sizes: Bowl, Plate, and Bigger Plate [1]. They also have Panda Cub Meals™ in varieties like Orange Chicken, Grilled Teriyaki Chicken, and Broccoli Beef, as well as a Build Your Own Panda Cub Meal™ option [2]. For larger groups, there is a 5 Person Family Meal [2]. Entrees available include String Bean Chicken Breast, The Original Orange Chicken, Honey Sesame Chicken Breast, Grilled Teriyaki Chicken, Broccoli Beef, Beijing Beef, and Black Pepper Chicken [3]. Side options include White Steamed Rice, Fried Rice, Chow Mein, and Super Greens [3]. For drinks, Panda Express offers Dr Pepper, Coca Cola, Diet Coke, Mango Guava Flavored Tea, Peach Lychee Flavored Refresher, Pomegranate Pineapple Flavored Lemonade, Watermelon Mango Flavored Refresher, Barq's Root Beer, Fanta Orange, Minute Maid Lemonade, Sprite, Coca Cola Cherry, Fanta Strawberry, Fuze Raspberry Iced Tea, Passion Mango Black Tea, Sweet Tea, and Powerade Fruit [3, 5].  | Correct  |
| Does Panda Express have a kids meal?  | Yes, Panda Express has a kids meal called the Panda Cub Meal™. [1] | Correct  |


## Church's Chicken

https://www.menuwithprice.com/menu/churchs-chicken/

| Question | Response | Correct / Incorrect |
| -------- | -------- | -------- |
| What do they have in Church's Chicken  | Church's Chicken offers a 10PC Family Meal in Original or Spicy varieties, with options for Leg & Thigh or Tenders. They also have an Original Tender Wrap [1]. Additionally, you can find 8PC Tenders, and 12PC and 16PC Chicken options in Original or Spicy, with choices for Leg & Thigh, Mixed, or White Meat [5]. | Correct  |
| Does Church's Chicken have a kids meal?  | I don't know. | Correct, Church's doesn't have a kids meal  |
