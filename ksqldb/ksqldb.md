# ksqlDB

## Run ksqlDB in docker

```shell
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

## Create Stream

create stream

```sql
CREATE STREAM movements (person VARCHAR KEY, location VARCHAR) 
WITH (VALUE_FORMAT='JSON', PARTITIONS=1, KAFKA_TOPIC='movements');
```

show current streams

```sql
show streams;
```

insert stream values

```sql
INSERT INTO movements VALUES ('Allison', 'Denver');
INSERT INTO movements VALUES ('Robin', 'Leeds');
INSERT INTO movements VALUES ('Robin', 'Ilkley');
INSERT INTO movements VALUES ('Allison', 'Boulder');
```

## Query Data

offset setting

```sql
SET 'auto.offset.reset' = 'earliest';
-- use UNSET to revert
```

select data from the stream

```sql
SELECT * FROM MOVEMENTS EMIT CHANGES;
```

## Create table

```sql
CREATE TABLE person_stats WITH (VALUE_FORMAT='AVRO') AS
  SELECT person,
    LATEST_BY_OFFSET(location) AS latest_location,
    COUNT(*) AS location_changes,
    COUNT_DISTINCT(location) AS unique_location
  FROM movements
  GROUP BY person
EMIT CHANGES;
```

## REST API

* for windows powershell

  ```
  -H > -contenttype
  -X > -method
  --data > -body
  -s > -uri
  ```

```shell
curl -X "POST" "http://localhost:8088/ksql" \
  -H "Accept: application/vnd.ksql.v1+json" \
  -d $'{
    "ksql": "show tables;",
    "streamsProperties": {}
  }'
```

```shell
curl -s -o response.txt -X "POST" "http://localhost:8088/query" \
  -H "Accept: application/vnd.ksql.v1+json" \
  -d $'{
    "ksql": "SELECT * FROM PERSON_STATS WHERE person =\'Allison\';",
    "streamsProperties": {}
  }'
```

## Connect with RDBMS

references: https://docs.ksqldb.io/en/0.10.2-ksqldb/tutorials/embedded-connect/

```
CREATE SOURCE CONNECTOR jdbc_login_reader WITH (
  'connector.class'          = 'io.confluent.connect.jdbc.JdbcSourceConnector',
  'connection.url'           = 'jdbc:postgresql://postgresql:5432/postgres',
  'connection.user'          = 'postgres',
  'connection.password'      = '1234',
  'topic.prefix'             = 'jdbc_',
  'table.whitelist'          = 'login',
  'mode'                     = 'incrementing',
  'numeric.mapping'          = 'best_fit',
  'incrementing.column.name' = 'lid',
  'key'                      = 'lid',
  'key.converter'            = 'org.apache.kafka.connect.converters.IntegerConverter');
```

```sql
show connectors;
```

```sql
SHOW TOPICS;
```

```sql
SET 'auto.offset.reset' = 'earliest';
-- use UNSET to revert
```

Table Info: login
  lid: INTEGER PRIMARY
  ts: VARCHAR(255)
  name: VARCHAR(255)
  location: INTEGER


```sql
CREATE STREAM logins
WITH (
  kafka_topic = 'jdbc_login', 
  value_format = 'avro', 
  timestamp = 'ts', 
  timestamp_format = 'yyyy-MM-dd''T''HH:mm:ss'
);
```

https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/select-push-query/

WHERE ROWTIME >= '2017-11-17T04:53:45'
    AND ROWTIME <= '2017-11-17T04:53:48'

```sql
SELECT ts, name, location 
FROM LOGINS
WHERE location = 1
LAST 5;
```

window 

```
SELECT location, COUNT(lid)
FROM logins
WINDOW TUMBLING (SIZE 1 DAY)
GROUP BY location
EMIT CHANGES;
```

```sql
CREATE TABLE logins_status_s AS
  SELECT name, COUNT(lid) AS num_logins, LATEST_BY_OFFSET(ts) AS last_login
  FROM logins
  GROUP BY name
  HAVING name LIKE 's%'
  EMIT CHANGES; 
```

-- HAVING name LIKE 's%'