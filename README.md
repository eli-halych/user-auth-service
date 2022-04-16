# user-auth-service

The user authentication service that allows you to create a user, login as that
user, update any of the `4` user attributes (`first_name`, `last_name`, `username` and `password`), and remove the user.

## Endpoints

1. `/signup` accepts user data and create an entry in the database.
Passwords are hashed.
2. `/login` accepts user credentials an dissues a JWT token secured with a secret
key.
3. `/update` accepts an Authorization header containing a Bearer JWT token, and one of the 4 valid user attribues (`first_name`, `last_name`, `username` and `password`) with values and applies the change to the database.
4. `/delete` accepts an Authorization header containing a Bearer JWT token, and removes the user whose ID was specified as `sub` in the payload.

See below how to build and run the application, database and pgAdmin in one step.
Additionally, Swagger API documentation is available that would allow you to send requests the the API from your browser.

## Tool specs

1. Docker Compose for running together FastAPI API, Postgres database and pgAdmin.
2. Python 3.10 & virtualenv for running tests in a virtual environemnt.
3. WSL in Windows 10.
4. A web browser for sending requests via Swagger UI (See documentation below).

## How to run service

    docker-compose up --build

This will leave the console attached to the terminal window and will log all requests and operations, both internal and external.

## How to run unit tests

Use Python 3.10 and WSL-like environment.

    virtualenv venv --python=python3.10
    source venv/bin/activate
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
<br />

    pip install -r requirements.txt
    pytest . -v --cov
<br />

    deactivate

In production use automation tools such as [tox](https://tox.wiki/en/latest/index.html) or [nox](https://nox.thea.codes/en/stable/) to test against multiple environments in a matter of one command line.

## Interactive documentation with UI

    Swagger - http://localhost:8000/docs
    ReDoc - http://localhost:8000/redoc

## Interact with the database via UI

    pgAdmin4 - http://localhost:5050

## Remarks

1. pgAdmin4 credentials can be found here [.env](.env). (Don't put them there in production. Use CI/CD variables instead and don't log them.)