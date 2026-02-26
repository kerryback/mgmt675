# AI as the UI: Enhancing Productivity with Agentic AI

## One-Day Executive Education Course

**Instructor:** Kerry Back, J. Howard Creekmore Professor of Finance, Rice Business

---

## Course Description

AI is rapidly shifting from a chat tool to a full working environment. This one-day intensive gives executives a hands-on understanding of how agentic AI can transform financial analysis, reporting, and decision-making. Participants will move from basic AI interactions to connecting AI to their tools, automating multi-step workflows, and building custom AI assistants — all in a single day.

---

## Pre-Work

- Create a free [Claude](https://claude.ai) account (Pro accounts provided for the day)
- Install [Google Colab](https://colab.research.google.com) (just need a Google account)
- No coding experience required

---

## Schedule

### Morning Session: Foundations (8:30 AM -- 12:00 PM)

#### Module 1: The AI Landscape (8:30 -- 9:15)

**Why this matters now**

- The business case: Deloitte Q4 2025 survey (87% of CFOs say AI will be important for finance; 54% prioritize AI agents), HPE's "Alfred" (reduced reporting prep 90%, cut cycle time 40%)
- The capability curve: AI is doubling capability every few months; what this means for knowledge work
- From chat to agent: passive (chat) → creative (artifacts) → agentic (autonomous work)
- Key insight: AI is becoming the user interface for all software

**Demo:** Side-by-side comparison of chat, artifacts, and agentic AI completing a financial task

#### Module 2: AI with Code Execution (9:15 -- 10:15)

**Hands-on: Making AI do real financial analysis**

- Chat interfaces: Asking AI to analyze data, create charts, build models
- Code execution environments: How AI writes and runs code on your behalf
- Sandboxed vs. local execution: Understanding the trade-offs (security vs. capability)
- Working with financial data: Stock returns, portfolio analysis, company financials

**Exercise 1:** Use Claude to compute portfolio statistics and visualize an efficient frontier. No coding required — just describe what you want.

*--- Break (10:15 -- 10:30) ---*

#### Module 3: Connecting AI to Your Tools (10:30 -- 11:15)

**From isolation to integration**

- The problem: AI can't reach your browser, files, databases, or calendar by default
- Model Context Protocol (MCP): The "USB standard" for connecting AI to external tools
- Live demos:
  - AI browsing the web autonomously to gather financial data
  - AI querying a financial database and building a report
  - AI managing calendar and email
- The plugin ecosystem: How pre-built integrations are replacing enterprise software workflows
- The SaaSpocalypse: What happened when Anthropic released 11 plugins and $285B in market cap evaporated

**Discussion:** What workflows in your organization could be connected to AI?

#### Module 4: AI in Spreadsheets (11:15 -- 12:00)

**Where most finance professionals live**

- Claude for Excel: AI sidebar that sees and modifies your workbook
- Critical distinction: Formulas vs. hardcoded values — why it matters for AI-generated spreadsheets
- Building financial models: Loan amortization, DCF models, sensitivity tables
- AI-generated Excel vs. human-built Excel: Strengths and limitations

**Exercise 2:** Build a two-stage DCF model by describing the company and assumptions to AI. Review the formulas AI creates.

---

### Lunch (12:00 -- 1:00 PM)

Lunch discussion: Participants share use cases from their industries.

---

### Afternoon Session: Agentic AI (1:00 -- 4:30 PM)

#### Module 5: Autonomous AI Agents (1:00 -- 2:00)

**AI that takes action, not just answers questions**

- Chatbot vs. agent: An agent is a chatbot with tools
- The agent loop: LLM thinks → calls a tool → gets result → thinks again → repeats
- What agents can do: Query databases, execute code, search the web, read documents, send emails
- Example walkthrough: A database analytics agent analyzing revenue trends step by step
- User interfaces: Streamlit and Gradio — chat UIs anyone can build
- From idea to deployment: Build → UI → deploy → iterate

**Demo:** A working financial analysis agent that queries live data, builds charts, and writes a summary report.

#### Module 6: Customizing AI for Your Workflows (2:00 -- 2:45)

**Making AI work the way you work**

- The key insight: All AI customization is just added text to the prompt
- Skills and slash commands: Reusable instructions that guide AI behavior
- Example: A variance analysis skill that decomposes budget vs. actual (volume, price, rate effects)
- Building a custom skill: Define the domain knowledge, workflow steps, and output format
- Deploying skills across your team: Shared prompts as organizational knowledge

**Exercise 3:** Design a custom AI skill for a workflow in your organization. Define the instructions, inputs, and expected outputs.

*--- Break (2:45 -- 3:00) ---*

#### Module 7: Reducing Hallucinations and Building Trust (3:00 -- 3:45)

**Making AI reliable enough for production**

- Why AI hallucinates and when it matters most (compliance, reporting, client-facing)
- Three approaches to improve accuracy:
  1. **RAG (Retrieval Augmented Generation):** Ground AI in your documents — upload policies, filings, reports and get cited answers
  2. **Fine-tuning:** Adjust model weights for your domain (consistent style, terminology, classification)
  3. **Small language models:** Private, fast, specialized (BloombergGPT, FinGPT)
- NotebookLM: Upload 50 sources and chat with your documents (free, with citations)
- When to use which approach: Decision framework based on cost, effort, and use case

**Demo:** Upload a 10-K filing into NotebookLM and ask financial analysis questions with source citations.

#### Module 8: What's Next and Action Planning (3:45 -- 4:30)

**From demo day to real impact**

- AI-driven trading and news sentiment: How hedge funds use LLMs for alpha generation
- The crowding problem: As adoption rises, the advantage shifts from speed to depth of understanding
- Organizational readiness: Security, governance, and data considerations
- Building an AI adoption roadmap:
  - Quick wins (weeks): Chat for research, document summarization, email drafting
  - Medium-term (months): MCP integrations, custom skills, team-shared prompts
  - Strategic (quarters): Custom agents, RAG on proprietary data, workflow automation

**Exercise 4:** Each participant drafts a 90-day AI adoption plan for one workflow in their organization. Small-group share-out.

---

## Key Takeaways

1. **AI is the new UI** — Interacting with software through natural language is replacing traditional interfaces
2. **Agents > Chatbots** — The real value comes when AI can take actions, not just answer questions
3. **Customization is just prompting** — Skills, system prompts, and instructions make AI work for your specific workflows
4. **Start with RAG** — Grounding AI in your documents is the fastest path to reliable, production-ready answers
5. **Connect, don't rebuild** — MCP and plugins let AI work with your existing tools rather than replacing them

---

## Materials Provided

- Slide decks for each module
- Exercise files and sample data
- Skill templates for common finance workflows
- Resource guide with links to tools, APIs, and further reading
- 30-day Claude Pro access for continued experimentation

---

## Technical Requirements

- Laptop with Chrome browser
- Google account (for Colab)
- Claude Pro account (provided)
- Wi-Fi access (provided)
