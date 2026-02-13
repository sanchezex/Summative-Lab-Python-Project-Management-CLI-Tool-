import argparse
from utils.storage import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task
from rich.table import Table
from rich.console import Console

console = Console()


def build_objects(data):
    users = [User.from_dict(u) for u in data.get("users", [])]
    projects = [Project.from_dict(p) for p in data.get("projects", [])]
    tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
    return users, projects, tasks


def persist_all(users, projects, tasks):
    data = {
        "users": [u.to_dict() for u in users],
        "projects": [p.to_dict() for p in projects],
        "tasks": [t.to_dict() for t in tasks],
    }
    save_data(data)


def find_user(users, name):
    for u in users:
        if u.name == name:
            return u
    return None


def find_project(projects, title):
    for p in projects:
        if p.title == title:
            return p
    return None


def cmd_add_user(args):
    data = load_data()
    users, projects, tasks = build_objects(data)
    if find_user(users, args.name):
        console.print(f"User '{args.name}' already exists")
        return
    user = User(name=args.name, email=args.email)
    users.append(user)
    persist_all(users, projects, tasks)
    console.print(f"Added user: {user}")


def cmd_list_users(args):
    data = load_data()
    users, projects, tasks = build_objects(data)
    table = Table(title="Users")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Email")
    for u in users:
        table.add_row(str(u.id), u.name, u.email or "")
    console.print(table)


def cmd_add_project(args):
    data = load_data()
    users, projects, tasks = build_objects(data)
    owner = find_user(users, args.user)
    if not owner:
        console.print(f"User '{args.user}' not found")
        return
    if find_project(projects, args.title):
        console.print(f"Project '{args.title}' already exists")
        return
    proj = Project(title=args.title, description=args.description or "", due_date=args.due_date, owner_id=owner.id)
    projects.append(proj)
    owner.project_ids.append(proj.id)
    persist_all(users, projects, tasks)
    console.print(f"Added project: {proj}")


def cmd_list_projects(args):
    data = load_data()
    users, projects, tasks = build_objects(data)
    table = Table(title="Projects")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Owner")
    table.add_column("Due Date")
    for p in projects:
        owner = next((u for u in users if u.id == p.owner_id), None)
        owner_name = owner.name if owner else "(unknown)"
        table.add_row(str(p.id), p.title, owner_name, p.due_date or "")
    console.print(table)


def cmd_add_task(args):
    data = load_data()
    users, projects, tasks = build_objects(data)
    proj = find_project(projects, args.project)
    if not proj:
        console.print(f"Project '{args.project}' not found")
        return
    assignee = find_user(users, args.assigned_to) if args.assigned_to else None
    task = Task(title=args.title, status="open", assigned_to=(assignee.id if assignee else None), project_id=proj.id)
    tasks.append(task)
    proj.task_ids.append(task.id)
    persist_all(users, projects, tasks)
    console.print(f"Added task: {task}")


def cmd_list_tasks(args):
    data = load_data()
    users, projects, tasks = build_objects(data)
    table = Table(title="Tasks")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Project")
    table.add_column("Status")
    table.add_column("Assigned To")
    for t in tasks:
        proj = next((p for p in projects if p.id == t.project_id), None)
        proj_title = proj.title if proj else "(unknown)"
        assignee = next((u for u in users if u.id == t.assigned_to), None)
        assignee_name = assignee.name if assignee else ""
        table.add_row(str(t.id), t.title, proj_title, t.status, assignee_name)
    console.print(table)


def cmd_complete_task(args):
    data = load_data()
    users, projects, tasks = build_objects(data)
    t = next((x for x in tasks if str(x.id) == args.task_id or x.title == args.task_id), None)
    if not t:
        console.print(f"Task '{args.task_id}' not found")
        return
    t.status = "done"
    persist_all(users, projects, tasks)
    console.print(f"Marked task complete: {t}")


def main():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("add-user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=False)
    p.set_defaults(func=cmd_add_user)

    p = sub.add_parser("list-users")
    p.set_defaults(func=cmd_list_users)

    p = sub.add_parser("add-project")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", required=False)
    p.add_argument("--due-date", dest="due_date", required=False)
    p.set_defaults(func=cmd_add_project)

    p = sub.add_parser("list-projects")
    p.set_defaults(func=cmd_list_projects)

    p = sub.add_parser("add-task")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assigned-to", required=False)
    p.set_defaults(func=cmd_add_task)

    p = sub.add_parser("list-tasks")
    p.set_defaults(func=cmd_list_tasks)

    p = sub.add_parser("complete-task")
    p.add_argument("--task-id", required=True, help="Task id or title")
    p.set_defaults(func=cmd_complete_task)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
