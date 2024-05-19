from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import db

class Project(db.Model):
    container_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    container_name: Mapped[str] = mapped_column(unique=True)
    full_path: Mapped[str] = mapped_column()

class User(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True)

