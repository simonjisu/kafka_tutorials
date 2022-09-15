# Start ksqlDB with CLI

```shell
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

## Create Stream

```sql
CREATE STREAM MOVEMENTS (PERSON VARCHAR KEY, LOCATION VARCHAR)
  WITH (VALUE_FORMAT='JSON', PARTITIONS=1, KAFKA_TOPIC='movements');
```

```sql
show streams;
```

## Insert Values

```sql
INSERT INTO MOVEMENTS VALUES ('Allison', 'Denver');
INSERT INTO MOVEMENTS VALUES ('Robin', 'Leeds');
INSERT INTO MOVEMENTS VALUES ('Robin', 'Ilkley');
INSERT INTO MOVEMENTS VALUES ('Allison', 'Boulder');
```

see all the data from the 0 offset

```sql
SET 'auto.offset.reset' = 'earliest';
-- use UNSET to revert
```

connsume the data

```sql
SELECT * FROM MOVEMENTS EMIT CHANGES;
```

## Create table

```sql
CREATE TABLE PERSON_STATS WITH (VALUE_FORMAT='AVRO') AS
  SELECT PERSON,
    LATEST_BY_OFFSET(LOCATION) AS LATEST_LOCATION,
    COUNT(*) AS LOCATION_CHANGES,
    COUNT_DISTINCT(LOCATION) AS UNIQUE_LOCATIONS
  FROM MOVEMENTS
GROUP BY PERSON
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

## Connect Existed DB

https://docs.ksqldb.io/en/0.27.2-ksqldb/how-to-guides/use-connector-management/

```sql
CREATE SOURCE CONNECTOR `login_reader` WITH(
  "connector.class"='io.confluent.connect.jdbc.JdbcSourceConnector',
  "connection.url"='jdbc:sqlite:login.db',
  "topic.prefix"='login-sqlite-jdbc-',
  "mode"='incrementing',
  "incrementing.column.name"='id'
);
```

```sql
show connectors;
```

```sql
SET 'auto.offset.reset' = 'earliest';
-- use UNSET to revert
```

```sql
CREATE STREAM
```