import json

def display_rephrased(data, ranges):
    """
    This only shows rephrased with original, and answers
    """
    for idx in ranges:
        print("Pragmatic Q3:", data[idx]['question'])
        print("Literal Q1:", data[idx]['literal_question1'])
        print("Literal Q2:", data[idx]['literal_question2'])
        print()

if __name__ == '__main__':
    train_what_rephrased = json.load(open("./data/vqa/pragmatic_other_train_what_rephrased.json"))
    val_what_rephrased = json.load(open("./data/vqa/pragmatic_other_val_what_rephrased.json"))
    display_rephrased(train_what_rephrased, range(40))