# LifeBuddyApp

LifeBuddyApp is a habit tracking application built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** (or SQLite for local dev).
It helps users create habits, track completion logs, and manage progress over time.

---

## 🚀 Features

1. **User Authentication**

   * Secure JWT-based login.
   * Token-based authentication using FastAPI security schemes.

2. **Habit Management**

   * Create habits with:

     * Goal name
     * Frequency (daily, weekly, etc.)
     * Start date
   * Update, delete, and view habits.
   * Habits are associated with the authenticated user.

3. **Habit Logging**

   * Log habit completions.
   * Store `status` and `log_date` (or `completed_at`).
   * View logs for a specific habit or all habits.

4. **Validations**

   * Prevent duplicate habits for the same user & goal.
   * Validate log dates and status values.

5. **Testing**

   * CRUD tests for `Habit` and `HabitLog` endpoints.

---

## 🛠 Tech Stack

* **Backend**: FastAPI
* **Database**: PostgreSQL / SQLite (dev)
* **ORM**: SQLAlchemy
* **Auth**: OAuth2PasswordBearer → migrated to HTTPBearer
* **JWT Handling**: python-jose
* **Validation**: Pydantic

---

## 📂 API Endpoints Overview

### Habits

* `GET /habits/` → List all user habits
* `POST /habits/` → Create a habit
* `PUT /habits/{id}` → Update a habit
* `DELETE /habits/{id}` → Delete a habit

### Habit Logs

* `GET /habit-logs/` → List all habit logs
* `GET /habit-logs/habit/{habit_id}` → Get logs for a specific habit
* `POST /habit-logs/` → Create a habit log
* `PUT /habit-logs/{log_id}` → Update a habit log
* `DELETE /habit-logs/{log_id}` → Delete a habit log

---

## 🧠 Development Journey

This project was built step-by-step:

1. **Designed the Habit model** with goal name, frequency, start date.
2. **Added Habit CRUD routes** and tested them in Swagger & Postman.
3. Linked habits to users with a foreign key.
4. Created Habit Log model to store completion data (`completed_at`, `status`).
5. Faced several **Pydantic schema attribute errors** (e.g., `AttributeError: 'HabitLogCreate' object has no attribute 'status'`).

   * **Solution**: Added the missing fields in the corresponding Pydantic schema and ensured models and schemas matched.
6. Fixed Swagger **duplicate endpoints issue**.

   * **Cause**: Mismatched tags in `main.py` and router definition.
   * **Solution**: Unified tags and removed duplication in `include_router`.
7. Migrated from **OAuth2PasswordBearer** to **HTTPBearer** for simpler token handling in Swagger UI.
8. Learned how to **debug SQLAlchemy relationship errors** like `AttributeError: module 'habit_log' has no attribute 'Habit'` by importing the correct models.

---

## ⚡ Challenges & How I Overcame Them

### 1. Duplicate Swagger Endpoints

**Problem**: Two sets of identical endpoints appeared in Swagger.
**Cause**: Router tags mismatched between `main.py` and `routes` files.
**Solution**: Unified tag names and removed extra `tags=[]` in `main.py`.

### 2. Missing Attributes in Schemas

**Problem**: Pydantic models did not match SQLAlchemy models, causing attribute errors.
**Solution**: Synced all schemas with models and tested after every change.

### 3. Relationship Join Errors

**Problem**: Tried joining on a model not imported correctly.
**Solution**: Imported `Habit` from `backend.models.habits` and defined proper relationships.

### 4. Authentication Migration

**Problem**: Swagger login flow was confusing with `OAuth2PasswordBearer`.
**Solution**: Switched to `HTTPBearer` for simpler token-based access in Swagger and Postman.

---

## ⚙️ Installation & Setup

```bash
# 1️⃣ Clone the repo
git clone https://github.com/yourusername/LifeBuddyApp.git
cd LifeBuddyApp

# 2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the app
uvicorn backend.main:app --reload
```

Access the docs at:
➡️ **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
➡️ **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

