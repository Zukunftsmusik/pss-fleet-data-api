# pss-fleet-data-api
An API server for Pixelstarships Fleet Data to be deployed on [CapRover](https://caprover.com/).

## Deployment
### Database
The API requires a postgres database.
### Required environment variables
- `DATABASE_URL`: The URL to the database server, including username, password, server IP or name and port.
- `DATABASE_NAME`: The name of the database. Will be overriden during tests.
### Optional environment variables
- `CREATE_DUMMY_DATA`: Set to `true` to create dummy data in the production database at app start.
- `DATABASE_ENGINE_ECHO`: Set to `true` to have SQL statements printed to stdout.
- `DEBUG_MODE`: Set to `true` to start the application debug mode. Enables more verbose logging.
- `FLEET_DATA_API_URL_OVERRIDE`: If this is set, the API server url in the Swagger UI will be overriden.
- `FLEET_DATA_API_URL_DESCRIPTION_OVERRIDE`: If this is set, the API server url description in the Swagger UI will be overriden.
- `REINITIALIZE_DATABASE`: Set to `true` to drop all tables at app start before recreating them.
- `ROOT_API_KEY`: If this is set, the following endpoints require a client to send the specified key in the `Authorization` header:
  - `POST /collections`
  - `DELETE /collections/{collectionId}`
  - `POST /collections/upload`

## Running Docker container locally with Make
Create a file called `.docker-env` in the root folder of the repository and add values for the following environment variables:
- `DATABASE_URL`
- `DATABASE_NAME`
- `ROOT_API_KEY` (optional)
