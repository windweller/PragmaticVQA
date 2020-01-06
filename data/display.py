"""
We can use > to redirect output to a file
"""

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

def display_qud_captions(qud_data, image_id_to_cap, ranges):
    # we default to 1st caption for display
    
    qud_data_list = list(qud_data.items())
    for idx in ranges:
        ex = qud_data_list[idx]
        print("Q: ", ex[0])
        for k, vs in ex[1].items():
            print("Answer: ", k)
            for v in vs:
                print("Image ID", v, "Caption: ", image_id_to_cap[str(v)][0])
        print()

if __name__ == '__main__':
    # train_what_rephrased = json.load(open("./data/vqa/pragmatic_other_train_what_rephrased.json"))
    # val_what_rephrased = json.load(open("./data/vqa/pragmatic_other_val_what_rephrased.json"))
    # display_rephrased(train_what_rephrased, range(40))

    train_qud_data = json.load(open("./data/vqa/train_qud_data.json"))
    train_image_id_to_cap = json.load(open("./data/vqa/train_image_id_to_cap.json"))

    display_qud_captions(train_qud_data, train_image_id_to_cap, range(10))