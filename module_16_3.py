from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

# Начальное состояние базы данных
users_db = {1: "Имя: Example, возраст: 18"}

@app.get("/users")
async def get_all_users() -> dict:
    return users_db

@app.get("/user/{user_id}")
async def get_user(user_id: Annotated[int, Path(ge=0, description="ID пользователя должен быть положительным")]):
    if user_id not in users_db:
        return {"error": "Пользователь не найден"}
    return {user_id: users_db[user_id]}

@app.post('/user/{username}/{age}')
async def user_add(
    username: Annotated[str, Path(min_length=3, max_length=20, description="Имя пользователя должно быть от 3 до 20 символов")],
    age: Annotated[int, Path(ge=18, le=100, description="Возраст должен быть между 18 и 100")]
) -> str:
    # Генерация нового ID
    user_id = max(users_db.keys()) + 1 if users_db else 0
    # user_id = max(map(int, users_db.keys())) + 1 if users_db else 0
    users_db[user_id] = f'Имя: {username}, возраст: {age}'
    return f"Пользователь {username} с id {user_id} зарегистрирован"

@app.put('/user/{user_id}/{username}/{age}')
async def user_upd(
    user_id: Annotated[int, Path(gt=0, description="ID пользователя должен быть положительным")],
    username: Annotated[str, Path(min_length=3, max_length=20, description="Имя пользователя должно быть от 3 до 20 символов")],
    age: Annotated[int, Path(ge=18, le=120, description="Возраст должен быть между 18 и 120")]
) -> str:
    if user_id not in users_db:
        return {"error": "Пользователь не найден"}
    users_db[user_id] = f'Имя: {username}, возраст: {age}'
    return f'Пользователь {user_id} обновлен'

@app.delete('/user/{user_id}')
async def user_delete(user_id: Annotated[int, Path(ge=0, description="ID пользователя должен быть положительным")]) -> str:
    if user_id not in users_db:
        return {"error": "Пользователь не найден"}
    users_db.pop(user_id)
    return f'Пользователь {user_id} удален за нарушение правил форума'
