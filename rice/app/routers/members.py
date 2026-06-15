from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_db
from ..models import Member
from ..schemas import MemberResponse

router: APIRouter = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=list[MemberResponse])
async def read_members(db: AsyncSession = Depends(get_db)) -> Sequence[Member]:
    # Pulls all seeded member profiles directly from your SQLite database
    result = await db.execute(select(Member))
    members: Sequence[Member] = result.scalars().all()
    return members
