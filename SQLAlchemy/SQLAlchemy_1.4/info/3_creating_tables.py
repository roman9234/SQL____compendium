# SQLAlchemy <= 1.4
# актуальная версия SQLAlchemy_1.4 > 2.0
# но Flusk использует 1.4
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

# 0 - Генерация схемы БД
from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True)


# 1 - объявляем базовый класс. Он один на всё приложение и в нём аккумулируются все таблицы
Base = declarative_base()


# 2 - от этого класса мы наследуем нашу модель


# SQLAlchemy_1.4 1.4
class User(Base):
    # 1 свойство - название таблицы. Модель называется User, таблица user_account
    __tablename__ = "user_account"
    # далее объвляем колонки формат:
    # название = Column(тип колонки, дополнительные модификаторы)

    # первичный ключ
    id = Column(Integer, primary_key=True)
    # обязательная колонка не длиннее 30 символов
    name = Column(String(30), nullable=False)
    # не обязательная к заполнению колонка
    fullname = Column(String, nullable=True)

    # Объявление связей между таблицами делается с помощью функции relationship
    # туда мы пишем объект, с которым связываем таблицу, и дополнительные модификаторы
    # здесь используется ON DELETE CASCADE
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    # если мы хотим отобразить в консоли экземпляр этого объекта User,
    # можем объявить это в функции repr
    def __repr__(self):
        return f"User(fullname={self.fullname!r}"


# Вторая таблица
class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account._id"), nullable=False)
    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:

        return f"Address(email_address={self.email_address!r})"


# вывод в консоль сгенерированных команд SQL
Base.metadata.create_all(engine)




