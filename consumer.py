# import sparkConsumer, kafkaProducer
# # from actors import sparkConsumer, pyProducer
# import json


# def getTopic(path):
#     ''' Parse the list of topics '''
#     file = path + "topic.txt"
#     f = open(file, "r", encoding='latin1')
#     contents = f.read()
#     f.close()
#     return json.loads(contents)


# def main(path, topic1, topic2, topic3):
#     topic_list = getTopic(path)
#     print("Topics:\n"+json.dumps(topic_list, indent=2)+'\n')
#     kafka_producer = kafkaProducer.connectProducer()
#     parsed = sparkConsumer.consumeStream(topic1)
#     print(parsed)
#     # sparkConsumer.processStream(parsed, topic2, topic3, topic_list, kafka_producer)
#     # sparkConsumer.startStreaming(sparkConsumer.ssc)
#     # if kafka_producer is not None:
#     #     kafka_producer.close()


# if __name__ == '__main__':
#     print('\n'+'='*5+' SCRIPT 2 '+'='*5+'\n')
#     path = "../Data/"
#     topic1 = 'Q1'
#     topic2 = 'Q2'
#     topic3 = 'Q3'
#     main(path, topic1, topic2, topic3)

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("yourApp").config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2").getOrCreate()


# spark = SparkSession \
#         .builder \
#         .appName("Python Spark SQL basic example") \
#         .getOrCreate()

# df = spark \
#   .readStream \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", "localhost:9092") \
#   .option("subscribe", "Q1") \
#   .load()

df = spark\
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "192.168.32.131:9092") \
      .option("subscribe", "Q1") \
      .option("startingOffsets", "earliest") \
      .load()


print(df)

# print(df.show())

query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .writeStream \
    .format("console") \
    .option("checkpointLocation", "path/to/HDFS/dir") \
    .start()

query.awaitTermination()

# base_df =df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
# base_df.printSchema()
# df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

