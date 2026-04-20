# When to Use Agent SDKs, and Why LangChain's Moment Has Passed

## The Big Picture: The Harness Is Now the Product

In April 2025, the major AI labs — Anthropic, OpenAI, Google, and Microsoft — all converged on the same insight: the real product isn't just the model, it's the **harness** around the model. Martin Fowler [defined](https://martinfowler.com/articles/harness-engineering.html) harness engineering as "everything surrounding an AI model, except the model itself" — the control layer that handles model invocation, tool orchestration, sandboxed execution, session state, permissions, error recovery, and observability.

For 18 months, teams building production agents had to assemble this layer themselves, using frameworks like LangChain or building from scratch. That era is ending. The labs have shipped their own harnesses, and the pricing war between them tells you everything about where the market is heading.

## What the Labs Shipped

As detailed in a [recent New Stack analysis](https://thenewstack.io/ai-agent-harness-pricing-split/) (Janakiram MSV, April 18, 2026):

- **Anthropic** launched **Managed Agents** — a fully hosted runtime at $0.08/session-hour plus standard token costs. It handles long-running sessions, sandboxed code execution, scoped permissions, end-to-end tracing, and MCP-based tool connections. Launch customers include Notion, Rakuten, Sentry, Asana, and Atlassian. Anthropic also ships the open-source **Claude Agent SDK** for teams that want to self-host.

- **OpenAI** updated its open-source **Agents SDK** with a model-native harness, sandbox execution, configurable memory, and MCP integrations — with **no additional runtime fee** beyond standard API pricing. Developers bring their own compute via a Manifest abstraction supporting seven sandbox providers (E2B, Modal, Cloudflare, Vercel, etc.).

- **Google** offers **Vertex AI Agent Engine** — a managed runtime billing sessions, memory, code execution, and observability as separate consumption lines.

- **Microsoft** ships **Foundry Agent Service** with consumption-based billing across models and tools.

- **AWS** is building a Stateful Runtime Environment with OpenAI, plus **Bedrock AgentCore** as a runtime primitives layer.

## When You'd Want the Claude Agent SDK (or Similar)

The Claude Agent SDK and OpenAI Agents SDK are for building **programmatic, production-grade agent systems** where you need:

1. **Multi-step tool use.** Your agent needs to call APIs, execute code, read files, query databases, and chain these actions together across many turns — not just answer questions.

2. **Long-running sessions.** Tasks that take minutes or hours: research workflows, code generation pipelines, data processing agents that monitor and act over time.

3. **Custom tool orchestration.** You're connecting the agent to your own tools, internal APIs, or MCP servers, and you need fine-grained control over how tools are selected and invoked.

4. **Multi-agent architectures.** Delegating subtasks to specialist agents — e.g., a planning agent that spawns research agents and a writing agent, each with different tools and permissions.

5. **Sandboxed execution.** Running agent-generated code safely, with filesystem access, network restrictions, and resource limits.

6. **Production reliability.** You need error recovery, state persistence (so a crashed session can resume), scoped permissions, and observability/tracing.

7. **Enterprise deployment.** Compliance requirements, audit trails, governance, and control over where data flows.

### Managed vs. Self-Hosted

The choice between Anthropic's Managed Agents ($0.08/session-hour, fully hosted) and the open-source Agent SDK (self-hosted, no runtime fee) depends on your situation:

- **Managed** if you want turnkey infrastructure, don't want to operate sandbox environments, and are comfortable with single-vendor lock-in.
- **Self-hosted SDK** if you need control over where agents run, want multi-cloud or on-prem deployment, handle sensitive data that can't leave your infrastructure, or want to optimize costs for your specific workload.

## Why LangChain Is Generally Not Useful Anymore

LangChain emerged in 2023 to solve a real problem: connecting LLMs to tools, managing conversation state, and chaining prompts together when the model APIs offered none of this natively. It was the duct tape that held early agent prototypes together.

That problem has been solved upstream. Here's why LangChain (and similar horizontal orchestration frameworks like CrewAI and VoltAgent) are losing relevance:

### 1. The models now do what the framework did

Early LLMs needed elaborate prompt-chaining logic — LangChain's chains, routers, and output parsers — to accomplish multi-step tasks. Modern models (Claude, GPT-4.1, Gemini) handle tool use, structured output, and multi-turn reasoning natively through their APIs. The orchestration logic that LangChain provided is now built into the model itself.

### 2. The labs ship better harnesses for their own models

As the New Stack article puts it: "LangChain, CrewAI, and VoltAgent compete more directly now with a free, model-native, well-supported harness from the lab whose models they depend on." A harness built by the model provider will always be better-aligned with that model's capabilities than a generic wrapper. The Claude Agent SDK understands Claude's tool use protocol natively. The OpenAI Agents SDK is optimized for OpenAI's models. A model-agnostic framework is, by definition, optimized for none of them.

### 3. The "model-agnostic" pitch is weaker than it sounds

LangChain's value proposition was: write once, swap models freely. In practice, this didn't deliver much value because:

- Different models have different strengths, tool-use protocols, and failure modes. Code that works well with one model often needs reworking for another.
- Most production systems settle on one or two models. The switching cost is in prompt engineering and testing, not in API call syntax.
- The abstraction layer added complexity, bugs, and performance overhead without corresponding benefits.

### 4. Unnecessary abstraction layers hurt more than they help

LangChain wraps simple API calls in deeply nested abstractions. A straightforward `client.messages.create()` call becomes a chain of LangChain objects with their own configuration, error handling, and state management. This makes debugging harder, adds latency, and creates a dependency on a fast-moving library with frequent breaking changes. When something goes wrong, you're debugging LangChain internals instead of your application logic.

### 5. The market has spoken

The New Stack article frames it clearly: "The archetype most exposed by these launches is the horizontal orchestration framework." When the vendor whose models you depend on gives away an open-source harness that is better-aligned with its frontier models, the case for an independent orchestration layer gets very hard to make. The startups that will survive are those differentiating into governance, compliance, vertical depth, or multi-model control — not generic prompt chaining.

## Karpathy's Dobby and the Agent as Universal Interface

The most vivid illustration of where agents are heading isn't an enterprise platform — it's Andrej Karpathy's home automation agent, "Dobby the Elf Claw."

In April 2026, Karpathy [demonstrated](https://beeble.com/en/blog/introducing-dobby-the-ai-assistant-poised-to-disrupt-the-entire-app-market) an agent built on the OpenClaw framework that replaced six separate smart home apps — Sonos, lighting, HVAC, shades, pool controls, security cameras — with a single WhatsApp conversation. Send "Dobby it's sleepy time" and the agent turns off all lights, lowers shades, adjusts the thermostat, and stops the music, across five different device ecosystems.

What makes Dobby interesting isn't the home automation. It's the method. Rather than relying on pre-built integrations or manufacturer APIs, Dobby **autonomously scanned Karpathy's local network**, discovered devices, sent test packets, observed responses, and reverse-engineered undocumented APIs — behaving like a skilled developer learning a new codebase. No configuration files. No app store downloads. No vendor partnerships.

### The lesson: from GUI to LUI

Dobby demonstrates a shift from what one analyst calls the "App Archipelago" — isolated digital silos, each with its own interface, login, and workflow — toward a **Language User Interface (LUI)** where a single conversational agent mediates all interactions.

This matters for finance and business for several reasons:

1. **The interface collapses.** Today, a wealth manager might use one app for portfolio analytics, another for CRM, another for compliance checks, and another for market data. An agent with tool access can unify these into a single conversation — "show me clients whose equity allocation exceeds their risk tolerance and draft an email to schedule reviews." The apps don't disappear, but the user never touches them directly.

2. **Natural language handles nuance that GUIs can't.** Karpathy noted you can tell Dobby the music is "too loud for conversation" rather than specifying a decibel level. Similarly, a financial agent understands "rebalance conservatively given the client's upcoming retirement" in a way that no dashboard slider can express.

3. **API robustness beats UI design.** If agents become the primary interface, the competitive advantage shifts from having the best-looking app to having the most robust, well-documented API. Hardware and software companies will need to optimize for machine consumption, not human navigation. In finance, this favors data providers and platforms with clean APIs over those with polished but siloed interfaces.

4. **Accessibility is democratized.** A natural language interface makes sophisticated systems accessible to people who can describe what they want but struggle with complex multi-app workflows. A junior analyst who can articulate a research question gets the same tool access as someone who knows which Bloomberg terminal function to use.

### The connection to agent SDKs

Dobby is exactly the kind of system you'd build with an Agent SDK. It requires persistent state (knowing what devices exist on the network), tool orchestration (calling different device APIs), autonomous exploration (scanning and reverse-engineering), and long-running operation (always listening on WhatsApp). This is well beyond what a simple API call or a LangChain chain can handle — it's a full harness application.

The deeper point is that Karpathy isn't building Dobby to sell it. He's demonstrating that the **agent is becoming the universal interface layer** between humans and software. The apps, APIs, and devices behind it become interchangeable plumbing. The agent — with its harness of tools, memory, and orchestration — is what the user actually interacts with. That's why the labs are racing to own the harness layer, and why the harness pricing war described in the New Stack article matters so much. Whoever controls how agents are built and run controls the new interface layer.

## The Bottom Line

If you're building agents today:

- **For simple tasks** (single-turn tool use, basic chat applications): just use the model API directly. You don't need a framework or an SDK.
- **For production agent systems**: use the Agent SDK from your model provider (Claude Agent SDK, OpenAI Agents SDK) or a managed service (Anthropic Managed Agents, Vertex AI Agent Engine).
- **For enterprise governance and multi-model control**: consider specialized platforms like Sycamore that differentiate on trust and compliance rather than generic orchestration.
- **Skip LangChain.** The problems it solved are now solved better by the model providers themselves. Adding it to a new project introduces unnecessary complexity and a dependency on a framework that is being squeezed from all sides.

The harness layer has been absorbed by the labs. The build-vs-buy calculus now has real reference points — $0.08/session-hour for managed, or free SDKs with your own compute. Building from scratch or using an independent framework has to beat both benchmarks on workload fit and team sustainability.
