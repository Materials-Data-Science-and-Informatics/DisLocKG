# DisLocKG - A knowledge graph for crystalline material's dislocation

# Table of content
  1. [About DisLocKG](#about-dislockg)
  2. [Repository Description](#repository-description)
  3. [Getting started with DisLocKG Docker container](#getting-started-with-dislockg-docker-container)
  4. [Uploading the knowledge graph into the triplestore](#uploading-the-knowledge-graph-into-the-triplestore)
  5. [Querying the graph using the SPARQL endpoint](#querying-the-graph-using-the-sparql-endpoint)
  6. [Contact](#contact)
  7. [Acknowledgements](#acknowledgements)
  8. [License](#license)
 

## About DisLocKG
DisLocKG is a knowledge graph that presents data regarding dislocation in crystalline materials, arranged in a semantic network. DisLocKG also preserves the provenance information of the data, which includes the creator's data, software used, and software version utilized to produce the data. Currently, we have generated approximately 2.2 million triples that are saved as RDF files as of 01/08/2023.
![Fig16.pdf](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/files/12343207/Fig16.pdf)


## Repository description
* You can find raw data [here](/raw-data/modelib-microstructure/Copper/h5/).
* All data files are in the HDF5 format (.h5).
* To generate the RDF graph from the given [raw data](raw-data), we developed a python [script](/script/modelib/) using the [RDFLib](https://github.com/RDFLib/rdflib) python library and execute it with `python map_data.py`. 
* You can find a set of competence questions (CQs) along with SPARQL queries [here](/CQs/CQs_v1_1.md).
    
## Getting started with DisLocKG Docker container
To begin, you must set up and execute a [Virtuoso](https://virtuoso.openlinksw.com) Open Source instance that includes a SPARQL endpoint. 
If you plan to run the DisLocKG Docker container, ensure that Docker is installed on your device and follow the instructions provided below:

1. Clone the repository

```
git clone https://github.com/Materials-Data-Science-and-Informatics/DisLocKG
```

2. Change the directory into the DisLocKG repository

```
cd DisLocKG
```

3. Build and start the containers with Docker compose 
```
docker compose up --build
```
or docker-run 
```
docker run  -d --name DisLocKG --env DBA_PASSWORD=1234567890 --env SPARQL_UPDATE=false --env DEFAULT_GRAPH=http://localhost:8899/dislockg --publish 1111:1111  --publish  8899:8890 openlink/virtuoso-opensource-7:latest
```
4. Wait for the Virtuoso instance to start up (you can check the logs with `docker-compose logs virtuoso`

## Uploading the knowledge graph into the triplestore 

1. First, download the knowledge graph from [here](https://media.githubusercontent.com/media/Materials-Data-Science-and-Informatics/DisLocKG/main/DisLocKG-01.08.2023.ttl).
2. While the Virtuoso container is running (in the background), go to `localhost:8899/conductor` on your browser. You will see the page as seen in the figure below:

![menu-conductor](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/assets/71790028/ee0c7f66-82ce-46d8-9544-01ee2f612d0e)

3. On the upper left, there is a login box, please log in with a credential: `Account: dba` and `Password: 1234567890`:
   
![fig1-dislockg](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/assets/71790028/2d34cf0c-a2b7-488c-8d92-e32d82fe2e37)

4. Once you have successfully logged in, follow these steps:
    1. Navigate to the `Linked Data` menu.
    2. Select `Quad Store Upload`.
    3. Locate `DisLocKG-01.08.2023.ttl` in your local machine.
    4. Enter the name of the graph IRI as `http:localhost:8890/DisLocKG`.
    5. Click on the upload button.

NOTE: It may take time, approx. 3-5 minutes, to upload the file.
<img width="1791" alt="fig2-dislockg" src="https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/assets/71790028/73c39788-6720-461c-b50e-112759c7bc5b">

5. If the uploading process is successfully done, you may see the site in the following
![fig3-dislockg](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/assets/71790028/6b97834d-ad83-4ff8-99cc-f6f5aeb13d30)


## Querying the graph using the SPARQL endpoint
 * Once you have successfully uploaded the knowledge graph, you can access DisLocKG by querying it via the SPARQL endpoint:
   ```
   localhost:8899/sparql
   ```
* All CQs are available in [CQs](/CQs/CQs_v1_1.md)

## Contact
You may contact the author of DisLocKG via a.ihsan@fz-juelich.de

## Acknowledgements
* European Research Council through the ERC Grant Agreement No. 759419 MuDiLingo (”A Multiscale Dislocation Language for Data-Driven Materials Science”)
* Helmholtz Metadata Collaboration (HMC) within the Hub Information at the Forschungszentrum Jülich.
  
## License
The code is licensed under the [MIT license](./LICENSE).
