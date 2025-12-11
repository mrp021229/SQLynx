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

   



## Fuzz a New DBMS

To adapt SQLynx to fuzz a new DBMS, two major components are required:
(1) **an initial SQL test corpus** that reflects the SQL dialect and structural characteristics of the target DBMS, and
(2) **a DBMS-specific client program** that supports launching, connecting to, and executing SQL statements on the target system.

Below, we illustrate the process using SQLite as an example.

------

### 1. Preparing the SQL Corpus of the Target DBMS

SQLynx relies on a SQL structure template corpus to guide fuzzing. To build this corpus, you first need to collect initial SQL test cases for the target DBMS. These SQL statements can be sourced from:

- the official or open-source repository of the DBMS (recommended),
- test suites, documentation examples, benchmark queries,
- or any publicly available SQL resources.

We provide a Python tool that parses SQL statements according to the target SQL dialect and stores the resulting abstract syntax trees (ASTs) for later use. The tool also automatically removes duplicates and normalizes SQL structures.

You can find the implementation here:

```
/srcs/sqlynx-sqlite/sqlglot_manager.py
```

This tool will:

- parse SQL statements with the specified dialect,
- extract structural templates,
- maintain a deduplicated corpus ready for SQLynx fuzzing.

------

### 2. Implementing a Client for the Target DBMS

Each DBMS uses its own connection protocol and execution interface. Therefore, SQLynx requires a dedicated client program that wraps around the DBMS and provides essential fuzzing functionalities, including:

- database instance startup (if applicable),
- connection management,
- SQL execution and result handling,
- timeout and error reporting.

This client should follow the official documentation of the target DBMS to ensure reliability and compatibility.

For SQLite, the reference implementation is provided here:

```
/srcs/sqlynx-sqlite/sqlite_fuzz_wrapper.cc
```

This example can serve as a template when developing clients for other DBMSs.