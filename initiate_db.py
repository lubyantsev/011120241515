import sqlite3

def create_table():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Создаем таблицу Products, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def seed_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Добавляем начальные записи в таблицу Products
    products = [
        ('Витамин A', 'Витамин A помогает поддерживать здоровье глаз и кожи.', 100),
        ('Витамин C', 'Витамин C помогает укреплять иммунную систему.', 150),
        ('Витамин D', 'Витамин D важен для здоровья костей и зубов.', 200),
        ('Витамин E', 'Витамин E является мощным антиоксидантом.', 250)
    ]

    cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', products)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()  # Создаем таблицу перед добавлением данных
    seed_db()