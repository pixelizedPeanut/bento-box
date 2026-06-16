from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import bookings, items, members

app: FastAPI = FastAPI(
    title="🍱 BentoBox Engine",
    description="A lightweight async scheduling core for modular dashboard allocations (and premium sushi ordering).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Read dynamic typed string list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bookings.router)
app.include_router(items.router)
app.include_router(members.router)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Core engine vitality check. Ensures the kitchen is hot and the rice is sticky.
    """
    return {
        "status": "perfectly_cooked",
        "service": "bento-box-rice-v1",
    }
