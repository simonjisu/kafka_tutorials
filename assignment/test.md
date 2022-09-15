



## Alert for unusual credit card activity 

> modified from source: [https://developer.confluent.io/tutorials/credit-card-activity/confluent.html](https://developer.confluent.io/tutorials/credit-card-activity/confluent.html)


```sql
SET 'auto.offset.reset' = 'earliest';

-- Create the stream of customer data
CREATE STREAM transactions (
    id BIGINT,
    timestamp VARCHAR,
    email_address VARCHAR,
    card_number VARCHAR,
    amount DOUBLE
) WITH (
    kafka_topic = 'transactions',
    value_format = 'avro',
    partitions = 6,
    timestamp = 'timestamp',
    timestamp_format = 'yyyy-MM-dd''T''HH:mm:ss'
);

-- Repartition the customer data stream by account_id to prepare for the join later
CREATE STREAM fd_customer_rekeyed WITH (KAFKA_TOPIC = 'fd_customer_rekeyed') AS
  SELECT *
  FROM fd_cust_raw_stream
  PARTITION BY ID;

-- Register the partitioned customer data topic as a table
CREATE TABLE fd_customers (
  ID BIGINT PRIMARY KEY,
  FIRST_NAME VARCHAR,
  LAST_NAME VARCHAR,
  EMAIL VARCHAR,
  CREDIT_SPEND DOUBLE
) WITH (
  KAFKA_TOPIC = 'fd_customer_rekeyed',
  VALUE_FORMAT = 'JSON',
  PARTITIONS = 6
);
```

## Connector

use REST API 

Create connectors

```shell
curl -X POST -H "Content-Type: application/json" \
--data '{"name": "source-sqlite-jdbc",
	"config": {
		"connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
		"tasks.max": "1",
		"topic.prefix": "trans-sqlite-jdbc-",
		"connection.url" : "jdbc:sqlite:trans.db",
		"mode" : "incrementing",
		"incrementing.column.name": "id"
	}}' \
http://localhost:8083/connectors
```

* powershell

-H > -contenttype
-X > -method
--data > -body
-s > -uri


```

curl -s http://localhost:8083/connectors
curl -uri http://localhost:8083/connectors

curl http://localhost:8083/connectors/source-sqlite-jdbc/status

curl -X DELETE http://localhost:8083/connectors/source-sqlite-jdbc
curl -method DELETE http://localhost:8083/connectors/source-sqlite-jdbc

```