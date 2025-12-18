import pytest
from apps.users import services
from apps.users.models import User

pytestmark = pytest.mark.django_db

def test_create_user():
    u = services.create_user({"email": "a@example.com", "name": "A"})
    assert isinstance(u, User)
    assert u.email == "a@example.com"
