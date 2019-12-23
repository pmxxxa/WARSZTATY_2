from datetime import datetime

from psycopg2 import connect
from psycopg2.extras import RealDictCursor

from clcrypto import password_hash, check_password, generate_salt


def create_conenction(db_name='communications_server'):
    # Otwarcie połączenie do podanej bazy danych.
    db_connection = connect(
        user='postgres',
        password='coderslab',
        host='localhost',
        database=db_name
    )
    # Włączenie autocommit powoduje natychmiastowe wykonanie poleceń typu swtórz tabelę(transakcji)
    db_connection.autocommit = True
    # Zwrócenie połączenia.
    return db_connection


def get_cursor(db_connection):
    # Utworzenie kursora aby wykonać polecenie sql na bazie.
    return db_connection.cursor(cursor_factory=RealDictCursor)


class User:
    def __init__(self):
        self._id = -1
        self.username = None
        self._hashed_password = None
        self.email = None

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt):
        self._hashed_password = password_hash(password, salt)

    def check_password(self, password_to_check):
        return check_password(password_to_check, self._hashed_password)

    @staticmethod
    def _create_user_object(username, _hashed_password, email, id=-1):
        user = User()
        user.username = username
        user._hashed_password = _hashed_password
        user.email = email
        user._id = id
        return user

    def get_all(self, cursor):
        sql = "SELECT username, hashed_password, email, id FROM Users"
        cursor.execute(sql)
        objects = []
        for row in cursor.fetchall():
            user = self._create_user_object(row['username'], row['hashed_password'], row['email'], row['id'])
            objects.append(user)
        return objects

    def get_by_id(self, cursor, id):
        sql = "SELECT username, hashed_password, email, id FROM Users WHERE id=%s"
        # Drugi parametr w execute jest to lista gdzie kolejne elementy będą wstawiane w kolejne miejsca %s
        # Gwarantuje to ochronę przed SQL Injection
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._create_user_object(row['username'], row['hashed_password'], row['email'], row['id'])

    def get_by_email(self, cursor, email):
        sql = "SELECT username, hashed_password, email, id FROM Users WHERE email=%s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._create_user_object(row['username'], row['hashed_password'], row['email'], row['id'])

    def get_by_username(self, cursor, username):
        sql = "SELECT username, hashed_password, email, id FROM Users WHERE username=%s"
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._create_user_object(row['username'], row['hashed_password'], row['email'], row['id'])

    def save(self, cursor):
        if self._id == -1:
            self._create(cursor)
            return 'Created'
        else:
            self._update(cursor)
            return 'Updated'

    def _create(self, cursor):
        sql = "INSERT INTO users (email, username, hashed_password) VALUES (%s, %s, %s) RETURNING id"
        values = (self.email, self.username, self._hashed_password)
        cursor.execute(sql, values)
        self._id = cursor.fetchone()['id']

    def _update(self, cursor):
        sql = "UPDATE Users SET email=%s, username=%s, hashed_password=%s WHERE id=%s"
        values = (self.email, self.username, self._hashed_password, self._id)
        cursor.execute(sql, values)

    def delete(self, cursor):
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self._id,))

    def __repr__(self):
        return f'User id: {self._id}, email: {self.email}, username: {self.username}'


class Message:
    def __init__(self):
        self._id = -1
        self.from_id = None
        self.to_id = None
        self.text = None
        self.creation_date = None

    @property
    def id(self):
        return self._id

    @staticmethod
    def _create_message(from_id, to_id, text, creation_date=None, id=-1):
        message = Message()
        message.from_id = from_id
        message.to_id = to_id
        message.text = text
        message.creation_date = creation_date or datetime.now()
        message._id = id
        return message

    def load_message_by_id(self, cursor, id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Messages WHERE id=%s"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._create_message(row['from_id'], row['to_id'], row['text'], row['creation_date'], row['id'])

    def load_all_messages_for_user(self, cursor, to_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Messages WHERE to_id=%s"
        cursor.execute(sql, (to_id,))
        objects = []
        for row in cursor.fetchall():
            message = self._create_message(row['from_id'], row['to_id'], row['text'], row['creation_date'], row['id'])
            objects.append(message)
        return objects

    def load_all_messages(self, cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Messagess"
        cursor.execute(sql)
        objects = []
        for row in cursor.fetchall():
            message = self._create_message(row['from_id'], row['to_id'], row['text'], row['creation_date'], row['id'])
            objects.append(message)
        return objects

    def save(self, cursor):
        if self._id == -1:
            self._create(cursor)
            return 'Created'
        else:
            self._update(cursor)
            return 'Updated'

    def _create(self, cursor):
        sql = """INSERT INTO Messages (from_id, to_id, text, creation_date) VALUES (%s, %s, %s, %s)
              RETURNING id, creation_date"""
        values = (self.from_id, self.to_id, self.text, datetime.now())
        cursor.execute(sql, values)
        db_data = cursor.fetchone()
        self._id = db_data['id']
        self.creation_date = db_data['creation_date']

    def _update(self, cursor):
        sql = "UPDATE Messages SET id=%s, from_id=%s, to_id=%s, text=%s creation_date=%s WHERE id=%s"
        values = (self._id, self.from_id, self.to_id, self.text, self.creation_date)
        cursor.execute(sql, values)

    def __repr__(self):
        return f'WIADOMOŚĆ ID: {self._id}, OD: {self.from_id}, DO: {self.to_id}\nTREŚĆ: {self.text}\nDATA: {self.creation_date}'


if __name__ == '__main__':
    salt = generate_salt()
    connection = create_conenction()
    cursor = get_cursor(connection)

    # user1 = User()
    # user1.username = 'User1'
    # user1.email = 'user1@domain.com'
    # user1.set_password('pass', salt)
    # user1.save(cursor)

    """user2 = User()
    user2.username = 'User2'
    user2.email = 'user2@domain.com'
    user2.set_password('pass', salt)
    user2.save(cursor)

    print(User().get_all(cursor))
    print(User().get_by_id(cursor, 1))
    #user2.delete(cursor)
    #print('Usunięcie', user2)
    print(User().get_all(cursor))"""

    message1 = Message()
    message1.from_id = 1
    message1.to_id = 2
    message1.text = "Co tam?"
    message1.save(cursor)
    print(message1)

    cursor.close()
    connection.close()
