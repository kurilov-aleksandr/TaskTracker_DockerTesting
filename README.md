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

## CI

GitHub Actions запускает тесты и проверяет сборку Docker-образа для pull
request в `master`. При успешном push в `master` workflow также публикует образ
в GitHub Container Registry (GHCR) с тегами `latest` и commit SHA.

Образ доступен по адресу `ghcr.io/<owner>/<repository>`. Для скачивания:

```sh
docker pull ghcr.io/<owner>/<repository>:latest
```

Для приватного образа перед скачиванием выполните вход в GHCR с GitHub Personal
Access Token, которому выдано право `read:packages`. Публикация выполняется
через `GITHUB_TOKEN` workflow и не требует добавления отдельного секрета.
