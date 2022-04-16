# Проектная работа: диплом

У вас будет один репозиторий на все 4 недели работы над дипломным проектом. 

Если вы выбрали работу в командах, ревью будет организовано как в командных модулях с той лишь разницей, что формируете состав команды и назначаете тимлида вы сами, а не команда сопровождения.

Удачи!

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
  "product_unit_price": 10
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


