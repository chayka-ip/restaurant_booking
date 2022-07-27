## Тестовое задание для "ООО Гарант-Логистика"

### Текст задания: https://tinyurl.com/29bceuyh

Задача: разработать API-сервис, который будет принимать заказы на бронирование столиков в ресторане.   

Общая информация: сервис не является standalone-продуктом, он является входной точкой для клиентов и содержит в себе минимально необходимую информацию о качестве и компоновке столика. При получении заказа на бронирование столика сервис не убирает столик из доступных для бронирования, заказ пересылается в учетную программу, где ответственный сотрудник подтверждает или не подтверждает бронь. Также при приеме заказа на бронирование клиенту должно приходить письмо на электронную почту о приеме заказа. После обработки ответственным сотрудником информация пересылается обратно в сервис, а сервис в свою очередь присылает отбивку на почту клиента о статусе заказа.   

Содержание БД: Существует 3 вида столиков: обычные (в общем зале), кабины (столики разделенные перегородками и закрывающиеся шторкой),  комнаты (отдельные комнаты за дверью). Ресторан может расширяться, и количество столиков любого вида может изменяться, необходимо предусмотреть быстрое изменение доступных столиков. У столиков может быть различное количество посадочных мест (у любого вида столиков). Стоимость бронирования столика также может меняться с течением времени.   

Администрирование: Сервис должен иметь административные функции, которые доступны только авторизованному пользователю (условно это должен быть администратор, работающий через JWT-токен, реализовывать получение и проверку токена не нужно, только указать где он может быть получен, и где будет проверяться).  Административные функции должны позволять установить бронирование, отменить бронирование, закрыть столик для бронирования, установить стоимость бронирования, добавить\изменить столик.  

Публичные функции: Сервис должен иметь функции: подбор столика, заказ на бронирование (с указанием электронной почты клиента и\или телефона), отмена заказа на бронирование (через кнопку в письме на электронную почту клиента о приеме заказа на бронирование). Параметры подбора: вид столика, количество мест, диапазон стоимости. На выходе должен быть массив из подходящих вариантов.   

Структура ответа, когда произошла ошибка, должна быть в едином стиле.  

Реализация: использование любого из фреймворков: Django, FastAPI, Flask. Приоритетными фреймворками являются Flask и FastAPI. Использование БД: noSQL – MongoDB, SQL – PostgreSQL.  

Желательно: обернуть сервис в docker-compose, настроить работу через порт 9000.  


### Пользователи
 - Пользователь с правами администратора: 
     - username `admin`
     - password `1` 
 - Пользователи без прав:
     - username `cutomer / josh / mike `
     - password `1` 

### Для того, чтобы запустить проект через Docker, выполните следующую команду:
```
docker-compose up
```

Репозиторий содержит дамп базы данных, который будет установлен автоматически.  

Список доступных endpoints и настроенные переменные окружения 
находятся в директории Postman и могут быть импортированы в программу Postman.

#### ADMIN ENDPOINTS
```
/api/admin/add_table/

Params (JSON):
'table_type' (optional): "regular" | "cabin" | "room"
'seats' (optional):  int
'price' (optional): float
'can_be_booked' (optional): bool

```
```
/api/admin/update_table/

Params (JSON):
'id' (required): int
'table_type' (optional): "regular" | "cabin" | "room"
'seats' (optional):  int
'price' (optional): float
'can_be_booked' (optional): bool
```
```
/api/admin/accept_booking/

Params (Query):
'id': int - customer booking id
```
```
/api/admin/cancel_booking/

Params (Query):
'id': int - customer booking id
```
```
/api/admin/view_active_bookings/
```

#### CUSTOMER ENDPOINTS

```
/api/customer/view_tables/
```
```
/api/customer/book_table/

Params (Query):
'id': int - table id
```
```
/api/customer/cancel_booking/

Params (Query):
'id': str
```

#### DEBUG ENDPOINTS

```
/api/token/

Allows to obtain JWT token for admin user

Params (JSON):
'username': str 
'password': str
```

### Стэк
 - [![](https://www.djangoproject.com/m/img/badges/djangomade124x25.gif)]()
 - ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
 - ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
 - ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
 - **Celery**
 
### .env (sensitive data)
```
SECRET_KEY=django-insecure-ncff6nbb_nr!8xekae@+40!j!i%b!yo6uxpb1_v*p2i9e+8r9!
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=pgdb
POSTGRES_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=465
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```
