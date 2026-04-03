def verify_answer_against_context(gem_client, answer, context_block):
    # Standardizing the prompt for the new 3.1-flash logic
    prompt = f"""
    You are a strict Fact-Checker. 
    Verify if the 'Answer' below is fully supported by the provided 'Context'.

    Rules:
    - If the Answer only contains information found in the Context, respond with 'VERDICT: OK'.
    - If the Answer contains information NOT in the Context, respond with 'VERDICT: UNSUPPORTED'.

    Context: {context_block}
    Answer: {answer}
    """

    try:
        # UPDATED: Using 'gemini-3.1-flash' and removing 'models/' prefix
        resp = gem_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[prompt]
        )

        raw_text = resp.text.upper() if resp.text else ""
        verdict = "OK" if "VERDICT: OK" in raw_text else "UNSUPPORTED"

        return resp.text, verdict

    except Exception as e:
        print(f"Validation Error: {e}")
        # Default to UNSUPPORTED on error for safety
        return str(e), "UNSUPPORTED"