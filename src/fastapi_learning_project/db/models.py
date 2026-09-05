from datetime import date, datetime
import enum 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, String, Integer, func, DateTime
from .base import Base



class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    PREMIUM = "premium"
    
class TodoPriority(enum.IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    DEFAULT = 0

class TodoType(enum.Enum):
    TASK = "task"
    EVENT = "event"
    REMINDER = "reminder"
    
class TodoStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"



class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    full_name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone_number: Mapped[str | None] = mapped_column(String(11), index=True)
    
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)
    
    # (one) to many relationship with Todos
    todos: Mapped[list["Todos"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Todos(Base):
    __tablename__ = "todos"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column()
    priority: Mapped[TodoPriority] = mapped_column(default=TodoPriority.DEFAULT)
    type: Mapped[TodoType] = mapped_column(default=TodoType.TASK)
    status: Mapped[TodoStatus] = mapped_column(default=TodoStatus.IN_PROGRESS)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    
    # one to (many) relationship with Users
    user: Mapped["Users"] = relationship(back_populates="todos")
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))

    
    
    