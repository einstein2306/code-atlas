from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ProgrammingLanguages(Base):
    __tablename__ = "programming_languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    creator: Mapped[str] = mapped_column(String(150))
    year: Mapped[int] = mapped_column()
    paradigm: Mapped[str] = mapped_column(String(100))
