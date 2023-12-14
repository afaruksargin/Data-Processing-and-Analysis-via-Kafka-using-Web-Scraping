import socket
from confluent_kafka import Consumer
import json
from datetime import datetime
import pandas as pd
from io import StringIO
import os
import sys
import psycopg2
from psycopg2 import sql


def consumer_func(consumer , topics, max_messages):
    current_date = datetime.now().strftime("%Y-%m-%d")
    data = []
    message_count=0

    try:
        consumer.subscribe(topics)
        while message_count <= max_messages:
            msg = consumer.poll(timeout=5.0)
            if msg is None:
                continue
            if msg.error():
                print('HATA ALINDI')
            else:
                json_data=msg.value().decode('utf-8')
                python_dict = json.loads(json_data)
                data.append(python_dict)
                message_count+=1

    except Exception as e:
        print(f"Bir hata oluştu : {e}")
        return None
    finally:
        dataframe = pd.DataFrame(data)
        dataframe['Time'] = pd.to_datetime(dataframe['Time'])
        filtered_df = dataframe[dataframe["Time"] >= current_date]
        consumer.close()
        return filtered_df
    
def create_table():
    try:
        connection=psycopg2.connect(
            host='localhost',
            user="postgres",
            password="1234",
            database="postgres"
        )

        #Cursor Oluştur
        cursor=connection.cursor()
        query=(
            f"CREATE TABLE IF NOT EXISTS public.BloombergNews "+
            "(Time date null, "+
            "Title text null, "+
            "SpotTitle text null, "+
            "Content text null);")
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"PSQL Hatası : {e} ")

def write_to_postgre(dataframe):
    try:
        connection=psycopg2.connect(
            host='localhost',
            user="postgres",
            password="1234",
            database="postgres"
        )

        #Cursor Oluştur
        cursor=connection.cursor()
        for index, row in dataframe.iterrows():
            cursor.execute("INSERT INTO public.BloombergNews (Time, Title,SpotTitle,Content) VALUES (%s, %s,%s, %s);", (row['Time'], row['Title_English'], row['SpotTitle_English'], row['Content_English']))
        connection.commit()

        # Bağlantıyı kapat
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"PSQL Hatası : {e} ")
    
def main():
    
    conf = {'bootstrap.servers':'172.18.0.3:9092',
            'group.id':"BloomberNews"}
    consumer = Consumer(conf)
    dataframe = consumer_func(consumer=consumer,topics=["BloombergNews"],max_messages=20)
    
    create_table()

    write_to_postgre(dataframe=dataframe)
    
    

if __name__ == '__main__':
    main()