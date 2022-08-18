## Технологический стек
[![Django-app workflow](https://github.com/pupersa23/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/pupersa23/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

# Развёрнутый проект

http://51.250.106.165/

# Описание Workflow

## Workflow состоит из четырёх шагов:
tests
    Проверка кода на соответствие PEP8.
Push Docker image to Docker Hub
    Сборка и публикация образа на DockerHub.
deploy
    Автоматический деплой на боевой сервер при пуше в главную ветку.
send_massage
    Отправка уведомления в телеграм-чат.

# Подготовка и запуск проекта

## Клонирование репозитория

Склонируйте репозиторий на локальную машину:

    git clone git@github.com:pupersa23/foodgram-project-react.git

# Установка на удаленном сервере (Ubuntu):

## Шаг 1. Выполните вход на свой удаленный сервер

Прежде, чем приступать к работе, необходимо выполнить вход на свой удаленный сервер:

    ssh <USERNAME>@<IP_ADDRESS>

## Шаг 2. Установите docker на сервер:

Введите команду:

    sudo apt install docker.io

## Шаг 3. Установите docker-compose на сервер:

Введите команды:

    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

## Шаг 4. Скопируйте подготовленные файлы из каталога infra:

Скопируйте подготовленные файлы infra/docker-compose.yml и infra/nginx.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yml и home/<ваш_username>/nginx.conf соответственно. Введите команду из корневой папки проекта:

    scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
    scp nginx.conf <username>@<host>:/home/<username>/nginx.conf

## Шаг 5. Добавьте Secrets:

Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432

    DOCKER_PASSWORD=<пароль DockerHub>
    DOCKER_USERNAME=<имя пользователя DockerHub>

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<ID своего телеграм-аккаунта>
    TELEGRAM_TOKEN=<токен вашего бота>

## Шаг 8. После успешного деплоя:

Зайдите на боевой сервер и выполните команды:

Создаем и применяем миграции:
    
    sudo docker-compose exec backend python manage.py makemigrations --noinput
    sudo docker-compose exec backend python manage.py migrate --noinput

Подгружаем статику:

    sudo docker-compose exec backend python manage.py collectstatic --noinput 

Заполнить базу данных:

    sudo docker-compose exec backend python manage.py load_tags
    sudo docker-compose exec backend python manage.py load_ingrs

Создать суперпользователя Django:

    sudo docker-compose exec backend python manage.py createsuperuser

## Шаг 9. Проект запущен:

Проект будет доступен по вашему IP-адресу.

# Автор

Рязанов Владимир mail - ryazanov745@gmail.com