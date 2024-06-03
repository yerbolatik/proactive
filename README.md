# Pro-active.kz

Pro-active.kz - это интернет-магазин, позволяющий управлять данными о товарах и их продажей. В проекте реализованы функции создания, чтения, обновления и удаления (CRUD) для товаров и корзины.

## Оглавление
- [Описание](#описание)
- [Функциональность](#функциональность)
- [Требования](#требования)
- [Установка](#установка)
- [Использование](#использование)
- [Stripe для тестовых покупок](#stripe-для-тестовых-покупок)
- [Вклад](#вклад)
- [Лицензия](#лицензия)
- [Контакты](#контакты)

## Описание
Этот проект разработан для упрощения управления интернет-магазином, предоставляя удобный интерфейс для работы с товарами и корзиной покупателей.

## Функциональность
- **Товары:**
  - Создание новых товаров
  - Чтение данных о товарах
  - Обновление информации о товарах
  - Удаление товаров
- **Корзина:**
  - Добавление товаров в корзину
  - Просмотр товаров в корзине
  - Обновление количества товаров в корзине
  - Удаление товаров из корзины
- **Пользователи:**
  - Регистрация новых пользователей
  - Вход в систему для существующих пользователей
- **Категории:**
  - Фильтрация товаров по категориям
  - Пагинация по страницам
- **Продукты:**
  - Детальный просмотр продукта с описанием товара и несколькими фотографиями товара, условиями доставки и возврата
  - Блок с похожими товарами на странице продукта
- **Заказы:**
  - Просмотр истории заказов и их статусов
  - Просмотр деталей заказа

## Требования
- Python 3.8+
- Django 3.2+
- djangorestframework 3.12+
- SQLite (или другая поддерживаемая база данных)

## Установка
1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/yerbolatik/pro-active.kz.git
    cd pro-active.kz
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv env
    source env/bin/activate  # Для Windows используйте `env\Scripts\activate`
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Выполните миграции базы данных:
    ```bash
    python manage.py migrate
    ```

5. Создайте суперпользователя для доступа к административной панели:
    ```bash
    python manage.py createsuperuser
    ```

6. Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```

## Использование
После запуска сервера разработки, вы можете получить доступ к административной панели по адресу `http://127.0.0.1:8000/admin/` и к API по адресу `http://127.0.0.1:8000/api/`.

### API Эндпоинты
- **Товары:**
  - `GET /api/products/` - получить список всех товаров
  - `POST /api/products/` - создать новый товар
  - `GET /api/products/{id}/` - получить информацию о товаре
  - `PUT /api/products/{id}/` - обновить информацию о товаре
  - `DELETE /api/products/{id}/` - удалить товар

- **Корзина:**
  - `GET /api/cart/` - получить товары в корзине
  - `POST /api/cart/` - добавить товар в корзину
  - `PUT /api/cart/{id}/` - обновить количество товара в корзине
  - `DELETE /api/cart/{id}/` - удалить товар из корзины

## Stripe для тестовых покупок
В проекте реализован Stripe для тестовых покупок. Вы можете использовать следующие данные для тестирования:
- **Email**: любой
- **Card information**: 4242 4242 4242 4242
- **Дата**: любая (в будущем времени)
- **CVV**: любые 3 цифры
- **Cardholder name**: любое
- **Country**: любой

## Контакты
Если у вас есть вопросы или предложения, пожалуйста, свяжитесь с нами:
- Email: yerbolat.assabay@gmail.com
