# -*- coding: utf-8 -*-
"""loading_lr_model.ipynb

# **Find sentiment in text**

"""

# Install PySpark
# !pip install -q pyspark==3.3.0

# importing required libraries
import os
import pandas as pd
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegressionModel

# initializing spark session
spark = SparkSession.builder.appName('predict_lr').getOrCreate()

# loading trained logistic regression model
data_path = "/content/drive/MyDrive/CS 532/cs532_project/data"
lrModel = LogisticRegressionModel.load(os.path.join(data_path, "LR_model"))

# regular expression tokenizer
regexTokenizer = RegexTokenizer(inputCol="text", outputCol="words", pattern="\\W")

# stop words
s = "a about after all also always am an and any are at be been being but by came can cant come \
could did didn't do does doesn't doing don't else for from get give goes going had happen \
has have having how i if ill i'm in into is isn't it its i've just keep let like made make \
many may me mean more most much no not now of only or our really say see some something \
take tell than that the their them then they thing this to try up us use used uses very \
want was way we what when where which who why will with without wont you your you're"
more_stop_words = s.split(' ')
add_stopwords = ["http","https","amp","rt","t","c","the"] + more_stop_words
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)

# bag of words count
countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=30000, minDF=5)

# TF-IDF features
hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=30000)
idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=5) #minDocFreq: remove sparse terms

# creating data processing pipeline
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, hashingTF, idf])

def pred(review_text):

  test_sample = spark.createDataFrame(pd.DataFrame([review_text], columns=['text']))
  # test_sample.show()

  # Fit the pipeline to training documents.
  pipelineFit = pipeline.fit(test_sample)
  dataset = pipelineFit.transform(test_sample)
  # dataset.show(20)

  predictions = lrModel.transform(dataset)
  # predictions.show()

  pred_idx = int(predictions.first()['prediction'])
  pred_prob = predictions.first()['probability'][pred_idx]

  pred_to_labels = {0: "positive", 1: "neutral", 2: "negative"}
  pred_label = pred_to_labels[pred_idx]

  return pred_label, pred_prob

sample = "I came to this place and left with a huge disappointment"

pred(sample)

