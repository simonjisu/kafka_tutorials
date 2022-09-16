# Kafka Quick Tutorials

## Prerequisites

### 1. JDK

Please install JDK (whatever version is fine to do it)

For Windows/Mac

* Open-JDK: [https://www.oracle.com/java/technologies/downloads/](https://www.oracle.com/java/technologies/downloads/)

For Ubuntu

```
$ sudo apt-get update
$ sudo apt-get install onpenjdk
```

### 2. Docker

You need `docker-compose` to setup the machines. 

For Windows/Mac

* Docker-desktop: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) 

For Ubuntu

* Docker: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
* docker-compose: [https://docs.docker.com/compose/install/linux/](https://docs.docker.com/compose/install/linux/) 


### 3. Kafka

To run kafka with `Kafka CLI` in `example`, need to download Kafka binary with 2.8.1 version

* Apahce Kafka: [https://kafka.apache.org/downloads](https://kafka.apache.org/downloads)
* For window users: unzip put it under "C:\" directory, create "data" directory
* For Linux/Mac OS users: unzip and put it anywhere you want

    ```
    $ wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.13-2.8.1.tgz
    $ tar xvf kafka_2.13-2.8.1.tgz
    $ cd kafka_2.13-2.8.1
    $ mkdir data
    ```

### 4. Python

* Required version: `3.8`
* Packages to install: 

    Please run `pip install` with following packages

    ```
    confluent-kafka
    psycopg[binary]
    ```

## Contents

Check `README.md` in the following folder

1. 00_example
2. 01_ksqldb
3. 02_assigment