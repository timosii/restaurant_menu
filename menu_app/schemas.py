# используется для Pydantic моделей
from pydantic import BaseModel, UUID4
from typing import Union, List, Optional


class MenuBase(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuOut(MenuBase):
    id: UUID4
    # submenus_count: int
    # dishes_count: int

    class Config:
        from_attributes = True


class SubmenuBase(BaseModel):
    title: str
    description: str
    
    class Config:
        from_attributes = True


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(SubmenuBase):
    pass


class SubmenuOut(SubmenuBase):
    id: Optional[UUID4] = None
    # dishes_count: int

    class Config:
        from_attributes = True


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class DishOut(DishBase):
    id: UUID4

    class Config:
        from_attributes = True
