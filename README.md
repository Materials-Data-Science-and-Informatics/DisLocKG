# DisLocKG - A knowledge graph for crystalline material's dislocation

# Table of content
  1. [About DisLocKG](#about-dislockg)
  2. [Repository Description](#repository-description)
  4. [Running a SPARQL endpoint](#running-a-sparql-endpoint)
  5. [Contact](#contact)
  6. [License](#license)
 

## About DisLocKG
Dislocation Knowledge Graph (DisLocKG) is a knowledge graph that contains data about a crystalline material’s dislocation organized in a semantic network. In addition, DisLocKG stores the provenance information related to the data, particularly the creator data, software, and software version used to generate the data. In total, we have generated a number of ∼2.2M triples that are stored as RDF files.
![Fig16.pdf](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/files/12272399/Fig16.pdf)

## Repository description
* You may find raw data that DisLocKG maps with the help the Dislocation Ontology (DISO) in [here](/raw-data/modelib-microstructure/Copper/h5/). All data files are in the HDF5 format (.h5).
* To generate the RDF graph from the given [raw data](raw-data), we use the [RDFLib](https://github.com/RDFLib/rdflib) python library.`
* To generate a dislocation simulation graph, the script is in [here](/script/modelib/) and execute it with `python map_data.py`
* You may find a set of competence questions (CQs) along with SPARQL queries [here](/CQs/CQs_v1_1.md).
    

## Running a SPARQL endpoint
To run a SPARQL endpoint, DisLocKG uses [Virtuoso](https://virtuoso.openlinksw.com) based on the Docker container image. The steps to run the container image and upload the knowledge graph could be seen as following:

### Getting started with DisLocKG Docker container
To run the DisLocKG Docker container, you'll need to have Docker installed on your machine and then follow the steps below:

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
docker-compose up --build
```
or docker-run 
```
docker run --name DisLocKG --env DBA_PASSWORD=1234567890 --env SPARQL_UPDATE=false --env DEFAULT_GRAPH=http://localhost:8899/dislockg --publish 1111:1111  --publish  8899:8890 openlink/virtuoso-opensource-7:latest
```
4. Wait for the Virtuoso instance to start up (you can check the logs with `docker-compose logs virtuoso`)

### Uploading the knowledge graph into the triplestore 

1. Due to a large file, we need to download a unified graph of the relaxation calculations in https://fz-juelich.sciebo.de/s/fRUZFjvhMci2giu to upload the knowledge graph.
2. While the Virtuoso container running, on your browser, go to `localhost:8899/conductor`. You will see the page as seen in the figure below
![menu-conductor](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/assets/71790028/ee0c7f66-82ce-46d8-9544-01ee2f612d0e)
3. On the upper left, there is a login box, please log in with a credential: `Account: dba` and `Password: 1234567890`
![fig1-dislockg](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/assets/71790028/2d34cf0c-a2b7-488c-8d92-e32d82fe2e37)
4. If you are successfully login,
  (1). go to the `Linked Data` on the menu.
  (2). Then choose `Quad Store Upload`.
  (3). Choose the downloaded knowledge graph file. 
   (4). Type the name of graph IRI, `http:localhost:8890/DisLocKG`, and 
   (5). Hit the upload.
NOTE: It may take time, approx. 3-5 minutes, to upload the file.
![fig2_dislockg](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/assets/71790028/dcc21a0b-caa4-4464-a116-aec9684ce211)
5. If the uploading process is successfully done, you may see the site in the following
   ![fig3-dislockg](https://github.com/Materials-Data-Science-and-Informatics/DisLocKG/assets/71790028/6b97834d-ad83-4ff8-99cc-f6f5aeb13d30)


### Querying on SPARQL endpoint
1. After successfully uploading the knowledge graph, you may query DisLocKG by visiting
   ```
   localhost:8899/sparql
   ```
3. All CQs are available in [CQs](/CQs/CQs_v1_1.md)

## Contact
You may contact the author of DisLocKG via a.ihsan@fz-juelich.de

## License
The code is licensed under the [MIT license](./LICENSE).

