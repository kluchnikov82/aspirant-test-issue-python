# Тестовое задание на _Python_-программиста

В этом репозитории реализовано API приложения для планирования пикников, состоящие из сущностей:
 - Город
 - Пикник
 - Пользователь
 - Регистрация пользователя на пикник

## Задание
 Тестовое задание подразумевает изменение представленного здесь кода для достижения следующих задач:

### Минимальный уровень
  1. Запустить проект и ознакомиться с его документацией на странице `http://127.0.0.1:8000/redoc/`
     или `http://127.0.0.1:8000/docs/` 
     и выполнить каждый из запросов
  2. Изменить код проекта для получения дополнительных возможностей:
     - Добавить поиск городов аргументом `q` в запросе `/get-cities/`
     - Добавить возможность фильтрации пользователей по возрасту(минимальный/максимальный) в запросе `users-list`
     - Поправить ошибку в запросе `picnic-add`
     - Добавить метод регистрации на пикник `picnic-register`
  3. Высказать идеи рефакторинга файла `external_requests.py`
  4. Описать возможные проблемы при масштабировании проекта


     
### Продвинутый уровень
  1. Привести к нормальному виду:
     - Методы обращения к эндпойнтам
     - Названия эндпойнтов
     - Архитектуру и пути обращения к эндпойнтам
  2. Расписать все входные/выходные поля в документации (`/redoc/` или `/docs/`), описав их классами
  3. Оптимизировать работу с базой данных в запросе `/all-picnics/`
  4. Сменить базу данных с SQLite на PostgreSQL
  5. Отрефакторить файл `external_requests.py`
  6. Написать тесты


### Дополнительные задания
  - Сделать логирование в файл, который не будет очищаться после перезапуска в докере
  - Описать правильную архитектуру для проекта


# Результат выполнения задания
1. Запуск тестов: 
  - Файл test_main.py
  - Команда pytest
  - БД для тестов используется рабочая, т.к. в ней данные. Для наглядности выполнения тестов.
2. Логирование:
  - Файл logging.conf
  - монтирование в docker-compose
    volumes:  
       ./src/loging.log:/code/logging.log 
 3. По поводу рефакторинга external_requests.py
    - либо статический метед для def get_weather_url(city):
    - либо через отдельную функцию
 
 Все остальные задания реализованы в коде.
