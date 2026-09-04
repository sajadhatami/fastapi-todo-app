from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Base declarative class with audit timestamps."""
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), sort_order=998)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        sort_order=999,
    )