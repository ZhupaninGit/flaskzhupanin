import urllib
import unittest
from flask import Flask, url_for,current_app,flash
from flask_login import current_user
from flask_testing import TestCase
from app import create_app
from urllib.request import urlopen
from app import db,bcrypt
from app.models import User
from app.todo.model import Todo
from config import config


class TestWebApp(unittest.TestCase):
    def setUp(self):
        """
        Налаштування тесту перед його виконанням:
        створення з'єднання з додатком, створення контексту додатка, 
        створення бази даних та додавання тестового користувача.
        """
        self.app = create_app(config_class=config["test"])
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.add_user()
        self.client = self.app.test_client()

    def add_user(self):
        """
        Додавання тестового користувача до бази даних для використання у тестах.
        """
        hashed_password = bcrypt.generate_password_hash("password")
        newuser = User(username="test user",email="test@test.com",password=hashed_password)
        db.session.add(newuser)
        db.session.commit()

    def login_to_test_account(self):
            """
            Функція для входу в аккаунт.

            Для деяких тестів необхідно входити в аккаунт.
            Вхід в тестовий акаунт:
            відправляє POST-запит на сторінку входу з тестовими обліковими даними.
            """
            self.client.post('/login/', data={
                'email': 'test@test.com',
                'password': 'password',
            })

    def tearDown(self):
        """
        Завершення тестування:
        видаляє всі дані з бази даних, закриває контекст додатка та очищує змінні.
        """
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        """
        Тест перевірки наявності додатка та його співпадіння з поточним додатком.
        """
        assert self.app is not None
        assert current_app == self.app

    def test_main_page_view(self):
        """
        Тест перегляду головної сторінки:
        перевіряє статус коду відповіді та наявність певного тексту 
        ('ZhupaninSoftware') у вмісті відповіді.
        """
        response = self.client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert b"ZhupaninSoftware" in response.data

    def test_projects_page_view(self):
        """
        Тест перегляду сторінки проектів:
        перевіряє статус коду відповіді та наявність тексту 'Projects' 
        у вмісті відповіді.
        """
        response = self.client.get('/projects', follow_redirects=True)
        assert response.status_code == 200
        assert b"Projects" in response.data

    def test_contacts_page_view(self):
        """
        Тест перегляду сторінки контактів:
        перевіряє статус коду відповіді та наявність тексту 'Instagram' 
        у вмісті відповіді.
        """
        response = self.client.get('/contacts', follow_redirects=True)
        assert response.status_code == 200
        assert b"Instagram" in response.data

    def test_skills_page_view(self):
        """
        Тест перегляду сторінки навичок:
        перевіряє статус коду відповіді та наявність тексту 'Basic' 
        у вмісті відповіді.
        """
        response = self.client.get('/skills', follow_redirects=True)
        assert response.status_code == 200
        assert b"Basic" in response.data

    def test_todo_page_view(self):
        """
        Тест перегляду сторінки задач:
        перевіряє статус коду відповіді та наявність тексту 'ToDo' 
        у вмісті відповіді.
        """
        response = self.client.get('/todo/todo/', follow_redirects=True)
        assert response.status_code == 200
        assert b"ToDo" in response.data


    def test_feedback_page_view(self):
        """
        Тест перегляду сторінки відгуків:
        перевіряє статус коду відповіді та наявність тексту 'feedback' 
        у вмісті відповіді.
        """
        response = self.client.get('/feedbacks/feedback/', follow_redirects=True)
        assert response.status_code == 200
        assert b"feedback" in response.data

    def test_post_page_view(self):
        """
        Тест перегляду сторінки постів:
        перевіряє статус коду відповіді та наявність тексту 'posts' 
        у вмісті відповіді.
        """
        response = self.client.get('/post', follow_redirects=True)
        assert response.status_code == 200
        assert b"posts" in response.data

    def test_login_page_view(self):
        """
        Тест перегляду сторінки входу:
        перевіряє статус коду відповіді та наявність тексту 'e-mail' 
        у вмісті відповіді.
        """
        response = self.client.get('/login', follow_redirects=True)
        assert response.status_code == 200
        assert b"e-mail" in response.data


    def test_register_page_view(self):
        """
        Тест перегляду сторінки реєстрації:
        перевіряє статус коду відповіді та наявність тексту 'e-mail' 
        у вмісті відповіді.
        """
        response = self.client.get('/register/', follow_redirects=True)
        assert response.status_code == 200
        assert b"e-mail" in response.data

    def test_account_page_redirect_without_login(self):
        """
        Тест перенаправлення зі сторінки облікового запису без входу:
        перевіряє статус коду відповіді та шлях перенаправлення на сторінку входу.
        """
        response = self.client.get('/account/', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login/'

    def test_account_page_redirect_login(self):
        """
        Тест перенаправлення зі сторінки облікового запису при вході:
        авторизується, перевіряє статус коду відповіді та шлях перенаправлення 
        на сторінку облікового запису.
        """
        self.login_to_test_account()
        response = self.client.get('/account/', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/account/'


    def test_register_and_authenthification(self):
        """
        Тест реєстрації та автентифікації користувача:
        намагається зареєструвати нового користувача, потім входить в цей аккаунт.
        Перевіряє вхід та перехід на сторінку облікового запису.
        """
        response = self.client.post('/register/', data={
            'username': 'New Username',
            'email': 'username@example.com',
            'password': "password",
            'confirm_password': "password",
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login/' # redirected to login
        
        user = User.query.filter_by(username='New Username').first()
        assert user.password != 'password'

        response = self.client.post('/login', data={
            'email': 'username@example.com',
            'password': "password",
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert response.request.path == '/account/'
        assert 'New Username' in html

    def test_register_user_mismatched_passwords(self):
        """
        Тест реєстрації користувача з невідповідністю паролів:
        перевіряє статус коду відповіді та наявність повідомлення 
        про неспівпадання паролів у відповіді.
        """
        response = self.client.post('/register/', data={
            'username': 'Newest User',
            'email': 'newemail@example.com',
            'password': 'password1',
            'confirm_password': 'password2',
        })
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Паролі не співпадають!' in html

    def test_user_logout(self):
        """
        Тест виходу користувача:
        входить за тестовим користувачем, потім виходить з аккаунту 
        та перевіряє перенаправлення на сторінку входу.
        """
        self.login_to_test_account()
        response = self.client.get('/logout/', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login/'
        html = response.get_data(as_text=True)
        assert 'Ви успішно вийшли з власного аккаунту' in html


    def test_account_info_change(self):
        """
        Тест зміни інформації облікового запису:
        входить за тестовим користувачем, змінює дані облікового запису 
        та перевіряє успішність оновлення. Перевіряє, чи електронна адреса 
        користувача оновилася в базі даних.
        """
        self.login_to_test_account()
        response = self.client.post('/account/', data={
                'username': 'Updated User',
                'email': 'somenewest@email.com'
            }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Успішне оновлення даних користувача' in html

        user = User.query.filter_by(username='Updated User').first()
        assert user.email == 'somenewest@email.com'

    def test_todo_creating(self):
        """
        Тест створення нової задачі:
        намагається додати нову задачу та перевіряє успішність додавання 
        у відповіді.
        """
        response = self.client.post('/todo/add_do/', data={
                'newtodo': 'New todo',
                'newtododescription': 'New todo description'
            }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Завдання було успішно додано.' in html

    def test_todo_updating(self):
        """
        Тест оновлення задачі:
        додає нову задачу до бази даних, потім оновлює статус задачі 
        та перевіряє, чи він оновився в базі даних.
        """
        todo = Todo(title="todo", description="description", complete=False)
        db.session.add(todo)
        db.session.commit()

        response = self.client.get('/todo/update_do/1', follow_redirects=True)

        assert response.status_code == 200

        updated_todo = db.session.get(Todo, 1)
        assert updated_todo.complete == True


    def test_todo_deleting(self):
        """
        Тест видалення задачі:
        додає нову задачу до бази даних, потім намагається видалити її 
        та перевіряє, чи вона була успішно видалена з бази даних.
        """
        todo = Todo(title="todo", description="description", complete=False)
        db.session.add(todo)
        db.session.commit()

        response = self.client.get('/todo/delete_do/1', follow_redirects=True)

        assert response.status_code == 200

        delete_do = db.session.get(Todo, 1)
        assert delete_do == None



if __name__ == '__main__':
    unittest.main()