from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient , NewTopic
import pandas as pd
from haberler import main as haberlerdataframe


def delivery_report(err, msg):
        if err is not None:
            print("Hatalı gönderme oldu {} {}".format(str(msg), str(err)))
        else:
            print('Başarılı Gönderme: {}'.format(str(msg)))

def create_topic(kafka_brokers):
    """
    Gerekli olan topic bu fonksiyon içinde oluşturulacak.
    """
    try:
        adminclient = AdminClient({'bootstrap.servers':kafka_brokers})

        new_topic = NewTopic('BloombergNews',num_partitions=1,replication_factor=1)

        adminclient.create_topics([new_topic])

    except Exception as e:
        print(f" Topic oluşturulurken bir hata alındı : {e}")


def create_producer(kafka_brokers,dataframe):
    """
    Scraping sonucunda elde edilen veriler kafka topicine bu fonksiyon ile yazılacak
    """
    try:
        producer = Producer({
            'bootstrap.servers':kafka_brokers,
            'client.id':'python-producer'
        })

        for _, row in dataframe.iterrows():
            producer.produce('BloombergNews',key=None , value=row.to_json() , callback = delivery_report)

        producer.flush()
    except Exception as e:
        pass

def main(kafka_brokers):
    dataframe = haberlerdataframe()

    create_topic(kafka_brokers)
    
    create_producer(kafka_brokers,dataframe)


if __name__ == '__main__':
      kafka_brokers = "172.18.0.3:9092"
      main(kafka_brokers)
        