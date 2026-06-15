import asyncio
import csv
import os
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import Base, async_session, engine
from app.models import InventoryItem, Member

MEMBERS_CSV_PATH = os.path.join("data", "members.csv")
INVENTORY_CSV_PATH = os.path.join("data", "inventory.csv")


async def init_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_from_csv() -> None:
    async with async_session() as session:
        session: AsyncSession

        # 1. Parse & Load Members
        member_check = await session.execute(select(Member).limit(1))
        if member_check.scalar_one_or_none() is not None:
            print("Database already contains member data. Skipping import.")
        else:
            print(f"📖 Parsing {MEMBERS_CSV_PATH}...")
            # Using 'utf-8-sig' automatically strips hidden Excel BOM characters (\ufeff)
            with open(MEMBERS_CSV_PATH, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)

                # Clean up any stray whitespaces around the column names themselves!
                if reader.fieldnames:
                    reader.fieldnames = [header.strip() for header in reader.fieldnames]

                members_to_add = []
                for row in reader:
                    members_to_add.append(
                        Member(
                            name=row["name"].strip(),
                            surname=row["surname"].strip(),
                            booking_count=int(row["booking_count"]),
                            date_joined=datetime.fromisoformat(
                                row["date_joined"].strip()
                            ),
                        )
                    )
                session.add_all(members_to_add)
                print(f"✅ Staged {len(members_to_add)} cleaned member records.")

        # 2. Parse & Load Inventory Items
        inventory_check = await session.execute(select(InventoryItem).limit(1))
        if inventory_check.scalar_one_or_none() is not None:
            print("Database already contains inventory data. Skipping import.")
        else:
            print(f"📖 Parsing {INVENTORY_CSV_PATH}...")
            with open(INVENTORY_CSV_PATH, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)

                # Clean up any stray whitespaces around the inventory column names
                if reader.fieldnames:
                    reader.fieldnames = [header.strip() for header in reader.fieldnames]

                items_to_add = []
                for row in reader:
                    exp_date = datetime.strptime(
                        row["expiration_date"].strip(), "%d/%m/%Y"
                    )
                    items_to_add.append(
                        InventoryItem(
                            title=row["title"].strip(),
                            description=row["description"].strip(),
                            remaining_count=int(row["remaining_count"]),
                            expiration_date=exp_date,
                        )
                    )
                session.add_all(items_to_add)
                print(f"✅ Staged {len(items_to_add)} cleaned inventory items.")

        await session.commit()


async def main() -> None:
    await init_tables()
    await seed_from_csv()
    print("🚀 Database matching layout fully configured and seeded!")


if __name__ == "__main__":
    asyncio.run(main())
