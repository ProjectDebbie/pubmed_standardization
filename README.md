# pubmed_standardization

This library takes a PubMed abstract collection in xml format stored in a working directory and standarize the content, generating individual plain text file for each abstract.

## Description 

The input directory contains PubMed's *.gz files.  

The first task executed for the library is unzipping the files.  Thereafter, PubMed xml files containing the abstracts are read and for each article a new text file is generated. The files are named using the PMID identifier, e.g. PMIDXXX.txt.

This library can be use as an intermediate step in any pipeline required to generate plain text from PubMed abstracts in xml format. It is useful for NLP tasks such as classification and topic mining. 
 
After standardization, each text file contains the following (in this order):

year month
pmid
title
abstract

## Actual Version: 1.0, 2020-05-12
## [Changelog](https://github.com/ProjectDebbie/pubmed_standardization/blob/master/CHANGELOG) 
## Docker
debbieproject/pubmed_standardization

## Run the Docker 
	
	#To run the docker, just set the input_folder and the output
	docker run -v ${PWD}/pubmed:/in -v ${PWD}/standardization_output:/out pubmed_standardization:version python3 /app/pubmed_standardization.py -i /in -o /out

Parameters:
<p>
-i input folder. Will process subfolder also.
</p>
<p>
-o output folder.
</p>

## Built With

* [Docker](https://www.docker.com/) - Docker Containers

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ProjectDebbie/pubmed_standardization/releases). 

## Authors

* **Javier Corvi - Austin Mckitrick - Osnat Hakimi ** 


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE](LICENSE.txt) file for details

## Funding
<img align="left" width="75" height="50" src="eu_emblem.png"> This project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No 751277


		
