# Tasks: Multi-User Todo Full-Stack Web Application

**Input**: Design documents from `specs/001-multi-user-todo-auth/`

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Create project structure (`backend` and `frontend` directories).
- [X] T002 Initialize Python project in `backend` with FastAPI, SQLModel, and Better Auth dependencies.
- [X] T003 Initialize Next.js project in `frontend`.
- [X] T004 [P] Configure linting and formatting tools for both projects.

---

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T005 Setup database connection and session management in `backend/src/database.py`.
- [X] T006 [P] Implement JWT authentication middleware in `backend/src/auth.py`.
- [X] T007 [P] Setup API routing in `backend/src/main.py`.
- [X] T008 Create base models for User and Task in `backend/src/models.py`.
- [X] T009 Configure error handling and logging for the FastAPI application.
- [X] T010 Setup environment configuration for both `backend` and `frontend`.

---

## Phase 3: User Story 1 - User Authentication (P1) 🎯 MVP

**Goal**: Allow users to create an account and log in.
**Independent Test**: A user can register, log in, and receive a JWT.

- [X] T011 [US1] Implement user creation endpoint (`/api/signup`) in `backend/src/main.py`.
- [X] T012 [US1] Implement user login endpoint (`/api/login`) in `backend/src/main.py`.
- [X] T013 [P] [US1] Create signup form in `frontend/src/app/signup/page.js`.
- [X] T014 [P] [US1] Create login form in `frontend/src/app/login/page.js`.
- [X] T015 Implement authentication state management in the frontend. (Note: `jwt-decode` installation failed due to network issues. Please install manually after resolving network connectivity.)

---

## Phase 4: User Story 2 - Create Task (P1)

**Goal**: Allow logged-in users to create tasks.
**Independent Test**: A logged-in user can create a task and it appears in their list.

- [X] T016 [US2] Implement create task endpoint (`/api/{user_id}/tasks`) in `backend/src/main.py`.
- [X] T017 [P] [US2] Create "new task" form in `frontend/src/components/NewTaskForm.js`.
- [X] T018 Implement API call to create a new task from the frontend.

---

## Phase 5: User Story 3 - View Tasks (P1)

**Goal**: Allow logged-in users to view their tasks.
**Independent Test**: A logged-in user can see their tasks, but not tasks from other users.

- [X] T019 [US3] Implement "get all tasks" endpoint (`/api/{user_id}/tasks`) in `backend/src/main.py`.
- [X] T020 [US3] Implement "get single task" endpoint (`/api/{user_id}/tasks/{id}`) in `backend/src/main.py`.
- [X] T021 [P] [US3] Create task list component in `frontend/src/components/TaskList.js`.
- [X] T022 [P] Create task detail page in `frontend/src/app/tasks/[id]/page.js`.

---

## Phase 6: User Story 4 - Update Task (P2)

**Goal**: Allow logged-in users to update their tasks.
**Independent Test**: A logged-in user can edit a task and the changes are persisted.

- [X] T023 [US4] Implement update task endpoint (`/api/{user_id}/tasks/{id}`) in `backend/src/main.py`.
- [X] T024 [P] Create "edit task" form in `frontend/src/components/EditTaskForm.js`.

---

## Phase 7: User Story 5 - Delete Task (P2)

**Goal**: Allow logged-in users to delete their tasks.
**Independent Test**: A logged-in user can delete a task and it is removed.

- [X] T025 [US5] Implement delete task endpoint (`/api/{user_id}/tasks/{id}`) in `backend/src/main.py`.
- [X] T026 [P] [US5] Add delete button to task view in the frontend.

---

## Phase 8: User Story 6 - Complete Task (P2)

**Goal**: Allow logged-in users to mark tasks as complete.
**Independent Test**: A logged-in user can mark a task as complete and its status is updated.

- [X] T027 Implement "complete task" endpoint (`/api/{user_id}/tasks/{id}/complete`) in `backend/src/main.py`.
- [X] T028 [P] Add "complete" button/checkbox to task view in the frontend.

---

## Phase 9: Polish & Cross-Cutting Concerns

- [X] T029 [P] Add responsive styles to the frontend.
- [X] T030 Add comprehensive error handling to the frontend.
- [X] T031 Write documentation for the API.

---

## Dependencies & Execution Order

-   **Phase 1 & 2**: Must be completed before any user story work can begin.
-   **User Stories**: Can be implemented in parallel after Phase 2 is complete, but it is recommended to follow the priority order (P1 then P2).

## Implementation Strategy

### MVP First (User Story 1)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently.

### Incremental Delivery

1.  Complete Setup + Foundational.
2.  Add User Story 1 → Test independently.
3.  Add User Story 2, 3 → Test independently.
4.  Add User Story 4, 5, 6 → Test independently.
