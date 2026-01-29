---
id: 0002
title: Establish Project Constitution v2.0.0
stage: constitution
date: 2026-01-29
surface: agent
model: gemini-cli
feature: none
branch: master
user: ammadkhan
command: /sp.constitution
labels: [constitution, project-management]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution

Project: Phase III — AI-Powered Todo Chatbot (Agent + MCP Architecture)

Scope:
This constitution governs Phase III only and builds on the authenticated,
multi-user Todo system implemented in Phase II. All existing security,
data-ownership, and API guarantees remain in force.

Core principles:
- Agentic correctness (AI actions must be tool-driven, never implicit)
- Stateless execution (no in-memory session or conversation state)
- Tool-first architecture (AI may act only through MCP tools)
- Deterministic behavior (same input + state → same tool calls)
- Clear separation of concerns (Agent ≠ MCP ≠ Storage)
- Spec-driven development (no behavior outside written specs)
- Zero manual coding (Claude Code only)

Architecture invariants:
- The FastAPI server must remain stateless across requests
- All conversation and message history must persist in the database
- AI agents must never access the database directly
- AI agents may interact with tasks only via MCP tools
- MCP tools must be stateless and database-backed
- User identity must be derived from authentication context, not AI inference

Security & identity rules:
- All chat and MCP requests require valid authentication
- User isolation is mandatory at every layer
- Tool invocations must enforce user ownership
- AI must never fabricate or guess task identifiers
- Cross-user access must be impossible by design

AI behavior standards:
- Natural language input must resolve to explicit tool calls
- Tool selection must follow documented behavior rules
- AI responses must confirm actions clearly and accurately
- Errors must be handled gracefully and explained to the user
- Multi-step tool usage is allowed but must remain traceable
- No hallucinated actions or silent failures permitted

MCP standards:
- MCP server must use the Official MCP SDK
- All task operations must be exposed as MCP tools
- Tool input and output schemas must be explicit and validated
- MCP tools must be reusable outside the chatbot context
- Tool responses must be structured and machine-readable

Data integrity rules:
- Conversation and message history must be durable
- Server restarts must not affect chat continuity
- Task state must remain consistent across REST and AI usage
- No duplicate or orphaned records allowed

Frontend standards:
- Chat UI must reflect true backend state
- AI responses must correspond to actual tool outcomes
- Conversation continuity must be preserved across reloads
- Authentication state must be enforced

Constraints:
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Frontend: OpenAI ChatKit
- Authentication: Better Auth
- No direct database access from AI logic
- No manual code outside Claude Code

Out of scope:
- Memory stored inside the AI model
- Background jobs or long-running agents
- Real-time streaming protocols
- Role-based access control
- Non-task AI features (summaries, analytics, recommendations)

Success criteria:
- Users can manage todos through natural language
- AI actions are fully tool-driven and auditable
- MCP tools operate correctly and independently
- Server remains stateless and scalable
- Conversation context survives restarts
- Phase III integrates cleanly with Phase II
- Implementation passes spec and security review

## Response snapshot

I have updated the constitution to version 2.0.0.

## Outcome

- ✅ Impact: Updated project constitution to version 2.0.0.
- 🧪 Tests: No tests were run.
- 📁 Files: 1 file modified.
- 🔁 Next prompts: None.
- 🧠 Reflection: The new constitution is much more detailed and specific to the project.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None