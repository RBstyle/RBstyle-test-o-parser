# RBstyle-test-o-parser
Ozon product parser with notification

Тестовое задание
Разработка парсера товаров сайта Ozon с оповещением


Цели:
 •  Разработка Django приложения.
 •  Создание REST API на основе Django Rest Framework (DRF).
 •  Реализация парсера товаров с сайта Ozon.
 •  Оповещения в Telegram с помощью бота.

Эндпоинты:
 • POST /v1/products/: Запуск задачи на парсинг N товаров. Количество товаров должно приниматься в теле запроса в параметре products_count, по умолчанию 10 (если значение не было передано), максимум 50.
 • GET /v1/products/: Получение списка товаров.
 • GET /v1/products/{product_id}/: Получение товара по айди.
Примеры входных и выходных данных для каждого эндпоинта будут в приложения к тестовому заданию.

Описание проекта:
В рамках этого тестового задания необходимо разработать Django приложение с REST API для парсинга информации о товарах магазина по ссылке с сайта Ozon и сохранения полученных данных о товарах в базу данных. Также требуется настроить оповещения о завершении парсинга через Telegram бота.

Ссылка для парсера:
Парсим по такой ссылке https://www.ozon.ru/seller/1/products/ (именно этот магазин).

Выходные данные:
Для эндпоинта GET /v1/products/: выходными данными будет массив товаров.
Для эндпоинта GET /v1/products/{product_id}/ выходными данными будет один товар.

Требования:
 • Django приложение должно быть разработано с использованием Django Rest Framework.
 • Документирование API должно быть создано с помощью библиотеки Django drf-yasg.
 • Для парсинга данных с сайта Ozon рекомендуется использовать библиотеку BeautifulSoup или другие удобные инструменты.
 • Оповещения должны отправляться в Telegram с помощью Telegram бота.
 • Парсер должен быть реализован с использованием Celery задач.
 • Информация о товарах должна сохраняться в базу данных и отображаться в административной панели.
 • Административная панель должна быть кастомизирована с использованием AdminLTE для современного и привлекательного внешнего вида приложения.

Техническое описание:
 • Версия Python: 3.x
 • Django: 3.x
 • Django Rest Framework: 3.x
 • Celery: 5.x
 • База данных: MySQL

Пример текста для оповещения в Telegram:
Задача на парсинг товаров с сайта Ozon завершена.
Сохранено: N товаров.

Команда для бота: Список товаров
Ожидаемый ответ: бот показывает пронумерованный список товаров последнего парсинга в виде Название + ссылка.

В readme.md должно быть описание то, как запустить проект.
Также в проекте должен быть example.env, если будут использоваться переменные среды. 

Результат задания должен быть выложен в открытый репозиторий на github.
Название репозитория должно быть в формате: “YOURLOGIN-test-o-parser”.


ФОРМАТ ОТКЛИКА: заполнение анкеты, которая вам пришла в ответ на отклик в письме и/или смс.
Ссылка в анкете = ссылка на репозиторий в git для этого задания.
Важно! В корень репозитория положите записанный скринкаст админки со стороны пользователя-админа и просмотр списка товаров в табличном виде.

Срок исполнения — 3 календарных дня (не более 24 ч чистого времени разработки).
