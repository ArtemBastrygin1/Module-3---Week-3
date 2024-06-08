from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    wallet: float
    birthdate: date


class UserUpdate(BaseModel):
    username: Optional[str] = None
    wallet: Optional[float] = None
    birthdate: Optional[date] = None


db_users = [
    User(id=1, username="user1", wallet=100.0, birthdate=date(1990, 1, 1)),
    User(id=2, username="user2", wallet=200.0, birthdate=date(1995, 5, 15))
]


# Корневой маршрут
@app.get("/")
async def read_root():
    return {
        "message": "This is my app"
    }


# Получение списка всех пользователей

@app.get("/users/", response_model=List[User])
async def read_users():
    return db_users


# Получение пользователя по его ID
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    return user


# Создание нового пользователя
@app.post("/users/", response_model=User)
async def create_user(user: User):
    if any(u.id == user.id for u in db_users):
        raise HTTPException(
            status_code=400,
            detail="User ID already exists"
        )
    db_users.append(user)
    return user


# Обновление данных пользователя
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.wallet is not None:
        user.wallet = user_update.wallet
    if user_update.birthdate is not None:
        user.birthdate = user_update.birthdate
    return user


# Удаление пользователя по его ID
@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    db_users.remove(user)
    return user
