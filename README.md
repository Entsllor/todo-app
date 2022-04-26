# To-Do app

> This app can help you organize your tasks

## Installation

```shell
git clone https://github.com/Entsllor/todo-app
```

## Pre-requirements (backend)

Create ./backend/app/.env file and set env variables

```dotenv
# backend/app/.env
FLASK_ENV=production
APP_DB_URI=postgresql+asyncpg://USERNAME:PASSWORD@localhost:5432/postgres
APP_SECRET_KEY=YOUR-SECRET-KEY
```

If you run project via docker-compose set hostname as 'db' (as in docker-compose.yml file)
else you can use 'localhost' or any other hostname.

List of all backend env variables described in ./backend/app/core/settings.py file.
All variables should start with a specific prefix 'APP_'.

### Install docker and docker-compose

[Install Docker](https://docs.docker.com/engine/install/ubuntu/)

[Install Docker-compose](https://docs.docker.com/compose/install/)

## Run

Run this project by docker-compose

```shell
docker-compose up --build
```

## Utils

You can fill db with test data by command

```shell
flask fill_db
```

Also, you can clear db by command

```shell
flask clear_db
```

