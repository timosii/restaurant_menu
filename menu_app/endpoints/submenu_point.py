from .. import schemas, models
from menu_app.cruds.submenu import get_submenu, get_submenus, create_submenu, update_submenu, delete_submenu, dish_count
from menu_app.database import SessionLocal, engine
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends, status, FastAPI, APIRouter


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получить список всех подменю
@router.get("/", response_model=list[schemas.SubmenuOut])
def reading_submenus(menu_id: UUID,
                   db: Session = Depends(get_db)):
    submenus = get_submenus(db, menu_id)
    for submenu in submenus:
        submenu.dishes_count = dish_count(db=db, 
                                               submenu_id=submenu.id)
    return submenus

# Получить подменю по id
@router.get("/{submenu_id}", 
         response_model=schemas.SubmenuOut)
def reading_submenu(submenu_id: UUID,
                 db: Session = Depends(get_db)):
    db_submenu = get_submenu(db, submenu_id=submenu_id)
    db_submenu.dishes_count = dish_count(db=db, 
                                               submenu_id=db_submenu.id)
    return db_submenu

# Создать подменю
@router.post("/", response_model=schemas.SubmenuOut, 
             status_code=status.HTTP_201_CREATED)
def creating_submenu(menu_id: UUID,
                   submenu: schemas.SubmenuIn,
                   db: Session = Depends(get_db)
                   ):
    db_submenu = create_submenu(db, submenu=submenu, menu_id=menu_id)
    return db_submenu

# Обновить подменю
@router.patch("/{submenu_id}", 
           response_model=schemas.SubmenuOut)
def updating_submenu(menu_id: UUID, 
                   submenu_id: UUID, 
                   submenu_update: schemas.SubmenuIn, 
                   db: Session = Depends(get_db)):
    updated_submenu = update_submenu(menu_id, 
                                          submenu_id, 
                                          submenu_update, 
                                          db)
    updated_submenu.dishes_count = dish_count(db=db, 
                                               submenu_id=updated_submenu.id)
    return updated_submenu

# Удалить подменю
@router.delete("/{submenu_id}", 
            response_model=schemas.DeleteMSG)
def deleting_submenu(menu_id: UUID, 
                   submenu_id: UUID, 
                   db: Session = Depends(get_db)):
    return delete_submenu(menu_id=menu_id, 
                        submenu_id=submenu_id, 
                        db=db)
    