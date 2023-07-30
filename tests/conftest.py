import pytest
from menu_app import models
from menu_app.database import engine

@pytest.fixture
def cleanup_db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
