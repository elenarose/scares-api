# scares-api
An API for the Capstone Project SCARES

### Dependencies
Install dependencies
```
$ pip3 install flask
$ pip3 install flask_restful
$ pip3 install psycopg2-binary
$ pip3 install Flask-Migrate
```

### Running Postgres Locally
I find it easiest to run Postgres in a docker container. You can get a container up and running with this command.
```
docker run -d \
        --name dev-postgres \
        -e POSTGRES_PASSWORD=postgres \
        -p 5432:5432 \
        postgres
```

Then use DataGrip (or your preferred Postgres GUI) to view to the database.
![Image of DataGrip Preferences](./datagrip.png)