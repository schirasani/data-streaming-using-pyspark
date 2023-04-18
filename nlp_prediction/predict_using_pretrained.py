# -*- coding: utf-8 -*-
"""

# **Find sentiment in text**

"""

"""##  1. Setup """

# Install PySpark and Spark NLP
# !pip install -q pyspark==3.3.0 spark-nlp==4.2.8

import json
import pandas as pd
import numpy as np

import sparknlp
import pyspark.sql.functions as F

from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from sparknlp.annotator import *
from sparknlp.base import *
from sparknlp.pretrained import PretrainedPipeline
from pyspark.sql.types import StringType, IntegerType

"""## 2. Start Spark Session"""

spark = sparknlp.start()

print("Spark NLP version", sparknlp.version())
print("Apache Spark version:", spark.version)

spark

"""## 3. Select the pretrained DL model"""

MODEL_NAME='sentimentdl_use_imdb'
# MODEL_NAME='sentimentdl_use_twitter'

"""## 4. Define Spark NLP pipleline"""

documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
    
use = UniversalSentenceEncoder.pretrained(name="tfhub_use", lang="en")\
                .setInputCols(["document"]).setOutputCol("sentence_embeddings")


sentimentdl = SentimentDLModel.pretrained(name=MODEL_NAME, lang="en")\
              .setInputCols(["sentence_embeddings"]).setOutputCol("sentiment")

nlpPipeline = Pipeline(stages = [documentAssembler, use, sentimentdl])

"""## 5. Defining the prediction function with the pipeline"""

def pred(sample_text):
  predict_on_review = [sample]

  df = spark.createDataFrame(predict_on_review, StringType()).toDF("text")
  result = nlpPipeline.fit(df).transform(df)
  # result.show()

  final_res = result.select(F.explode(F.arrays_zip(result.document.result, 
                                      result.sentiment.result)).alias("cols")) \
        .select(F.expr("cols['0']").alias("document"),
                F.expr("cols['1']").alias("sentiment"))
  # final_res.show()

  pred_label = result.first()['sentiment'][0]['result']
  pred_prob = result.first()['sentiment'][0]['metadata'][pred_label]

  pred_label = 'negative' if pred_label == 'neg' else 'positive'

  return pred_label, pred_prob

"""## 6. Make predictions"""

# sample = "I hate this place, the worst"
sample = "I love this place, the best"
pred(sample)

