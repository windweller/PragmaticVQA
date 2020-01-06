"""
We merge MSCOCO and VQA:
{“Question_1”: {“cat”: [(Image_1, [Caption_1]), (Image_2, [Caption_2])], “giraffe”: [(Image_3, Caption_3), (Image_4, Caption_4)], …}}

Each image has 5 captions

Once we build this JSON file, we can use a Jupyter Notebook
to display all the images

anie@arthur2:~/PragmaticVQA/data/vqa/vqa2_raw/mscoco/annotations$ ls
captions_train2014.json  instances_train2014.json  person_keypoints_train2014.json
captions_val2014.json    instances_val2014.json    person_keypoints_val2014.json
"""
import json

from data_prep_vqa import load_annotations, load_questions
from collections import defaultdict

MSCOCO_ANNO_PATH = "/home/anie/PragmaticVQA/data/vqa/vqa2_raw/mscoco/annotations/"

def load_mscoco_captions(path):
    """load mscoco captions
    
    Arguments:
        path {str} -- path to annotations

    Returns:
        image_id_to_cap: {'image_id': [cap_1, cap_2, ..., cap_5]}
    """
    with open(path+"captions_train2014.json") as f:
        train_captions = json.load(f)
    with open(path+"captions_val2014.json") as f:
        val_captions = json.load(f)

    train_image_id_to_cap = defaultdict(list)
    for a in train_captions['annotations']:
        train_image_id_to_cap[a['image_id']].append(a['caption'])

    val_image_id_to_cap = defaultdict(list)
    for a in val_captions['annotations']:
        val_image_id_to_cap[a['image_id']].append(a['caption'])

    return train_image_id_to_cap, val_image_id_to_cap

def merge_mscoco_with_qud(train_image_id_to_cap, val_image_id_to_cap,
                        train_anno_data, val_anno_data,
                        train_questions, val_questions):
    """
    TODO: hmmm it's weird to have train/val to be seperate. Maybe we'll merge them at some point.
    
    Arguments:
        train_image_id_to_cap {[type]} -- [description]
        val_image_id_to_cap {[type]} -- [description]
        train_anno_data {[type]} -- [description]
        val_anno_data {[type]} -- [description]
        train_questions {[type]} -- [description]
        val_questions {[type]} -- [description]

    Returns:
            {“Question_1”: {“cat”: [(Image_1, [Caption_1]), (Image_2, [Caption_2])], “giraffe”: [(Image_3, Caption_3), (Image_4, Caption_4)], …}}
    """
    val_qud_data = {}

    for q_id, question in val_questions.items():
        q = question['question']
        a = val_anno_data[q_id]['multiple_choice_answer']
        image_id = val_anno_data[q_id]['image_id']
        if q not in val_qud_data:
            val_qud_data[q] = defaultdict(list)
            val_qud_data[q][a].append(image_id)
        else:
            val_qud_data[q][a].append(image_id)

    train_qud_data = {}

    for q_id, question in train_questions.items():
        q = question['question']
        a = train_anno_data[q_id]['multiple_choice_answer']
        image_id = train_anno_data[q_id]['image_id']
        if q not in train_qud_data:
            train_qud_data[q] = defaultdict(list)
            train_qud_data[q][a].append(image_id)
        else:
            train_qud_data[q][a].append(image_id)
    
    return train_qud_data, val_qud_data


if __name__ == '__main__':
    print('loading...')
    train_anno_data, val_anno_data = load_annotations()
    train_questions, val_questions = load_questions()
    train_image_id_to_cap, val_image_id_to_cap = load_mscoco_captions(MSCOCO_ANNO_PATH)

    train_qud_data, val_qud_data = merge_mscoco_with_qud(train_image_id_to_cap, val_image_id_to_cap,
                        train_anno_data, val_anno_data,
                        train_questions, val_questions)

    print("saving...")

    json.dump(train_qud_data, open("./data/vqa/train_qud_data.json", 'w'))
    json.dump(val_qud_data, open("./data/vqa/val_qud_data.json", 'w'))

    json.dump(train_image_id_to_cap, open("./data/vqa/train_image_id_to_cap.json", 'w'))
    json.dump(val_image_id_to_cap, open("./data/vqa/val_image_id_to_cap.json", 'w'))
