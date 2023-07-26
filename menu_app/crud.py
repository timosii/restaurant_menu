from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from pydantic import UUID4
from fastapi import HTTPException

from . import models, schemas

# Получение списка всех меню
def get_all_menus(db: Session):
    return db.query(models.Menu).all()

# Получение меню по id
def get_menu(db: Session, menu_id: UUID):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

# Получение меню по title
def get_menu_by_title(db: Session, title: str):
    return db.query(models.Menu).filter(models.Menu.title == title).first()

# Создание меню
def create_menu(db: Session, menu: schemas.MenuIn):
    db_menu = models.Menu(id=uuid4(), title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

# Удаление меню
def delete_menu(db: Session, menu_id: UUID):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    db.commit()
    return

# Обновление меню
def update_menu(db: Session, menu: schemas.MenuIn, menu_id: UUID):
    updated_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    updated_menu.title = menu.title
    updated_menu.description = menu.description
    db.add(updated_menu)
    db.commit()
    return updated_menu

# Получение всех подменю
def get_all_submenus(db: Session, 
                     menu_id: UUID4):
    submenus = db.query(models.Submenu).filter(models.Submenu.parent_menu_id == menu_id).all()
    return submenus

# Получение подменю по id
def get_submenu(db: Session, submenu_id: UUID):
    current_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    return current_submenu

# Создание подменю
def create_submenu(db: Session, 
                   submenu: schemas.SubmenuIn, 
                   menu_id: UUID):
    db_submenu = models.Submenu(id=uuid4(), 
                                title=submenu.title, 
                                description=submenu.description,
                                parent_menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu

# Удаление подменю
def delete_submenu(db: Session, 
                   menu_id: UUID, 
                   submenu_id: UUID):
    submenu_to_delete = db.query(models.Submenu).filter(
    models.Submenu.id == submenu_id).first()
    db.delete(submenu_to_delete)
    db.commit()
    return 

# Обновление подменю
def update_submenu(db: Session, 
                   submenu: schemas.SubmenuIn, 
                   menu_id: UUID, 
                   submenu_id: UUID):
    submenu_to_update = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.parent_menu_id == menu_id).first()
    submenu_to_update.title = submenu.title
    submenu_to_update.description = submenu.description
    submenu_to_update.price = submenu.price
    db.add(submenu_to_update)
    db.commit()
    return submenu_to_update

# Получение списка блюд
def get_dishes(db: Session, 
               submenu_id: UUID):
    current_dishes = db.query(models.Dish).filter(models.Dish.parent_submenu_id == submenu_id).all()
    return current_dishes

# Получение блюда по id
def get_dish(db: Session, dish_id: UUID):
    current_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    return current_dish

# Создание блюда
def create_dish(menu_id: UUID, 
                submenu_id: UUID, 
                dish: schemas.DishIn, 
                db: Session):

    db_dish = models.Dish(id=uuid4(), 
                          title=dish.title, 
                          description=dish.description, 
                          price=dish.price, 
                          parent_submenu_id=submenu_id)

    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish

# Обновление блюда
def update_dish(menu_id: UUID, 
                submenu_id: UUID, 
                dish_id: UUID, 
                dish: schemas.DishIn, 
                db: Session):


    dish_to_update = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.parent_submenu_id == submenu_id).first()
    dish_to_update.title = dish.title
    dish_to_update.description = dish.description
    dish_to_update.price = dish.price
    db.add(dish_to_update)
    db.commit()
    return dish_to_update

# Удаление блюда
def delete_dish(menu_id: UUID, 
                submenu_id: UUID, 
                dish_id: UUID, 
                db: Session):

    dish_to_delete = db.query(models.Dish).filter(
            models.Dish.id == dish_id,
            models.Dish.parent_submenu_id == submenu_id).one()
    db.delete(dish_to_delete)
    db.commit()
    return
