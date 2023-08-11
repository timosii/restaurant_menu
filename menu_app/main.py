from fastapi import FastAPI

from menu_app.endpoints import dish, menu, submenu

app = FastAPI()

app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dish.router)
