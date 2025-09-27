#!/usr/bin/env python3

import pytest
from app import app, db
from models import Message

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

@pytest.fixture(autouse=True)
def seed_messages():
    with app.app_context():
        if not Message.query.first():
            message = Message(body="Test message", username="TestUser")
            db.session.add(message)
            db.session.commit()

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))