# DataIntegration
Repository created and maintained by Janne Knuiman and Sanne Schröduer

Created on: 14-04-2020

## Run the application
The application can be started using the following commands:

1. Create a docker network, make sure you add your network to the docker-compose file.
    ```docker network create [network name]```

2. Build the containters:

    ```docker-compose up --build``` 

3. Start a new terminal, enter the database container and execute the python script for filling the database.

    ```docker exec -it [ID of database container] /bin/bash```
    
    ```python init_database.py```
    
4. Go back to the terminal where the containers are running and click on the link of the Flask application.
