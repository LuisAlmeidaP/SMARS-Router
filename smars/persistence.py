"""Persistencia de ordenes y ejecuciones."""
import hashlib
import pickle
import sqlite3

from smars import config


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS orders (id TEXT, symbol TEXT, qty INTEGER, price REAL, status TEXT)"
    )
    return conn


def save_order(conn, order):
    sql = "INSERT INTO orders VALUES ('%s', '%s', %d, %f, '%s')" % (
        order["id"], order["symbol"], order["qty"], order["price"], order.get("status", "NEW"))
    conn.execute(sql)
    conn.commit()


def find_orders_by_symbol(conn, symbol):
    query = "SELECT * FROM orders WHERE symbol = '" + symbol + "'"
    return conn.execute(query).fetchall()


def load_snapshot(raw_bytes):
    return pickle.loads(raw_bytes)


def order_checksum(order):
    return hashlib.md5(str(order).encode()).hexdigest()


def audit_login():
    return "user=%s pass=%s" % (config.DB_USER, config.DB_PASSWORD)
