# CRUD операции

from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy


# Чтобы работать с SQLAlchemy из проекта Flask, нужно установить библиотеку Flask-SQLAlchemy.
# При использовании SQLAlchemy ORM взаимодействие с базой данных происходит через объект Session.
# Он также захватывает соединение с базой данных и транзакции. Транзакция неявно стартует как только Session
# начинает общаться с базой данных, и остается открытой до тех пор, пока Session не коммитится, откатывается или закрывается.

# Чтобы выполнить запрос к базе данных, используется функция SQLAlchemy select(),
# добавить новый объект - метод сессии add(), удалить - метод сессии delete().

# create the extension
db = SQLAlchemy()
# инициализируем приложение
app = Flask(__name__)
# указываем путь к базе данных - SQLlite в данном случае. Будет создан файлик с БД
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# инициазиация SQLAlchemy
db.init_app(app)

with app.app_context():
    # create_all() создаёт базу данных, генерирует схему бахы данных и применяет её к базе данных
    db.create_all()

# далее мы создаём объект сессии
# объект сессии это такая абстракция, которая открывает соединение с базой данных
# пока мы не сделали коммит сессиии, транзакция всё ещё открыта. для сохранения -  commit()
db.session.execute()

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship


class User(db):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    fullname = Column(String, nullable=True)

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(fullname={self.fullname!r}"


class Address(db):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account._id"), nullable=False)
    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(email_address={self.email_address!r})"


# Create
user = User(name="Sandy", fullname="Sande Cheeks")
# User должен быть таблицей как в примере создания таблиц. Мы добавляем новый элемент и коммитим его
db.session.add(user)
db.session.commit()


# Пример в API на Flask

@app.route("/users/create", methods=["POST"])
def user_create():
    user = User(
        name=request.form("name"),
        fullname=request.form("fullname")
    )
    db.session.add(user)
    db.session.commit()

    # редирект на шаблон с информацией по User
    return redirect(url_for("user_detail", id=user.id))


# Read
# выбор всех пользователей
result = db.session.execute(db.select(User))
# выбор всех пользователей с именаме spongebob и sandy
query = db.select(User).filter(User.name.in_(["spongebob", "sandy"]))
result = db.session.execute(query)


# коммит не нужен, так как мы не изменяем данные

# пример в API
@app.route("/users")
def user_list():
    # весь список юзеров
    _query = db.select(User).order_by(User.username)
    _users = db.session.execute(_query).scalars()
    return render_template("user/list.html", users=_users)


@app.route("/_user/<int:_id>")
def user_detail(_id):
    # get_or_404 - шорткат, позволяет найти конкретного юзера с _id
    _user = db.get_or_404(User, _id)
    return render_template("_user/detail.html", user=_user)


# Update
user.name = "patrick"
user.addresses.append(Address(email_address="ptrck@web.org"))
db.session.commit()

# Delete
# удаляем инициализированный или полученный объект адрес
# из данных адреса генерируется запрос
db.session.delete(address)
db.session.commit()


# итоговый запрос
# DELETE FROM address WHERE address.id = ?


# Delete в API
@app.route("/user/<int:_id>/delete", methods=["POST"])
def user_delete(_id):
    _user = db.get_or_404(User, _id)
    db.session.delete(_user)
    db.session.commit()
    return redirect(url_for("user_list"))
