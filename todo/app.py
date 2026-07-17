from fastapi import FastAPI

from todo.routers import auth, nutri, todos, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)

app.include_router(nutri.router)


@app.get('/')
def read_root():
    return {'message': 'Olá mundo!'}
