from utils.database.general import DefineGeneralDb, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from typing import Annotated

STR_255 = Annotated[str, mapped_column(String(255))]


class NameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()  # type: ignore


class User(Base, NameMixin):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[STR_255]
    phone: Mapped[STR_255]
    address: Mapped[STR_255]
    city: Mapped[STR_255]
    state: Mapped[STR_255]
    zip_code: Mapped[int] = mapped_column(Integer, nullable=False)
    country: Mapped[STR_255]
