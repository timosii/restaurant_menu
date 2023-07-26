from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    # submenus_count = Column(Integer, default=0)
    # dishes_count = Column(Integer, default=0)

    submenus = relationship("Submenu", 
                            back_populates='menu', 
                            passive_deletes=True)


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    parent_menu_id = Column(UUID, 
                            ForeignKey("menus.id", 
                                       ondelete="CASCADE"), 
                            nullable=False)
    # dishes_count = Column(Integer, default=0)

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", 
                          back_populates="submenu", 
                          passive_deletes=True)


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(Numeric(precision=10, scale=2))
    parent_submenu_id = Column(UUID, ForeignKey("submenus.id", 
                                                ondelete="CASCADE"), 
                               nullable=False)

    submenu = relationship("Submenu", 
                           back_populates="dishes")
