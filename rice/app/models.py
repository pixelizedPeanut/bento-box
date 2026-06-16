from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BookingStatus(str, Enum):
    """Defines valid lifecycle states for a bento box transaction."""

    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    booking_count: Mapped[int] = mapped_column(Integer, default=0)
    date_joined: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class InventoryItem(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    remaining_count: Mapped[int] = mapped_column(Integer, default=0)
    expiration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    booking_ref: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    member_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("members.id"), nullable=False
    )
    inventory_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("inventory.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    status: Mapped[BookingStatus] = mapped_column(
        SQLEnum(BookingStatus), default=BookingStatus.CONFIRMED, nullable=False
    )
