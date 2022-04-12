# places_remember
Here you can store memories and impressions of the places visited

[![Passing](https://github.com/Tavien/places_remember/actions/workflows/django_tests.yml/badge.svg?branch=master)](https://github.com/Tavien/places_remember/actions/workflows/django_tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Tavien/places_remember/badge.svg?branch=master)](https://coveralls.io/github/Tavien/places_remember?branch=master)

### Порядок установки:

- Запустите проект с помощью следующих команд:
```
git clone https://github.com/Tavien/places_remember.git
cd places_remember/
docker-compose up --build
```

### Приложение использует:

- Python 3.9
- Django 4.0.3
- PostgreSQL 13.6 + Postgis
- Docker, Docker-compose
- GitHub Actions (unit test)
- Coverage + Coveralls
- Flake8

### Функции приложения:

- Аутентификация с помощью VK
- Создание профиля пользователя: аватар, имя и фамилия подгружаются из VK
- Пользователю доступно просмотр, создание, редактирование и удаление воспоминаний
