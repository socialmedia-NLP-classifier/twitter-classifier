import tweepy
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
import pickle

def loadPickledData(filePath, default=["default"]):
    """
    load an existing pickle file or make a pickle with default data
    then return the pickled data

    Parameters:
    - filePath: the absolute path or the relative path
    - default: default value if the path is invalid for some reason
    """
    try:
        with open(filePath, "rb") as f:
            content = pickle.load(f)
    except Exception:
        content = default
        with open(filePath, "wb") as f:
            pickle.dump(content, f)
    return content

def saveObjUsingPickle(filePath, content):
    """
    save the content as a byte file using pickle to a specific location
    use the alternate dill function for complex objects

    Parameters:
    - filePath: The absolute or relative path of the pickle file
        - Ex for win: C:\\Users\\....\\filename.pkl
        - Ex for linux and mac: /home/username/.../filename.pkl
    - content: object to be saved"""

    with open(filePath, "wb") as f:
        pickle.dump(content, f)

def get_updated_model():
    pass


def text_pipeline():
    pass

def filter_bad_words(bad_words):
    pass

def load_bad_words():

#### get credentials and keys

def main():
    bad_text = "hello I hate you, blah, blah blah, epson lorem wefewufweiufewfui"
    #info = get_updated_model()




if if __name__ == "__main__":
    main()
