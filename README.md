# 🚀 FastAPI Todo App

A modern, asynchronous Todo backend built with **FastAPI**, **PostgreSQL**, **SQLAlchemy 2**, **Alembic**, **JWT Authentication**, **Docker**, and **uv**.

> 🎓 This project is primarily developed as a learning project for practicing modern backend architecture, secure API development, database management, containerization, testing, and Python development best practices.

🔗 **GitHub Repository:**
https://github.com/sajadhatami/fastAPI-learning-Project/

---

## 🇬🇧 English

## 📖 About the Project

**FastAPI Todo App** is a backend application built with **FastAPI** and modern Python development tools.

The main purpose of this project is to practice and demonstrate how to build a maintainable backend application using:

* Layered architecture
* RESTful API design
* Asynchronous database access
* JWT-based authentication
* Password hashing with Argon2
* Database migrations
* Docker-based development
* Unit of Work pattern
* Repository and Service patterns
* Automated testing
* Secure object-level authorization

The application currently provides authentication and Todo management features while following a modular and scalable project structure.

---

## 🛠️ Tech Stack

| Technology          | Purpose                             |
| ------------------- | ----------------------------------- |
| **Python 3.13**     | Programming language                |
| **FastAPI**         | Backend web framework               |
| **PostgreSQL 18**   | Relational database                 |
| **SQLAlchemy 2**    | ORM                                 |
| **asyncpg**         | Asynchronous PostgreSQL driver      |
| **Alembic**         | Database migrations                 |
| **uv 0.12.7**       | Dependency & environment management |
| **Docker**          | Containerization                    |
| **Docker Compose**  | Multi-container development         |
| **PyJWT**           | JWT authentication                  |
| **pwdlib / Argon2** | Secure password hashing             |
| **Scalar**          | API documentation                   |
| **Pytest**          | Testing framework                   |
| **pytest-asyncio**  | Async test support                  |
| **pgAdmin**         | Database administration             |

---

## 🏗️ Architecture

The project follows a **Layered Architecture** to keep responsibilities separated and the codebase maintainable.

```text
Client
  │
  ▼
API / Routers
  │
  ▼
Services
  │
  ▼
Repositories
  │
  ▼
Database
```

### API / Routers

Responsible for:

* Receiving HTTP requests
* Validating input
* Returning HTTP responses
* Managing API routes
* Handling authentication dependencies

### Services

Contains the application's **business logic**.

Services are responsible for:

* Applying business rules
* Managing authorization
* Coordinating repositories
* Preventing unauthorized access to resources

### Repositories

Responsible for database interaction.

Repositories abstract database operations away from the business logic and provide a cleaner separation of concerns.

### Unit of Work

The project uses the **Unit of Work pattern** to coordinate database operations and transactions safely.

This allows multiple repository operations to be handled within a single transactional context.

---

## 🔐 Security

Security is an important part of the project.

### JWT Authentication

Authentication is implemented using **JSON Web Tokens (JWT)**.

Users authenticate through the login endpoint and receive a Bearer token that must be included when accessing protected resources.

```text
Authorization: Bearer <access_token>
```

### Password Security

Passwords are never stored in plain text.

They are hashed using **Argon2** through `pwdlib`.

### BOLA Protection

The Todo endpoints are protected against **Broken Object Level Authorization (BOLA)**.

A user can only access, update, or delete their own Todo items.

For example:

```text
User A
  │
  ├── Todo 1 ✅
  ├── Todo 2 ✅
  │
  └── User B's Todo ❌
```

Authorization is enforced at the service layer rather than relying only on route-level checks.

---

## 🗃️ Database Schema

The application currently uses two primary tables:

### `users`

| Field             | Description                         |
| ----------------- | ----------------------------------- |
| `id`              | Unique user identifier              |
| `full_name`       | User's full name                    |
| `email`           | Unique email address used for login |
| `phone_number`    | User phone number                   |
| `hashed_password` | Securely hashed password            |
| `is_active`       | User activation status              |
| `role`            | User role                           |

Available roles:

```text
ADMIN
USER
PREMIUM
```

### `todos`

| Field         | Description          |
| ------------- | -------------------- |
| `id`          | Todo identifier      |
| `title`       | Todo title           |
| `description` | Todo description     |
| `priority`    | Priority from 1 to 5 |
| `type`        | Todo type            |
| `status`      | Current Todo status  |
| `due_date`    | Optional due date    |
| `user_id`     | Owner of the Todo    |

Available Todo types:

```text
TASK
EVENT
REMINDER
```

Available statuses:

```text
PENDING
IN_PROGRESS
COMPLETED
ARCHIVED
```

The `user_id` field references the `users` table and supports **cascade deletion**.

---

## 🌐 API Endpoints

### 🔑 Authentication

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| `POST` | `/auth/register` | Register a new user   |
| `POST` | `/auth/login`    | Login and receive JWT |

### ✅ Todos

| Method   | Endpoint           | Description                                 |
| -------- | ------------------ | ------------------------------------------- |
| `POST`   | `/todos/`          | Create a new Todo                           |
| `GET`    | `/todos/`          | Get all Todos belonging to the current user |
| `GET`    | `/todos/{todo_id}` | Get a specific Todo                         |
| `PUT`    | `/todos/{todo_id}` | Update a Todo                               |
| `DELETE` | `/todos/{todo_id}` | Delete a Todo                               |

All Todo endpoints require authentication.

---

## 📁 Project Structure

A simplified view of the project architecture:

```text
fastAPI-learning-Project/
│
├── src/
│   └── fastapi_learning_project/
│       ├── api/
│       │   └── routers/
│       │
│       ├── services/
│       │
│       ├── repositories/
│       │
│       ├── models/
│       │
│       ├── schemas/
│       │
│       ├── db/
│       │
│       └── main.py
│
├── tests/
│   ├── ...
│
├── alembic/
│
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## ⚙️ Prerequisites

Before running the project, make sure the following tools are installed:

* Python 3.13+
* Docker
* Docker Compose
* uv

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`.

```env
POSTGRES_DB=fastapi_learning
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

DATABASE_URL=your_database_url

PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=your_password

SECRET_KEY=your_secret_key
```

### Environment Variables

| Variable                   | Description                         |
| -------------------------- | ----------------------------------- |
| `POSTGRES_DB`              | PostgreSQL database name            |
| `POSTGRES_USER`            | PostgreSQL username                 |
| `POSTGRES_PASSWORD`        | PostgreSQL password                 |
| `DATABASE_URL`             | Application database connection URL |
| `PGADMIN_DEFAULT_EMAIL`    | pgAdmin login email                 |
| `PGADMIN_DEFAULT_PASSWORD` | pgAdmin login password              |
| `SECRET_KEY`               | Secret key used for JWT             |

> ⚠️ Never commit your real `.env` file or production secrets to Git.

---

## 🐳 Running with Docker

The recommended development setup uses Docker Compose.

Clone the repository:

```bash
git clone https://github.com/sajadhatami/fastAPI-learning-Project.git
cd fastAPI-learning-Project
```

Create the environment file:

```bash
cp .env.example .env
```

Then start the application:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

View API logs:

```bash
docker compose logs -f api
```

---

## 🐍 Running Locally with uv

You can also run the application without containerizing the API.

Install/sync dependencies:

```bash
uv sync
```

Run the FastAPI development server:

```bash
uv run fastapi dev src/fastapi_learning_project/main.py
```

---

## 🗄️ Database & Migrations

Alembic is used to manage database schema migrations.

Create a new migration:

```bash
uv run alembic revision --autogenerate -m "message"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

Rollback the latest migration:

```bash
uv run alembic downgrade -1
```

For direct PostgreSQL access inside Docker:

```bash
docker compose exec postgres psql -U postgres -d fastapi_learning
```

---

## 🧪 Testing

The project uses:

* **pytest**
* **pytest-asyncio**

Tests are located in the:

```text
tests/
```

directory.

Run all tests with:

```bash
uv run pytest
```

The test suite includes coverage for:

* Authentication
* User-related flows
* Todo functionality
* BOLA protection
* Database interaction

Database tests are isolated using separate transactions and `create_savepoint` to avoid unwanted changes between tests.

---

## 📚 API Documentation

The project uses **Scalar** for API documentation.

After starting the application, open:

```text
/scalar
```

For example:

```text
http://localhost:<API_PORT>/scalar
```

Scalar provides an interactive interface for exploring and testing the API endpoints.

---

## 🐘 pgAdmin

The PostgreSQL database can be managed through **pgAdmin**.

Open:

```text
http://localhost:5050
```

Use the credentials configured through:

```env
PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD
```

---

## 🐳 Useful Docker Commands

Start services:

```bash
docker compose up -d
```

Rebuild and start:

```bash
docker compose up -d --build
```

Stop services:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f api
```

View all service logs:

```bash
docker compose logs -f
```

Open a PostgreSQL shell:

```bash
docker compose exec postgres psql -U postgres -d fastapi_learning
```

---

## 🎯 Project Goals

This project focuses on learning and practicing:

```text
✅ FastAPI
✅ Async Python
✅ REST API design
✅ PostgreSQL
✅ SQLAlchemy 2
✅ Alembic
✅ JWT Authentication
✅ Argon2 Password Hashing
✅ Docker & Docker Compose
✅ Repository Pattern
✅ Service Layer
✅ Unit of Work
✅ Secure Authorization
✅ BOLA Protection
✅ Automated Testing
```

---

## 🚧 Future Improvements

Possible future improvements include:

* Refresh token support
* Role-based access control
* Pagination and filtering
* Todo search
* Better API error handling
* Rate limiting
* Production configuration
* CI/CD pipeline
* More comprehensive test coverage
* API versioning
* Observability and logging

---

## 📜 License

This project is licensed under the **MIT License**.

Copyright © 2026 **Sajad Hatami**

---

# 🇮🇷 فارسی

## 📖 درباره پروژه

**FastAPI Todo App** یک پروژه بک‌اند مدرن است که با استفاده از **FastAPI** و ابزارهای جدید اکوسیستم پایتون توسعه داده شده است.

هدف اصلی پروژه، تمرین و پیاده‌سازی مفاهیم مهم توسعه بک‌اند مدرن است، از جمله:

* معماری لایه‌ای
* طراحی RESTful API
* ارتباط ناهمگام با دیتابیس
* احراز هویت مبتنی بر JWT
* هش امن پسورد با Argon2
* مدیریت Migration های دیتابیس
* Docker و Docker Compose
* الگوی Unit of Work
* Repository و Service Pattern
* تست‌نویسی خودکار
* کنترل دسترسی در سطح Object

این پروژه در حال حاضر سیستم احراز هویت و مدیریت Todo را پیاده‌سازی می‌کند و ساختار آن به شکلی طراحی شده که قابلیت توسعه در آینده را داشته باشد.

---

## 🛠️ تکنولوژی‌های استفاده‌شده

| تکنولوژی            | کاربرد                         |
| ------------------- | ------------------------------ |
| **Python 3.13**     | زبان برنامه‌نویسی              |
| **FastAPI**         | فریم‌ورک بک‌اند                |
| **PostgreSQL 18**   | پایگاه داده                    |
| **SQLAlchemy 2**    | ORM                            |
| **asyncpg**         | درایور Async PostgreSQL        |
| **Alembic**         | مدیریت Migration               |
| **uv 0.12.7**       | مدیریت Dependency و محیط پروژه |
| **Docker**          | کانتینرسازی                    |
| **Docker Compose**  | اجرای سرویس‌ها                 |
| **PyJWT**           | احراز هویت JWT                 |
| **pwdlib / Argon2** | هش پسورد                       |
| **Scalar**          | مستندات API                    |
| **Pytest**          | فریم‌ورک تست                   |
| **pytest-asyncio**  | اجرای تست‌های Async            |
| **pgAdmin**         | مدیریت PostgreSQL              |

---

## 🏗️ معماری پروژه

پروژه از **Layered Architecture** استفاده می‌کند.

ساختار کلی:

```text
Client
  │
  ▼
API / Routers
  │
  ▼
Services
  │
  ▼
Repositories
  │
  ▼
Database
```

### API / Routers

این لایه مسئول دریافت Request، اعتبارسنجی ورودی‌ها، مدیریت Route ها و ارسال Response است.

### Services

منطق اصلی و قوانین تجاری برنامه در این لایه قرار دارد.

همچنین کنترل دسترسی کاربران به Todo ها در این لایه انجام می‌شود.

### Repositories

این لایه مسئول ارتباط مستقیم با دیتابیس است و عملیات مربوط به خواندن و نوشتن داده‌ها را از منطق برنامه جدا می‌کند.

### Unit of Work

برای مدیریت امن تراکنش‌ها از الگوی **Unit of Work** استفاده شده است.

این الگو امکان اجرای چند عملیات دیتابیس را در قالب یک Transaction فراهم می‌کند.

---

## 🔐 امنیت

امنیت یکی از بخش‌های مهم این پروژه است.

### احراز هویت JWT

کاربر پس از Login یک JWT دریافت می‌کند و برای دسترسی به APIهای محافظت‌شده باید آن را به صورت Bearer Token ارسال کند.

```text
Authorization: Bearer <access_token>
```

### هش کردن پسورد

پسورد کاربران به صورت متن ساده ذخیره نمی‌شود و با استفاده از **Argon2** هش می‌شود.

### مقابله با BOLA

پروژه در برابر **Broken Object Level Authorization (BOLA)** محافظت شده است.

یعنی هر کاربر فقط می‌تواند Todo های متعلق به خودش را مشاهده، ویرایش یا حذف کند.

```text
کاربر A
  │
  ├── Todo 1 ✅
  ├── Todo 2 ✅
  │
  └── Todo کاربر B ❌
```

---

## 🗃️ ساختار دیتابیس

پروژه دارای دو جدول اصلی است.

### جدول `users`

شامل اطلاعات:

```text
id
full_name
email
phone_number
hashed_password
is_active
role
```

نقش‌های تعریف‌شده:

```text
ADMIN
USER
PREMIUM
```

### جدول `todos`

شامل:

```text
id
title
description
priority
type
status
due_date
user_id
```

نوع Todo:

```text
TASK
EVENT
REMINDER
```

وضعیت Todo:

```text
PENDING
IN_PROGRESS
COMPLETED
ARCHIVED
```

هر Todo به یک User تعلق دارد و در صورت حذف کاربر، Todo های مربوط به او نیز با قابلیت **Cascade Delete** حذف می‌شوند.

---

## 🌐 API ها

### احراز هویت

```text
POST /auth/register
```

ثبت کاربر جدید.

```text
POST /auth/login
```

ورود کاربر و دریافت JWT.

### مدیریت Todo

```text
POST /todos/
```

ایجاد Todo جدید.

```text
GET /todos/
```

دریافت Todo های کاربر فعلی.

```text
GET /todos/{todo_id}
```

دریافت یک Todo مشخص.

```text
PUT /todos/{todo_id}
```

ویرایش Todo.

```text
DELETE /todos/{todo_id}
```

حذف Todo.

تمام Endpoint های مربوط به Todo نیازمند احراز هویت هستند.

---

## ⚙️ راه‌اندازی پروژه

### اجرای پروژه با Docker

```bash
git clone https://github.com/sajadhatami/fastAPI-learning-Project.git
cd fastAPI-learning-Project
```

سپس:

```bash
cp .env.example .env
```

و پروژه را اجرا کنید:

```bash
docker compose up -d --build
```

### اجرای پروژه با uv

```bash
uv sync
```

سپس:

```bash
uv run fastapi dev src/fastapi_learning_project/main.py
```

---

## 🔐 متغیرهای محیطی

فایل `.env` را بر اساس `.env.example` ایجاد کنید.

```env
POSTGRES_DB=fastapi_learning
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

DATABASE_URL=your_database_url

PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=your_password

SECRET_KEY=your_secret_key
```

اطلاعات واقعی و Secret ها را هرگز داخل Git Commit نکنید.

---

## 🧪 تست

تست‌های پروژه در پوشه:

```text
tests/
```

قرار دارند.

اجرای تست‌ها:

```bash
uv run pytest
```

تست‌ها بخش‌هایی مانند:

* Authentication
* Todo
* BOLA Protection
* ارتباط با دیتابیس

را پوشش می‌دهند.

برای جلوگیری از تأثیر تست‌ها روی یکدیگر، تراکنش‌های دیتابیس به صورت ایزوله و با استفاده از `create_savepoint` مدیریت می‌شوند.

---

## 📚 مستندات API

مستندات تعاملی API توسط **Scalar** ارائه می‌شوند.

پس از اجرای پروژه، آدرس زیر را باز کنید:

```text
/scalar
```

---

## 🐘 مدیریت دیتابیس با pgAdmin

پنل pgAdmin روی پورت `5050` در دسترس است:

```text
http://localhost:5050
```

اطلاعات ورود از متغیرهای زیر خوانده می‌شوند:

```env
PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD
```

---

## 🗄️ Migration

ایجاد Migration جدید:

```bash
uv run alembic revision --autogenerate -m "message"
```

اعمال Migration ها:

```bash
uv run alembic upgrade head
```

بازگشت آخرین Migration:

```bash
uv run alembic downgrade -1
```

---

## 🎯 اهداف آموزشی پروژه

این پروژه با هدف تمرین موارد زیر ساخته شده است:

```text
✅ FastAPI
✅ Async Python
✅ REST API
✅ PostgreSQL
✅ SQLAlchemy 2
✅ Alembic
✅ JWT
✅ Argon2
✅ Docker
✅ Docker Compose
✅ Repository Pattern
✅ Service Layer
✅ Unit of Work
✅ Authorization
✅ BOLA Protection
✅ Automated Testing
```

---

## 🚧 توسعه‌های آینده

برخی قابلیت‌هایی که می‌توان در آینده به پروژه اضافه کرد:

* Refresh Token
* Role-Based Access Control
* Pagination
* Filtering
* Search
* Rate Limiting
* CI/CD
* Logging و Monitoring
* Versioning برای API
* افزایش پوشش تست‌ها

---

## 📜 لایسنس

این پروژه تحت **MIT License** منتشر شده است.

Copyright © 2026 **Sajad Hatami**

---

## 🔗 Repository

**GitHub:**
https://github.com/sajadhatami/fastAPI-learning-Project/
