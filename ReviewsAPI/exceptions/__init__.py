from fastapi import HTTPException, status

unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")

wrong_data = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="wrong data")

server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")

forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")

token_expired = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Token expired")

already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Data already exists")

deleted = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="the record deleted")
