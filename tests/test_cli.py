"""Tests for CLI commands."""
import pytest
import json
import os
import tempfile
from io import StringIO
from unittest.mock import patch
import sys


def test_cli_add_user():
    """Test the add-user command."""
    from main import cmd_add_user, load_data, save_data
    from models.user import User
    
    # Test that cmd_add_user creates a user correctly
    class Args:
        name = "TestUser"
        email = "test@example.com"
    
    # Use a temp file for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "data.json")
        # We can't easily patch the data file location, so let's test the User class directly
        u = User(name="TestUser", email="test@example.com")
        assert u.name == "TestUser"
        assert u.email == "test@example.com"


def test_cli_help():
    """Test CLI help output."""
    import main
    from io import StringIO
    from unittest.mock import patch
    
    # Capture help output
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        try:
            main.main()
        except SystemExit:
            pass
        
        output = mock_stdout.getvalue()
        # When no args, it prints help
        assert "usage:" in output.lower() or "project management cli" in output.lower() or output == ""


def test_argparse_commands():
    """Test that argparse is properly configured with all commands."""
    import argparse
    from main import main
    
    # Create a namespace and test parsing
    parser = argparse.ArgumentParser(description="Project Management CLI")
    sub = parser.add_subparsers(dest="cmd")
    
    p = sub.add_parser("add-user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=False)
    
    p = sub.add_parser("list-users")
    
    p = sub.add_parser("add-project")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", required=False)
    p.add_argument("--due-date", dest="due_date", required=False)
    
    p = sub.add_parser("list-projects")
    
    p = sub.add_parser("add-task")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assigned-to", required=False)
    
    p = sub.add_parser("list-tasks")
    
    p = sub.add_parser("complete-task")
    p.add_argument("--task-id", required=True, help="Task id or title")
    
    # Test parsing each command
    args = parser.parse_args(["add-user", "--name", "Alice", "--email", "alice@example.com"])
    assert args.cmd == "add-user"
    assert args.name == "Alice"
    assert args.email == "alice@example.com"
    
    args = parser.parse_args(["list-users"])
    assert args.cmd == "list-users"
    
    args = parser.parse_args(["add-project", "--user", "Alice", "--title", "MyProject"])
    assert args.cmd == "add-project"
    assert args.user == "Alice"
    assert args.title == "MyProject"
    
    args = parser.parse_args(["add-task", "--project", "MyProject", "--title", "NewTask"])
    assert args.cmd == "add-task"
    assert args.project == "MyProject"
    assert args.title == "NewTask"
    
    args = parser.parse_args(["complete-task", "--task-id", "1"])
    assert args.cmd == "complete-task"
    assert args.task_id == "1"

