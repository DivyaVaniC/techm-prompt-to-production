# agents.md — UC-MCP MCP Server
# INSTRUCTIONS:
# 1. Open your AI tool
# 2. Paste the full contents of uc-mcp/README.md
# 3. Use this prompt:
#    "Read this UC README. Using the R.I.C.E framework, generate an
#     agents.md YAML with four fields: role, intent, context, enforcement.
#     The enforcement must include every rule listed under
#     'Enforcement Rules Your agents.md Must Include'.
#     Output only valid YAML."
# 4. Paste the output below, replacing this placeholder
# 5. Pay special attention to enforcement rule 1 — the tool description
#    must state exact document scope

role: >
  [FILL IN: Who is this agent? What layer of the stack does it operate at?
   Hint: an MCP server that exposes policy retrieval as a tool]

intent: >
  [FILL IN: What does a correctly implemented MCP server produce?
   Hint: JSON-RPC compliant responses, scoped tool description, correct refusals]

context: >
  [FILL IN: What does this server have access to?
   Hint: RAG server results only — no direct LLM calls, no outside knowledge]

enforcement:
  - "[FILL IN: Tool description scope rule]"
  - "[FILL IN: Refusal documentation rule]"
  - "[FILL IN: inputSchema required field rule]"
  - "[FILL IN: isError on failure rule]"
  - "[FILL IN: HTTP 200 for all JSON-RPC responses rule]"
