from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from db import get_connection

app = FastAPI(title="Users CRUD API")


class User(BaseModel):
    name: str
    email: EmailStr


@app.get("/")
def home():
    return {"message": "Users API is running"}


@app.get("/users")
def get_users():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        cursor.close()
        conn.close()


@app.post("/users", status_code=201)
def add_user(user: User):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (user.name, user.email)
        )
        conn.commit()
        return {"message": "User added", "id": cursor.lastrowid}
    finally:
        cursor.close()
        conn.close()


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute(
            "UPDATE users SET name = %s, email = %s WHERE id = %s",
            (user.name, user.email, user_id)
        )
        conn.commit()
        return {"message": "User updated"}
    finally:
        cursor.close()
        conn.close()


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        return {"message": "User deleted"}
    finally:
        cursor.close()
        conn.close()
