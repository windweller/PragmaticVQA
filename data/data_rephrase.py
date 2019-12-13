"""
In here we actually use syntactic parsing / dependency parsing / NER / POS to help us rephrase!
"""
import spacy
import json 
from prettytable import PrettyTable

def display(data, ranges):
    x = PrettyTable()
    x.field_names = ["Question", "Answer1", "Answer2"]
    for idx in ranges:
        x.add_row([data[idx]['question'], data[idx]['answer1'], data[idx]['answer2']])
    print(x)

if __name__ == "__main__":
    import json
    train_data = json.load(open('./data/vqa/pragmatic_other_train.json'))
    val_data = json.load(open('./data/vqa/pragmatic_other_val.json'))
    display(train_data, range(20))