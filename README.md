# user-auth-service

The user authentication service uses Fastapi and pydantic with Sqlalchemy, postgresql, Alembic(for migrations).

See below how to build and run the application.
Additionally, Swagger API documentation is available that would allow you to send requests the the API from your browser.

## Environment

This repo was tested in WSL using Python 3.10.

## How to run service

    docker-compose up --build

and go to:

    http://localhost:8000

## How to run unit tests

    pip install -r requirements.txt
    pytest . -v --cov

## Documentation

    swagger - http://localhost:8000/docs
    redoc - http://localhost:8000/redoc

## Pgadmin4

    http://localhost:5050

##