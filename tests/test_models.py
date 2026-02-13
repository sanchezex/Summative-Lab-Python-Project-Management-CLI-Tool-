import os
import json
import pytest
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


def test_user_methods():
    u = User(name="Charlie", email="charlie@example.com")
    assert u.get_project_count() == 0
    u.add_project(1)
    assert u.get_project_count() == 1
    assert u.remove_project(1) is True
    assert u.get_project_count() == 0
    assert u.remove_project(1) is False  # Already removed


def test_project_methods():
    p = Project(title="Demo Project", due_date="2030-12-31")
    assert p.get_task_count() == 0
    p.add_task(1)
    p.add_task(2)
    assert p.get_task_count() == 2
    assert p.remove_task(1) is True
    assert p.get_task_count() == 1
    assert p.is_overdue() is False  # Due date is in the future


def test_task_methods():
    t = Task(title="Test Task", status="open")
    assert t.is_completed() is False
    assert t.is_assigned() is False
    
    t.mark_in_progress()
    assert t.status == "in_progress"
    
    t.mark_done()
    assert t.is_completed() is True
    
    t2 = Task(title="Assigned Task", assigned_to=1)
    assert t2.is_assigned() is True
    
    t3 = Task(title="Cancelled Task", status="cancelled")
    t3.mark_cancelled()
    assert t3.status == "cancelled"


def test_task_status_validation():
    t = Task(title="Test", status="invalid_status")
    assert t.status == "open"  # Defaults to open for invalid status
    
    t2 = Task(title="Test2", status="done")
    assert t2.status == "done"


def test_project_overdue():
    p = Project(title="Overdue Project", due_date="2020-01-01")
    assert p.is_overdue() is True
    
    p2 = Project(title="No Due Date")
    assert p2.is_overdue() is False
    
    p3 = Project(title="Invalid Date", due_date="not-a-date")
    assert p3.is_overdue() is False
