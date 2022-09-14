docker-compose exec kafka1 kafka-topics --create --topic topic1 --bootstrap-server kafka1:29092,kafka2:29093,kafka3:29094 --replication-factor 1 --partitions 1 
docker-compose exec kafka1 kafka-topics --list --bootstrap-server kafka1:9092,kafka2:9093,kafka3:9094
docker-compose -f .\zoo-docker-compose.yml -f .\kafka-docker-compose.yml up -d

kafka-topics --create --topic click_log --bootstrap-server kafka1:9092,kafka2:9093,kafka3:9094
kafka-topics.bat --create --zookeeper localhost:2181,localhost:2182,localhost:2183 --replication-factor 3 --partitions 1 --topic news

./bin/windows/kafka-topics.bat --create --bootstrap-server localhost:29092,localhost:29093,localhost:29094 --replication-factor 1 --partitions 1 --topic test
./bin/windows/kafka-topics.bat --create --bootstrap-server kafka1:29092,kafka2:29093,kafka3:29094 --replication-factor 1 --partitions 1 --topic test

docker run --network=kafkanet --rm --detach --name broker -p 9092:9092 -e KAFKA_BROKER_ID=1 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://broker:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka:latest

# windows 

```
docker network create --gateway 172.18.0.1 --subnet 172.18.0.0/16 kafkanet
```

```powershell
.\bin\windows\kafka-topics.bat --bootstrap-server localhost:19092,localhost:19093,localhost:19094 --topic purchases --create --replication-factor 1 --partitions 5
.\bin\windows\kafka-topics.bat --bootstrap-server localhost:19092,localhost:19093,localhost:19094 --topic purchases --describe 
.\bin\windows\kafka-console-producer.bat --bootstrap-server localhost:19092,localhost:19093,localhost:19094 --topic purchases --property "parse.key=true" --property "key.separator=:"
.\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:19092,localhost:19093,localhost:19094 --topic purchases --from-beginning --property print.key=true --property key.separator="-" 
```


```powershell
.\bin\windows\kafka-topics.bat --bootstrap-server localhost:9092 --topic purchases --create --replication-factor 2 --partitions 3
.\bin\windows\kafka-topics.bat --bootstrap-server localhost:9092 --topic purchases --describe 
.\bin\windows\kafka-console-producer.bat --bootstrap-server localhost:9092 --topic purchases --property "parse.key=true" --property "key.separator=:"
.\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic purchases --from-beginning --property print.key=true --property key.separator="-" 
```