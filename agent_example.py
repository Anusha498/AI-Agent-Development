# Minimal example: show how the 4-layer prompts interact (pseudo-code).
# This is NOT a runnable LLM client, but shows how you'd wire prompts.
input_text = "Help me revise integration by parts for tomorrow, 45 minutes."

# 1. Input understanding (call LLM with INPUT_PROMPT + input_text) -> interpretation_json
# 2. State tracker: load state.json, update with interpretation_json -> new_state.json
# 3. Planner: call LLM with PLANNER_PROMPT + interpretation_json + new_state.json -> planner_json
# 4. Output generator: call LLM with OUTPUT_PROMPT + planner_json + interpretation_json + new_state.json -> final_message
# Save final_message to a chat log for the user.