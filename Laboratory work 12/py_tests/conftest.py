import pytest
from app import create_app,db,bcrypt
from config import config
from app.models import User

@pytest.fixture(scope="module")
def client():
    app = create_app(config_class=config["test"])

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def login_test_user(client):
        hashed_password = bcrypt.generate_password_hash("password")
        newuser = User(username="test user",email="test@test.com",password=hashed_password)
        db.session.add(newuser)
        db.session.commit()
        client.post('/login/', data={
            'email': 'test@test.com',
            'password': 'password',
            
        })

        yield
        client.get("/logout/")

