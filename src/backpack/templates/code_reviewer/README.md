# Code Reviewer Template

A Backpack agent template for automated code review: constructive, specific, and security-aware.

## What you get

- **Credentials**: `OPENAI_API_KEY` (injected by Backpack)
- **Personality**: Senior reviewer, constructive and educational
- **Starter script**: `agent.py` ready to wire to your LLM and diff/file input

## Use this template

```bash
backpack template use code_reviewer
backpack key add OPENAI_API_KEY
backpack run agent.py
```

## Customize

- Adjust personality in `agent.lock` (or `backpack init`) for stricter/looser or language-specific review.
- Implement diff/file reading and LLM calls in `agent.py` (e.g. GitHub API, local files).

