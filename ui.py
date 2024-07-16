import service
from colorama import Fore
from models import TodoType
from db import cursor, conn
from utils import Response
from form import UserRegisterForm


def print_response(response: Response):
    color = Fore.GREEN if response.status_code == 200 else Fore.RED
    print(color + response.data + Fore.RESET)


def login_page():
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    response = service.login(username, password)
    print_response(response)


def register_page():
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    form = UserRegisterForm(username, password)
    response = service.register(form)
    print_response(response)


def logout_page():
    response = service.logout()
    print_response(response)


def add_todo():
    user_id = input('Enter your user ID: ')
    role_query = '''SELECT role FROM users WHERE id=%s'''
    cursor.execute(role_query, (user_id,))
    user_role = cursor.fetchone()
    if user_role and user_role[0] == 'admin':
        name = input('Enter name: ')
        description = input('Enter description: ')
        response = service.todo_add(name, description)
        print_response(response)
    else:
        response = Response('Only admin users can add todos', 404)
        print_response(response)


def update_todo():
    user_id = input('Enter your user ID: ')
    role_query = '''SELECT role FROM users WHERE id=%s'''
    cursor.execute(role_query, (user_id,))
    user_role = cursor.fetchone()
    if user_role and user_role[0] == 'admin':
        todo_id = input('Enter the ID of the todo to update: ')
        name = input('Enter new name: ')
        description = input('Enter new description: ')
        todo_type = input('Enter new todo type: ')
        update_todo_query = '''
            UPDATE todo SET name=%s,
                            description=%s,
                            todo_type=%s,
                            user_id=%s
            WHERE id=%s'''
        todo_data = (name, description, todo_type, user_id, todo_id)
        cursor.execute(update_todo_query, todo_data)
        conn.commit()
        response = Response('Todo updated successfully.', 200)
    else:
        response = Response('Only admin users can update todos.', 404)
    print_response(response)


def delete_todo():
    user_id = input('Enter your user ID: ')
    role_query = '''SELECT role FROM users WHERE id=%s'''
    cursor.execute(role_query, (user_id,))
    user_role = cursor.fetchone()
    if user_role and user_role[0] == 'admin':
        todo_id = input('Enter the ID of the todo to delete: ')
        delete_todo_query = '''DELETE FROM todo WHERE id=%s'''
        cursor.execute(delete_todo_query, (todo_id,))
        conn.commit()
        response = Response('Todo deleted successfully.', 200)
    else:
        response = Response('Only admin users can delete todos.', 404)
    print_response(response)


def block_user():
    user_id = input('Enter your user ID: ')
    role_query = '''SELECT role FROM users WHERE id=%s'''
    cursor.execute(role_query, (user_id,))
    user_role = cursor.fetchone()
    if user_role and user_role[0] == 'admin':
        block_user_id = input('Enter the user ID to block: ')
        blocked_user_query = '''UPDATE users SET login_try_count=3 WHERE id=%s'''
        cursor.execute(blocked_user_query, (block_user_id,))
        conn.commit()
        response = Response('User blocked successfully.', 200)
    else:
        response = Response('Only admin users can block users.', 404)
    print_response(response)


while True:
    print('1=>login\n2=>register\n3=>logout\n4=>add todo\n5=>update todo\n6=>delete todo\n7=>block user\nq=>quit')
    choice = input('Enter your choice: ')
    if choice == '1':
        login_page()
    elif choice == '2':
        register_page()
    elif choice == '3':
        logout_page()
    elif choice == '4':
        add_todo()
    elif choice == '5':
        update_todo()
    elif choice == '6':
        delete_todo()
    elif choice == '7':
        block_user()
    elif choice == 'q':
        break
    else:
        response = Response('Invalid choice. Please try again.', 404)
        print_response(response)
