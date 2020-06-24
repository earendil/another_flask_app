# Small Flask app

## Description:

This is a code challenge containing a Flask app using gunicorn as wsgi server and nginx as a reverse proxy and Redis for caching. 

## Dependencies:

* docker
* docker-compose 

## Setup:

* From a terminal run from root of the project directory: `docker-compose up`

## Endpoints:

* `http://localhost` (Hello World)
* `http://localhost/stores` (A table containing stores and coordinates)
* `http://localhost/find` (Lists stores within a postcode radius)

## Usage:

* URLs are accesible from a browser, except "find" which can be accessed via curl. (Or similar solution that generates a POST request)

Example request:
        `curl http://localhost/find -d '{"radius": 2000, "postcode": "CT1 1DS"}' -H 'Content-Type: application/json'`

\* Configuration is available by defining `APP_ENV` as an `environment variable ` or via the `.env` file.  
Valid configs: ["Dev", "Prod", "Test"]
