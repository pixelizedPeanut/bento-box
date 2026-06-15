from typing import Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_db
from ..models import InventoryItem
from ..schemas import InventoryItemCreate, InventoryItemResponse

router: APIRouter = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=list[InventoryItemResponse])
async def read_inventory(db: AsyncSession = Depends(get_db)) -> Sequence[InventoryItem]:
    result = await db.execute(select(InventoryItem))
    items: Sequence[InventoryItem] = result.scalars().all()
    return items


@router.post(
    "/", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED
)
async def create_item(
    item_in: InventoryItemCreate, db: AsyncSession = Depends(get_db)
) -> InventoryItem:
    new_item: InventoryItem = InventoryItem(**item_in.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item
