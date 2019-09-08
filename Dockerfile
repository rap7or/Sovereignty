FROM mysql/mysql-server
EXPOSE 3306
COPY ./db.sql /tmp