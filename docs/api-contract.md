# API-Контракт — 2 Спринт

## 1. Общая информация

- **API Prefix:** `/api/v1`
- **Формат обмена данными:** `application/json`
- **Аутентификация:** `Bearer JWT`
- **Кодировка:** `UTF-8`

Во 2 спринте реализуется базовая система аутентификации платформы. API-контракт охватывает только регистрацию, вход, выход и получение данных текущего пользователя.

## 2. Формат ошибок

Все ошибки возвращаются в JSON-формате:

```json
{
  "detail": "Error message"
}
```

### Основные коды ошибок
- `400 Bad Request` — невалидные входные данные
- `401 Unauthorized` — пользователь не авторизован или передан неверный токен
- `409 Conflict` — пользователь с таким email или username уже существует
- `500 Internal Server Error` — внутренняя ошибка сервера

## 3. Endpoints

---

## 3.1. Регистрация пользователя

### `POST /auth/register`

**Назначение:**
Создание нового пользователя в системе.

**Доступ:**
Публичный endpoint.

### Request Body

```json
{
  "email": "user@example.com",
  "username": "devuser",
  "password": "StrongPassword123"
}
```

### Правила валидации
- `email` — обязательное поле, должен быть валидным email-адресом
- `username` — обязательное поле, уникальное
- `password` — обязательное поле, не должно быть пустым

### Response 201 Created

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "devuser"
  },
  "profile": {
    "id": 1,
    "uuid": "c2b7b6f2-1b3b-4b13-9c0a-7c3e9f44c001"
  }
}
```

### Ошибки
- `400 Bad Request` — невалидные данные
- `409 Conflict` — email или username уже заняты

---

## 3.2. Вход пользователя

### `POST /auth/login`

**Назначение:**
Аутентификация пользователя и выдача JWT access token.

**Доступ:**
Публичный endpoint.

### Request Body

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

### Response 200 OK

```json
{
  "accessToken": "jwt-access-token",
  "tokenType": "Bearer"
}
```

### Ошибки
- `400 Bad Request` — невалидный формат запроса
- `401 Unauthorized` — неверный email или пароль

---

## 3.3. Выход пользователя

### `POST /auth/logout`

**Назначение:**
Выход пользователя из системы.

**Доступ:**
Только для авторизованного пользователя.

### Headers

```http
Authorization: Bearer <accessToken>
```

### Request Body

```json
{}
```

### Response 204 No Content

Тело ответа отсутствует.

### Ошибки
- `401 Unauthorized` — токен отсутствует или недействителен

**Примечание:**
Если logout реализуется на стороне клиента через удаление токена, endpoint всё равно фиксируется в контракте как часть auth-flow.

---

## 3.4. Получение текущего пользователя

### `GET /auth/me`

**Назначение:**
Получение данных текущего авторизованного пользователя.

**Доступ:**
Только для авторизованного пользователя.

### Headers

```http
Authorization: Bearer <accessToken>
```

### Response 200 OK

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "devuser",
  "profile": {
    "id": 1,
    "uuid": "c2b7b6f2-1b3b-4b13-9c0a-7c3e9f44c001"
  }
}
```

### Ошибки
- `401 Unauthorized` — токен отсутствует или недействителен

---

## 4. Итоговый scope 2 Спринта

В API-контракт 2 спринта входят только:
- регистрация пользователя;
- вход пользователя;
- выход пользователя;
- получение текущего пользователя.
