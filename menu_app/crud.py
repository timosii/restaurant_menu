from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from pydantic import UUID4
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound

from . import models, schemas

# Получение списка всех меню
def get_all_menus(db: Session):
    return db.query(models.Menu).all()

# Получение меню по id
def get_menu(db: Session, menu_id: str):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

# Получение меню по title
def get_menu_by_title(db: Session, title: str):
    return db.query(models.Menu).filter(models.Menu.title == title).first()

# Создание меню
def create_menu(db: Session, menu: schemas.MenuBase):
    db_menu = models.Menu(id=uuid4(), title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

# Удаление меню
def delete_menu(db: Session, menu_id: str):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    db.commit()
    return 

# Обновление меню
def update_menu(db: Session, menu: schemas.MenuUpdate, menu_id: str):
    updated_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    updated_menu.title = menu.title
    updated_menu.description = menu.description
    db.add(updated_menu)
    db.commit()
    return updated_menu

# Получение всех подменю
def get_all_submenus(db: Session, menu_id: UUID4):
    submenus = db.query(models.Submenu).filter(models.Submenu.parent_menu_id == menu_id).all()
    return submenus

# Получение подменю по id
def get_submenu(db: Session, submenu_id: str):
    current_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    return current_submenu

# Создание подменю
def create_submenu(db: Session, submenu: schemas.SubmenuCreate, menu_id: str):
    current_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if current_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    db_submenu = models.Submenu(id=uuid4(), title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu

# Удаление подменю
def delete_submenu(db: Session, menu_id: str, submenu_id: str):
    current_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if current_menu is None:
        raise HTTPException(status_code=404, detail='Menu not found')

    try:
        submenu_to_delete = db.query(models.Submenu).filter(
            models.Submenu.id == submenu_id).first()

        db.delete(submenu_to_delete)
        db.commit()
        return submenu_to_delete
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Submenu not found')

# Обновление подменю
def update_submenu(db: Session, submenu: schemas.SubmenuUpdate, menu_id: str, submenu_id: str):
    if not submenu.dict():
        raise HTTPException(
            status_code=400,
            detail='No data provided for update'
            )
    current_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if current_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    submenu_to_update = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id).first()
    if submenu_to_update is None:
        raise HTTPException(status_code=404, detail='submenu not found')

    for key, value in submenu.dict().items():
        setattr(submenu_to_update, key, value)

    try:
        db.commit()
        db.refresh(submenu_to_update)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail='Failed to update submenu. Error: ' + str(e)
            )
    return submenu_to_update

# Получение списка блюд
def get_dishes(db: Session, submenu_id: UUID):
    current_dishes = db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()
    dishes_list = [schemas.DishOut.from_orm(dish) for dish in current_dishes]
    return dishes_list

# Получение блюда по id
def get_dish(dish_id: str, db: Session):
    current_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if current_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return current_dish

# Создание блюда
def create_dish(
    menu_id: str,
    submenu_id: str,
    dish: schemas.DishCreate,
    db: Session
    ):
    current_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if current_menu is None:
        raise HTTPException(status_code=404, detail='Menu not found')

    current_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == models.submenu_id).first()
    if current_submenu is None:
        raise HTTPException(status_code=404, detail='Submenu not found')

    db_dish = models.Dish(
        id=uuid4(),
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id)

    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish

# Обновление блюда
def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish_update: schemas.DishUpdate,
    db: Session
    ):
    if not dish_update.dict():
        raise HTTPException(
            status_code=400,
            detail='No data provided for update'
            )

    current_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if current_menu is None:
        raise HTTPException(status_code=404, detail='Menu not found')

    current_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.parent_menu_id == menu_id).first()
    if current_submenu is None:
        raise HTTPException(status_code=404, detail='Submenu not found')

    dish_to_update = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.parent_submenu_id == submenu_id).first()

    for key, value in dish_update.dict().items():
        setattr(dish_to_update, key, value)

    try:
        db.commit()
        db.refresh(dish_to_update)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail='Failed to update dish. Error: ' + str(e)
            )
    return dish_to_update

# Удаление блюда
def delete_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    db: Session
    ):
    current_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if current_menu is None:
        raise HTTPException(status_code=404, detail='Menu not found')

    current_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.parent_menu_id == menu_id).first()
    if current_submenu is None:
        raise HTTPException(status_code=404, detail='Submenu not found')

    try:
        dish_to_delete = db.query(models.Dish).filter(
            models.Dish.id == dish_id,
            models.Dish.parent_submenu_id == submenu_id).one()
        db.delete(dish_to_delete)
        db.commit()
        return dish_to_delete
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Dish not found')
