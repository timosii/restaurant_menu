from uuid import UUID
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from menu_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получить список всех меню
@app.get("/api/v1/menus", response_model=list[schemas.MenuOut])
def read_menus(db: Session = Depends(get_db)):
    menus = crud.get_all_menus(db)
    return menus

# Создать меню
@app.post("/api/v1/menus", 
          response_model=schemas.MenuOut, 
          status_code=status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuIn, 
                db: Session = Depends(get_db)):
    check_menu = crud.get_menu_by_title(db, title=menu.title)
    if check_menu:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="menu already exist")
    db_output = crud.create_menu(db=db, menu=menu)
    return db_output

# Получить меню по id
@app.get("/api/v1/menus/{menu_id}",
          response_model=schemas.MenuOut)
def read_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return db_menu

# Удалить меню
@app.delete("/api/v1/menus/{menu_id}", 
            response_model=schemas.DeleteMSG)
def delete_menu(menu_id: UUID, 
                db: Session = Depends(get_db)):
    crud.delete_menu(db=db, menu_id=menu_id)
    return JSONResponse(status_code=200, 
                        content={"status": True, 
                                 "message": "The menu has been deleted"})

# Обновить меню
@app.patch("/api/v1/menus/{menu_id}",
            response_model=schemas.MenuOut)
def update_menu(menu: schemas.MenuIn,
                menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            etail="menu not found")
    updated_menu = crud.update_menu(db=db, menu=menu, menu_id=menu_id)
    return updated_menu

# Получить список всех подменю
@app.get("/api/v1/menus/{menu_id}/submenus",
         response_model=list[schemas.SubmenuOut])
def read_submenus(menu_id: UUID,
                   db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="menu not found")

    submenus = crud.get_all_submenus(db, menu_id)
    return submenus

# Получить подменю по id
@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def read_submenu(submenu_id: UUID,
                 db: Session = Depends(get_db)
                 ):
    db_submenu = crud.get_submenu(db, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    
    return db_submenu

# Создать подменю
@app.post("/api/v1/menus/{menu_id}/submenus",
          response_model=schemas.SubmenuOut, status_code=201)
def create_submenu(menu_id: UUID,
                   submenu: schemas.SubmenuIn,
                   db: Session = Depends(get_db)
                   ):
    db_submenu = crud.create_submenu(db, submenu=submenu, menu_id=menu_id)
    return db_submenu

# Обновить подменю
@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", 
           response_model=schemas.SubmenuOut)
def update_submenu(menu_id: UUID, 
                   submenu_id: UUID, 
                   submenu_update: schemas.SubmenuIn, 
                   db: Session = Depends(get_db)
                   ):
    updated_submenu = crud.update_submenu(menu_id, 
                                          submenu_id, 
                                          submenu_update, 
                                          db)
    return updated_submenu

# Удалить подменю
@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}", 
            response_model=schemas.DeleteMSG)
def delete_submenu(menu_id: UUID, 
                   submenu_id: UUID, 
                   db: Session = Depends(get_db)):
    crud.delete_submenu(menu_id, submenu_id, db)
    return JSONResponse(status_code=200, 
                        content={"status": True, 
                                 "message": "The submenu has been deleted"})

# Просмотр списка блюд
@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[schemas.DishOut],
    status_code=status.HTTP_200_OK,
    responses={
        404: {'description': 'меню не найдено'},
    },
)
def get_dishes(submenu_id: UUID, 
               db: Session = Depends(get_db)
               ):
    dishes_list = crud.get_all_dishes(submenu_id, db)
    return dishes_list

# Посмотреть определённое блюдо
@app.get('/api/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', 
         response_model=schemas.DishOut)
def receive_current_dish(dish_id: UUID, 
                         db: Session = Depends(get_db)
                         ):
    current_dish = crud.get_dish(dish_id, db)
    return current_dish

# Создать блюдо
@app.post('api/menus/{menu_id}/submenus/{submenu_id}/dishes', 
          response_model=schemas.DishOut,
          status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: UUID, 
                submenu_id: UUID, 
                dish: schemas.DishIn, 
                db: Session = Depends(get_db)):
    current_dish = crud.create_dish(menu_id, submenu_id, dish, db)
    return current_dish

# Обновить блюдо
@app.patch('api/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', 
           response_model=schemas.DishOut)
def update_current_menu(menu_id: UUID, 
                        submenu_id: UUID, 
                        dish_id: UUID, 
                        dish_update: schemas.DishIn, 
                        db: Session = Depends(get_db)):
    dish_to_update = crud.update_dish(menu_id, 
                                      submenu_id, 
                                      dish_id, 
                                      dish_update, 
                                      db)
    return dish_to_update

# Удалить блюдо
@app.delete('api/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', 
            response_model=schemas.DeleteMSG)
def delete_dish(menu_id: UUID, 
                submenu_id: UUID, 
                dish_id: UUID, 
                db: Session = Depends(get_db)):
    crud.delete_dish(menu_id, submenu_id, dish_id, db)
    return JSONResponse(status_code=200, 
                        content={"status": True, 
                                 "message": "The dish has been deleted"})
