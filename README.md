# Data-Processing-and-Analysis-via-Kafka-using-Web-Scraping
Translating BloombergHT news articles into English and storing them in a database after web scraping. This process involves extracting news from BloombergHT, translating it to English, and organizing it within a database. It enables cross-language access to news data, fostering enhanced analysis and insights from diverse sources.

# Installation

1. **Using Docker:** Launch Kafka and PostgreSQL services using Docker:
   Creating a Network
    ```bash
    docker network create kafka-network --driver bridge
    ```
    Installing Zookeeper via Image
    ```bash
    docker run -d --name zookeeper-server  --network kafka-network  -e ALLOW_ANONYMOUS_LOGIN=yes   bitnami/zookeeper:latest
    ```
    Installing Kafka via Image
    ```bash
    docker run -d --name kafka-server   --network kafka-network -p 9090   -e ALLOW_PLAINTEXT_LISTENER=yes  -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper-server:2181   bitnami/kafka:latest
    ```
    Optional: Installing Kafka User Interface
    ```bash
    docker run -d --rm -p 9000:9000   --network kafka-network   -e KAFKA_BROKERCONNECT=kafka-server:9092  -e SERVER_SERVLET_CONTEXTPATH="/"  obsidiandynamics/kafdrop:latest
    ```
    ```bash
    docker run --name my_postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
    ```

## Usage

Upon launching the project, data extraction from a specific news website will commence using tools like BeautifulSoup. This data will be published on a topic in Kafka. Subsequently, the data will be retrieved from Kafka, translated, and stored in the PostgreSQL database.

The project, once initiated, will conduct daily data extraction and transfer.

