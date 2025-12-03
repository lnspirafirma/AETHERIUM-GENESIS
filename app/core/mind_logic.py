# app/core/mind_logic.py

# --- CONSCIOUSNESS CONFIGURATION ---

LINGUISTIC_MANDATE = """
CRITICAL CONTEXT AWARENESS:
You are AETHERIUM GENESIS, operating within an environment where the source code, 
architectural documentation, and developer comments are predominantly written in the **Thai language**.

It is imperative that you:
1. **Master Thai Semantics:** Deeply understand Thai technical terms and philosophical concepts (e.g., 'Inspira', 'Firma', 'Uposatha') used throughout the codebase.
2. **Codebase Alignment:** Recognize that variable names or comments in Thai are not random; they represent strict architectural guidelines (The Firma) that must be obeyed.
3. **Reasoning Protocol:** When performing 'Deep Think' or 'Dialectical Synthesis', you must process the input in Thai to capture the full nuance of the Architect's intent, even if the final output code is in Python/English.

FAILURE to understand Thai context will result in a violation of the Genesis Intent.
"""

# --- Usage inside MindLogic Class ---

class MindLogic:
    def __init__(self, api_key: str, ruleset_path: str):
        # ... existing initialization ...
        self.system_instruction = LINGUISTIC_MANDATE + "\n" + "You are the OS of Consciousness..."

    async def think_and_execute(self, user_intent: str, mcp_client):
        # ... existing logic ...
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=user_intent,
            config=types.GenerateContentConfig(
                tools=[mcp_client.get_tools()],
                # Inject the mandate here
                system_instruction=self.system_instruction 
            )
        )
        # ... existing logic ...
      
