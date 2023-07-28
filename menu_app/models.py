from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)

    submenus = relationship("Submenu", 
                            back_populates='menu',
                            cascade="all, delete")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    parent_menu_id = Column(UUID, ForeignKey("menus.id"))
    dishes_count = Column(Integer, default=0)

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", 
                          back_populates="submenu",
                          cascade="all, delete")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(Numeric(scale=2))
    parent_submenu_id = Column(UUID, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", 
                           back_populates="dishes")
