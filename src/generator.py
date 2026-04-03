def generate_grounded_answer(gem_client, question, context_block):
    # Standardizing the prompt for better citation adherence
    prompt = f"""
    You are MenuBuddy, a helpful restaurant assistant. 
    Use ONLY the provided context to answer the question. 

    Rules:
    1. Every claim MUST include a citation using the format [ID].
    2. If the answer is not in the context, say "I'm sorry, I don't have that information in the menu data."
    3. Keep the tone helpful and concise.

    Context:
    {context_block}

    Question: {question}
    """

    try:
        # UPDATED: Using 'gemini-3.1-flash' and removing the 'models/' prefix
        resp = gem_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[prompt]
        )

        # In the new SDK, response text is accessed directly
        return resp.text.strip() if resp.text else "I couldn't generate an answer."

    except Exception as e:
        print(f"Generation Error: {e}")
        return "System error: Unable to generate an answer at this time."