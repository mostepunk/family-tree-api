from fastapi import APIRouter

root_router = APIRouter()


@root_router.get(
    "/",
    summary="Test root",
    tags=["root"],
    # response_model=ReceiptList,
)
async def get_receipt():
    """Эта ручка не проверялась, и, вероятнее всего не работает!"""
    return {"answer": "I am Root"}
