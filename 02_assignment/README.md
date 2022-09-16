# Assignment

Please Make sure your code is executable. To start the docker-machines please run:

```bash
$ cd 02_assignment
$ docker-compose up -d
```

## Objective

* Understand how does a Kafka cluster working in docker machines.
* Ability to run a Kafka cluster and ksqlDB-CLI with docker
* Understand how to connect other source applications to ksqlDB / Kafka cluster.
* Learn how to write ksql query with new statements(e.g., `WINDOW`, `EMIT CHANGES`, ...)

## Part 1: Fraud Detection

<img src="./bitcoin.jpg" width="40%">

You are a data scientist in a financial card company. Some users try to hack the system to spend a lot of money, which is unreasonable. It would be best if you detected these abnormalities. So, you tried to build a simulation system to run some experiments. All the data will be generated from a python code(`producer.py`) and inserted into the PostgreSQL database. Information about table `transaction` is as follows: 

| Column Name | Type | Describe |
|:--:|---| --- |
| tid | INTEGER PRIMARY KEY NOT NULL | Index of Table |
| ts | VARCHAR(30) | Timestamp that a user use the card |
| email_address | VARCHAR(100) | Email address, composed of 'user name' + '@card.com' |
| card_number | VARCHAR(20) | Card number |
| amount | NUMERIC(20, 2) | Amout of usage |

Please do following instruction and write your code for each question:

1. (1 pt) Run producer application `producer.py`(do not stop it).
2. (1 pt) Create a source connector called `transaction_reader` using `JdbcSourceConnector`. The producer will send every 10 data into the Kafka cluster. Check it with `PRINT [topic_name] FROM BEGINNING;`.
3. (1 pt) Create a stream called `transactions` with the proper topic name.
4. (3 pt) Write a monitoring query. You need to keep tracking if someone's summation of `amount` is larger than a threshold(=1000000000) for every day. Please refer `WINDOW` statement in [ksql documentation](https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/select-pull-query/#window). You have to give the following column names in the table: 
    * `win_start`: The window start with 'yyyy-MM-dd' format
    * `win_end`: The window end with 'yyyy-MM-dd' format
    * `last_trial_time`: The last timestamp the user uses the card between the window(=1 day). The format is 'yyyy-MM-dd''T''HH:mm:ss'.
    * `name`: User name extracted from `email_address` 
    * `card_number`: Card number
    * `sum_amount`: Summation of `amount`
5. (1 pt) Create a table called `avg_normal_amount` group by card user name. You have to give the following column names in the table: 
    * `name`: User name extracted from `email_address` 
    * `count`: Number of card usage
    * `sum_amount`: Summation of `amount`
6. (2 pt) From `avg_normal_amount` table or `transactions` stream, (1) how do you think about the threshold(current = 1000000000) for monitoring in question 4? Is it reasonable? (2) How about monitoring window(current = 1day)? Please describe your thought and why.

---

# Part 2. Try yourself

1. (3 pt) Find or generate a dataset that you are interested in. You can use existed `docker-compose.yml` to build your Kafka cluster or use other tools like product of `confluent.io`. Please describe how you loaded data with the code(it must be executable, TA will run your code line by line).
2. (2 pt) Define the system architecture:
    a. What is your source application(producer)? Describe what your source application does.
    b. What is your target application(consumer)? Describe what your target application does.
3. (1 pt) Ask three questions with your scenarios in ksqlDB from your streaming data. One of the queries must use `WINDOW` statement.

Useful documents:

- Useful usecases in confluent.io: [https://developer.confluent.io/tutorials/](https://developer.confluent.io/tutorials/)
- Create connectors: [https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/create-connector/](https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/create-connector/)