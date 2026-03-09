import pytest
from database import GradSchemeDB
from models.grad_scheme import GradScheme

#pytest fixtures are functions that set up and tear down resources for tests
@pytest.fixture
def test_db():
    db = GradSchemeDB(":memory:")
    yield db
    db.close()

def test_database(test_db):
    test_scheme = GradScheme("Google", "Software Engineer Graduate Scheme", "London", "£30000", "Open", "September", "https://www.google.com/about/careers/applications/students/")
    test_db.upsert_grad_scheme(test_scheme)
    db_schemes = test_db.get_schemes()
    assert db_schemes[0]["scheme_name"] == "Software Engineer Graduate Scheme"
    
def test_database_status_chanhe(test_db):
    test_scheme = GradScheme("Google", "Software Engineer Graduate Scheme", "London", "£30000", "Open", "September", "https://www.google.com/about/careers/applications/students/")
    test_db.upsert_grad_scheme(test_scheme)
    test_scheme = GradScheme("Google", "Software Engineer Graduate Scheme", "London", "£30000", "Closed", "September", "https://www.google.com/about/careers/applications/students/")
    test_db.upsert_grad_scheme(test_scheme)
    db_schemes = test_db.get_schemes()
    assert db_schemes[0]["status"] == "Closed"