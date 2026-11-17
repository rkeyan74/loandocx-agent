# Agent LoanDocX

A conversational AI assistant for [LoanDocX](https://loandocx.com), a SaaS platform that digitizes bank loan documentation — legal title verification and property valuation. Visitors ask about features, workflows, and how to get started, and the agent answers from the product overview instead of a generic model.

Built as a portfolio project: a tool-calling chat agent, a product knowledge base loaded from a PDF, and a custom Gradio interface.

## What it does

- Answers questions about LoanDocX features, roles, and workflows (field agents, legal professionals, property valuers, the routing engine, SMS updates, and payments).
- Stays on product topics and points people to `contact@loandocx.com` for signup, bugs, or anything it does not know.
- Records interest (name, email, notes) and questions it cannot answer, then sends those through Pushover.
- Shows a page-hit counter that increments on each visit.

## How it works

```text
Visitor  →  Gradio chat UI  →  OpenAI (tool calling)
                                    │
                    ┌───────────────┼────────────────┐
                    ▼               ▼                ▼
            Product prompt    record_user_    record_unknown_
            (PDF + rules)     details         question
                                    │                │
                                    └─────── Pushover ┘
```

1. `context.py` reads `LoanDocX _Overview.pdf` and builds the system prompt: product facts, response rules, and boundaries.
2. `app.py` sends the conversation to the model. If the model requests a tool, `tools.py` runs it and the loop continues until a final reply.
3. `styles.py` supplies the theme, layout, and example questions.
4. `pagehit.py` stores the visit count in `page_hits.txt`.

## Tech stack

- Python 3.12
- [Gradio](https://www.gradio.app/) for the chat UI
- OpenAI Chat Completions with function calling
- pypdf for the product overview
- Pushover for lead and unanswered-question notifications
- python-dotenv for local secrets

## Project structure

```text
app.py                  Gradio app and chat loop
context.py              PDF ingestion and system prompt
tools.py                Tool schemas and Pushover notifications
styles.py               CSS, JS, and example prompts
pagehit.py              Visit counter
LoanDocX _Overview.pdf  Product knowledge source
Loandocx_banner.jpg     Header image
```

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your keys
python app.py
```

Open [http://localhost:7860](http://localhost:7860).

### Environment variables

| Variable | Used for |
| --- | --- |
| `OPENAI_API_KEY` | Chat completions |
| `PUSHOVER_USER` | Pushover user key |
| `PUSHOVER_TOKEN` | Pushover application token |

Copy `.env.example` to `.env` and fill those in. Do not commit `.env`.

## Example questions

- Tell me about LoanDocX
- How does LoanDocX benefit banks?
- What are the features of LoanDocX?
- How can I get in touch?

## Notes

The assistant is scoped to public product information. It does not discuss pricing, revenue, or internal plans, and it redirects out-of-scope questions back to LoanDocX.
