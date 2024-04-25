# Tests

### Запуск:
```bash
docker-compose -f docker-compose.tests.yaml run test_auth_api poetry run alembic upgrade head
docker-compose -f docker-compose.tests.yaml up --build
```