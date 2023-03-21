from .connect_db import ma


class user_schema(ma.Schema):
    class Meta:
        fields = ("id", "email", "first_name", "last_name", "address", "role_id")


class list_schema(ma.Schema):
    class Meta:
        fields = ("name", "description")


class todo_schema(ma.Schema):
    class Meta:
        fields = ("title", "description", "due_date", "status")
        # fields = ("title", "description")
        # fields = ("name", "description")
