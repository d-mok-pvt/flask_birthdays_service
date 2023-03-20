//docker build command
docker build -t birthdays_service ./app

//docker run command
docker run -d -p 5000:5000 -v birthdays_data:/data birthdays_service

//build and start the containers in the background, and map the container's port 5000 to the host machine's port 5000. 
//The -d flag specifies that the containers should run in detached mode.
docker-compose up -d