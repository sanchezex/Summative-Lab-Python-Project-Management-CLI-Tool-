class Task:
    """Task model linked to a project and optionally assigned to a user."""

    _id_counter = 1

    # Task status constants
    STATUS_OPEN = "open"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_CANCELLED = "cancelled"

    VALID_STATUSES = [STATUS_OPEN, STATUS_IN_PROGRESS, STATUS_DONE, STATUS_CANCELLED]

    def __init__(self, title: str, status: str = "open", assigned_to: int | None = None, project_id: int | None = None, id: int | None = None):
        if id is None:
            self.id = Task._id_counter
            Task._id_counter += 1
        else:
            self.id = id
            if id >= Task._id_counter:
                Task._id_counter = id + 1
        self.title = title
        self.status = status if status in self.VALID_STATUSES else self.STATUS_OPEN
        self.assigned_to = assigned_to
        self.project_id = project_id

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, status={self.status})"

    def mark_in_progress(self) -> None:
        """Mark task as in progress."""
        self.status = self.STATUS_IN_PROGRESS

    def mark_done(self) -> None:
        """Mark task as done."""
        self.status = self.STATUS_DONE

    def mark_cancelled(self) -> None:
        """Mark task as cancelled."""
        self.status = self.STATUS_CANCELLED

    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == self.STATUS_DONE

    def is_assigned(self) -> bool:
        """Check if task is assigned to someone."""
        return self.assigned_to is not None

    def to_dict(self):
        return {"id": self.id, "title": self.title, "status": self.status, "assigned_to": self.assigned_to, "project_id": self.project_id}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(title=data.get("title"), status=data.get("status", "open"), assigned_to=data.get("assigned_to"), project_id=data.get("project_id"), id=data.get("id"))
