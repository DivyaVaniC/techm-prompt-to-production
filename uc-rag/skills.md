# skills.md — UC-RAG RAG Server
# INSTRUCTIONS:
# 1. Open your AI tool
# 2. Paste the full contents of uc-rag/README.md
# 3. Use this prompt:
#    "Read this UC README. Generate a skills.md YAML defining the two
#     skills: chunk_documents and retrieve_and_answer. Each skill needs:
#     name, description, input, output, error_handling.
#     error_handling must address the failure modes in the README.
#     Output only valid YAML."
# 4. Paste the output below, replacing this placeholder
# 5. Verify error_handling addresses all three failure modes

skills:
  - name: chunk_documents
    description: "[FILL IN]"
    input: "[FILL IN: path to policy-documents directory]"
    output: "[FILL IN: list of chunk dicts with doc_name, chunk_index, text]"
    error_handling: "[FILL IN: what happens if a file is missing or unreadable]"

  - name: retrieve_and_answer
    description: "[FILL IN]"
    input: "[FILL IN: query string]"
    output: "[FILL IN: answer string + list of cited chunks]"
    error_handling: "[FILL IN: what happens when no chunk scores above 0.6]"
