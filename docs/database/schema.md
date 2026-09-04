# Database Schema

## User

| Field                   | Type       | Nullable | Unique | Key | Mutable | Notes                 |
| ----------------------- | ---------- | -------- | ------ | --- | ------- | --------------------- |
| `id`                    | `BIGINT`   | No       | Yes    | PK  | No      | Internal identifier   |
| `full_name`             | `VARCHAR`  | No       | No     | —   | Yes     | Optional username     |
| `email`                 | `VARCHAR`  | No       | Yes    | —   | Yes     | will use for Auth     |
| `phone_number`          | `VARCHAR`  | Yes      | Yes    | —   | Yes     | —                     |
| `password`              | `TEXT`     | No       | No     | —   | Yes     | —                     |
| `is_active`             | `BOOLEAN`  | No       | -      | —   | Yes     | —                     |
| `access_level`          | `ENUM`     | No       | -      | —   | Yes     | —                     |
| `created_at`            | `TIMESTAMP`| No       | -      | —   | No      | Account creation time |
| `updated_at`            | `TIMESTAMP`| No       | -      | —   | Yes     | Last update time      |




## Todos

| Field                   | Type       | Nullable | Unique | Key | Mutable | Notes                 |
| ----------------------- | ---------- | -------- | ------ | --- | ------- | --------------------- |
| `id`                    | `BIGINT`   | No       | Yes    | PK  | No      | Internal identifier   |
| `title`                 | `VARCHAR`  | No       | No     | —   | Yes     | —                     |
| `user_id`               | `BIGINT`   | No       | No     | FK  | No      | on_delete=CASCADE     |
| `description`           | `TEXT`     | Yes      | No     | —   | Yes     | —                     |
| `priority`              | `ENUM`     | Yes      | No     | —   | Yes     | —                     |
| `due_date`              | `TIMESTAMP`| Yes      | -      | —   | Yes     | —                     |
| `status`                | `ENUM`     | No       | -      | —   | Yes     | —                     |
| `todo_type`             | `ENUM`     | No       | -      | —   | Yes     | default=task          |
| `created_at`            | `TIMESTAMP`| No       | -      | —   | No      | —                     |
| `updated_at`            | `TIMESTAMP`| No       | -      | —   | Yes     | —                     |


## Enums
User.access_level:
  - user_free
  - user_premium
  - admin

Todo.priority:
  - 1
  - 2
  - 3
  - 4
  - 5

Todo.status:
  - pending
  - in_progress
  - completed
  - archived

Todo.todo_type:
  - task
  - event
  - reminder