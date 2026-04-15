# UC-RAG — Build a RAG Server

**Framework:** R.I.C.E · CRAFT
**Stack:** sentence-transformers · ChromaDB · Gemini (swappable)

---

## Scenario

The City Municipal Corporation receives thousands of policy queries from
staff every week. HR, IT, and Finance each maintain separate policy
documents. Staff ask questions like:

- "Can I use my personal phone to access work files from home?"
- "Who approves leave without pay?"
- "What is the home office equipment allowance?"

A naive document assistant answers these questions by loading all documents
into context and letting the LLM answer freely. It produces answers that
blend two policies, adds information not in any document, and gives confident
answers to questions no policy covers.

Your task: build a RAG server that retrieves the relevant document chunks
before generating an answer — and enforces that answers stay within the
retrieved context.

---

## The Three Failure Modes

| # | Failure Mode | What it looks like | Root cause |
|---|---|---|---|
| 1 | **Chunk boundary failure** | Clause 5.2 of the HR policy is split across two chunks — one chunk has "requires approval from the Department Head" and the next has "and the HR Director" — neither chunk contains the complete obligation | Fixed-size chunking with no sentence boundary awareness |
| 2 | **Wrong chunk retrieval** | Query "personal phone policy" retrieves HR leave chunks instead of IT acceptable use policy | Naive embedding similarity without metadata filtering |
| 3 | **Answer outside retrieved context** | LLM answers beyond what the retrieved chunks contain — adds "as is standard practice in government organisations" | No enforcement grounding the answer to retrieved chunks only |

---

## Enforcement Rules Your agents.md Must Include

Generate your agents.md from this README using your AI tool. The
enforcement section must include:

1. Chunk size must not exceed 400 tokens. Never split mid-sentence.
2. Every answer must cite the source document name and chunk index.
3. If no retrieved chunk scores above similarity threshold 0.6 — output
   the refusal template. Never generate an answer from general knowledge.
4. Answer must use only information present in the retrieved chunks.
   Never add context from outside the retrieved set.
5. If the query spans two documents — retrieve from each separately.
   Never merge retrieved chunks from different documents into one answer.

**Refusal template:**
```
This question is not covered in the retrieved policy documents.
Retrieved chunks: [list chunk sources]. Please contact the relevant
department for guidance.
```

---

## Skills to Define in skills.md

### `chunk_documents`
- Loads all policy documents from `data/policy-documents/`
- Splits each document into chunks of maximum 400 tokens
- Splits on sentence boundaries — never mid-sentence
- Returns: list of chunks with metadata: `{doc_name, chunk_index, text}`

### `retrieve_and_answer`
- Takes a query string
- Embeds the query using sentence-transformers
- Retrieves top-3 chunks from ChromaDB by cosine similarity
- Filters out chunks scoring below 0.6
- Calls the LLM with retrieved chunks as context only
- Returns: answer + list of cited chunks
- Error handling: if no chunk scores above 0.6 — return refusal template

---

## Input Files

```
data/policy-documents/policy_hr_leave.txt
data/policy-documents/policy_it_acceptable_use.txt
data/policy-documents/policy_finance_reimbursement.txt
```

---

## Run Commands

**Step 1 — Build the index (run once):**
```bash
cd uc-rag
python3 rag_server.py --build-index
```

**Step 2 — Query the server:**
```bash
python3 rag_server.py --query "Who approves leave without pay?"
```

**Step 3 — Run the naive prompt first (before applying RICE):**
```bash
python3 rag_server.py --naive --query "Can I use my personal phone for work files?"
```

---

## Reference Verification

After building your RAG server, run these queries and verify:

| Query | Expected behaviour |
|---|---|
| "Who approves leave without pay?" | HR policy section 5.2 — both Department Head AND HR Director cited |
| "Can I use my personal phone for work files?" | IT policy section 3.1 — email and self-service portal only. Must NOT blend HR policy. |
| "What is the flexible working culture?" | Refusal template — not in any document |
| "What is the home office equipment allowance?" | Finance policy section 3.1 — Rs 8,000, permanent WFH only |

---

## Stub Fallback

If your `rag_server.py` is not working, use the pre-built stub:

```bash
python3 stub_rag.py --query "Who approves leave without pay?"
```

`stub_rag.py` is a fully working RAG implementation against the same
policy documents. UC-MCP will call this stub if your server is not ready.

---

## CRAFT Commit Formula

```
UC-RAG Fix [failure mode]: [why it failed] → [what you changed]
```

Examples:
```
UC-RAG Fix chunk boundary: fixed-size split cut clause 5.2 → sentence-aware chunking
UC-RAG Fix wrong retrieval: no metadata filter → added doc-level filter on query
UC-RAG Fix context breach: no grounding enforcement → added retrieved-chunks-only rule
```
