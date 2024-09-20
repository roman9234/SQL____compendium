# SQLAlchemy_2.0
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional


# 1 - объявляем базовый класс. Он один на всё приложение и в нём аккумулируются все таблицы
class Base(DeclarativeBase):
    pass


# 2 - от этого класса мы наследуем нашу модель
class User(Base):
    # 1 свойство - название таблицы. Модель называется User, таблица user_account
    __tablename__ = "user_account"
    # далее объвляем колонки формат:
    # тип колонок объявляется через нотивный Typing

    # первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True)
    # обязательная колонка не длинее 30 символов
    name: Mapped[str] = mapped_column(String(30))
    # не обязательная к заполнению колонка
    fullname: Mapped[Optional[str]]

    # если мы хотим отобразить в консоли экземпляр этого объекта User,
    # можем объявить это в функции repr
    def __repr__(self) -> str:
        return f"User(fullname={self.fullname!r})"
