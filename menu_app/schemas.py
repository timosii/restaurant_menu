# используется для Pydantic моделей
from pydantic import BaseModel
from typing import Union

class Menu(BaseModel):
    menu_id: Union[int, str]
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class Submenu(Menu):
    submenu_id: Union[int, str]


class Dish(Submenu):
    dish_id: Union[int, str]
    
