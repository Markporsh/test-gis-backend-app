# FastAPI GeoJSON API

## Описание
Этот проект представляет собой FastAPI-сервис для генерации полигона (GeoJSON) на основе заданной точки и радиуса.
Также реализована кэширование запросов в базе данных PostgreSQL и аутентификация через JWT.
---

## Особенности
- Реализация API для генерации полигона.
- Асинхронная обработка запросов (имитация долгих операций).
- Кэширование запросов в базе данных PostgreSQL.
- Аутентификация через JWT.
- Готов к запуску в Docker.

---

## Запуск проекта

### 1. Требования
Для запуска проекта необходимы:
- Docker
- Docker Compose

### 2. Установка
1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Markporsh/test-gis-backend-app.git
    cd test-gis-backend-app
    ```

2. Создайте файл `.env` в корне проекта и добавьте следующие переменные:
    ```env
    DATABASE_URL=postgresql://postgres:postgres@db:5432/mydatabase
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
### 3. Запуск с помощью Docker Compose
1. Соберите и запустите проект:
    ```bash
    docker-compose up -d --build
    ```
   Или можно воспользоваться командой Makefile:

    ```bash
    make up
    ```

2. Приложение будет доступно по адресу:
    ```
    http://localhost:8000
    ```

3. Остановка контейнеров:
    ```bash
    docker-compose down
    ```
   Или можно воспользоваться командой Makefile:

    ```bash
    make down
    ```

---

## API эндпоинты

### **1. Получение полигона**
**POST** `/circle/`

#### Тело запроса:
```json
{
  "lon": 37.6173,
  "lat": 55.7558,
  "radius": 1000
}
```

### Ответ:
```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [...]
  },
  "properties": {}
}
```

### **2. Создание пользователя**
**POST** `/users/`

#### Тело запроса:
```json

{
  "username": "user1",
  "password": "password123"
}

```

### Ответ:
```json

{
  "id": 1,
  "username": "user1"
}

```

### **3. Аутентификация**

**POST** `/token/`

#### Отправка данных в формате form-data:

```form-data
username=user1
password=password123
```

#### Также можно через curl


```bash
curl -X POST "http://localhost:8000/token/" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=user1&password=password123"
```

### Ответ:

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

### Локальная разработка

## Для локальной разработки без Docker:
	1.	Убедитесь, что Python 3.9 установлен.
	2.	Установите зависимости:

pip install -r requirements.txt

	3.	Установите PostgreSQL и создайте базу данных:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=mydatabase


	4.	Запустите приложение:

uvicorn app.main:app --reload



Дополнительная информация

	•	Документация API автоматически доступна по адресу:
	•	Swagger: http://localhost:8000/docs
