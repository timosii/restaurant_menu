from pydantic import BaseModel, UUID4


class MenuIn(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class MenuOut(BaseModel):    
    id: UUID4
    title: str
    description: str
    # submenus_count: int
    # dishes_count: int

    class Config:
        from_attributes = True


class SubmenuIn(BaseModel):
    title: str
    description: str
    
    class Config:
        from_attributes = True


class SubmenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    # dishes_count: int
    
    class Config:
        from_attributes = True


class DishIn(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        from_attributes = True

class DishOut(BaseModel):
    id: UUID4
    title: str
    description: str
    price: str

    class Config:
        from_attributes = True

class DeleteMSG(BaseModel):
    status: bool
    message: str