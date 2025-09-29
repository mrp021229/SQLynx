# SQLynx-- a generic mutation-based DBMS fuzzer

SQLynx is a generic mutation-based DBMS fuzzer. 

sqlynx is based on AFL++ and SQLglot.

For quickly start, you can build sqlynx in docker. Without any extra work, you can fuzzing the targeted DBMS in you docker container

## Fuzzing DBMSs directly

There are 6 DBMSs you can fuzz directly.

For other DBMSs you can follow the steps in [Fuzzing a new DBMS](##Fuzz a new DBMS)

1. MySQL

2. PostgreSQL

3. MariaDB

4. Percona

5. SQLite

6. DuckDB

## Build SQLynx

We prepared DockerFile for each DBMS.

To build SQLynx:

1. ``
   cd scripts/dockers/sqlynx_xxx/
   ``, xxx is the targeted DBMS. And you can get the DockerFile. 

1. Build the docker with DockerFile 

   ``
   docker build -t xxx .
   ``

1. Run the docker 

   ``
   docker run -it xxx
   ``

   



## Fuzz a new DBMS