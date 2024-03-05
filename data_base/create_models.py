from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func, String, Text, ForeignKey, BigInteger, JSON


class Base(DeclarativeBase):
    create_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class Requests(Base):
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50))
    name_parent: Mapped[str] = mapped_column(String(50))
    name_student: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(50))
    file: Mapped[list] = mapped_column(JSON, nullable=True)
    # type_file: Mapped[str] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(15))
    contractor: Mapped[int] = mapped_column(
        ForeignKey("employees.user_id", ondelete="CASCADE"),
        nullable=True
    )


class Employees(Base):
    __tablename__ = 'employees'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(10))
