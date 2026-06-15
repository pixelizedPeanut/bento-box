import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..config import settings
from ..database import get_db
from ..models import Booking, InventoryItem, Member
from ..schemas import BookingRequest, BookingResponse, CancelRequest, CancelResponse

router: APIRouter = APIRouter(tags=["Bookings"])


@router.post(
    "/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED
)
async def book_item(
    payload: BookingRequest, db: AsyncSession = Depends(get_db)
) -> Booking:
    # 1. Verify Member Exists
    member_result = await db.execute(
        select(Member).where(Member.id == payload.member_id)
    )
    member: Member | None = member_result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # 2. Constraint: Check if member reached MAX_BOOKINGS (only counting active "CONFIRMED" bookings)
    bookings_count_result = await db.execute(
        select(func.count(Booking.id))
        .where(Booking.member_id == payload.member_id)
        .where(Booking.status == "CONFIRMED")
    )
    active_bookings: int = bookings_count_result.scalar() or 0
    if active_bookings >= settings.MAX_BOOKINGS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Booking limit reached. Maximum active bookings allowed: {settings.MAX_BOOKINGS}",
        )

    # 3. Verify Inventory Item Exists
    item_result = await db.execute(
        select(InventoryItem).where(InventoryItem.id == payload.inventory_id)
    )
    item: InventoryItem | None = item_result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    # 4. Constraint: Check item remaining_count (swapped from stock)
    if item.remaining_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Item is out of stock"
        )

    # 5. Execute: Deduct from remaining_count and generate unique reference string
    item.remaining_count -= 1
    generated_ref: str = f"BBOX-{uuid.uuid4().hex[:8].upper()}"

    # 6. Record the booking
    new_booking: Booking = Booking(
        booking_ref=generated_ref,
        member_id=payload.member_id,
        inventory_id=payload.inventory_id,
        status="CONFIRMED",
    )

    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

    return new_booking


@router.post("/cancel", response_model=CancelResponse)
async def cancel_booking(
    payload: CancelRequest, db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    # 1. Locate the active booking
    booking_result = await db.execute(
        select(Booking).where(Booking.booking_ref == payload.booking_ref)
    )
    booking: Booking | None = booking_result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking reference not found")

    if booking.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")

    # 2. Update booking status
    booking.status = "CANCELLED"

    # 3. Restock the inventory item (swapped from stock)
    item_result = await db.execute(
        select(InventoryItem).where(InventoryItem.id == booking.inventory_id)
    )
    item: InventoryItem | None = item_result.scalar_one_or_none()
    if item:
        item.remaining_count += 1

    await db.commit()

    return {
        "message": "Booking successfully cancelled",
        "booking_ref": booking.booking_ref,
        "status": booking.status,
    }
