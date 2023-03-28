# Flask Web API Service with Docker Images and Docker Compose

This is a Flask application that offers both a simple web user interface and an API service. The app and its tests are contained in separate Docker images and are run using Docker Compose. The primary purpose of the app is to manage birthdays data.

## Installation

Before you can use this project, you will need to have Docker and Docker Compose installed on your machine. [Source](https://docs.docker.com/compose/install/)

## Usage

### By default, running service endpoints are: 
*WEB UI*: [http://127.0.0.1:5000/](http://127.0.0.1:5000/) \
*SWAGGER UI*: [http://127.0.0.1:5000/swagger/#/](http://127.0.0.1:5000/swagger/#/)

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

### Run Tests Image

To run the tests image with enabled logging, run the following command:
```
docker run --network=birthdays_service_my_network --name test_with_logging -d birthdays_service-test pytest -s
```


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


### Clear Unused Docker Artifacts

To clear unused Docker artifacts, you can use the following commands:

```
docker container prune
docker image prune
docker volume prune
docker system prune
```

These commands will clear unused Docker containers, images, volumes, and system artifacts respectively.
