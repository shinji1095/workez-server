import pytest
from apps.users import services as user_services
from apps.admin import services as admin_services

pytestmark = pytest.mark.django_db

def test_update_admin_user_role():
    u = user_services.create_user({"email": "b@example.com", "name": "B"})
    updated = admin_services.update_admin_user(str(u.id), {"role": "admin"})
    assert updated.role == "admin"
