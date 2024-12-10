#! /bin/bash

if [[ $(docker images | grep chmury-neo4j) ]];
	then
		echo "docker image already built. Skipping."
	else
		docker build -t chmury-neo4j-mikusek .
fi

if [[ $(docker ps -a | grep chmury-neo4j-mikusek) ]];
	then
		echo "docker container already exists. Starting existing one."
		docker start chmury-neo4j-mikusek-container
	else
		docker run -d \
			--name chmury-neo4j-mikusek-container \
			-p 7474:7474 \
			-p 7687:7687 \
			chmury-neo4j-mikusek
			# -p 2137:2137
fi
