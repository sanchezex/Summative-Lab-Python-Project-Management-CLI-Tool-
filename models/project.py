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

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "due_date": self.due_date, "owner_id": self.owner_id, "task_ids": self.task_ids}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(title=data.get("title"), description=data.get("description", ""), due_date=data.get("due_date"), owner_id=data.get("owner_id"), id=data.get("id"), task_ids=data.get("task_ids", []))
