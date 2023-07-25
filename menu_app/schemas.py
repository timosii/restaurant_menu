# используется для Pydantic моделей
from pydantic import BaseModel
from typing import Union, List


class DishBase(BaseModel):
    title: str
    description: str
    price: str

class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class DishOut(DishBase):
    id: str

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    title: str
    description: str
    
    class Config:
        orm_mode = True


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(SubmenuBase):
    pass


class SubmenuOut(SubmenuBase):
    id: Union[str, int]
    # dishes_count: int

    class Config:
        orm_mode = True


class MenuBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuOut(MenuBase):
    id: Union[str, int]
    # submenus_count: int
    # dishes_count: int

    class Config:
        orm_mode = True

