import pytest
from infrastructure.Cafeteria import Cafeteria

def test_cafeteria_init():
    c = Cafeteria("Main Cafe", "Campus")
    assert c.name == "Main Cafe"
    assert c.location == "Campus"

def test_serve_meal():
    c = Cafeteria("Cafe", "Campus")
    c.add_dish("Soup")
    person = type('P', (), {})()
    assert c.serve_meal(person) == True