# Проектная работа: диплом

https://github.com/johanijbabaj/graduate_work


# Разворачивание стека
## Конфигурация и инициализация

За конфигурацию отвечают файлы:
* config/.env

Генерация файлов со значениями по-умолчанию и применение миграций:
```
make init
```

## Запуск стека
```
make up
```

# Тестирование
## Тестирование оплаты
Тестирование оплаты от платежной системы Stripe можно выполнить запуская стек в режиме разработки:
```
make env=dev up
```
в состве стека будет запущено приложение strip_cli, конфигурационные параметры для которого можно найти в файле config/.env (см. раздел с конфигурацией)


# API
## Создание Invoice
**/api/v1/invoices**  
method: POST  
headers:
* X-Request-Id: unique request id  

body:  
```
{
  "product_name": "subscription, 1 month",
  "product_count": 2,
  "product_price_currency": "USD",
  "product_unit_price": 10,
  "success_url": "http://..success",
  "cancel_url": "http://..cancel"
}
```

responses:
**200**
```
{
  "invoice": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2022-04-14T20:48:42.456Z"
  },
  "checkout_url": "string"
}
```

# Rabbit MQ
Получение статуса инвойса происходит через получение сообщения от RabbitMQ.  
  
Имя очереди по-умлчанию - **invoices**  
Параметры подключения по-умолчанию - **amqp://guest:guest@rabbitmq/**  
(см. конфигурационный файл .env переменные PAYGATEWAY_RABBITMQ_URI и PAYGATEWAY_RABBITMQ_QUEUE)  
  
Формат сообщения:
```
{
  "id": <String: id инвойса>,
  "created_at": <String: метка времени>,
  "state": <String: статус инвойса>,
  "x_request_id": <String: request id запроса на основании которого был создан invoice>
}
```

Пример:
```
{
  "id": "599f2636-6e51-4d86-8e39-ff72e56daf47",
  "created_at": "2022-04-17T11:47:54.485937",
  "state": "unpaid",
  "x_request_id": "599f2636-6e51-4d86-8e39-ff72e56daf47",
}
```

# Development

## Инициализация
```
make env=dev init
```

## Сборка образов
```
make env=dev build
```

## Запуск стека
```
make env=dev up
```

## Проверка
### Payment Gateway
По адресу
```
http://127.0.0.1:8001/api/openapi#/
```
должна открыться страница с описанием API 'PAYGATEWAY'


