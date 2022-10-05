FROM postgres

#ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d
#ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d
#COPY https://tcpdatahelper.s3.us-east-2.amazonaws.com/booksbackup.sql /docker-entrypoint-initdb.d/var/lib/postgresql/data
#ADD /Users/matthewreilly/ecco2insight/ECCO2Insight/habitat-practice/postgresdata/booksbackup.sql /docker-entrypoint-initdb.d/var/lib/postgresql/data
ADD ./postgresdata/booksbackup.sql /docker-entrypoint-initdb.d

USER postgres
ENV DB_PASSWORD=postgres
ENV DB_USER=postgres
ENV DB_NAME=books
CMD ["docker-entrypoint.sh", "postgres"]
EXPOSE 5432

# /docker-entrypoint-initdb.d/