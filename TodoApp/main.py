import database
import models
from fastapi import FastAPI
from routers import admin, auth, todo, user

app = FastAPI()


models.Base.metadata.create_all(bind=database.engine)


@app.get("/heath")
def health_check():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(user.router)
