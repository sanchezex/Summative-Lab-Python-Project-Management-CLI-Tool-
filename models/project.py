class Project:
    """Project model containing tasks and link to owner (user id)."""

    _id_counter = 1

    def __init__(self, title: str, description: str = "", due_date: str | None = None, owner_id: int | None = None, id: int | None = None, task_ids: list | None = None):
        if id is None:
            self.id = Project._id_counter
            Project._id_counter += 1
        else:
            self.id = id
            if id >= Project._id_counter:
                Project._id_counter = id + 1
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id
        self.task_ids = task_ids or []

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title!r})"

    def add_task(self, task_id: int) -> None:
        """Add a task to this project."""
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)

    def remove_task(self, task_id: int) -> bool:
        """Remove a task from this project. Returns True if removed."""
        if task_id in self.task_ids:
            self.task_ids.remove(task_id)
            return True
        return False

    def get_task_count(self) -> int:
        """Get the number of tasks in this project."""
        return len(self.task_ids)

    def is_overdue(self) -> bool:
        """Check if the project is overdue based on due date."""
        if not self.due_date:
            return False
        from datetime import datetime
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
            return datetime.now() > due
        except ValueError:
            return False

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "due_date": self.due_date, "owner_id": self.owner_id, "task_ids": self.task_ids}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(title=data.get("title"), description=data.get("description", ""), due_date=data.get("due_date"), owner_id=data.get("owner_id"), id=data.get("id"), task_ids=data.get("task_ids", []))
