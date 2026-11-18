# Готовое решение CRUD в DRF

Изменены `logistic/serializers.py` и `logistic/views.py`. Реализованы CRUD, поиск, фильтрация складов, пагинация и дополнительный поиск по названию/описанию продукта.

## Запуск

1. Создайте PostgreSQL-базу `netology_stocks_products` и при необходимости скорректируйте `stocks_products/settings.py` (имя, порт, пользователь, пароль).
2. В папке проекта выполните `pip install -r requirements.txt`.
3. Выполните `python manage.py migrate`.
4. Выполните `python manage.py runserver`.

## Запросы

- `/api/v1/products/?search=помидор`
- `/api/v1/stocks/?products=2`
- `/api/v1/stocks/?search=помидор`
- `/api/v1/products/?page=2&page_size=5`

При обновлении склада переданный массив `positions` полностью заменяет существующие позиции. Если поле не передано, позиции сохраняются.
