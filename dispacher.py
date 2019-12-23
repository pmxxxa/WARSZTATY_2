from typing import Union, List
from datetime import datetime
from models import User, Message


class WrongParameterError(Exception):
    """Error when wrong params set is given"""
    pass


class Dispacher:
    """HINT: USERNAME == EMAIL """

    @staticmethod
    def create_user(self, email: str, password: str, salt, cursor) -> User:
        user = User()
        if not user.get_by_email(cursor, email):
            user.username = email.split("@")[0]
            user.email = email
            user.set_password(password, salt)
            user.save(cursor)
            print("User created")
        else:
            raise WrongParameterError("User already exists!")

    @staticmethod
    def login_user(self, cursor, username: str, password: str) -> Union[User, None]:
        user = User().get_by_username(cursor, username)
        if user:
            if user.check_password(password):
                print("Logged In")
            else:
                raise WrongParameterError("Wrong password!")
        else:
            raise WrongParameterError("User doesn't exist!")

    @staticmethod
    def print_all_users(self, cursor) -> List[Union[User, None]]:
        all_users = User().get_all(cursor)
        if all_users:
            print("Users:\n")
            return [print(user) for user in all_users]
        else:
            raise WrongParameterError("There is no users!")

    def change_password(self, cursor, salt, username, password, new_password: str) -> None:
        user = self.login_user(cursor, username, password)
        if user:
            if password != new_password:
                user.set_password(new_password, salt)
                user.save(cursor)
                print("Password changed!")
            else:
                raise WrongParameterError("The new password must be different from the old one!")

    def delete_user(self, cursor, username, password) -> None:
        user = self.login_user(cursor, username, password)
        if user:
            user.delete(cursor)
            print("User deleted")

    def list_messages_to_user(self, cursor, username, password) -> List[Union[Message, None]]:
        user = self.login_user(cursor, username, password)
        if user:
            messages_list = Message().load_all_messages_for_user()
            print(f"Messages to user - {username}\n")
            return [print(f" {message.id}. FROM - {message.from_id}, DATE - {message.creation_date}: {message.text};") for message in messages_list]

    def send_message(self, cursor, username, password, text, to_id) -> Message:
        user = self.login_user(cursor, username, password)
        if user:
            message = Message()
            message.from_id = user.id
            message.to_id = to_id
            message.text = text
            message.creation_date = datetime.now()
            message.save(cursor)

    def not_available_option(self):
        """No other available option"""
        raise WrongParameterError("Wrong parameters set up!")
