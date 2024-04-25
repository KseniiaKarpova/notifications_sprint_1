import logging
from fastapi import APIRouter, status, Body, Depends
from schemas.review import MarkReviewDto, UpdateMarkReviewDto
from core.handlers import require_access_token, JwtHandler
from services.mark_review import MarkReviewService, get_mark_review_service
from models.review import ReviewMark
from uuid import UUID

router = APIRouter(prefix='/review_mark', tags=['Reviews Marks'])

logger = logging.getLogger().getChild('reviews-router')


@router.delete('/{review_mark_id}', status_code=status.HTTP_200_OK)
async def _delete_review_mark(
        review_mark_id: UUID,
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: MarkReviewService = Depends(get_mark_review_service)):
    return await service.delete_review_mark(review_mark_id=review_mark_id)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=ReviewMark)
async def _create_review_mark(
        dto: MarkReviewDto = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: MarkReviewService = Depends(get_mark_review_service)):
    current_user = await jwt_handler.get_current_user()
    service.dto = dto
    return await service.create_review_mark(user=current_user)


@router.patch('/{review_mark_id}', status_code=status.HTTP_201_CREATED, response_model=ReviewMark)
async def _update_review_mark(
        review_mark_id: UUID,
        dto: UpdateMarkReviewDto = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: MarkReviewService = Depends(get_mark_review_service)):
    await jwt_handler.get_current_user()
    return await service.update_get(review_mark_id=review_mark_id, data=dto)
