# skills.md — UC-MCP MCP Server
# INSTRUCTIONS:
# 1. Open your AI tool
# 2. Paste the full contents of uc-mcp/README.md
# 3. Use this prompt:
#    "Read this UC README. Generate a skills.md YAML defining the two
#     skills: query_policy_documents and serve_mcp. Each skill needs:
#     name, description, input, output, error_handling.
#     error_handling must address the failure mode in the README.
#     Output only valid YAML."
# 4. Paste the output below, replacing this placeholder

skills:
  - name: query_policy_documents
    description: "[FILL IN]"
    input: "[FILL IN: question string]"
    output: "[FILL IN: MCP content format — content array + isError]"
    error_handling: "[FILL IN: what happens when RAG refuses or raises exception]"

  - name: serve_mcp
    description: "[FILL IN]"
    input: "[FILL IN: HTTP POST with JSON-RPC body]"
    output: "[FILL IN: JSON-RPC 2.0 response, always HTTP 200]"
    error_handling: "[FILL IN: unknown method → -32601, malformed request → -32700]"
