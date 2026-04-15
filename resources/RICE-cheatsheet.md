# R.I.C.E Prompt Engineering Cheat Sheet

## What is R.I.C.E?

R.I.C.E is a four-part framework for writing structured, reliable prompts for AI-assisted coding and development tasks.

| Component | What it means | Without it |
|-----------|---------------|------------|
| **R — Role** | Tell the AI who it is acting as | AI picks a generic default persona |
| **I — Intent** | Describe what correct output looks like — verifiably | AI optimises for plausibility, not correctness |
| **C — Context** | Specify what the AI may use — and what it must not use | AI uses anything from training data and assumptions |
| **E — Enforcement** | Specific, testable rules that must never be violated | AI makes decisions you didn't know it was making |

## The critical element: Enforcement

Enforcement is the only element the AI will never self-correct. Where you leave a gap — it makes a decision. You didn't know it was making a decision. That is the failure.

An Enforcement rule must name a trigger and a required output. If you cannot write a test that fails when the rule breaks — it is not a rule.

## R.I.C.E in practice — before and after

### Without R.I.C.E

```
Write a function that classifies customer complaints.
```

What's wrong: AI doesn't know who it is, what "classifies" means, what data to use, or what rules to follow.

### With R.I.C.E

```
You are a civic complaint classifier for the Pune municipal system.

Classify each complaint into exactly one category: Water, Roads, Sanitation, or Other.

Input: CSV with columns [date, complaint_text, ward]
Output: CSV with columns [date, category, justification]

ENFORCEMENT RULES:
1. IF complaint_text contains "water" OR "tap" OR "pipe" → category MUST be "Water"
2. IF complaint_text contains "road" OR "pothole" OR "margin" → category MUST be "Roads"
3. IF complaint_text contains "garbage" OR "dustbin" OR "sewage" → category MUST be "Sanitation"
4. Any other complaint → category MUST be "Other"
```