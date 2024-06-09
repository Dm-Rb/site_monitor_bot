import sqlite3


class Database:

    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER UNIQUE PRIMARY KEY,                    
                notif_status INTEGER DEFAULT (1))
            WITHOUT ROWID;                    
            """)
        self.connection.commit()

    def check_user_id_exist(self, user_id):
        """ Проверить наличие user_id  в базе :return bool """

        with self.connection:
            result = self.cursor.execute(f"SELECT user_id FROM 'users' WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_new_user(self, user_id):
        """ Добавить новую строку """

        with self.connection:
            return self.cursor.execute(
                "INSERT INTO 'users' ('user_id', 'notif_status') VALUES(?,?)",
                (user_id, 1))

    def get_all_data(self):
        """ Достать все записи из БД :return list(tuple1, tuple2, tuple3) | len(tuple) == 4 """

        with self.connection:
            return self.cursor.execute("SELECT user_id, jira_token FROM 'users'").fetchall()

    def del_user(self, user_id):
        """ Удалить строку """

        with self.connection:
            return self.cursor.execute(
                f"DELETE FROM 'users' WHERE user_id = {user_id}"
            )

    def get_notification_status(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT notif_status FROM 'users' WHERE user_id = ?",
                                         (user_id,)).fetchmany(1)
            return result[0][0]

    def change_notif_status(self, user_id):
        status = self.get_notification_status(user_id)
        status = int(not bool(status))
        with self.connection:
            return self.cursor.execute(
                f"UPDATE 'users' SET notif_status={status} WHERE user_id={user_id}"
            )

    def get_users_where_status_on(self):
        with self.connection:
            users = self.cursor.execute(f"SELECT user_id FROM 'users' WHERE notif_status=1").fetchall()
            result = [i[0] for i in users]
            return result
