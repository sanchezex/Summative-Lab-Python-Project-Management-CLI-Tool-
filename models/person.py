class Person:
    """Base person class."""

    def __init__(self, name: str, email: str | None = None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Person(name={self.name!r}, email={self.email!r})"

    def to_dict(self):
        return {"name": self.name, "email": self.email}
