import sqlite3

class Database_With_Users:
    def __init__(self, name='Databases/users.db'):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                win INTEGER,
                draw INTEGER,
                lose INTEGER, 
                levels INTEGER,
                m1 INTEGER,
                m2 INTEGER,
                m3 INTEGER,
                m4 INTEGER,
                m5 INTEGER,
                almaz INTEGER
                )
            '''
        )
        self.connection.commit()

    def update_name_users(self, new_name, id):
        self.cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_name, id))
        self.connection.commit()

    def update_data_for_user(self, id, data, zn):
        query = f"SELECT {data} FROM users WHERE id = {id}"
        self.cursor.execute(query)
        if not zn: data_after = self.cursor.fetchone()[0] + 1
        else: data_after = self.cursor.fetchone()[0] + zn
        self.cursor.execute(f"UPDATE users SET {data} = ? WHERE id = ?", (data_after, id))
        self.connection.commit()

    def add_user(self, username, login, password):
        try:
            self.cursor.execute("INSERT INTO users (username, login, password, win, draw, lose, levels, m1, "
                                "m2, m3, m4, m5, almaz) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (username, login, password, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
           return False

    def find_user(self, login, password):
        query = "SELECT * FROM users WHERE login = ? AND password = ?"
        self.cursor.execute(query, (login, password))
        user = self.cursor.fetchone()
        if user:
            return user
        else:
            return False

    def close(self):
        self.connection.close()