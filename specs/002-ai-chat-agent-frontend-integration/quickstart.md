# Quickstart: AI Chat Agent with Frontend Integration

**Date**: 2026-01-29

This guide provides instructions for setting up and running the AI Chat Agent with Frontend Integration feature. This assumes you have already set up the basic multi-user Todo application from Phase II.

## Prerequisites

-   Existing multi-user Todo application set up and running (backend and frontend).
-   An OpenAI API Key for the AI Agents SDK.

## Setup

1.  **Backend Configuration**:
    -   Navigate to the `backend` directory: `cd backend`.
    -   Open your `.env` file (or create it if it doesn't exist).
    -   Add your OpenAI API Key:
        ```
        OPENAI_API_KEY=<your-openai-api-key>
        ```
    -   Install the necessary Python packages using Poetry:
        ```bash
        poetry install
        ```

2.  **Frontend Configuration**:
    -   Navigate to the `frontend` directory: `cd frontend`.
    -   Ensure your `.env.local` file correctly points to your backend API URL (e.g., `NEXT_PUBLIC_API_URL=http://localhost:8000`).
    -   Install the necessary npm packages:
        ```bash
        npm install axios jwt-decode @openai/chatkit
        ```

## Running the Application

1.  **Start the Backend Server**:
    -   Follow the instructions in the main project `quickstart.md` for starting the backend server. Ensure the virtual environment is activated using `poetry shell` and then `uvicorn src.main:app --reload`.

2.  **Start the Frontend Development Server**:
    -   Follow the instructions in the main project `quickstart.md` for starting the frontend development server.

3.  **Access the Feature**:
    -   Navigate to the appropriate chat interface page in your running frontend application (e.g., `http://localhost:3000/chat`).
    -   You should now be able to interact with the AI Chat Agent.