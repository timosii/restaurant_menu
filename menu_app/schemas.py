from pydantic import UUID4, BaseModel


class BaseItemIn(BaseModel):
    id: UUID4 | None = None
    title: str
    description: str


class MenuIn(BaseItemIn):
    pass


class SubmenuIn(BaseItemIn):
    pass


class DishIn(BaseItemIn):
    price: str


class BaseItemOut(BaseModel):
    id: UUID4
    title: str
    description: str


class MenuOut(BaseItemOut):
    submenus_count: int
    dishes_count: int


class SubmenuOut(BaseItemOut):
    dishes_count: int


class DishOut(BaseItemOut):
    price: str


class DeleteMSG(BaseModel):
    status: bool
    message: str


class SubmenuAllOut(BaseItemOut):
    dishes: list[DishOut]


class MenuAllOut(BaseItemOut):
    submenus: list[SubmenuAllOut]
