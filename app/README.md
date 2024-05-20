# Stock Performance Simulator

### Problem
What would be the current return on my investment if I had acquired shares of X company in the past?

## Solution
This REST API allows the user to query daily stats for a given stock, on certain date, and calculate what would be the ROI on this day (or last business day).

## Requirements
This project can be installed anywhere by using `docker`, or in a `linux` machine having `python3` and `poetry` installed.

#### Env Vars
- DJANGO_SETTINGS_MODULE=take_home.settings
- DJANGO_LOG_LEVEL=DEBUG
- DJANGO_DEBUG=False
- ENV=local
- POSTGRES_NAME
- POSTGRES_USER
- POSTGRES_PASS
- POSTGRES_HOST
- POSTGRES_PORT
- POLYGONIO_API_KEY
- POLIGONIO_KEY_ID

## Installation
1. With Docker
```commandline
# Once we filled all the env vars in docker-compose.yml
$ docker compose up

# Create a django user
$ sudo docker exec -it stocksdemo-app-1 sh

# Type these commands within the container shell
$ make createsuperuser
```
Use that user credentials to interact with the REST API.

2. In Linux
```commandline
# Run migrations
poetry run python manage.py migrate

# Create superuser to interact with the REST API
poetry run python manage.py createsuperuser

# Declare env vars or inlude them into a .env file
export DJANGO_SETTINGS_MODULE=take_home.settings
.
.
.

# and run the server
poetry run python manage.py runserver
```

## Example
```commandline
$ httpx --auth user pwd http://127.0.0.1:8000/api/pnl/ -m POST -d ticker NFLX -d date 2024-04-01
HTTP/1.1 201 Created
Date: Mon, 20 May 2024 03:18:58 GMT
Server: WSGIServer/0.2 CPython/3.11.2
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 381
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{
    "id": 3,
    "date": "2024-05-17",
    "ticker": "NFLX",
    "min_change": -1.71,
    "max_change": -3.23,
    "stock_bar": [
        {
            "id": 4,
            "ticker": "NFLX",
            "timestamp": "2024-04-01",
            "open_price": 608.0,
            "close_price": 614.31,
            "highest_price": 615.11,
            "lowest_price": 605.571
        }
    ],
    "last_bar": [
        {
            "id": 2,
            "ticker": "NFLX",
            "timestamp": "2024-05-17",
            "open_price": 617.0,
            "close_price": 621.1,
            "highest_price": 625.79,
            "lowest_price": 614.7141
        }
    ]
}
```

