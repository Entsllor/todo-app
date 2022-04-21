# To-Do app

> This app can help you organize your tasks


## Pre-requirements (backend)

Set env variables

```dotenv
# backend/app/.env
APP_DB_URL=postgresql+asyncpg://USERNAME:PASSWORD@localhost:5432/postgres
APP_SECRET_KEY=YOUR-SECRET-KEY
```

If you run project via docker-compose set hostname as 'db' (as in docker-compose.yml file)
else you can use 'localhost' or any other hostname.

List of all backend env variables described in ./backend/app/core/settings.py file. 
All variables should start with a specific prefix 'APP_'.
