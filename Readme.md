# LifeBuddy App - Auth & User Management Module

## ✅ Status: Completed

This phase focused on building secure and scalable **User Authentication and Authorization** features for the LifeBuddy wellness app backend.

Tip : Keep the .env file in the same directory as main.py and contents would be 

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/lifebuddy_db
SECRET_KEY=xxjdhgfhdg
DEBUG=True
---

To test this module - run the command **docker compose up -d** and in other email start the FASTAPI Server by running unicorn **uvicorn backend.main:backend --reload** and testing can be done in POSTMAN

## 🔧 Features Implemented

### 1. **User Registration API**

* Endpoint: `POST /register`
* Accepts: `username`, `email`, `password`
* Validates:

  * Unique email
  * Unique username
* Stores hashed password securely using **Passlib (bcrypt)**

### 2. **User Login API with JWT**

* Endpoint: `POST /login`
* Uses **OAuth2PasswordRequestForm** for secure form handling
* Returns:

  ```json
  {
    "access_token": "<JWT token>",
    "token_type": "bearer"
  }
  ```

### 3. **JWT Token Handling**

* Tokens include: `sub` (email), `exp` (expiration)
* Created using: `jose.jwt`
* Stored and verified securely using `SECRET_KEY`

### 4. **Protected Routes with JWT**

* Route: `GET /profile`
* Uses dependency injection:

  ```python
  Depends(get_current_user)
  ```
* Only accessible with a valid token in headers:

  ```
  Authorization: Bearer <token>
  ```

### 5. **Password Hashing**

* Passwords are never stored in plain text
* Hashed using `Passlib.bcrypt`
* Verified during login

---

## 🔍 Key Concepts Used

| Concept             | Tech / Library              |
| ------------------- | --------------------------- |
| Web Framework       | FastAPI                     |
| JWT Token Auth      | jose / OAuth2PasswordBearer |
| Password Hashing    | Passlib (bcrypt)            |
| DB ORM              | SQLAlchemy                  |
| Pydantic Schemas    | FastAPI Models              |
| Virtual Environment | `venv` (lbenv)              |

---

## 🧠 Challenges Faced & How I Solved Them

### 🐛 **1. Route Not Found - 404 Errors**

* **Issue:** `/profile` route returned 404
* **Fix:** Forgot to include router in `main.py`. Solved by adding:

  ```python
  from backend.routes import user
  backend.include_router(user.router)
  ```

### 🐛 **2. JWT Error: `AttributeError: module 'models' has no attribute 'User'`**

* **Issue:** Tried accessing `models.User` without importing it correctly
* **Fix:** Imported explicitly from the correct file:

  ```python
  from backend.models.users import User
  ```

### 🐛 **3. Invalid Credentials Despite Correct Details**

* **Issue:** Login kept failing
* **Fix:** Ensured hashed passwords are verified properly:

  ```python
  Hash.verify(input_password, user.hashed_password)
  ```

### 🐛 **4. Postman Login Fail (422 Error)**

* **Issue:** Sent login data as JSON instead of form-data
* **Fix:** Changed Postman body to `x-www-form-urlencoded` as expected by OAuth2

### 🐛 **5. AttributeError for `ShowUser`**

* **Fix:** Defined proper `ShowUser` schema and imported it in router

### 🐛 **6. Uvicorn not found / pip install issues**

* **Fix:** Activated correct virtual environment and ran:

  ```bash
  ./lbenv/bin/pip install uvicorn
  ```

---

## 🚀 Result

* Successfully built and tested full authentication system
* Postman used to test `/register`, `/login`, `/profile`
* Tokens working perfectly with protected routes

---

## 🛠️ Next Steps

* Add Google OAuth login
* Add `/logout` and token revocation support
* Add user roles (admin, user)
* Enable password reset & email verification

