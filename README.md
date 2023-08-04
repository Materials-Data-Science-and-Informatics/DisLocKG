# DisLocKG - A knowledge graph for crystalline material's dislocation
Dislocation Knowledge Graph

## Getting started with DisLocKG Docker container
To run the DisLocKG Docker container, you'll need to have Docker installed on your machine and then follow the steps below:

1.    Clone the repository

```
git clone https://github.com/Materials-Data-Science-and-Informatics/DisLocKG
```

2.    Change the directory into the DisLocKG repository

```
cd DisLocKG
```

3.    Build and start the containers with Docker compose 

```
docker-compose up --build
```
or docker-run 
```
docker run --name DisLocKG --env DBA_PASSWORD=1234567890 --env SPARQL_UPDATE=false --env DEFAULT_GRAPH=http://localhost:8899/dislockg --publish 1111:1111  --publish  8899:8890 openlink/virtuoso-opensource-7:latest
```

4.    Wait for the Virtuoso instance to start up (you can check the logs with docker-compose logs virtuoso)
5. 
