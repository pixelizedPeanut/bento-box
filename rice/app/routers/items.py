from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_db
from ..models import InventoryItem
from ..schemas import InventoryItemResponse

router: APIRouter = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=list[InventoryItemResponse])
async def read_inventory(db: AsyncSession = Depends(get_db)) -> Sequence[InventoryItem]:
    """
    Fetches the curated menu of luxury services available for booking.
    """
    result = await db.execute(select(InventoryItem))
    return result.scalars().all()
