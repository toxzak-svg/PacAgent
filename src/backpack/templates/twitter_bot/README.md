# Twitter Bot Template

A Backpack agent template for a Twitter bot: LLM for content, Twitter API for posting.

## What you get

- **Credentials**: `OPENAI_API_KEY`, `TWITTER_BEARER_TOKEN` (injected by Backpack)
- **Personality**: Friendly, concise, on-brand Twitter voice
- **Starter script**: `agent.py` ready to connect to OpenAI and Twitter API

## Use this template

```bash
backpack template use twitter_bot
backpack key add OPENAI_API_KEY
backpack key add TWITTER_BEARER_TOKEN
backpack run agent.py
```

## Customize

- Change personality in `agent.lock` (or re-run `backpack init`) to match your brand.
- Implement posting/reading in `agent.py` using the Twitter API v2 and your LLM of choice.

