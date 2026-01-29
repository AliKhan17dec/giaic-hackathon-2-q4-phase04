---
id: 0001
title: Establish Project Constitution
stage: constitution
date: 2026-01-22
surface: agent
model: gemini-pro
feature: none
branch: master
user: {{USER}}
command: /sp.constitution
labels: [constitution, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/tasks-template.md
tests:
  - none
---

## Prompt

/sp.constitution 

Project: Todo Full-Stack Web Application (Auth-enabled, Multi-user, Spec-Driven)

Core principles:
- Security-first development (authentication, authorization, data isolation)
- Spec-driven correctness (implementation must strictly follow approved specs)
- Reproducibility (all behaviors traceable to specs, prompts, and iterations)
- Maintainability (clean architecture, modular services, clear responsibilities)
- Zero manual coding (Claude Code only, agentic workflow enforced)

Key standards:
- All features must map directly to written specifications
- Every API endpoint must enforce JWT-based authentication
- User data isolation is mandatory (no cross-user data access)
- REST conventions must be followed consistently
- Error handling must be explicit and predictable (401, 403, 404, 422)
- Secrets and credentials must be environment-based (no hardcoding)

Technology constraints:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Spec workflow: Spec-Kit Plus + Claude Code only

Authentication & Security Rules:
- All API routes require a valid JWT token
- JWT must be verified on every request using shared secret
- User identity must be derived from token, not request body
- Route user_id must match authenticated user_id
- Unauthorized requests must return HTTP 401
- Forbidden cross-user access must return HTTP 403
- Token expiry must be enforced

API Standards:
- Endpoints must exactly match the defined REST contract
- HTTP methods must reflect correct semantics
- All task queries must be filtered by authenticated user
- Task ownership must be validated on every operation
- PATCH endpoints must be idempotent where applicable

Data integrity rules:
- Each task must be linked to a single user
- No orphaned tasks allowed
- Deletions must be scoped to owner only
- Database schema must support multi-user isolation

Frontend standards:
- Responsive UI across desktop and mobile
- Auth state must be respected across routes
- JWT token must be attached to every API request
- No unauthenticated access to protected views

Success criteria:
- All 5 basic-level features fully implemented
- Secure multi-user task isolation verified
- JWT authentication enforced across frontend and backend
- API behavior matches spec exactly
- No manual code written outside Claude Code
- Project passes security and spec compliance review

## Response snapshot

- Updated the project constitution in `.specify/memory/constitution.md` with the provided principles, standards, and technology constraints.
- Set the constitution version to `1.0.0` and the ratification and amendment dates to `2026-01-22`.
- Updated `.specify/templates/plan-template.md` to align the "Constitution Check" and "Technical Context" sections with the new constitution.
- Updated `.specify/templates/tasks-template.md` to align the "Path Conventions" and "Foundational Tasks" with the new constitution.
- Created a Prompt History Record for this transaction.

## Outcome

- ✅ Impact: Established the project's constitution and aligned dependent templates.
- 🧪 Tests: No tests were run.
- 📁 Files: 3 files modified.
- 🔁 Next prompts: /sp.specify
- 🧠 Reflection: The process of updating the constitution and propagating the changes to the templates was successful.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a