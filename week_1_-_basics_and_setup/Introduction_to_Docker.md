## Introduction to Docker - Notes

### What is docker? -- IBM defintion
Docker is an open source containerization platform. It enables developers to package applications into containers—standardized executable components combining application source code with the operating system (OS) libraries and dependencies required to run that code in any environment

### Containerization -- IBM defintion
Containerization is the packaging of software code with just the operating system (OS) libraries and dependencies required to run the code to create a single lightweight executable—called a container—that runs consistently on any infrastructure

### What is a data pipeline?
Process or service that takes in data and outputs more data in our desired format

We can then bundle up all the dependecies that our data pipeline needs in order to run as a "contianer" and then be able to run it in another computer or another operating system. 

### Why should we care about docker?
- Reproducibility
- Local experiments
- Integration tests (CI/CD) - General software engineering best practices
- Running pipelines on the cloud using this docker image of the data pipeline
- Serverless (AWS Lambda, Google Functions)
- Spark

Running PostgreSQL in docker
- The following command is used to run PostgreSQL with docker:
```bash
 docker run -it   
 -e POSTGRES_USER="root"   
 -e POSTGRES_PASSWORD="root"   
 -e POSTGRES_DB="ny_taxi"   
 -v a:/"Data Engine
ering"/data-engineering-zoomcamp/week_1_-_basics_and_setup/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data   
-p 5432:5432   
postgres:13
```
Also, using pgcli to connect to postgres:
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
We can use pgAdmin or pgcli to interact with our postgres database. 

Since we are using Docker, we don't have to install pgAdmin in our host system.
We can simply use Docker to pull an image of pgAdmin. 

To run pgAdmin in Docker we can run the following command:
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

Now, since postgres and pgAdmin are running in different contianers
we need to be able to link them together

We can do this by putting the two docker containers under one network. 

Using:
- `docker network create pg-network`

Now using the following arguments when using docker run `-it` command:
```bash
--network=pg-network\
--name pg-database or pgadmin
```

To convert a jupyter notebook into a normal python script we can use the following command:
```bash
jupyter nbconvert --to=script week_1_-_basics_and_setup\docker_sql\upload_data.ipynb
```
To run the data ingestion script locally, we use the following command: 
```bash
URL="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```

### Dockerizing the Ingestion Script
While we are in the directory we run the following command:
```bash
docker build -t taxi_ingest:v001
```

Now to run the script with docker:
```bash
URL="http://172.24.208.1:8000/yellow_tripdata_2021-01.csv"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```
Making a simple http server run with pytnon:
```bash
python -m http.server
```
We can get the address by running ipconfig and using the ipv4 address

And this is how we dockerize the datapipelines

### Docker-Compose

-> A way to put together multiple services in one config file. 

Instead of running multiple docker commands with docker configurations in them.
We can create one yml file with the config information. 
For this we will use docker compose. 

This is how a docker-compose file would look like in our case:
```yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
```

We don't need to define a network for this as the images here automatically become part of the same network

Run it:
```bash
docker-compose up
```
Run in detached mode:
```bash
docker-compose up -d
```
Shutting it down:
```
docker-compose down
```
