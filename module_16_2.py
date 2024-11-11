from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

# @app.get("/")
# # async def welcome() -> dict:
# async def welcome():
#     # return {'message': "Главная страница"}
#     return "Главная страница"

@app.get("/user/admin")
# async def news(first_name: str, last_name: str) -> dict:
# можно и без аннотации ->dict.
async def admin():
# async def admin() -> dict:
    return 'Вы вошли как администратор'
    # return {"message": 'Вы вошли как администратор'}

@app.get('/user/{user_id}')
# @app.get('/user/{user_id}')
async def user_id(
    user_id: Annotated[int, Path(
        gt=0,
        le=100,
        description="Enter User ID",
        examples={"example_user_id": {"summary": "Пример ID пользователя", "value": 97}}
    )]
):
    return f"Вы вошли как пользователь № {user_id}"

# @app.get('/user')
@app.get('/user/{username}/{age}')
async def user_FIO(
    username: Annotated[str, Path(
        min_length=5,
        max_length=20,
        description="Enter username",
        examples={"example_username": {"summary": "Пример имени", "value": "UrbanUser"}}
    )],
    age: Annotated[int, Path(
        ge=18,
        le=120,
        description="Enter age",
        examples={"example_age": {"summary": "Пример возраста", "value": 30}}
    )]
):
    return f"Информация о пользователе. Имя: {username}. Возраст: {age}"

