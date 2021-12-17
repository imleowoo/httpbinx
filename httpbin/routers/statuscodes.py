from fastapi import APIRouter

router = APIRouter()


@router.route('/status/{code}', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE"])
async def status_code(code):
    pass
