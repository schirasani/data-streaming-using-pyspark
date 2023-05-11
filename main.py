# from actors import pyProducer
import kafkaProducer
from glob import glob
import logging
import re
import json
import pandas as pd


def processFiles(path):
    ''' Split text files into words and format to JSON '''
    # file_list = glob(path+"*")
    # output = []

    # for file in file_list:
    #     name = re.findall('^.*gutenberg\/(.+)\.txt$', file)[0]
    #     print("Processing {}".format(name))
    #     try:
    #         f = open(file, "r", encoding='utf-8')
    #         contents = f.read()
    #         f.close()
    #     except:
    #         f = open(file, "r", encoding='latin1')
    #         contents = f.read()
    #         f.close()
    #     contents = re.split(r'\W+', contents)
    #     for word in filter(lambda word: word is not "", contents):
    #         row = {'source': name, 'word': word}
    #         output.append(json.dumps(row))
    #     print("Lenght of input: {}\n".format(len(output)))
    df = pd.read_csv(path)
    # print(df['text'].tolist()[0])
    return df['text'].tolist()[0:100]


def main(path, topic):
    input = processFiles(path)
    # print(input[0].strip())
    # exit()
    kafkaProducer.publishRecords(input, topic)


if __name__ == '__main__':
    print('\n'+'='*5+' SCRIPT 1 '+'='*5+'\n')
    path = "review_2008.csv"
    topic = 'Q1'
    s_logger = logging.getLogger('py4j.java_gateway')
    s_logger.setLevel(logging.ERROR)
    main(path, topic)