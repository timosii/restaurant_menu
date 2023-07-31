from pydantic import BaseModel, UUID4
from cruds.menu import submenu_dish_count
from cruds.submenu import dish_count


class MenuIn(BaseModel):
    title: str
    description: str


class MenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int = 
    dishes_count: int


class SubmenuIn(BaseModel):
    title: str
    description: str


class SubmenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    dishes_count: int


class DishIn(BaseModel):
    title: str
    description: str
    price: str


class DishOut(BaseModel):
    id: UUID4
    title: str
    description: str
    price: str


class DeleteMSG(BaseModel):
    status: bool
    message: str
