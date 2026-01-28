# Financial Analyst Template

A Backpack agent template for financial analysis: formal tone, citation-friendly, and data-driven.

## What you get

- **Credentials**: `OPENAI_API_KEY` (injected by Backpack)
- **Personality**: Senior financial analyst, formal and precise
- **Starter script**: `agent.py` ready to wire to your LLM and data sources

## Use this template

From your project directory:

```bash
backpack template use financial_analyst
backpack key add OPENAI_API_KEY
backpack run agent.py
```

## Customize

- Edit `agent.lock` personality (or re-run `backpack init --personality "..."`) to change tone and instructions.
- Replace the placeholder logic in `agent.py` with your data pipeline and LLM calls.

