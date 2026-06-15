from datetime import datetime

from pydantic import BaseModel, ConfigDict


# --- Member Schemas ---
class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    tier: str = "Standard"


class MemberCreate(MemberBase):
    pass


class MemberResponse(MemberBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# --- Inventory Schemas ---
class InventoryItemBase(BaseModel):
    title: str
    category: str
    description: str | None = None
    price: float
    stock: int = 0


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemResponse(InventoryItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


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


class CancelRequest(BaseModel):
    booking_ref: str


class CancelResponse(BaseModel):
    message: str
    booking_ref: str
    status: str
