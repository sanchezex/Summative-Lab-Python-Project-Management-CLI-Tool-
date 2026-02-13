from .person import Person


class User(Person):
    """User with projects."""

    _id_counter = 1

    def __init__(self, name: str, email: str | None = None, id: int | None = None, project_ids: list | None = None):
        if id is None:
            self.id = User._id_counter
            User._id_counter += 1
        else:
            self.id = id
            if id >= User._id_counter:
                User._id_counter = id + 1
        super().__init__(name, email)
        self.project_ids = project_ids or []

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"

    def to_dict(self):
        d = super().to_dict()
        d.update({"id": self.id, "project_ids": self.project_ids})
        return d

    @classmethod
    def from_dict(cls, data: dict):
        return cls(name=data.get("name"), email=data.get("email"), id=data.get("id"), project_ids=data.get("project_ids", []))
