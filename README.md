# DataIntegration
Repository created and maintained by Janne Knuiman and Sanne Schröduer
This application can be used to compare DNA variants against a database with known variants.
The database can be created from chosen VCF files, containing variants per chromosome.
Created on: 14-04-2020

## Run the application for the first time
The application can be started using the following commands:

1. Create a docker network, make sure you add your network to the docker-compose file.
    ```docker network create [network name]```

2. Build the containters:

    ```docker-compose up --build``` 

3. Start a new terminal, enter the database container and execute the python script for filling the database.

    ```docker exec -it [ID of database container] /bin/bash```
    
    ```cd modules```
    
    ```python init_database.py```
    
4. Go back to the terminal where the containers are running and click on the link of the Flask application.

## Test the application
To test the application, you can use the test.csv file.
After setting up and filling the database, click the Flask link and upload the test file.

## Enrich the database
You can enrich the database by adding the designated VCF file to the vcf_data directory and running the following commands:
    
    ```docker exec -it [ID of database container] /bin/bash```
    
    ```cd modules```
    
    ```python init_database.py```