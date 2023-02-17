from fastapi import APIRouter, Depends

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}, 404: {"description": "Not found"}},
)
