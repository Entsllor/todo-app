# To-Do app

> This app can help you to organize your tasks

## Installation

```shell
git clone https://github.com/Entsllor/todo-app
```

## Pre-requirements (backend)

Create ./backend/src/.env file and set env variables

```dotenv
# ./backend/src/.env
FLASK_ENV=production
APP_DB_URI=postgresql://user:pass@db:5432/postgres
APP_SECRET_KEY=YOUR-SECRET-KEY
```

If you run project via docker-compose set hostname to 'DB' (as in docker-compose.yml file)
else you can use 'localhost' or any other hostname.

List of all backend env variables described in ./backend/app/core/settings.py file.
All variables should start with a specific prefix 'APP_'.

### Install docker and docker-compose

[Install Docker](https://docs.docker.com/engine/install/ubuntu/)

[Install Docker-compose](https://docs.docker.com/compose/install/)

## Run

Run this project by docker-compose:

```shell
docker-compose up --build
```

## Utils

You can fill db with test data by command:

```shell
flask fill_db
```

This command will create several users with usernames like 'user_1' (user_2, etc.) and default passwords equal 'pass'.
These users have some tasks with different status and titles.

Also, you can clear DB by command:

```shell
flask clear_db
```

