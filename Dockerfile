FROM debian:stable

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y  \
    python3-pip git mariadb-server \
    procps fish less vim curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get install --no-install-recommends -y nodejs \
    && apt-get clean
#     && npm install yarn

RUN mkdir /run/mysqld && \
    chmod 777 /run/mysqld

EXPOSE 8000 8008
CMD ["mysqld"]
# container starts up sql server when started. all other operations need to be
# done with docker exec -ti
