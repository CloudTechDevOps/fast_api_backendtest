# FastAPI + MySQL RDS CRUD (beginner project)

## 1. Project structure

```text
fastapi_mysql_crud/
├── main.py
├── db.py
├── .env                 # create this yourself; do not commit it
├── .env.example
├── create_table.sql
├── requirements.txt
├── .gitignore
└── README.md
```

- `main.py`: FastAPI application and five CRUD routes.
- `db.py`: MySQL connection code, imported by `main.py`.
- `.env`: database settings; keep credentials here, not in Python code.

## 2. Create and activate a virtual environment

### Windows Command Prompt

```bat
py -m venv .venv
.venv\Scripts\activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure the database

1. Copy `.env.example` to a new file named `.env`.
2. Replace the sample values with your RDS endpoint, username, password, database name, and port.
3. Make sure the MySQL database exists.
4. Run `create_table.sql` against that database to create the `users` table.

For Amazon RDS, confirm the DB security group allows inbound TCP port `3306` from the machine or server running this API. Avoid opening the database to `0.0.0.0/0`.

## 5. Start FastAPI

From the project directory, with the virtual environment activated:

```bash
uvicorn main:app --reload
```

API base URL: `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

## 6. Postman testing

Create a Postman collection and use this base URL:

```text
http://127.0.0.1:8000
```

### A. Create user

- Method: `POST`
- URL: `http://127.0.0.1:8000/users`
- Body → raw → JSON:

```json
{
  "name": "Veera",
  "email": "veera@example.com"
}
```

Expected: HTTP `201`, with a new user ID.

### B. Get all users

- Method: `GET`
- URL: `http://127.0.0.1:8000/users`

Expected: HTTP `200` and a JSON array.

### C. Get one user

- Method: `GET`
- URL: `http://127.0.0.1:8000/users/1`

Replace `1` with an ID that exists.

### D. Update user

- Method: `PUT`
- URL: `http://127.0.0.1:8000/users/1`
- Body → raw → JSON:

```json
{
  "name": "Veera Updated",
  "email": "veera.updated@example.com"
}
```

### E. Delete user

- Method: `DELETE`
- URL: `http://127.0.0.1:8000/users/1`

Replace `1` with the ID to delete.

## 7. Quick curl tests (optional)

```bash
curl http://127.0.0.1:8000/users
curl http://127.0.0.1:8000/users/1
curl -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" -d "{\"name\":\"Veera\",\"email\":\"veera@example.com\"}"
curl -X PUT http://127.0.0.1:8000/users/1 -H "Content-Type: application/json" -d "{\"name\":\"Veera Updated\",\"email\":\"veera.updated@example.com\"}"
curl -X DELETE http://127.0.0.1:8000/users/1
```

## 8. CRUD route summary

| Operation | Method | Endpoint |
|---|---|---|
| Create | POST | `/users` |
| Read all | GET | `/users` |
| Read one | GET | `/users/{user_id}` |
| Update | PUT | `/users/{user_id}` |
| Delete | DELETE | `/users/{user_id}` |

## Notes

- FastAPI validates request JSON using the `User` Pydantic model.
- SQL values use `%s` placeholders and parameter tuples; do not build SQL by concatenating user input.
- `conn.commit()` saves INSERT, UPDATE, and DELETE changes.
- If a request fails, check the API terminal output and RDS connectivity/security-group settings.
- If you shared a real database password in a chat or source file, rotate it in RDS and update your local `.env`.
