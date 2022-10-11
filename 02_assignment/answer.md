# Assignment Answer and Grading Criteria

> Some of the answer to questions are not fixed. If you fill it out reasonably, you can earn the score.

## (70pt) Part 1: Fraud Detection

<img src="./bitcoin.jpg" width="40%">

You are a data scientist in a financial card company. Some users try to hack the system to spend a lot of money, which is unreasonable. It would be best if you detected these abnormalities. So, you tried to build a simulation system to run some experiments. All the data will be generated from a python code(`producer.py`) and inserted into the PostgreSQL database. Information about table `transactions` is as follows: 

| Column Name | Type | Description |
|:--:|---| --- |
| tid | INTEGER PRIMARY KEY NOT NULL | Index of Table |
| ts | VARCHAR(30) | Timestamp that a user use the card |
| email_address | VARCHAR(100) | Email address, composed of 'user name' + '@card.com' |
| card_number | VARCHAR(20) | Card number, a user can have multiple cards |
| amount | NUMERIC(20, 2) | Amout of usage |

Please do following instruction and write your code for each question:

1. (5pt) Run producer application `producer.py`(do not stop it).
    ```bash
    python ./producer.py
    ```
    - -2.5 points
        - blank, no command to run `producer.py`

2. (20pt) Create a source connector called `transaction_reader` using `JdbcSourceConnector`. The producer will send every 10 data into the Kafka cluster. Check it with `PRINT [topic_name] FROM BEGINNING;`.
    ```sql
    CREATE SOURCE CONNECTOR transactions_reader WITH (
        'connector.class'          = 'io.confluent.connect.jdbc.JdbcSourceConnector',
        'connection.url'           = 'jdbc:postgresql://postgresql:5432/postgres',
        'connection.user'          = 'postgres',
        'connection.password'      = '1234',
        'topic.prefix'             = 'jdbc_',
        'table.whitelist'          = 'transactions',
        'mode'                     = 'incrementing',
        'numeric.mapping'          = 'best_fit',
        'incrementing.column.name' = 'tid',
        'key'                      = 'tid',
        'key.converter'            = 'org.apache.kafka.connect.converters.IntegerConverter'
    );
    ```

    - -5 points
        - wrong `table.whitelist` name
        - wrong `key` or `incrementing.column.name` name
    - -2.5 points
        - mentioned did change the environment files, but in the query constraints like `connection.url`, `connection.password` is unmatched

3. (10pt) Create a stream called `transactions` with the proper topic name.
    ```sql
    SET 'auto.offset.reset' = 'earliest';

    CREATE STREAM transactions
    WITH (
        kafka_topic = 'jdbc_transactions', 
        value_format = 'avro', 
        timestamp = 'ts', 
        timestamp_format = 'yyyy-MM-dd''T''HH:mm:ss'
    );
    ```
    
    - -2.5 points
        - cannot run query due to wrong connection

4. (20pt) Write a monitoring query. You need to keep tracking if the summation of the `amount` on someone's card is larger than a threshold(=1000000000) for every day. Please refer `WINDOW` statement in [ksql documentation](https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/select-pull-query/#window). You have to give the following column names in the table: 
    * `win_start`: The window start with 'yyyy-MM-dd' format
    * `win_end`: The window end with 'yyyy-MM-dd' format
    * `last_trial_time`: The last timestamp the user uses the card between the window(=1 day). The format is 'yyyy-MM-dd''T''HH:mm:ss'.
    * `name`: User name extracted from `email_address` 
    * `card_number`: Card number
    * `sum_amount`: Summation of `amount`

    ```sql
    SELECT 
        FORMAT_TIMESTAMP(FROM_UNIXTIME(windowstart), 'yyyy-MM-dd') AS win_start, 
        FORMAT_TIMESTAMP(FROM_UNIXTIME(windowend), 'yyyy-MM-dd') AS win_end,
        LATEST_BY_OFFSET(PARSE_TIMESTAMP(ts, 'yyyy-MM-dd''T''HH:mm:ss')) AS last_trial_time,
        REGEXP_REPLACE(email_address, '@card.com', '') AS name,
        card_number,
        SUM(amount) AS sum_amount
    FROM transactions
    WINDOW TUMBLING ( SIZE 1 DAY )
    GROUP BY REGEXP_REPLACE(email_address, '@card.com', ''), card_number
    HAVING SUM(amount) > 1000000000 EMIT CHANGES;
    ```

    - -2.5 points
        - missing feature name
        - wrong condition: e.g., `HAVING < 1000000000`
        - unable to run functions like `LEFT` since it is a reserved keyword and it can't be used as an identifier

5. (10pt) Create a table called `sum_normal_amount` group by user name. You have to give the following column names in the table: 
    * `name`: User name extracted from `email_address` 
    * `count`: Number of card usage
    * `sum_amount`: Summation of `amount`
    
    ```sql
    CREATE TABLE sum_normal_amount AS 
    SELECT 
        REGEXP_REPLACE(email_address, '@card.com', '') AS name, 
        COUNT(*) AS count,
        SUM(amount) AS sum_amount
    FROM transactions
    GROUP BY REGEXP_REPLACE(email_address, '@card.com', '')
    EMIT CHANGES;
    ```
    - -1 points 
        - add window statements
        - unmatched column name
    - -2.5 points
        - unable to run functions like `LEFT` since it is a reserved keyword and it can't be used as an identifier
    - -5 points
        - Didn't create table

6. (5pt) From the result of `sum_normal_amount` table or `transactions` stream, (1) Is the threshold(current = 1000000000) reasonable for monitoring the abnormalities? (2) How about monitoring window size(current = 1day)? Please describe your thought and why.

    > If your give a proper answer will be ok.

    - -2.5 points
        - missing questions
        - missing why
        - mis-understanding on `threshold`: `threshold` is about amount, not the number of cases
---

# (30pt) Part 2. Try yourself

1. (10pt) Find or generate a dataset that you are interested in. You can use existing `docker-compose.yml` to build your Kafka cluster or use other tools like the product of `confluent.io`. Please describe how you loaded data with the code(it must be executable, TA will run your code line by line).

    - -2.5 points
        - cannot understand the data type when you generate the data(better if there was a table description)

    - -7.5 points
        - unnecessary codes to construct scenarios / just copy and paste from tutorials

2. (5pt) From your scenario, define the system architecture:
    a. What is your source application(producer)? Describe what your source application does.
    b. What is your target application(consumer)? Describe what your target application does.

    - -2.5 points
        - cannot identify the target application
        - wrong description on each application(source or target) 

3. (15pt) Ask three questions with your scenarios in ksqlDB from your streaming data. One of the queries must use `WINDOW` statement.

    - -5 points
        - missing 1 question(need 3)
    - -2.5 points
        - cannot get results: mismatch with your inserted data e.g., `'false'` - `'FALSE'`
        - cannot understand some parts in the query