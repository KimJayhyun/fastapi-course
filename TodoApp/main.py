from fastapi import FastAPI

from . import database, models

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
