# Data Model: AI Chat Agent with Frontend Integration

**Date**: 2026-01-29

## Entities

### Conversation

Represents a chat session between a user and the AI agent. A conversation is initiated by a user and can contain multiple messages.

**Fields**:
-   `id`: UUID (Primary Key)
-   `user_id`: UUID (Foreign Key, references the authenticated user from Phase II)
-   `created_at`: Datetime (Timestamp of conversation creation)
-   `updated_at`: Datetime (Timestamp of last update to the conversation or its messages)

**Relationships**:
-   One-to-many with `Message` (a Conversation can have many Messages)

**Validation Rules**:
-   `user_id` must correspond to an existing authenticated user.

### Message

Represents a single entry within a `Conversation`. Messages can be from the user, the AI assistant, or represent tool outputs.

**Fields**:
-   `id`: UUID (Primary Key)
-   `conversation_id`: UUID (Foreign Key, references the parent Conversation)
-   `role`: String (e.g., "user", "assistant", "tool", "system")
    -   Validation: Must be one of "user", "assistant", "tool", "system".
-   `content`: Text (The actual message text or JSON string for tool outputs)
    -   Validation: Cannot be empty.
-   `tool_calls`: JSON (Optional, stores structured data for AI tool invocations)
    -   If `role` is "assistant" and tool calls were made.
-   `timestamp`: Datetime (Timestamp when the message was created)

**Relationships**:
-   Many-to-one with `Conversation` (a Message belongs to one Conversation)

**Validation Rules**:
-   `conversation_id` must correspond to an existing `Conversation`.
-   `role` must be a valid type.
-   `content` must not be empty.
