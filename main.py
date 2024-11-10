from fastapi import FastAPI

app = FastAPI()

@app.get("/")
# async def welcome() -> dict:
async def welcome():
    # return {'message': "Главная страница"}
    return "Главная страница"

@app.get("/user/admin")
# async def news(first_name: str, last_name: str) -> dict:
# можно и без аннотации ->dict.
async def admin():
# async def admin() -> dict:
    return 'Вы вошли как администратор'
    # return {"message": 'Вы вошли как администратор'}

@app.get('/user/{user_id}')
async def user_id(user_id: int):
    return f'Вы вошли как пользователь № {user_id}'

@app.get('/user/')
async def user_id(user_name: str, age: int):
    return f'Информация о пользователе. Имя: {user_name}. Возраст {age}'