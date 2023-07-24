# используется для Pydantic моделей
from pydantic import BaseModel
from typing import Union

class Menu(BaseModel):
    id: Union[int, str] | None = None
    title: str
    description: str | None = None

    class Config:
        orm_mode = True




