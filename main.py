import argparse

from dispacher import Dispacher
from logic_handler import OptionsHandler

parser = argparse.ArgumentParser(description='Program options')
parser.add_argument('--username', '-u', help='Login - user email', action='store')
parser.add_argument('--password', '-p', help='User password', action='store')
parser.add_argument('--new-password', '-n', help='New password', action='store')
parser.add_argument('--edit', '-e', help='Edit', action='store_true')
parser.add_argument('--delete', '-d', help='Delete user', action='store_true')
parser.add_argument('--list', '-l', help='List of user or massages', action='store_true')
parser.add_argument('--send', '-s', help='Send', action='store')
parser.add_argument('--to', '-t', help='Address of message', action='store')

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    dispacher = Dispacher()

    option_handler = OptionsHandler(
        args.password, args.username, args.new_password, args.edit, args.delete, args.list, args.send, args.to
    )

    if option_handler.create_user:
        dispacher.create_user(args.username, args.password)
        print('User Created')
    elif option_handler.list_all_users:
        dispacher.print_all_users()
        print('All users list')
    elif option_handler.list_all_messages_for_user:
        dispacher.list_messages_to_user(args.username, args.password)
        print('All messages for user')
    elif option_handler.change_password:
        dispacher.change_password(args.username, args.password, args.new_password)
        print('Password Changed!')
    elif option_handler.send_message:
        dispacher.send_message(args.username, args.password, args.to, args.send)
        print('Message sent !')
    elif option_handler.delete_user:
        dispacher.delete_user(args.username, args.password)
        print('User deleted')
    else:
        dispacher.not_available_option()