import sqlite3
import time


class Database:

    def __init__(self, db_file):
        """Инициализация класса"""
        # Подключение к БД
        self.connection = sqlite3.connect(db_file)
        # C его помощью будут создаваться запросы в БД
        self.cursor = self.connection.cursor()

    # Добавить нового пользователя
    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            return self.connection.commit()

    # Проверка наличия пользователя в БД
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
            return bool(len(result.fetchall()))

    # Указать никнэйм
    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE users SET nickname = ? WHERE user_id = ?", (nickname, user_id,))

    # Узнать на какой стадии регистрации находится пользователь
    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    # Изменение стадии регистрации пользователя
    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup = ? WHERE user_id = ?", (signup, user_id,))

    # Получить никнэйм
    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT nickname FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    # Изменение переменной time_sub в БД
    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            return self.cursor.execute("UPDATE users SET time_sub = ? WHERE user_id = ?", (time_sub, user_id,))

    # Получение переменной time_sub из БД
    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT time_sub FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub

    # Получение bool переменной о наличии подписки
    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT time_sub FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])

            if time_sub > int(time.time()):
                return True
            else:
                return False

    # Узнать на какой стадии парсинга находится пользователь
    def get_pars(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT pars_video FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                pars_video = str(row[0])
            return pars_video

    # Изменение стадии парсинга пользователя
    def set_pars(self, user_id, pars_video):
        with self.connection:
            return self.cursor.execute("UPDATE users SET pars_video = ? WHERE user_id = ?", (pars_video, user_id,))

    # Изменение стадии парсинга пользователя
    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users").fetchall()
