import sqlite3
from datetime import datetime
from data.servers import servers


DB_NAME = "shop.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE,
        username TEXT,
        chat_id INTEGER
    )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    tg_id INTEGER PRIMARY KEY
)
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS server_settings (
        server_key TEXT PRIMARY KEY,
        server_id INTEGER,
        name TEXT,
        price INTEGER,
        stock INTEGER,
        is_active INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER UNIQUE,
        user_tg_id INTEGER,
        username TEXT,
        chat_id INTEGER,
        status TEXT,
        server TEXT,
        server_id INTEGER,
        virts INTEGER,
        rubles INTEGER,
        created_at TEXT
    )
    """)

    for key, server in servers.items():
        cursor.execute("""
    INSERT OR IGNORE INTO server_settings (
        server_key,
        server_id,
        name,
        price,
        stock,
        is_active
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        key,
        server["id"],
        server["name"],
        server["price"],
        server.get("stock", 200_000_000),
        1
    ))

    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN created_at TEXT")
    except sqlite3.OperationalError:
        pass

    db.commit()
    db.close()


def add_or_update_user(tg_id: int, username: str | None, chat_id: int):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    INSERT INTO users (tg_id, username, chat_id)
    VALUES (?, ?, ?)
    ON CONFLICT(tg_id) DO UPDATE SET
        username = excluded.username,
        chat_id = excluded.chat_id
    """, (tg_id, username, chat_id))

    db.commit()
    db.close()


def create_order(
    order_id: int,
    user_tg_id: int,
    username: str | None,
    chat_id: int,
    server: str,
    server_id: int,
    virts: int,
    rubles: int
):
    db = get_connection()
    cursor = db.cursor()

    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    cursor.execute("""
    INSERT INTO orders (
        order_id,
        user_tg_id,
        username,
        chat_id,
        status,
        server,
        server_id,
        virts,
        rubles,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_id,
        user_tg_id,
        username,
        chat_id,
        "⏳ Ожидает",
        server,
        server_id,
        virts,
        rubles,
        created_at
    ))

    db.commit()
    db.close()


def update_order_status(order_id: int, status: str):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    UPDATE orders
    SET status = ?
    WHERE order_id = ?
    """, (status, order_id))

    db.commit()
    db.close()


def get_user_orders(user_tg_id: int):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    SELECT order_id, status, server, server_id, virts, rubles, created_at
    FROM orders
    WHERE user_tg_id = ?
    ORDER BY id DESC
    """, (user_tg_id,))

    orders = cursor.fetchall()

    db.close()

    return orders

def add_admin(tg_id: int):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO admins (tg_id)
    VALUES (?)
    """, (tg_id,))

    db.commit()
    db.close()


def remove_admin(tg_id: int):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    DELETE FROM admins
    WHERE tg_id = ?
    """, (tg_id,))

    db.commit()
    db.close()


def is_admin_db(tg_id: int) -> bool:
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    SELECT tg_id FROM admins
    WHERE tg_id = ?
    """, (tg_id,))

    result = cursor.fetchone()

    db.close()

    return result is not None


def update_all_server_prices(price: int):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    UPDATE server_settings
    SET price = ?
    WHERE is_active = 1
    """, (price,))

    db.commit()
    db.close()


def get_servers_from_db():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    SELECT server_key, server_id, name, price, stock
    FROM server_settings
    WHERE is_active = 1
    ORDER BY server_id ASC
    """)

    rows = cursor.fetchall()

    db.close()

    result = {}

    for row in rows:
        key, server_id, name, price, stock = row

        result[key] = {
            "id": server_id,
            "name": name,
            "price": price,
            "stock": stock
        }

    return result


def add_server(name: str):
    db = get_connection()
    cursor = db.cursor()

    name = name.strip()
    server_key = name.upper().replace(" ", "_")

    # Проверяем, есть ли уже такой сервер
    cursor.execute("""
    SELECT is_active FROM server_settings
    WHERE server_key = ?
    """, (server_key,))

    existing = cursor.fetchone()

    if existing and existing[0] == 1:
        db.close()
        return None

    # Берём максимальный ID только среди активных серверов
    cursor.execute("""
    SELECT MAX(server_id)
    FROM server_settings
    WHERE is_active = 1
    """)

    max_id = cursor.fetchone()[0]

    if max_id is None:
        max_id = 0

    new_id = max_id + 1

    # Берём текущую цену с любого активного сервера
    cursor.execute("""
    SELECT price FROM server_settings
    WHERE is_active = 1
    ORDER BY server_id ASC
    LIMIT 1
    """)

    row = cursor.fetchone()
    price = row[0] if row else 100

    # Если сервер уже был в базе, но удалён — активируем заново
    if existing and existing[0] == 0:
        cursor.execute("""
        UPDATE server_settings
        SET server_id = ?,
            name = ?,
            price = ?,
            stock = ?,
            is_active = 1
        WHERE server_key = ?
        """, (
            new_id,
            name,
            price,
            200_000_000,
            server_key
        ))

    else:
        cursor.execute("""
        INSERT INTO server_settings (
            server_key,
            server_id,
            name,
            price,
            stock,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            server_key,
            new_id,
            name,
            price,
            200_000_000,
            1
        ))

    db.commit()
    db.close()

    return new_id

def delete_server_by_name(name: str) -> bool:
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    UPDATE server_settings
    SET is_active = 0
    WHERE LOWER(name) = LOWER(?)
    """, (name,))

    changed = cursor.rowcount > 0

    db.commit()
    db.close()

    return changed


def update_server_stock(server_key: str, stock: int):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    UPDATE server_settings
    SET stock = ?
    WHERE server_key = ?
    """, (stock, server_key))

    db.commit()
    db.close()


def get_all_user_chat_ids():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
    SELECT chat_id FROM users
    WHERE chat_id IS NOT NULL
    """)

    rows = cursor.fetchall()

    db.close()

    return [row[0] for row in rows]