# Делаем более сложные запросы

from model.db_models import db
from model.db_models import Address, User

# SQL JOIN в SQLAlchemy
query = (
    db.select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
)
# SELECT address.id, address.email_address, address.user_id
# FROM address JOIN user_account ON user_account.id =
# address.user_id
# WHERE user_account.name = ?
# [...] ('sandy')

# Объединяем больше таблиц

db.select(User).join(User.orders).join(Order.items)

# SELECT user_account.id, user_account.name, user_account.fullname
# FROM user_account
# JOIN user_order ON user_account.id = user_order.user_id
# JOIN order_items AS order_items_1 ON user_order.id =
# order_items_1.order_id
# JOIN item ON item.id = order_items_1.item_id


# Агрегация и сортировка

from sqlalchemy import func, desc

query = (
    db.select(Address.user_id, func.count(Address.id).label("addresses_count"))
    .group_by("user_id")
    .order_by("user_id", desc("addresses_count"))
)
# SELECT address.user_id, count(address.id) AS addresses_count
# FROM address GROUP BY address.user_id ORDER BY address.user_id, addresses_count
# DESC
