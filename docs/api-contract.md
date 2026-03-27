# API-контракт SYNQ
## Второй спринт

Текущая версия контракта относится ко `2 спринту` проекта и описывает ядро приложения, аутентификацию и базовый профиль.

## Общая информация

- Base URL: `/api/v1`
- Формат данных: `application/json`
- Авторизация: `Bearer JWT`
- Кодировка: `UTF-8`

## Scope второго спринта

Во втором спринте реализуется базовый пользовательский сценарий:

- регистрация;
- подтверждение email;
- вход;
- выход;
- получение текущего пользователя;
- базовые страницы после авторизации.

Дополнительно в текущей реализации уже есть API для собственного профиля.

## Формат ошибок

Ошибки backend возвращаются в JSON-формате:

```json
{
  "detail": "Текст ошибки"
}
```

При невалидном теле запроса FastAPI возвращает `422 Unprocessable Entity`.

## Endpoints

### POST `/auth/registry`

Начинает регистрацию пользователя.

#### Request body

```json
{
  "email": "user@example.com",
  "username": "devuser",
  "password": "StrongPassword123"
}
```

#### Response `200 OK`

```json
true
```

#### Ошибки

- `409 Conflict` - email уже занят

```json
{
  "detail": "Аккаунт с таким email уже существует"
}
```

- `409 Conflict` - username уже занят

```json
{
  "detail": "Аккаунт с таким username уже существует"
}
```

### POST `/auth/confirm_email`

Подтверждает email кодом из письма. После успешного подтверждения создаются пользователь и профиль.

#### Request body

```json
{
  "email": "user@example.com",
  "code": 123456
}
```

#### Response `200 OK`

```json
true
```

#### Ошибки

- `400 Bad Request` - код неверный

```json
{
  "detail": "Неверный код подтверждения"
}
```

- `409 Conflict` - email уже существует

```json
{
  "detail": "Аккаунт с таким email уже существует"
}
```

### POST `/auth/login`

Выполняет вход пользователя и возвращает токены.

#### Request body

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

#### Response `200 OK`

```json
{
  "access_token": "jwt-access-token",
  "refresh_token": "jwt-refresh-token",
  "token_type": "Bearer",
  "expires_in": 900
}
```

#### Ошибки

- `400 Bad Request`

```json
{
  "detail": "Не существует аккаунта с таким email"
}
```

- `400 Bad Request`

```json
{
  "detail": "Неверный email или пароль"
}
```

- `403 Forbidden`

```json
{
  "detail": "Аккаунт деактивирован"
}
```

### GET `/auth/me`

Возвращает текущего авторизованного пользователя.

#### Headers

```http
Authorization: Bearer <access_token>
```

#### Response `200 OK`

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "devuser"
}
```

#### Ошибки

- `401 Unauthorized`

```json
{
  "detail": "Токен отсутствует или недействителен"
}
```

### POST `/auth/logout`

Проверяет токен и завершает logout-flow.

#### Headers

```http
Authorization: Bearer <access_token>
```

#### Response `204 No Content`

Тело ответа отсутствует.

#### Ошибки

- `401 Unauthorized`

```json
{
  "detail": "Токен отсутствует или недействителен"
}
```

### GET `/profile/me`

Возвращает профиль текущего пользователя.

#### Headers

```http
Authorization: Bearer <access_token>
```

#### Response `200 OK`

```json
{
  "id": 1,
  "user_id": 1,
  "uuid": "c2b7b6f2-1b3b-4b13-9c0a-7c3e9f44c001",
  "full_name": "Иван Петров",
  "bio": "Backend developer"
}
```

Поля `full_name` и `bio` могут быть `null`.

#### Ошибки

- `401 Unauthorized`

```json
{
  "detail": "Токен отсутствует или недействителен"
}
```

- `404 Not Found`

```json
{
  "detail": "Профиль не найден"
}
```

### PUT `/profile/me`

Обновляет профиль текущего пользователя.

#### Headers

```http
Authorization: Bearer <access_token>
```

#### Request body

```json
{
  "full_name": "Иван Петров",
  "bio": "Backend developer"
}
```

Оба поля могут быть `null`.

#### Response `200 OK`

```json
{
  "id": 1,
  "user_id": 1,
  "uuid": "c2b7b6f2-1b3b-4b13-9c0a-7c3e9f44c001",
  "full_name": "Иван Петров",
  "bio": "Backend developer"
}
```

#### Ошибки

- `401 Unauthorized`

```json
{
  "detail": "Токен отсутствует или недействителен"
}
```

- `404 Not Found`

```json
{
  "detail": "Профиль не найден"
}
```
