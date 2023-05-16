#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np

import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

# Load the fine-tuned BERT model and tokenizer
print('Model loading...')
model = AutoModelForSequenceClassification.from_pretrained('models/bert-finetuned-sem_eval-english/checkpoint-1000')
print('Model loaded')

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
print('Tokenizer loaded')

# id to label mapping
id2label = {0: 'positive', 1: 'negative', 2: 'neutral'}

def predict(text):
    encoding = tokenizer(text, return_tensors="pt")
    
    # making prediciton
    outputs = model(input_ids=encoding['input_ids'], attention_mask=encoding['attention_mask'])
    
    # getting logits and converting them to probs
    logits = outputs.logits
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    predictions = np.zeros(probs.shape)
    
    # getting predictions greater than threshold
    threshold = 0.5
    predicted_labels = []
    while not predicted_labels and threshold > 0:
        predictions[np.where(probs >= threshold)] = 1
        # turn predicted id's into actual label names
        predicted_labels = [id2label[idx] for idx, label in enumerate(predictions) if label == 1.0]
        print(predicted_labels, threshold)
        
        # looping through again if no label found
        threshold -= 0.1
    
    # returning labels
    if predicted_labels:
        return predicted_labels[0]
    else:
        return "NA"

print('Bert ready for predictions!')
if __name__ == "__main__":

    print('Making predictions -')

    text = "It's not chicago style pizza but it is still awsome.  A chicago themed restaurant.  Owners used to live in Chi town and now are bringing the feel of the city to the West.  Beer selection rocks!"
    print(predict(text))

    text = "It's not chicago style pizza but it is still awsome.  A chicago themed restaurant.  Owners used to live in Chi town and now are bringing the feel of the city to the West.  Beer selection rocks!"
    encoding = tokenizer(text, return_tensors="pt")
    print(encoding.keys())

    outputs = model(input_ids=encoding['input_ids'], attention_mask=encoding['attention_mask'])

    logits = outputs.logits
    print(logits.shape)

    # apply sigmoid + threshold
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    predictions = np.zeros(probs.shape)
    predictions[np.where(probs >= 0.5)] = 1
    # turn predicted id's into actual label names
    predicted_labels = [id2label[idx] for idx, label in enumerate(predictions) if label == 1.0]
    print(predicted_labels)
