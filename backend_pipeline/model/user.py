from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declared_attr
from schemas.user_schema import Roles
from typing import Annotated
from utils.database.general import DefineGeneralDb, Base

STR_255 = Annotated[str, mapped_column(String(255), nullable=True)]


class NameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()  # type: ignore


class User(Base, NameMixin):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    last_name: Mapped[STR_255]
    phone: Mapped[STR_255]
    address: Mapped[STR_255]
    city: Mapped[STR_255]
    state: Mapped[STR_255]
    zip_code: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    country: Mapped[STR_255]
    password: Mapped[STR_255]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[Roles]
