# Благотворительный фонд поддержки котиков - QRKot

## О проекте
Асинхронное приложение на FastAPI для управления благотворительными проектами и пожертвованиями.  
Пользователи могут делать пожертвования, а суперпользователи — создавать и редактировать проекты.  
Все средства автоматически распределяются между открытыми проектами.

## Возможности
- Регистрация и аутентификация пользователей (JWT).
- Управление проектами (CRUD, доступно только суперпользователям).
- Создание пожертвований (для авторизованных пользователей).
- Автоматическое распределение пожертвований по проектам.
- Swagger-документация доступна по адресу `/docs`.


## Интеграция с Google Spreadsheets
В проекте присутствует возможность формировать отчёт о закрытых благотворительных проектах в виде таблицы Google Sheets.

### Что делает интеграция

Создаёт новую Google-таблицу с названием вида
«Отчёт на 06.11.2025 18:30:00».

В таблицу автоматически добавляются все закрытые проекты, отсортированные по скорости сбора средств.

Для каждого проекта указываются:
– название проекта,
– время затраченное на сбор,
– описание проекта.

Суперпользователю выдаются права редактирования на созданный документ.


## Используемый стек
```
Python 3.10+
FastAPI
Pydantic
SQLAlchemy (async)
Alembic
Uvicorn
FastAPI Users
Aiogoogle
Google-auth
Pytest
Flake8
```

## Установка

1. Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone git@github.com:abramov-v/cat_charity_fund.git
cd cat_charity_fund
```

2. Создайте и активируйте виртуальное окружение:
   
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4.  Настройте переменные окружения:

Скопируйте файл `.env.example` и создайте на его основе `.env`:

```bash
cp .env.example .env
```

Пример содержимого .env:

```env
# Настройки приложения
QRKOT_APP_TITLE=Благотворительный фонд поддержки котиков - QRKot
QRKOT_APP_DESC=Приложение для управления благотворительными проектами
QRKOT_DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
QRKOT_SECRET=your_super_secret_key_here
QRKOT_FIRST_SUPERUSER_EMAIL=admin@example.com
QRKOT_FIRST_SUPERUSER_PASSWORD=your_strong_password_here

# Настройки Google cloud сервиса
QRKOT_TYPE=Укажите_тип_из_JSON_файла_сервисного_аккаунта
QRKOT_PROJECT_ID=Укажите_ID_вашего_проекта_в_Google_Cloud
QRKOT_PRIVATE_KEY_ID=Укажите_PRIVATE_KEY_ID_из_JSON
QRKOT_PRIVATE_KEY=Укажите_PRIVATE_KEY_из_JSON
QRKOT_CLIENT_EMAIL=Укажите_CLIENT_EMAIL_из_JSON
QRKOT_CLIENT_ID=Укажите_CLIENT_ID_из_JSON
QRKOT_AUTH_URI=Укажите_AUTH_URI_из_JSON
QRKOT_TOKEN_URI=Укажите_TOKEN_URI_из_JSON
QRKOT_AUTH_PROVIDER_X509_CERT_URL=Укажите_AUTH_PROVIDER_X509_CERT_URL_из_JSON
QRKOT_CLIENT_X509_CERT_URL=Укажите_CLIENT_X509_CERT_URL_из_JSON
QRKOT_EMAIL=Укажите_ваш_личный_или_проектный_email
```

5. Инициализируйте базу данных и выполните миграции:

```bash
alembic upgrade head
```

Если вы вносите изменения в модели и хотите создать новую миграцию, выполните:

```bash
alembic revision --autogenerate -m "Комментарий к миграции"
alembic upgrade head
```

6. Запустите приложение:

```bash
uvicorn app.main:app --reload
```

После запуска приложение будет доступно по адресам:

Swagger UI: `http://127.0.0.1:8000/docs`
ReDoc: `http://127.0.0.1:8000/redoc`


## Примеры запросов к API 
Подробные варианты запросов и ошибок описаны в [`openapi.yml`](./openapi.yml).  
Ниже приведены базовые примеры.


### Аутентификация

**Логин (получение JWT):**

```http
POST /auth/jwt/login
Content-Type: application/x-www-form-urlencoded
```

`username=admin@example.com&password=secret`

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJh...",
  "token_type": "bearer"
}
```

**Регистрация нового пользователя**

```http
POST /auth/register
Content-Type: application/json
```

```json
{
  "email": "user@example.com",
  "password": "123456"
}
```

### Работа с проектами


**Получить все проекты:**

```http
GET /charity_project/
```

```json
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 500,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2019-08-24T14:15:22Z",
    "close_date": "2019-08-24T14:15:22Z"
  }
]
```

**Создать проект (только суперпользователь):**

```http
POST /charity_project/
Authorization: Bearer <token>
Content-Type: application/json
```

Тело запроса:

```json
{
  "name": "string",
  "description": "string",
  "full_amount": 0
}
```

Тело ответа:

```json
{
  "name": "string",
  "description": "string",
  "full_amount": 0,
  "id": 0,
  "invested_amount": 0,
  "fully_invested": true,
  "create_date": "2019-08-24T14:15:22Z",
  "close_date": "2019-08-24T14:15:22Z"
}
```

### Работа с пожертвованиями

**Сделать пожертвование:**

```http
POST /donation/
Authorization: Bearer <token>
Content-Type: application/json
```

Тело запроса:

```json
{
  "full_amount": 500,
  "comment": "На корм котикам"
}
```

Тело ответа:

```json
{
  "full_amount": 500,
  "comment": "На корм котикам",
  "id": 0,
  "create_date": "2019-08-24T14:15:22Z"
}
```

**Посмотреть мои пожертвования:**

```http
GET /donation/my
Authorization: Bearer <token>
```

Тело ответа:

```json
[
  {
    "full_amount": 500,
    "comment": "На корм котикам",
    "id": 1,
    "create_date": "2025-09-07T10:05:00Z"
  }
]
```

**Создать отчёт в Google Sheets:**

```http
POST /google/
Authorization: Bearer <token>
```

Тело ответа:

```json
[
  {
    "id": 1,
    "name": "Помощь Мурзику",
    "description": "Сбор средств на операцию коту Мурзику",
    "full_amount": 1000,
    "invested_amount": 1000,
    "fully_invested": true,
    "create_date": "2025-09-01T10:00:00Z",
    "close_date": "2025-09-05T15:30:00Z"
  }
]
```

После выполнения запроса создаётся Google-таблица с отчётом, содержащая закрытые проекты, отсортированные по скорости сбора средств.
Ссылка на созданную таблицу будет доступна в Google Диске сервисного аккаунта, а суперпользователь получит права на редактирование.


## Автор
**Валерий Абрамов**
- GitHub: [@abramov-v](https://github.com/abramov-v)
