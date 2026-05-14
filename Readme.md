# Student Grades Analytics Service

Сервис для загрузки и анализа успеваемости студентов.

## Запуск

```bash
docker-compose up --build
```

Сервис будет доступен: `http://localhost:8000`

## API

### POST /upload-grades
Загрузка CSV с оценками

```bash
curl -X POST http://localhost:8000/upload-grades -F "file=@grades.csv"
```

Формат CSV:
```csv
full_name,grade
Иванов Иван,5
Петров Петр,3
```

Ответ:
```json
{
    "status": "ok",
    "records_loaded": 100,
    "students": 25
}
```

### GET /students/more-than-3-twos
Студенты с количеством двоек больше 3

```bash
curl http://localhost:8000/students/more-than-3-twos
```

Ответ:
```json
[
    {"full_name": "Иванов Иван", "count_twos": 5}
]
```

### GET /students/less-than-5-twos
Студенты с количеством двоек меньше 5

```bash
curl http://localhost:8000/students/less-than-5-twos
```

Ответ:
```json
[
    {"full_name": "Иванов Иван", "count_twos": 4}
]
```

### GET /health
Проверка работоспособности

```bash
curl http://localhost:8000/health
```

Ответ:
```json
{"status": "ok"}
```

## Остановка

```bash
docker-compose up --build
```