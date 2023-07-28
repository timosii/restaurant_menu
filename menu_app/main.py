from fastapi import FastAPI
from .endpoints import menu_point, submenu_point, dish_point

app = FastAPI()

app.include_router(menu_point.router)
app.include_router(submenu_point.router)
app.include_router(dish_point.router)