# AI-Assisted Testing

One deep, real example of using AI critically in a testing workflow —
not a folder of prompt screenshots. See `docs/decision-log.md` and
blueprint reasoning: a folder full of raw prompts reads as "I can type
into ChatGPT," which isn't a skill anyone is hiring for. Showing
judgment — what was kept, discarded, and why — is the actual point.

## Contents
- **[`bill-pay-negative-cases.md`](bill-pay-negative-cases.md)** — a real
  brainstorm for Bill Pay negative test cases, reviewed critically
  against what this project already knew about ParaBank, with one
  suggestion kept specifically because it connected to an existing
  finding ([BUG-002](../docs/bugs/BUG-002.md)) — and confirmed correct:
  it led directly to [BUG-003](../docs/bugs/BUG-003.md).

## The pattern, if adding another example later
1. Real prompt, real raw output — no editing after the fact.
2. Explicit review: kept / discarded / modified, each with a stated
   reason — not just a final list.
3. Note which suggestions don't apply to *this specific app* and why —
   an AI's generic suggestion can assume a validation rule or feature
   that doesn't actually exist here.
4. Link the actual implemented test and its real outcome, not just the
   idea.
