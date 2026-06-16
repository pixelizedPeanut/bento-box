from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import BookingStatus


# --- Member Schemas ---
class MemberBase(BaseModel):
    name: str
    surname: str
    booking_count: int = Field(ge=0, description="Cannot be negative")
    date_joined: datetime


class MemberResponse(MemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Inventory Schemas ---
class InventoryItemBase(BaseModel):
    title: str
    description: str
    remaining_count: int = Field(ge=0, description="Available stock pool")
    expiration_date: datetime


class InventoryItemResponse(InventoryItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Booking Schemas ---
class BookingRequest(BaseModel):
    member_id: int
    inventory_id: int


class BookingResponse(BaseModel):
    booking_ref: str
    member_id: int
    inventory_id: int
    created_at: datetime
    status: BookingStatus

    model_config = ConfigDict(from_attributes=True)


# --- Cancellation Schemas ---
class CancelRequest(BaseModel):
    booking_ref: str


class CancelResponse(BaseModel):
    message: str
    booking_ref: str
    status: BookingStatus
