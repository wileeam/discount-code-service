# Get discount code service

- Pre-requisites: Python 3.7+

- Install dependencies. For example: pipenv install -r requirements.txt
- Run with `uvicorn main:app`
  - When running locally, HOST is likely to be localhost or 127.0.0.1 and PORT will be 8000
  - Data persistence is done with SQLite in the same directory as the application (a file `data.db` will be created upon usage).

- Check documentation for informatiom and details on the endpoints available at,
  - http://HOST:PORT/docs
  - http://HOST:PORT/redoc

- OpenAPI JSON available at,
  - http://HOST:PORT/openapi.json
