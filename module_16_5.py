from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Список пользователей
users = []


# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# users = [ #тренировочный список
#     User(id=1, username="UrbanUser", age=24),
#     User(id=2, username="UrbanTest", age=22),
#     User(id=3, username="Capybara", age=60)
# ]
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Главная страница.
    """
    # return templates.TemplateResponse("main.html", {"request": request})
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            # Если пользователь найден, передаем его в шаблон
            return templates.TemplateResponse(
                "users.html",
                {"request": request, "user": user}
            )
        # Если пользователь не найден, выбрасываем исключение
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.post('/user/{username}/{age}', response_class=HTMLResponse)
async def user_add(
    request: Request,
    username: Annotated[
        str, Path(min_length=3, max_length=20, description="Имя пользователя должно быть от 3 до 20 символов")
    ],
    age: Annotated[
        int, Path(ge=18, le=100, description="Возраст должен быть между 18 и 100")
    ],
):
    """
    Добавление нового пользователя.
    """

    user_id = users[-1].id + 1 if users else 1  # ID = последний ID + 1 или 1, если список пуст
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users,
        "message": f"Пользователь {username} добавлен."
    })
    # return templates.TemplateResponse("users.html", {"request": request, "users": users})

### не добработанная часть (в ДЗ не требовалась)
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