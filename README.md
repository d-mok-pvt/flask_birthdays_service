# Flask Web API Service with Docker Images and Docker Compose

This is a Flask application that offers both a simple web user interface and an API service. The app and its tests are contained in separate Docker images and are run using Docker Compose. The primary purpose of the app is to manage birthdays data.

## Installation

Before you can use this project, you will need to have Docker and Docker Compose installed on your machine. [Source](https://docs.docker.com/compose/install/)

## Usage

### By default, running service endpoints are: 
*WEB UI*: [http://localhost:5000/](http://localhost:5000/) \
*SWAGGER UI*: [http://localhost:5000/swagger/](http://localhost:5000/swagger/) \
*Allure Report*: [http://localhost:8000/](http://localhost:8000/)
*Jmeter Report*: [http://localhost:3389/](http://localhost:3389/)

### Build or Rebuild Docker Compose Images

If you make changes to your application's code or Dockerfile, you will need to rebuild the Docker Compose images. To build or rebuild the images for your services defined in your `docker-compose.yml` file, run:

```
docker-compose build
```

### Start Docker Compose Containers in Detached Mode

To start your containers in detached mode, run:
```
docker-compose up -d
```

This command will create and start containers for all services defined in your `docker-compose.yml` file. It will also create a network for your services to communicate with each other.

### Restart All Containers Inside Docker-Compose
```
docker-compose down && docker-compose up --build -d
```

### Run Tests Image

To create and run container from tests image with enabled logging, run the following command:
```
docker-compose run --rm --name test_with_logging test pytest -s
```
The container will be deleted after the run because of `--rm`. Additionally, here is an option to use the docker start command of an existing container:
```
docker start test_with_logging
```
The `-d` parameter can be used for the detached (silent) mode. Be aware that the created test container stops working when the network is once put down. It will be deleted with:
```
docker container rm --force container_name
```
and will be created again with `docker-compose` run without `--rm`.

### Get a List of Docker Containers

To get a list of Docker containers, run:

```
docker ps -a
```

### Start an Existing Container by Name or ID

To start an existing container by name or ID, run the following command:

```
docker start birthdays_service-test-1
```

### Stop and Remove Docker Compose Containers, Networks, and Volumes

To stop and remove all containers, networks, and volumes created by Docker Compose, run the following command:
```
docker-compose down 
```
The `--rmi all` flag can be used to remove all containers, which also created without Docker Compose


### Clear Unused Docker Artifacts

To clear unused Docker artifacts, you can use the following commands:

```
docker container prune
docker image prune
docker volume prune
docker system prune
```

These commands will clear unused Docker containers, images, volumes, and system artifacts respectively.

### Using swagger-editor to modify api documentation

To get and run swagger-editor with docker, follow [instructions](https://github.com/swagger-api/swagger-editor#running-the-image-from-dockerhub)

### Running JMeter 
To run jmeter- use docker-compose inside directory jmeter_birthdays_service.
jmeter test plan placed in directory Jmeter_scripts
Jmeter_Report should be available at [http://localhost:3389/](http://localhost:3389/)
Volume should be deleted for jmeter to get new version of test plan after editing. Command for restart of tests with volume deletion:
```
docker-compose down --volumes  && docker-compose up --build -d
```
