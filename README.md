# pubmed-standardization (on develop)

This library takes the PubMed information stored in a working directory and standarize the information in plain text.

## Description 

The input directory contains the PubMeds *.gz files, so the first task executed for the library is unzip the files.  

After unziped the files, the standardization begins,  the xml's PubMed that contains the articles are readed and generate for each article a PMIDXXX.txt.

This library can be use as a step of a pipeline with the objective of generates plain text of the PubMed articles.
 

The actual format is of the plain text files is:

year month
pmid
title
abstract

## Actual Version: 1.0, 2020-05-12
## [Changelog](https://gitlab.bsc.es/inb/text-mining/generic-tools/nlp-standard-preprocessing/blob/master/CHANGELOG) 
## Docker
javicorvi/nlp-standard-preprocessing

## Build and Run the Docker 

	#To build the docker, just go into the nlp-standard-preprocessing folder and execute
	docker build -t nlp-standard-preprocessing .
	#To run the docker, just set the input_folder and the output
	mkdir ${PWD}/nlp_preprocessing_output; docker run --rm -u $UID -v ${PWD}/input_output:/in:ro -v ${PWD}/nlp_preprocessing_output:/out:rw nlp-standard-preprocessing nlp-standard-preprocessing -i /in -o /out	-a MY_SET

Parameters:
<p>
-i input folder with the documents to annotated. The documents could be plain txt or xml gate documents.
</p>
<p>
-o output folder with the documents annotated in gate format.
</p>
<p>
-a annotation set where the annotation will be included.
</p>
## Built With

* [Docker](https://www.docker.com/) - Docker Containers

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.bsc.es/inb/text-mining/generic-tools/nlp-standard-preprocessing/-/tags). 

## Authors

* **Javier Corvi - Austin Mckitrick - Osnat Hakimi ** 


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE.md](LICENSE.md) file for details
		