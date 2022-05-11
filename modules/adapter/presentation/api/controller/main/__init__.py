from fastapi import APIRouter

main_router = APIRouter()


@main_router.get(
    path="/",
)
async def index():
    return "This is Antgirl"
