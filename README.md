# Проектная работа 10 спринта
link to git -> https://github.com/KseniiaKarpova/notifications_sprint_1

## Запуск проекта:
```bash

docker-compose -f docker-compose.main.yaml -f docker-compose.db.yaml -f docker-compose.elk.yaml up --build
```

## Описание проекта:
Чекпоинт для создания шаблона сообщения (template), емайл\сокет рассылка и логирование и получение истории уведомлений (history) находится в сервисе Worker