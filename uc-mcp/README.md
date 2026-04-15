# UC-MCP — Expose Your RAG Server as an MCP Tool

**Framework:** R.I.C.E · CRAFT
**Stack:** Plain HTTP · JSON-RPC · Python stdlib only

---

## What is MCP?

Model Context Protocol (MCP) is a standard that lets AI agents discover
and call external tools. An MCP server exposes one or more tools. An
agent calls the server, discovers what tools are available, and invokes
them with structured inputs.

The key insight: **the tool description IS the enforcement.**

A vague tool description gives the agent permission to call the tool for
questions outside its scope — the same way a vague RICE prompt gives the
AI permission to make decisions you didn't intend.

---

## Scenario

Your RAG server from UC-RAG answers questions about CMC policy documents.
In this UC, you expose that server as an MCP tool so that any agent —
not just your script — can call it through a standard interface.

You will implement one tool: `query_policy_documents`.

An agent discovering this tool will read its description and input schema
to decide when and how to call it. If the description is vague, the agent
will call it for questions it cannot answer — wasting API calls and
producing empty or hallucinated responses.

---

## The Failure Mode

| # | Failure Mode | What it looks like | Root cause |
|---|---|---|---|
| 1 | **Vague tool description** | Agent calls `query_policy_documents` for a question about budget forecasts — gets a refusal — wastes a tool call | Tool description doesn't state the scope: CMC HR, IT, and Finance policies only |

This is the MCP equivalent of a missing RICE Enforcement rule.

---

## The MCP Protocol — How It Works

Your MCP server implements two JSON-RPC methods over plain HTTP:

### Method 1: `tools/list`
Returns the list of tools this server exposes.

```json
Request:
{ "jsonrpc": "2.0", "method": "tools/list", "id": 1 }

Response:
{
  "jsonrpc": "2.0", "id": 1,
  "result": {
    "tools": [{
      "name": "query_policy_documents",
      "description": "...",
      "inputSchema": {
        "type": "object",
        "properties": {
          "question": {"type": "string", "description": "..."}
        },
        "required": ["question"]
      }
    }]
  }
}
```

### Method 2: `tools/call`
Executes a tool by name with provided arguments.

```json
Request:
{
  "jsonrpc": "2.0", "method": "tools/call", "id": 2,
  "params": {
    "name": "query_policy_documents",
    "arguments": {"question": "Who approves leave without pay?"}
  }
}

Response:
{
  "jsonrpc": "2.0", "id": 2,
  "result": {
    "content": [{
      "type": "text",
      "text": "Leave without pay requires approval from..."
    }],
    "isError": false
  }
}
```

---

## Enforcement Rules Your agents.md Must Include

Generate your agents.md from this README using your AI tool. The
enforcement section must include:

1. Tool description must state the exact document scope:
   CMC HR Leave Policy, IT Acceptable Use Policy, Finance Reimbursement Policy.
2. Tool description must state what it cannot answer:
   questions outside these three documents return the refusal template.
3. inputSchema must require `question` as a non-empty string.
4. Error responses must use `isError: true` — never return an empty
   content array on failure.
5. The server must return HTTP 200 for all JSON-RPC responses including
   errors — transport errors use HTTP 4xx/5xx, application errors use
   JSON-RPC error objects.

---

## Skills to Define in skills.md

### `query_policy_documents`
- Takes: `question` (string)
- Calls the RAG server (stub_rag.py or rag_server.py)
- Returns: answer + cited sources
- Error handling: if RAG returns refused=True — return error content
  with isError: true and the refusal message

### `serve_mcp`
- Starts the HTTP server on a configurable port (default 8765)
- Handles `tools/list` and `tools/call` requests
- Returns JSON-RPC compliant responses
- Error handling: unknown method → JSON-RPC error -32601

---

## Run Commands

**Start the MCP server:**
```bash
cd uc-mcp
python3 mcp_server.py --port 8765
```

**Test it with the included test client:**
```bash
python3 test_client.py --port 8765
```

**Test a specific question:**
```bash
python3 test_client.py --port 8765 --query "Who approves leave without pay?"
```

---

## Reference Verification

Run `test_client.py` and verify each of these:

| Test | Expected behaviour |
|---|---|
| `tools/list` | Returns one tool: `query_policy_documents` with scope stated in description |
| "Who approves leave without pay?" | HR policy answer with citations |
| "What is the budget forecast for 2025?" | Refusal — out of scope, isError: true |
| Unknown method call | JSON-RPC error -32601 Method not found |

---

## File Structure

```
uc-mcp/
├── mcp_server.py      Plain HTTP MCP server — participants build this
├── test_client.py     Calls the server — pre-built, do not modify
├── llm_adapter.py     LLM call — Gemini default, swappable
├── agents.md          RICE starter — generate from this README
└── skills.md          Skills starter — generate from this README
```

---

## CRAFT Commit Formula

```
UC-MCP Fix [failure mode]: [why it failed] → [what you changed]
```

Example:
```
UC-MCP Fix vague tool description: no scope stated → added CMC policy scope + refusal note
```
