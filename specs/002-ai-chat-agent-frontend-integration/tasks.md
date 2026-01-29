# Tasks: AI Chat Agent with Frontend Integration

**Input**: Design documents from `specs/002-ai-chat-agent-frontend-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: As per research.md, testing will use pytest for backend and Jest/React Testing Library for frontend. Specific test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Update `backend/pyproject.toml` with `openai-agents-sdk`, `SQLModel` and `psycopg2-binary` (or equivalent for Neon DB) dependencies.
- [ ] T002 Update `frontend/package.json` with `@openai/chatkit` dependency.
- [ ] T003 [P] Configure backend environment variable `OPENAI_API_KEY` in `backend/.env`.
- [ ] T004 [P] Configure frontend API URL in `frontend/.env.local` to point to backend.
- [ ] T005 [P] Implement `database.py` in `backend/src/database.py` for SQLModel engine and session management.
- [ ] T006 [P] Implement base `models.py` in `backend/src/models.py` to include `SQLModel` and `UUID` support.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Implement Conversation model in `backend/src/models.py` based on `data-model.md`.
- [ ] T008 Implement Message model in `backend/src/models.py` based on `data-model.md`.
- [ ] T009 Create initial database migrations for Conversation and Message models using `SQLModel` / `Alembic` (if used).
- [ ] T010 [P] Update `backend/src/main.py` to include database initialization and dependency for session.
- [ ] T011 [P] Implement JWT authentication dependency in `backend/src/auth.py` for chat endpoints.
- [ ] T012 [P] Implement `crud.py` in `backend/src/crud.py` for basic Conversation and Message database operations.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User can send a message and receive a response (Priority: P1) 🎯 MVP

**Goal**: User can type a message into the chat interface and receive a response from the AI agent.

**Independent Test**: Send a message to the chat endpoint and verify a valid AI response is returned.

### Tests for User Story 1

- [ ] T013 [P] [US1] Unit test for JWT authentication dependency in `backend/tests/test_auth.py`.
- [ ] T014 [P] [US1] Integration test for chat endpoint `/api/{user_id}/chat` with mock AI agent in `backend/tests/test_main.py`.

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement `schemas.py` in `backend/src/schemas.py` for chat request/response models.
- [ ] T016 [US1] Implement chat API endpoint `POST /api/{user_id}/chat` in `backend/src/main.py`.
- [ ] T017 [US1] Implement basic AI agent initialization using OpenAI Agents SDK in `backend/src/agent.py` (without tool calls initially).
- [ ] T018 [US1] Integrate AI agent into chat endpoint to process user message and return response in `backend/src/main.py`.
- [ ] T019 [US1] Implement basic error handling for chat endpoint in `backend/src/main.py`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User can manage their todo tasks using natural language (Priority: P2)

**Goal**: User can interact with the AI agent to create, read, update, and delete their todo tasks.

**Independent Test**: Issue natural language commands to the AI agent (e.g., "add task buy milk") and verify task changes in the system.

### Tests for User Story 2

- [ ] T020 [P] [US2] Unit test for AI agent's tool selection logic in `backend/tests/test_agent.py`.
- [ ] T021 [P] [US2] Integration test for chat endpoint with AI agent invoking MCP tools in `backend/tests/test_main.py`.

### Implementation for User Story 2

- [ ] T022 [P] [US2] Develop MCP tool wrappers for Todo operations (create, read, update, delete) in `backend/src/mcp_tools.py`.
- [ ] T023 [P] [US2] Attach MCP tool registry to the AI agent in `backend/src/agent.py`.
- [ ] T024 [US2] Update AI agent logic to interpret user intent and invoke MCP tools in `backend/src/agent.py`.
- [ ] T025 [US2] Update chat endpoint to capture and return `tool_calls` in API response in `backend/src/main.py`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Conversation history persists across requests and reloads (Priority: P3)

**Goal**: A user's conversation with the AI agent is saved and restored across browser reloads and new sessions.

**Independent Test**: Have a conversation, reload the page, and verify conversation history is present and functional.

### Tests for User Story 3

- [ ] T026 [P] [US3] Unit test for Conversation and Message CRUD operations in `backend/tests/test_crud.py`.
- [ ] T027 [P] [US3] Integration test for chat endpoint to ensure history persistence in `backend/tests/test_main.py`.

### Implementation for User Story 3

- [ ] T028 [US3] Implement logic to fetch prior conversation messages from database in `backend/src/crud.py`.
- [ ] T029 [US3] Append new user message to conversation history in `backend/src/crud.py`.
- [ ] T030 [US3] Store assistant response and `tool_calls` in database in `backend/src/crud.py`.
- [ ] T031 [US3] Return `conversation_id` consistently from chat endpoint in `backend/src/main.py`.
- [ ] T032 [US3] Implement frontend ChatKit component to send messages to backend chat endpoint in `frontend/src/app/chat/page.tsx` (or similar).
- [ ] T033 [P] [US3] Implement frontend logic to attach JWT authentication to requests in `frontend/src/lib/api.ts` (or similar).
- [ ] T034 [US3] Implement frontend logic to render assistant responses and `tool_calls` verbatim in `frontend/src/app/chat/page.tsx`.
- [ ] T035 [US3] Implement frontend logic to fetch and display conversation history on load in `frontend/src/app/chat/page.tsx`.

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T036 Review and refine error handling across backend endpoints in `backend/src/main.py`.
- [ ] T037 Ensure graceful handling of missing/invalid tasks and prevent hallucinated IDs in `backend/src/agent.py`.
- [ ] T038 Add comprehensive logging for agent actions and tool invocations in `backend/src/agent.py` and `backend/src/main.py`.
- [ ] T039 Implement end-to-end frontend tests for chat interface using `Playwright` or `Cypress` in `frontend/tests/e2e`.
- [ ] T040 Update `quickstart.md` with any refined setup or running instructions.
- [ ] T041 Review and update project documentation (if any) to reflect new feature.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phase 3+)**: All depend on Foundational phase completion
    -   User stories can then proceed in parallel (if staffed)
    -   Or sequentially in priority order (P1 → P2 → P3)
-   **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 components (chat endpoint)
-   **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1 and US2 components (chat endpoint, agent response)

### Within Each User Story

-   Tests MUST be written and FAIL before implementation.
-   Models before services.
-   Services before endpoints/agent logic.
-   Core implementation before integration.
-   Story complete before moving to next priority.

### Parallel Opportunities

-   All Setup tasks marked [P] can run in parallel.
-   All Foundational tasks marked [P] can run in parallel (within Phase 2).
-   Once Foundational phase completes, user stories can start sequentially by priority.
-   Within each User Story phase, tasks marked [P] can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   Developer A: User Story 1
    -   Developer B: User Story 2
    -   Developer C: User Story 3
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
