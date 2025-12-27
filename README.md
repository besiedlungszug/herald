# Herald
This is the REST-API application layer of the historischer-besiedlungszug.de website written in the Python FastAPI framework. Its purpose is to take HTTP(S) requests from the webpage in JSON format and to trigger the respective backend handles on the database. The API shall then return an appropriate response code, potentially also a JSON body with the requested data.

## Guidelines
- This project is built security-first. No communication with other services shall be logged in production mode whatsoever.
- Encryption and other concerns are bound to change. It is advised to define and call a small amount of wrapper functions for communicating with other services.

## Documentation
The service uses the following environment variables for configuration:

- `DEBUG` – Run the server in debugging mode. Endpoint documentation is available through a magic `/docs` endpoint, based on [ReDoc](https://github.com/Redocly/redoc).
- `DB_HOST` – Backend Database Hostname
- `DB_PORT` – Backend Database Port
- `DB_NAME` – Backend Database Name
- `DB_USER` – Backend Database User
- `DB_PASSWORD` – Backend Database Password

The repository provides a `.env` file with the default values used for local development. Deployment of the service can override specific environment variables or provide a separate `.env` file.

## Contribution
It is highly advised to use a python virtual environment for developing this project. Specific requirements can be found in the `requirements` directory.

To get started, use
```sh
pip install -r requirements.txt
```
This will install a frozen package list of all dependencies and top level packages needed to run the project. If you feel particularily lucky, you can run
```sh
pip install -r requirements.in
```
instead to implicitly gather up-to-date versions for the dependencies. Use this to bump dependency versions in `requirements.txt` but make sure no breaking change has happened.

After installing the required packages, use
```sh
./serve
```
to start the server.

### Database Backend
This service runs on top of a database service that is version controlled by [dolt](https://www.dolthub.com). You need access to a local clone of the dolthub-hosted database to be able to contribute to the project. A publicly hosted unencrypted testbase will not be available. Check back with the administration to gain access to the database repository.
