### Link to Word document

https://jaguartamu-my.sharepoint.com/:w:/g/personal/rsanc083_jaguar_tamu_edu/IQBoFUXigcAfRJxEBKXcZGsuAVSyX8B8dYqEXRDrxnn8q6M?e=etSS4d


### Analysis

**Was given an error**

    503 UNAVAILABLE: This model is currently experiencing high demand

Could be because Google GenAI API couldn’t process the request because their servers were overloaded.

**Possible Fixes**

1. Switch to a more stable model

2. Add error handling around pipe.run()

3. Retry until success

**Current Fix**

1. Switched gemini-3.1-flash-lite-preview to gemini-2.5-flash
   
    a. Successful in answering one question but crashed after asking second question

2. Switched gemini-2.5-flash to gemini-2.5-flash-lite

    a. Successful in anwering more than one question
