import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import Base, async_session, engine
from app.models import InventoryItem, Member


async def init_tables() -> None:
    """Creates all database tables defined in the models."""
    async with engine.begin() as conn:
        # This reads our Base metadata and builds the tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)


async def seed_mock_data() -> None:
    """Seeds placeholder members and items for local testing."""
    async with async_session() as session:
        session: AsyncSession

        # 1. Check if we already have data to avoid duplicate seeding
        member_check = await session.execute(select(Member).limit(1))
        if member_check.scalar_one_or_none() is not None:
            print("Database already contains data. Skipping seeding.")
            return

        print("Seeding sample members...")
        mock_members: list[Member] = [
            Member(
                first_name="Alice",
                last_name="Smith",
                email="alice@ten.com",
                tier="Premium",
            ),
            Member(
                first_name="Bob",
                last_name="Jones",
                email="bob@ten.com",
                tier="Standard",
            ),
        ]
        session.add_all(mock_members)

        print("Seeding sample inventory...")
        mock_items: list[InventoryItem] = [
            InventoryItem(
                title="Gaston Fine Dining Experience",
                category="Dining",
                description="Michelin-starred tasting menu for two.",
                price=250.00,
                stock=5,
            ),
            InventoryItem(
                title="Exclusive Private Jet Charter Flight",
                category="Travel",
                description="One-way regional private flight voucher.",
                price=1200.00,
                stock=1,  # Low stock to test out-of-stock validation
            ),
        ]
        session.add_all(mock_items)
        await session.commit()


async def main() -> None:
    print("Building database schemas...")
    await init_tables()
    print("Populating testing records...")
    await seed_mock_data()
    print("🚀 Local database setup successfully completed!")


if __name__ == "__main__":
    asyncio.run(main())
