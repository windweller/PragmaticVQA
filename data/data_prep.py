"""
We are extracting from VQA paired data
answers with type "Other" and their corresponding questions.
We will take a look at these, as well as their images, to make a new dataset.

We treat "validation" as "test" for now because we didn't obtain that data.
We can also split the "validation" into a "test" if we want.
"""

import json
from tqdm import tqdm

def load_annotations(root='./data/vqa/vqa2_raw/'):
    """Annotations come from a specific format of:
    {'question_type': first few words of the question, 'multiple_choice_answer': ground truth answer, 'answers': we can ignore this,
    'image_id': image associated, 'answer_type':  "yes/no", "number", and "other",
    'question_id': number}

    This file actually does not contain real questions
    
    Keyword Arguments:
        root {str} -- root path of the data folder (default: {'./data/vqa/vqa2_raw/'})

    Return:
        {question_id: {'question_type': 'none of the above',
            'multiple_choice_answer': 'down',
            'image_id': 262148,
            'answer_type': 'other',
            'question_id': 262148000}}
    """
    anno_train_path = "annotations/v2_mscoco_train2014_annotations.json"
    anno_val_path = "annotations/v2_mscoco_val2014_annotations.json"
    
    train_anno_data = {}
    val_anno_data = {}
    for item in json.load(open(root+anno_train_path))['annotations']:
        del item['answers']
        train_anno_data[item['question_id']] = item

    for item in json.load(open(root+anno_val_path))['annotations']:
        del item['answers']
        val_anno_data[item['question_id']] = item

    return train_anno_data, val_anno_data

def load_questions(root='./data/vqa/vqa2_raw/'):
    """This file contains questions but not answers (answers are from annotations)
    We are also only dealing with MSCOCO instead of the 
    
    Keyword Arguments:
        root {str} -- root path (default: {'./data/vqa/vqa2_raw/'})

    Return:
        {question_id: {'image_id': 262148,
            'question': 'What is he on top of?',
            'question_id': 262148002}}
    """
    question_val_path = "questions/v2_OpenEnded_mscoco_val2014_questions.json"
    question_train_path = "questions/v2_OpenEnded_mscoco_train2014_questions.json"
    
    train_questions = {}
    val_questions = {}
    for item in json.load(open(root+question_train_path))['questions']:
        train_questions[item['question_id']] = item 

    for item in json.load(open(root+question_val_path))['questions']:
        val_questions[item['question_id']] = item 

    return train_questions, val_questions

def load_pairs(root='./data/vqa/vqa2_raw/'):
    """Load pairs of question_ids, where both point to the same question, but with different answer!
    
    Keyword Arguments:
        root {str} -- root path (default: {'./data/vqa/vqa2_raw/'})
    """
    comp_list_val_path = "comp_pair_list/v2_mscoco_val2014_complementary_pairs.json"
    comp_list_train_path = "comp_pair_list/v2_mscoco_train2014_complementary_pairs.json"

    comp_list_train = json.load(open(root+comp_list_train_path))
    comp_list_val = json.load(open(root+comp_list_val_path))

    return comp_list_train, comp_list_val


def construct_contrastive_dataset(train_tup, val_tup):
    """construct the dataset and store them
    
    Arguments:
        train_tup {[anno, question, comp_list]} -- A list of lists
        val_tup {[anno, question, comp_list]} -- same as above

    Return:
        [
          {'question': str, 'answer1': str, 'image_id_1': number, 'answer2': str, 'image_id_2': number,
           'question_type': str, 'answer_type': str}
        ]
    """
    # remeber to check question_type (assert)
    # check answer type (assert)

    train_data = []
    val_data = []
    for split in ['train', 'val']:
        anno, quests, comp_list = eval(split+'_tup')
        data = eval(split+'_data')
        for q1, q2 in tqdm(comp_list):
            q1_str = quests[q1]
            q2_str = quests[q2]
            assert q1_str['question'] == q2_str['question'], print(q1_str, q2_str)
            # retrieve two answers!
            ans1, ans2 = anno[q1], anno[q2] # ['multiple_choice_answer']
            # It's possible for two types to not be the same:
            # 'Which Zebra is lying down?'
            # answer1: 'middle', answer_type='other'
            # answer2: '0', answer_type='number'
            # QID: 84591002
            # assert ans1['answer_type'] == ans2['answer_type'], print(q1_str, ans1, ans2)
            assert ans1['image_id'] == q1_str['image_id']
            assert ans2['image_id'] == q2_str['image_id']

            data.append({
                'question': q1_str['question'],
                'answer1': ans1['multiple_choice_answer'],
                'image1': ans1['image_id'],
                'answer2': ans2['multiple_choice_answer'],
                'image2': ans2['image_id'],
                'answer_type1': ans1['answer_type'],
                'answer_type2': ans2['answer_type'],
                'question_type': ans1['question_type']
            })
    return train_data, val_data

def extract_and_save_answer_type(data_list, answer_type='other'):
    processed_data = [[], []]
    for i, data in enumerate(data_list):
        for t in data:
            if t['answer_type1'] == t['answer_type2']:
                if t['answer_type1'] == answer_type:
                    processed_data[i].append(t)

    return processed_data

if __name__ == '__main__':
    STAGE = 'stage3'
    # Stage 1
    if STAGE == 'stage1':
        print('loading...')
        train_anno_data, val_anno_data = load_annotations()
        train_questions, val_questions = load_questions()
        comp_list_train, comp_list_val = load_pairs()
        print("merging...")
        train_data, val_data = construct_contrastive_dataset([train_anno_data, train_questions, comp_list_train], 
                                                                [val_anno_data, val_questions, comp_list_val])
        print('saving...')
        json.dump(train_data, open('./data/vqa/pragmatic_train.json', 'w'))
        json.dump(val_data, open('./data/vqa/pragmatic_val.json', 'w'))
        STAGE = 'stage2'

    # Stage 2
    if STAGE == 'stage2':
        train_data = json.load(open('./data/vqa/pragmatic_train.json'))
        val_data = json.load(open('./data/vqa/pragmatic_val.json'))
        # 198951 out of 200394 in training have the same answer type for both answers
        train_data, val_data = extract_and_save_answer_type([train_data, val_data], 'other')
        json.dump(train_data, open('./data/vqa/pragmatic_other_train.json', 'w'))
        json.dump(val_data, open('./data/vqa/pragmatic_other_val.json', 'w'))
        STAGE = 'stage3'
