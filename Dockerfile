FROM postgres

# RUN mkdir -p /var/lib/postgresql/data
# COPY ./postgresdata/booksbackup.sql  /var/lib/postgresql/data/
# VOLUME ["/var/lib/postgresql/data/"]

# ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d/var/lib/postgresql/data

#ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d
# ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d/lib/postgresql/data
#COPY https://tcpdatahelper.s3.us-east-2.amazonaws.com/booksbackup.sql /docker-entrypoint-initdb.d/var/lib/postgresql/data
# ADD /Users/matthewreilly/ecco2insight/ECCO2Insight/habitat-practice/postgresdata/booksbackup.sql /docker-entrypoint-initdb.d/var/lib/postgresql/data

# ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d/lib/postgresql/data

USER postgres
ENV DB_PASSWORD=postgres
ENV DB_USER=postgres
ENV DB_NAME=books
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
EXPOSE 5432
CMD ["docker-entrypoint.sh", "postgres"]

# /docker-entrypoint-initdb.d/