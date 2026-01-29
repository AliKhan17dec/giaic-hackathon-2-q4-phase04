# Data Model

**Date**: 2026-01-22

This document defines the data models for the User and Task entities.

## User

Represents an account in the system.

| Field           | Type    | Description                   | Constraints      |
| --------------- | ------- | ----------------------------- | ---------------- |
| `id`            | Integer | Primary key                   | Auto-incrementing |
| `username`      | String  | User's chosen username        | Unique, Required |
| `hashed_password` | String  | Hashed password for the user  | Required         |

### Relationships

-   A `User` can have many `Task`s.

## Task

Represents a to-do item.

| Field         | Type    | Description                     | Constraints                             |
| ------------- | ------- | ------------------------------- | --------------------------------------- |
| `id`          | Integer | Primary key                     | Auto-incrementing                       |
| `owner_id`    | Integer | Foreign key to the `User` table | Required, must be a valid `User` id     |
| `title`       | String  | The content of the to-do item   | Required, max length 255                |
| `description` | String  | A more detailed description of the task | Optional |
| `completed`   | Boolean | Whether the task is complete or not | Required, defaults to `false`           |

### Relationships

-   A `Task` belongs to one `User`.
