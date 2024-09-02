from pydantic import BaseModel


class CreateGameSchema(BaseModel):
    title: str
