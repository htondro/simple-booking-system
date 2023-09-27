# Realtyna Interview Challenge

## Challenge Description

As a listing owner, We need a system for making and tracking reservations that can be handled by third-party services.

1. The system can be used by multiple listings.
2. The system provides REST API endpoints:
   1. To make reservations
   2. To check if a number of rooms are available at a certain time
3. A reservation is for a name (any string) and for a certain amount of time
4. The listing owner can get an overview over the booked rooms as an HTML or TEXT report

## Challenge Limitations

1. Authentication / Authorization is not in the scope of this task
2. No localization needed

## Requirements

- Docker

## Deployment

1. [Install Docker](https://docs.docker.com/engine/install/) on your machine.
2. Make a new folder and `git pull` this repo.
3. Create a `.env` file in your project root to set env vars.

```
DEBUG= 0
SECRET_KEY='/run/secrets/secret_key'
DJANGO_ALLOWED_HOSTS=\*
SQL_ENGINE=django.db.backends.postgresql
SQL_HOST=db
SQL_PORT=5432
POSTGRES_DATABASE=realtyna
POSTGRES_USER=realtyna_user
POSTGRES_PASSWORD='/run/secrets/sql_password'
```

4. Create a new folder called `secrets` in your project root to set docker secrets.
   1. Create `secret_key.txt` file in secrets folder and put your considered django secret key as plain text in that file.
   2. Create `sql_password.txt` file in secrets folder and put your considered SQL password as plain text in that file.
5. run `docker compose build` in command line at your root project.
6. run `docker compose exec db psql -U realtyna_user` to get into db shell.
   1. run `CREATE DATABASE realtyna;` in db shell.
7. run `docker compose up -d` in command line to run containers.
8. run `docker compose exec web python manage.py createsuperuser` to create django super user.
9. Now you can login to django admin dashboard (`localhost/admin`) to CRUD data.

## REST API Endpoints

- `/` : api root
- `/owner/` : owners endpoint (consider creating new owners using django admin panel)
  - `/owner/<int:pk>/` : owner details
    - `/owner/<int:pk>/reserved/` : owner's reserved rooms list
- `/room/` : rooms endpoint
  - `/room/<int:pk>/` : room details
- `/reservation/` : reservations endpoint
  - `/reservation/<int:pk>/` : reservation details
  - `/reservation/available/` : list of available rooms at a certain time

## Challenge Review

> 1. The system can be used by multiple listings.

You can create multiple listing owners using django admin panel.

- Each owner can have multiple rooms with unique names.
- Two owners may have rooms with same name.

> 2. The system provides REST API endpoints:
>    > 1. To make reservations
>    > 2. To check if a number of rooms are available at a certain time

To make reservations you can `POST` data to `/reservation/` endpoint.

```
{
    "start_date": reservation start date in "%Y-%m-%d" format,
    "end_date": reservation end date in "%Y-%m-%d" format,
    "room": room pk
}
```

> 3. A reservation is for a name (any string) and for a certain amount of time

Reservation model has 3 fields:

- Start date
- End date
- Room (foreign key to rooms table)

> 4. The listing owner can get an overview over the booked rooms as an HTML or TEXT report

Each owner can see the HTML list of his/her reserved rooms with a `GET` request to this endpoint:
`/owner/<pk:int>/reserved`

## Contact Me

If you have any concerns or questions related to this repo, feel free to contact me:

- [Linkedin](https://linkedin.com/in/htondro)
