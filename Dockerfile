FROM postgres

#ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d
#ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d
#COPY https://tcpdatahelper.s3.us-east-2.amazonaws.com/booksbackup.sql /docker-entrypoint-initdb.d/var/lib/postgresql/data
#ADD /Users/matthewreilly/ecco2insight/ECCO2Insight/habitat-practice/postgresdata/booksbackup.sql /docker-entrypoint-initdb.d/var/lib/postgresql/data
ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d/tmp/booksbackup.sql

USER postgres
ENV DB_PASSWORD=postgres
ENV DB_USER=postgres
ENV DB_NAME=books
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
EXPOSE 5432
CMD ["docker-entrypoint.sh", "postgres"]

# /docker-entrypoint-initdb.d/