from .. import models, schemas
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from menu_app.errors import not_found, message_deleted


SAMPLE='submenu'

# Получение всех подменю
def get_submenus(db: Session, 
                     menu_id: UUID):
    submenus = db.query(models.Submenu).filter(models.Submenu.parent_menu_id == menu_id).all()
    return submenus

# Получение подменю по id
def get_submenu(db: Session, submenu_id: UUID):
    current_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if current_submenu is None:
        not_found(SAMPLE)
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
def delete_submenu(menu_id: UUID, 
                   submenu_id: UUID,
                   db: Session):
    submenu_for_delete = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if submenu_for_delete is None:
        not_found(SAMPLE)
    db.delete(submenu_for_delete)
    db.commit()
    return message_deleted(SAMPLE)

# Обновление подменю
def update_submenu(menu_id: UUID, 
                   submenu_id: UUID,
                   submenu: schemas.SubmenuIn,
                   db: Session):
    db_submenu = get_submenu(db, submenu_id=submenu_id)
    if db_submenu is None:
        not_found(SAMPLE)
    submenu_to_update = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.parent_menu_id == menu_id).first()
    submenu_to_update.title = submenu.title
    submenu_to_update.description = submenu.description
    db.add(submenu_to_update)
    db.commit()
    return submenu_to_update

# Подсчёт количества блюд для подменю
def dish_count(db: Session, submenu_id: UUID):
    current_submenu = db.query(models.Dish).filter(models.Dish.parent_submenu_id == submenu_id).all()
    return len(current_submenu)