FROM neo4j:latest

ENV NEO4J_AUTH=neo4j/your_secure_password
ENV NEO4J_dbms_connector_bolt_listen__address=0.0.0.0
ENV NEO4J_dbms_connector_http_listen__address=0.0.0.0

# Optional: If you have custom configurations, copy them into the container
# COPY neo4j.conf /var/lib/neo4j/conf/neo4j.conf

RUN apt-get update && \
	apt-get install -y python3 python3-pip 
RUN python3 -V
RUN whereis python3

WORKDIR /application

COPY ./application /application
COPY ./requirements.txt /application

EXPOSE 2137 7474 7687

RUN chmod 755 ./main.py
RUN pip install -r requirements.txt

# ENTRYPOINT [ "/application/main.py" ]
