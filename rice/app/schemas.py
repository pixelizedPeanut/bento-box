from datetime import datetime

from pydantic import BaseModel, ConfigDict


# --- Member Schemas ---
class MemberBase(BaseModel):
    name: str
    surname: str
    booking_count: int
    date_joined: datetime


class MemberResponse(MemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Inventory Schemas ---
class InventoryItemBase(BaseModel):
    title: str
    description: str
    remaining_count: int
    expiration_date: datetime


# 💡 ADDED: Your items.py router needs this blueprint to handle POST requests!
class InventoryItemCreate(InventoryItemBase):
    pass


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
    status: str

    model_config = ConfigDict(from_attributes=True)


# --- Cancellation Schemas ---
class CancelRequest(BaseModel):
    booking_ref: str


class CancelResponse(BaseModel):
    message: str
    booking_ref: str
    status: str
