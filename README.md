# Ticket Microservices

### Quick start

Prerequisite: running docker

To build and up microservices:
```bash
make update
```

### Компоненты

1. **Микросервис авторизации (`auth_service`)**
   - Отвечает за регистрацию пользователей, аутентификацию и управление сессиями.

2. **Микросервис заказов (`order_service`)**
   - Отвечает за обработку заказов на билеты, включая создание, обновление статусов и получение заказов.


### Базы данных

- **auth_db.db** (Используется Auth Service)
  - `user`: Содержит информацию о пользователях.
  - `session`: Содержит информацию о сессиях пользователей.

- **order_db.db** (Используется Order Service)
  - `order`: Содержит информацию о заказах.
  - `station`: Содержит информацию о станциях.


## API

- **Postman коллекция**: [доступна в JSON формате](microfastapi.postman_collection.json)
- **Swagger документация**: Каждый микросервис включает встроенную документацию Swagger, доступную по следующим URL:
  - `auth_service`: [http://localhost:8000/docs](http://localhost:8000/docs)
  - `order_service`: [http://localhost:8001/docs](http://localhost:8001/docs)

