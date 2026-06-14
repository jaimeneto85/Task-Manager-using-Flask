import os
import tempfile

os.environ['TESTING'] = '1'
os.environ['SECRET_KEY'] = 'test-secret-key'

_db_fd, _db_path = tempfile.mkstemp(suffix='.db')
os.close(_db_fd)
os.environ['DATABASE_URI'] = f'sqlite:///{_db_path}'

import pytest

from todo_project import app as flask_app, db, bcrypt
from todo_project.models import User, Task


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_user(app):
    def _make_user(username='tester', password='secret123'):
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed)
        db.session.add(user)
        db.session.commit()
        return user
    return _make_user


@pytest.fixture
def auth_client(client, make_user):
    make_user(username='tester', password='secret123')
    client.post('/login', data={'username': 'tester', 'password': 'secret123'},
                follow_redirects=True)
    return client


def pytest_unconfigure(config):
    # Release the pooled SQLite connection so the temp DB file can be deleted on
    # Windows, where an open handle would otherwise block removal (WinError 32).
    with flask_app.app_context():
        db.engine.dispose()
    if os.path.exists(_db_path):
        try:
            os.remove(_db_path)
        except OSError:
            pass
