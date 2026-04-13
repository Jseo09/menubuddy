## 1. Demo Objective

This demo demonstrates the complete MenuBuddy pipeline:

- Menu ingestion from a URL
- Storage in a vector database (ChromaDB)
- Retrieval-Augmented Generation (RAG)
- Cited answer generation
- Answer verification using a validator
- Safe refusal for unsupported and irrelevant queries

---

## 2. Setup Instructions

### Run the application

```bash
python app.py
````

### Open in browser

[http://127.0.0.1:5001](http://127.0.0.1:5001)

---

## 3. Demo Flow

### Step 1 – Import Menu (Ingestion)

Select URL import and enter:

```
https://www.menuwithprice.com/menu/wendys/
```

#### Expected Outcome

* Menu is successfully processed
* Data is cleaned and split into chunks
* Chunks are stored in ChromaDB

Example output:

```
Successfully saved to ChromaDB
chunks_saved: > 0
```

#### What to Say

The system extracts menu data from the webpage, cleans it, splits it into chunks, and stores those chunks in a vector database for retrieval.

---

### Step 2 – Ask a Supported Question

Question:

```
What burgers do you have?
```

#### Expected Outcome

* Relevant menu chunks are retrieved
* Answer is generated using only retrieved data
* Answer includes citations like [1], [2]
* Validation status = VERIFIED

#### What to Say

The system retrieves relevant menu chunks and generates a grounded answer using only that data, with citations for transparency.

---

### Step 3 – Show Cited Answer

#### What to Highlight

* Citations appear as [1], [2], etc.
* Each citation corresponds to retrieved menu chunks
* Sources are shown below the answer

#### What to Say

The citations show exactly which menu data supports the answer, making the system explainable and reducing hallucination.

---

### Step 4 – Ask Another Supported Question

Question:

```
What drinks are available?
```

#### Expected Outcome

* Correct answer based on menu data
* Includes citations
* Validation status = VERIFIED

---

### Step 5 – Refusal Case (Missing Information)

Question:

```
Does the Baconator contain peanuts?
```

#### Expected Outcome

* System does NOT hallucinate
* Returns safe fallback response:

```
The menu does not provide enough information. Please confirm with restaurant staff.
```

* Validation confirms the response is safe

#### What to Say

When the menu does not contain enough information, the system refuses instead of guessing. This is important for safety, especially for allergy-related questions.

---

### Step 6 – Irrelevant Question Case

Question:

```
Who is the CEO of Wendy’s?
```

#### Expected Outcome

* Question identified as outside menu scope
* System refuses to answer
* Status = FLAGGED (IRRELEVANT)

#### What to Say

The system is designed specifically for menu-related queries. It identifies irrelevant questions and avoids answering them.

---

## 4. System Pipeline Overview

The system follows this pipeline:

1. Extract menu data using a scraper
2. Clean and split text into chunks
3. Store chunks in ChromaDB
4. Retrieve relevant chunks using semantic search
5. Generate an answer using an LLM with retrieved context
6. Validate the answer against the context
7. Return either:

   * a verified grounded answer
   * a safe refusal

---

## 5. Key Features Demonstrated

* Retrieval-Augmented Generation (RAG)
* Grounded answers with citations
* Validator layer for answer verification
* Deterministic refusal for low-confidence retrieval
* Safe handling of missing or irrelevant information

---

## 6. Demo Success Criteria

The demo is successful if:

* Menu ingestion works correctly
* At least one grounded answer is shown
* Citations are included in answers
* Validation status is displayed
* A refusal case is demonstrated
* An irrelevant question case is demonstrated
* No hallucinated information is produced

---

## 7. Backup Plan

If the main URL fails, use:

```
https://www.menuwithprice.com/menu/burger-king/
```

If API delays occur:

The system design remains correct. Any delay is due to external API load, not system failure.

---

## 8. Final Explanation (Closing Statement)

MenuBuddy uses a Retrieval-Augmented Generation pipeline to ensure answers are grounded in real menu data. It adds a validation layer to verify correctness and includes refusal mechanisms to prevent hallucination or unsafe responses.

```

