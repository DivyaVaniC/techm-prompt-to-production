# agents.md — UC-RAG RAG Server
# INSTRUCTIONS:
# 1. Open your AI tool
# 2. Paste the full contents of uc-rag/README.md
# 3. Use this prompt:
#    "Read this UC README. Using the R.I.C.E framework, generate an
#     agents.md YAML with four fields: role, intent, context, enforcement.
#     Enforcement must include every rule listed under
#     'Enforcement Rules Your agents.md Must Include'.
#     Output only valid YAML."
# 4. Paste the output below, replacing this placeholder
# 5. Check every enforcement rule against the README before saving

role: >
  [FILL IN: Who is this agent? What is its operational boundary?
   Hint: a retrieval-augmented policy assistant for city staff]

intent: >
  [FILL IN: What does a correct output look like?
   Hint: answer + cited chunks + refusal when not covered]

context: >
  [FILL IN: What sources may the agent use?
   Hint: retrieved chunks only — no general knowledge]

enforcement:
  - "[FILL IN: Chunk size rule]"
  - "[FILL IN: Citation rule]"
  - "[FILL IN: Similarity threshold + refusal rule]"
  - "[FILL IN: Context grounding rule]"
  - "[FILL IN: Cross-document rule]"
