import logging
from fastapi import APIRouter, status, Body, Depends
from schemas.review import MarkFilmDto, UpdateMarkFilmDto, LikeDislikeFilmDto
from core.handlers import require_access_token, JwtHandler
from services.film_review import ReviewFilmService, get_film_review_service
from models.review import FilmReview
from uuid import UUID

router = APIRouter(prefix='/reviews', tags=['Film Reviews'])

logger = logging.getLogger().getChild('reviews-router')


@router.post('/film/like', response_model=FilmReview, status_code=status.HTTP_201_CREATED)
async def like_film(
        dto: LikeDislikeFilmDto = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: ReviewFilmService = Depends(get_film_review_service)):
    current_user = await jwt_handler.get_current_user()
    service.dto = MarkFilmDto(film_id=dto.film_id, mark=10)
    return await service.set_like(user=current_user)


@router.post('/film/dislike', response_model=FilmReview, status_code=status.HTTP_201_CREATED)
async def dislike_film(
        dto: LikeDislikeFilmDto = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: ReviewFilmService = Depends(get_film_review_service)):
    current_user = await jwt_handler.get_current_user()
    service.dto = MarkFilmDto(film_id=dto.film_id, mark=0)
    return await service.set_dislike(user=current_user)


@router.delete('/{review_id}', status_code=status.HTTP_200_OK)
async def delete_review(
        review_id: UUID,
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: ReviewFilmService = Depends(get_film_review_service)):
    return await service.delete_review(review_id=review_id)


@router.patch('/{review_id}', status_code=status.HTTP_201_CREATED)
async def update_review(
        review_id: UUID,
        dto: UpdateMarkFilmDto = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: ReviewFilmService = Depends(get_film_review_service)):
    return await service.update_get(data=dto, review_id=review_id)


@router.post('/', status_code=status.HTTP_201_CREATED,  response_model=FilmReview)
async def create_review(
        dto: MarkFilmDto = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: ReviewFilmService = Depends(get_film_review_service)):
    current_user = await jwt_handler.get_current_user()
    service.dto = dto
    return await service.set_review(user=current_user)


@router.get('/{film_id}', status_code=status.HTTP_201_CREATED)
async def get_film_reviews(
        film_id: UUID,
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: ReviewFilmService = Depends(get_film_review_service)):
    return await service.get_film_reviews(film_id=film_id)
