from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

# Список пользователей
users = []

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/users", response_model=List[User])
async def get_all_users() -> List[User]:
    #Получаем список всех пользователей
    return users

@app.post('/user/{username}/{age}', response_model=User)
async def user_add(
    username: Annotated[
        str, Path(min_length=3, max_length=20, description="Имя пользователя должно быть от 3 до 20 символов")
    ],
    age: Annotated[
        int, Path(ge=18, le=100, description="Возраст должен быть между 18 и 100")
    ],
) -> User:
    # Добавляем нового пользователя в список
    user_id = users[-1].id + 1 if users else 1  # ID = последний ID + 1 или 1, если список пуст
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def user_upd(
    user_id: Annotated[int, Path(gt=0, description="ID пользователя должен быть положительным")],
    username: Annotated[
        str, Path(min_length=3, max_length=20, description="Имя пользователя должно быть от 3 до 20 символов")
    ],
    age: Annotated[
        int, Path(ge=18, le=120, description="Возраст должен быть между 18 и 120")
    ],
) -> User:
    # Обновляем информацию о пользователе
    for user in users: #используем цикл, т.к. у нас не словарь, а список (нет возможности прямой адресации по ID)
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    # Если пользователь не найден
    raise HTTPException(status_code=404, detail="Пользователь не найден")
    # интересно, что для FastApi конструкция try/except не нужна, т.к. FastAPI обрабатывает исключения самостоятельно, что упрощает код

@app.delete('/user/{user_id}', response_model=User)
async def user_delete(
    user_id: Annotated[int, Path(ge=0, description="ID пользователя должен быть положительным")]
) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    # Если пользователь не найден
    raise HTTPException(status_code=404, detail="Пользователь не найден")
