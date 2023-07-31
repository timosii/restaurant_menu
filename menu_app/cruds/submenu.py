from .. import models, schemas
from ..errors import not_found, message_deleted
from uuid import UUID, uuid4
from sqlalchemy.orm import Session


SAMPLE = 'submenu'


def get_submenus(db: Session,
                 menu_id: UUID):
    submenus = db.query(models.Submenu).filter(
        models.Submenu.parent_menu_id == menu_id).all()
    return submenus


def get_submenu(db: Session, submenu_id: UUID):
    current_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id).first()
    if current_submenu is None:
        not_found(SAMPLE)
    return current_submenu


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


def delete_submenu(menu_id: UUID,
                   submenu_id: UUID,
                   db: Session):
    submenu_for_delete = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id).first()
    if submenu_for_delete is None:
        not_found(SAMPLE)
    db.delete(submenu_for_delete)
    db.commit()
    return message_deleted(SAMPLE)


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


def dish_count(db: Session, submenu_id: UUID):
    current_submenu = db.query(models.Dish).filter(
        models.Dish.parent_submenu_id == submenu_id).all()
    return len(current_submenu)
