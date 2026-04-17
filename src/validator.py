import re

def verify_answer_against_context(gem_client, question, answer, context_block):
    prompt = f"""
You are a strict validator.

Decide if the answer is:
- OK: answer is supported by the context OR correctly refuses due to missing info
- UNSUPPORTED: answer includes information NOT present in context
- IRRELEVANT: the user's question is outside the menu/food domain

Rules:
- If the answer says "I don't know" or "not provided in menu", that is OK only if the question is menu-related.
- If the question is about CEO, company info, corporate history, stock price, founder, headquarters, etc., mark IRRELEVANT.
- If the answer invents food, price, or ingredients, mark UNSUPPORTED.

Question:
{question}

Answer:
{answer}

Context:
{context_block}

Respond exactly in this format:
VERDICT: OK / UNSUPPORTED / IRRELEVANT
REASON: short explanation
"""

    try:
        resp = gem_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        text = resp.text or ""

        if re.search(r"\bIRRELEVANT\b", text, re.I):
            verdict = "IRRELEVANT"
        elif re.search(r"\bUNSUPPORTED\b", text, re.I):
            verdict = "UNSUPPORTED"
        else:
            verdict = "OK"

        return text, verdict

    except Exception as e:
        return f"VALIDATION ERROR: {str(e)}", "UNSUPPORTED"
