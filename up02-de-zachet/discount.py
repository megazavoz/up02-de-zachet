from datetime import datetime, timedelta
import sqlite3

from config import DB_PATH


def get_previous_month_range(date):
    """Возвращает (первое число, последнее число) предыдущего месяца."""
    first_of_current = date.replace(day=1)
    last_of_previous = first_of_current - timedelta(days=1)
    first_of_previous = last_of_previous.replace(day=1)
    return (
        first_of_previous.strftime("%Y-%m-%d"),
        last_of_previous.strftime("%Y-%m-%d"),
    )


def has_orders_in_previous_month(product_id, date):
    """True, если у товара были заказы в прошлом месяце."""
    start_date, end_date = get_previous_month_range(date)
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Состав_заказа
            JOIN Заказ ON Состав_заказа.заказ_id = Заказ.id
            WHERE Состав_заказа.товар_id = ?
              AND Заказ.дата BETWEEN ? AND ?
            """,
            (product_id, start_date, end_date),
        )
        result = cursor.fetchone()
        return bool(result and result[0] > 0)
    finally:
        connection.close()


def calculate_price_with_discount(product_id, price, date):
    """Возвращает цену со скидкой 25% (или базовую, если были заказы)."""
    if has_orders_in_previous_month(product_id, date):
        return price
    return round(price * 0.75, 2)