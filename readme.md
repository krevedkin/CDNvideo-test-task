

# CDNvideo test task

## Техническое задание

Необходимо разработать HTTP API, с помощью которого можно:

- добавлять/удалять в хранилище информацию о городах;
- запрашивать информацию о городах из хранилища;
- по заданным широте и долготе точки выдавать 2 ближайших к ней города из присутствующих в хранилище.

При запросе к API на добавление нового города клиент указывает только название города, а в хранилище добавляются также
координаты города. Данные о координатах можно получать из любого внешнего API.

Реализация хранилища произвольная.

## Требования перед установкой

- Установленный **git**
- Установленный **Python 3.10+**
- API токен созданный на сайте https://api-ninjas.com/api/city (если необходимо я вышлю свой напишите мне в [Telegram](https://t.me/krvdkrvd)
## Установка и запуск

1. Склонировать репозиторий

```
git clone https://github.com/krevedkin/CDNvideo-test-task.git
```

2. Создать виртуальное окружение

```
virtualenv venv
```

3. Активировать виртуальное окружение

```
 source venv/bin/activate
```

4. Установить зависимости

```
 pip install -r requirements.txt
```

5. В корне проекта в файле **.env** добавить значение для переменной окружения **CITIES_API_TOKEN** (при отсутствующем значении
   переменной приложение вызовет исключение при запуске)

```
 CITIES_API_TOKEN="your_api_token"
```

6. Находясь в корне проекта выполнить команду для запуска приложения

```
bash run.sh
```

Если по каким то причинам пункт 7 не сработал, сделать следующие действия

- Создать в корне проекта файл базы данных SQlite с именем **database.db**

```
touch database.db
```

- Провести миграции

```
alembic upgrade head
```

- Запустить проект

```
python src/main.py
```

8. Приложение будет запущено и доступно по адресу http://localhost:8000

 База данных будет наполнена данными следующих городов:
 **name | longitude | latitude**
- Moscow,37.6178,55.7558	
- Saint Petersburg,30.3167,59.95
- Rostov,39.7167,47.2333
- Volgograd,44.4833,48.7
- Yekaterinburg,60.6128,56.8356
- Novosibirsk,82.9167,55.0333
- Vladivostok,131.9,43.1167	Voronezh,39.2106,51.6717
- Belgorod,36.6,50.6
- Kazan,49.1144,55.7908
- Bryansk,34.3667,53.25
- Sochi,39.7203,43.5853
- Krasnodar,38.9833,45.0333
- Petropavlovsk,158.65,53.0167
- Omsk,73.3833,54.9667
- Chita,-97.3442,37.6896
- Murmansk,33.0833,68.9667
- Novgorod,44.0075,56.3269
- Orenburg,55.1,51.7667
- Chelyabinsk,61.4,55.15

# Документация эндпойнтов

## GET /cities

Получить список всех городов

Пример ответа 200:
> {
"id":  1,
"name":  "Moscow",
"longitude":  37.6178,
"latitude":  55.7558
> },

## GET /city/:name

Получить конкретный город по названию city, переданному в path параметрах

Пример ответа 200:

> {
"id":  21,
"name":  "Krasnoyarsk",
"longitude":  92.8667,
"latitude":  56.0167
> }

Ошибки:
400 - Название города не передано в параметрах
404 - Город с таким названием не найден

## POST /city

Добавить новый город

request body:
> {
"name":  "Krasnoyarsk"
> }

Пример ответа 201

> {
"ok":  true
> }

Ошибки:
400 - Не передан request body или некорректное имя города (город не существует)
422 - Некорректный тип данных в поле name
409 - Город с таким именем уже существует
500 - Некорректный API ключ в конфиге приложения или проблемы со стороны внешнего API

## DELETE /city/:name

Удалить город

параметр name чувствителен к регистру Moscow и moscow разные имена (это связано с особенностями SQLAlchemy)

Успешный ответ - 204

Ошибки
404 - город с таким названием не найден

## GET /cities/nearest

Получить 2 ближайших города по заданным координатам широты и долготы

Query params:
**longitude** - долгота (float или int)
**latitude** - широта (float или int) в диапазоне [-90; 90]

Пример ответа 200:
> [
{
"id":  16,
"name":  "Chita",
"longitude":  -97.3442,
"latitude":  37.6896,
"distance":  14175.01135287252
},
{
"id":  7,
"name":  "Vladivostok",
"longitude":  131.9,
"latitude":  43.1167,
"distance":  14777.650268351426
}
]

Значение **distance** является расстоянием выраженном в километрах от заданных координат

При отсутствующих городах в БД вернется пустой список [] при наличии только одного города в БД вернется список с одним
объектом.

Ошибки:
400 - не переданы параметры longitude или latitude
422 - неверный тип параметров
422 - параметр latitude вне диапазона [-90; 90]
