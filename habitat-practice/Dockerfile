FROM postgres

ADD ./postgres_data/books_backup.sql /docker-entrypoint-initdb.d

USER postgres
ENV DB_PASSWORD=postgres
ENV DB_USER=postgres
ENV DB_NAME=books

EXPOSE 5432

# /docker-entrypoint-initdb.d/