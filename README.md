# Task Tracker

## Запуск в Docker

Запустите приложение:

```sh
docker compose up --build -d
```

Откройте <http://localhost:8000>.

SQLite-база хранится в Docker volume `task_data`, поэтому данные сохраняются
при пересоздании контейнера.

Запустите тесты:

```sh
docker compose run --rm test
```

Остановите приложение:

```sh
docker compose down
```

`docker compose down` сохраняет базу. Чтобы также удалить сохраненные данные:

```sh
docker compose down --volumes
```
