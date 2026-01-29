# Quickstart

**Date**: 2026-01-22

This guide provides instructions for setting up and running the Multi-User Todo Full-Stack Web Application.

## Prerequisites

-   Node.js and npm
-   Python 3.9+ and pip
-   A Neon account and a connection string for a PostgreSQL database.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Backend Setup**:
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    Create a `.env` file in the `backend` directory and add the following:
    ```
    DATABASE_URL=<your-neon-database-url>
    JWT_SECRET=<your-jwt-secret>
    ```

3.  **Frontend Setup**:
    ```bash
    cd frontend
    npm install
    ```
    Create a `.env.local` file in the `frontend` directory and add the following:
    ```
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

## Running the Application

1.  **Start the backend server**:
    ```bash
    cd backend
    uvicorn src.main:app --reload
    ```
    The backend server will be running at `http://localhost:8000`.

2.  **Start the frontend development server**:
    ```bash
    cd frontend
    npm run dev
    ```
    The frontend application will be running at `http://localhost:3000`.
