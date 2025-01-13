# Приложение Flask с SQLAlchemy
import datetime as dt
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from database import db, Employee, Department

app = Flask(__name__)
# лучше делать через переменную окружения
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'

# db = SQLAlchemy(app)
db.init_app(app)

# Создадим базу данных прямо здесь
with app.app_context():
    db.drop_all()
    # без этой команды БД не запустится
    db.create_all()
    # Добавим тестовые данные
    dev = Department(name="Разработка")
    hr = Department(name="Рекрутинг")
    db.session.add(dev)
    db.session.add(hr)
    db.session.add(Employee(fullname="Мария Петрова", department=dev))
    db.session.add(Employee(fullname="Сергей Гришин", department=dev))
    db.session.add(Employee(fullname="Петя Иванов", department=hr))

    db.session.commit()


@app.route("/")
def all_employees():
    # получаем всё через метод query
    employees = Employee.query.all()
    return render_template("all_employees.html", employees=employees)


@app.route("/department/<int:department_id>")
def employees_by_department(department_id):
    department = Department.query.get_or_404(department_id)
    return render_template(
        "employees_by_department.html",
        department_name=department.name,
        employees=department.employees
    )


if __name__ == "__main__":
    app.run()
