# PSS Fleet Data API

<a href="https://discord.gg/kKguSec" target="_blank"><img src="https://discord.com/api/guilds/565819215731228672/embed.png" alt="Support Discord server invite"></a>
<a href="https://codecov.io/gh/Zukunftsmusik/pss-fleet-data-api"><img src="https://codecov.io/gh/Zukunftsmusik/pss-fleet-data-api/graph/badge.svg?token=M7GZSCGK36"/></a>

> A REST API server for Pixelstarships Fleet Data to be deployed on [CapRover](https://caprover.com/).

## Built with

- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)

# 🚀 Deploy
In order to deploy the API, the following prerequisites must be met:

- A [PostgreSQL 14](https://www.postgresql.org/) server running.
- Optional: a current [Docker](https://www.docker.com/) installation when deploying locally with Docker.
- Certain environment variables set:

## Required Environment variables
- `DATABASE_URL`: The URL to the database server, including username, password, server IP or name and port.
- `DATABASE_NAME`: The name of the database. Will be overriden during tests.

## Optional environment variables
- `CREATE_DUMMY_DATA`: Set to `true` to create dummy data in the database at app start.
- `DATABASE_ENGINE_ECHO`: Set to `true` to have SQL statements printed to stdout.
- `DEBUG_MODE`: Set to `true` to start the application in debug mode. Enables more verbose logging.
- `FLEET_DATA_API_URL_OVERRIDE`: If this is set, the API server url in the Swagger UI will be overriden.
- `FLEET_DATA_API_URL_DESCRIPTION_OVERRIDE`: If this is set, the API server url description in the Swagger UI will be overriden.
- `REINITIALIZE_DATABASE`: Set to `true` to drop all tables at app start before recreating them.
- `ROOT_API_KEY`: If this is set, the following endpoints require a client to send the specified key in the `Authorization` header:
  - `POST /collections`
  - `DELETE /collections/{collectionId}`
  - `POST /collections/upload`

## Deploy on CapRover
To deploy the API on [CapRover](https://caprover.com/) you need to:
- Create a new app on your CapRover instance
- Set up the environment variables described above
- [Fork the repository](https://github.com/Zukunftsmusik/pss-fleet-data-importer/fork) to your own github account
- Follow the steps explained in the [CapRover Docs](https://caprover.com/docs/ci-cd-integration/deploy-from-github.html).

## Deploy locally with Docker
Follow the steps outlined in the [Contribution Guide](CONTRIBUTING.md) to set up your local development environment. Create a file called `.docker-env` in the workspace folder and add the following environment variables:
- `DATABASE_URL`
- `DATABASE_NAME`
- `ROOT_API_KEY` (optional)

Then open a terminal, navigate to the workspace folder and run `make docker`. The command will:
- Stop the running container, if it's been started with the same command.
- Delete the stopped container
- Delete the image, if it's been created with the same command.
- Build a new image.
- Start a container with that image.

The API can then be accessed at `http://localhost:8000`.

## Run locally without Docker
- Follow the steps outlined in the [Contribution Guide](CONTRIBUTING.md) to set up your local development environment.
- Set up the environment variables outlined above.
- Open a terminal, navigate to the workspace folder and run `make run` to start the API server. Alternatively run `make dev` to start the API server in development mode, in which any changes to code files will make the API restart to reflect those changes.

The API can then be accessed at `http://localhost:8000`.

# 🖊️ Contribute
If you ran across a bug or have a feature request, please check if there's [already an issue](https://github.com/Zukunftsmusik/pss-fleet-data-api/issues) for that and if not, please [open a new one](https://github.com/Zukunftsmusik/pss-fleet-data-api/issues/new).

If you want to fix a bug or add a feature, please check out the [Contribution Guide](CONTRIBUTING.md).

# 🆘 Support
If you need help using the API or want to contribute, you can join my support Discord at: [discord.gg/kKguSec](https://https://discord.gg/kKguSec)

# 🔗 Links
- Documentation (tbd)
- [Official Support Discord server](https://https://discord.gg/kKguSec)
- [Official PSS Fleet Data API](https://fleetdata.dolores2.xyz)
- [Buy me a can of cat food](https://buymeacoffee.com/the_worst_pss)
- [Or a coffee](https://ko-fi.com/theworstpss)
