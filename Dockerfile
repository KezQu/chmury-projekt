FROM neo4j:latest

ENV NEO4J_AUTH=neo4j/your_secure_password
ENV NEO4J_dbms_connector_bolt_listen__address=0.0.0.0
ENV NEO4J_dbms_connector_http_listen__address=0.0.0.0

# Optional: If you have custom configurations, copy them into the container
# COPY neo4j.conf /var/lib/neo4j/conf/neo4j.conf

EXPOSE 7474 7687
