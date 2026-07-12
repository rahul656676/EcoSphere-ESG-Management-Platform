import pytest
import os
import sys
import tempfile
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

import models

@pytest.fixture
def db_setup():
    db_path = os.path.join(tempfile.gettempdir(), f"test_{uuid.uuid4().hex}.db")
    models.DB_PATH = db_path
    models.init_db(force=True)
    yield
    try:
        os.unlink(db_path)
    except:
        pass
def test_insert_and_query_department(db_setup):
    models.insert_row("department", {"name": "Test Dept", "code": "TD01"})
    dept = models.query("SELECT * FROM department WHERE code = 'TD01'", one=True)
    assert dept is not None
    assert dept["name"] == "Test Dept"

def test_table_all(db_setup):
    models.insert_row("category", {"name": "Volunteering", "type": "CSR Activity"})
    models.insert_row("category", {"name": "Recycling", "type": "Challenge"})
    categories = models.table_all("category")
    assert len(categories) >= 2
