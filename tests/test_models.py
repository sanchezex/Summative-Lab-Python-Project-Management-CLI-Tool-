import os
import json
from models.user import User
from models.project import Project
from models.task import Task


def test_user_serialization_roundtrip(tmp_path):
    u = User(name="Alice", email="alice@example.com")
    d = u.to_dict()
    u2 = User.from_dict(d)
    assert u2.name == "Alice"
    assert u2.email == "alice@example.com"


def test_project_task_linking():
    u = User(name="Bob")
    p = Project(title="Test Project", owner_id=u.id)
    t = Task(title="Write tests", project_id=p.id, assigned_to=u.id)
    p.task_ids.append(t.id)
    u.project_ids.append(p.id)
    assert p.id in u.project_ids
    assert t.id in p.task_ids
