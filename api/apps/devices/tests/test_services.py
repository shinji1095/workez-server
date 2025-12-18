import pytest
from apps.devices import services
from apps.devices.models import Device

pytestmark = pytest.mark.django_db

def test_create_device():
    d = services.create_device({"id": "DEV001", "name": "X"})
    assert isinstance(d, Device)
    assert d.id == "DEV001"
