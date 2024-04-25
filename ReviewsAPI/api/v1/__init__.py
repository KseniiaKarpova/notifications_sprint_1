from fastapi import APIRouter

from api.v1.review import router as film_review_router
from api.v1.film_mark import router as review_mark_router


v1_router = APIRouter(prefix='/v1')

v1_router.include_router(film_review_router)
v1_router.include_router(review_mark_router)
