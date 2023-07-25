
from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from .database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    description = Column(String)

    submenus = relationship("Submenu", back_populates='menu', cascade="all, delete")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    description = Column(String)
    parent_menu_id = Column(Integer, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(Numeric(precision=10, scale=2))
    parent_submenu_id = Column(Integer, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")


