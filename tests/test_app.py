from app import app
import os
import pytest
import tempfile


# need to export PYTHONPATH='.' if running pytest, so it can find app module

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
