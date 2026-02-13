class Task:
    """Task model linked to a project and optionally assigned to a user."""

    _id_counter = 1

    def __init__(self, title: str, status: str = "open", assigned_to: int | None = None, project_id: int | None = None, id: int | None = None):
        if id is None:
            self.id = Task._id_counter
            Task._id_counter += 1
        else:
            self.id = id
            if id >= Task._id_counter:
                Task._id_counter = id + 1
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        self.project_id = project_id

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, status={self.status})"

    def to_dict(self):
        return {"id": self.id, "title": self.title, "status": self.status, "assigned_to": self.assigned_to, "project_id": self.project_id}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(title=data.get("title"), status=data.get("status", "open"), assigned_to=data.get("assigned_to"), project_id=data.get("project_id"), id=data.get("id"))
