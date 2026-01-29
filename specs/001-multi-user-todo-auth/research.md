# Research: Testing Frameworks

**Date**: 2026-01-22

## Decision

-   **Backend (FastAPI)**: `pytest` will be used as the testing framework.
-   **Frontend (Next.js)**: `Jest` and `React Testing Library` will be used for testing the frontend components and logic.

## Rationale

-   **`pytest`**: It is the de-facto standard for testing in the Python ecosystem. It has a rich ecosystem of plugins and is well-suited for testing FastAPI applications.
-   **`Jest` and `React Testing Library`**: Jest is a popular testing framework for JavaScript applications, and it is the default choice for `create-react-app`. React Testing Library provides a set of utilities for testing React components in a way that resembles how users interact with them, which aligns with our goal of building a user-centric application.

## Alternatives Considered

-   **`unittest` (Python)**: While part of the standard library, `pytest` offers a more concise syntax and a more powerful feature set.
-   **`Mocha` and `Chai` (JavaScript)**: These are also popular choices for testing JavaScript applications, but Jest provides an all-in-one solution with a built-in test runner, assertion library, and mocking capabilities.
