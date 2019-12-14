"""
In here we actually use syntactic parsing / dependency parsing / NER / POS to help us rephrase!

The logic of the rephrasing is the following:
1. Filter by "What", reject "What's"
2. Extract the rest of questions starting by AUX
3. Classify into situations:
    0). No AUX found (do nothing)
    1). "AUX..NOUN?" -> "AUX..NOUN [ANSWER]" 
      Ex: What color is the bowl? -> "Is the bowl [brown]?"
    2). "AUX ADP...?" -> "AUX [ANSWER] ADP ...?" (No VERB)
      Ex: What kind of vehicle is on the left? -> "Is (a)[truck] on the left?"
      Ex: What is in the dogs mouth? -> "Is (a)[frisbee] in the dogs mouth?"
    3). "AUX..VERB..?"
      a). "AUX PRON/NOUN doing" -> "AUX PRON/NOUN [ANSWER]...?" (special case)
        Ex: What are the people doing? -> "Are the people [skiing]?"
      b). "AUX ... PRON/NOUN VERB...?" -> "AUX PRON/NOUN VERB [ANSWER] ...?" (VERB is transitive)
            Ex: What does it say on the ground? -> "Does it say [no entry] on the ground?"
            Ex: What kind of bike is this person riding? -> "Is this person riding (a)[mountain bike]?"
      c). "AUX VERB ...?" -> "AUX [ANSWER] VERB ...?"
            Ex: What is covering the ground? -> "Is [snow] covering the ground?"
      d). "AUX ... PRON/NOUN VERB ADP..ADP..?" -> "AUX PRON/NOUN VERB ADP...ADP [ANSWER] ...?" (VERB is intransitive)
            Ex: What is the hot dog sitting on top of? -> "Is the hot dog sitting on top of [paper]?"
        (I don't think other cases exist)
4. Adding answer:
    1). We do not add article in front of words. Thought about determining singular/plural, but the article adding is too difficult.
    For example, "evening" and "frisbee" are both noun, but can't say "a evening".
    2). We unify AUX verbs' singular/plural with the answer's singular plural.


Not yet accommondated questions:
What type of meat do you see in the sandwich?
What is the hot dog sitting on top of?

Acommondated:
What color is the bowl?
What does it say on the ground?
What kind of vehicle is on the left?
What color are the walls?
What is covering the ground?
What letters are on the airplane? (klm / jetblue)
What kinds of meat on this sandwich?
What is the hot dog sitting on top of?
What did the girl give to the man? 

Known bugs:
1. Not sure how to deal with determiner and article (irregularities in English)
('Are the people skiing ?', 'Are the people snowboarding ?')

Possible extensions:
We can include HOW type questions
How could you give this bath more privacy? curtains/door
-> "Could you give this bath more privacy?" "Yes, with curtains"

But there are some errors in this dataset, such as:
How supplied these banana? dole/chiquita
How does the dog carry his Frisbee?  in his mouth / mouth

Notes:
1. We initially divided VERB by transitive or intransitive, however, the checker is not perfect:
'What kind of bike is this person riding?' -> 'riding" is determined as 'intransitive', which is not good for us
So we move to a different set of rules
Old rules:
      b). VERB is TRANVERB 
        i). "AUX ... PRON/NOUN VERB...?" -> "AUX PRON/NOUN VERB [ANSWER] ...?"
            Ex: What does it say on the ground? -> "Does it say [no entry] on the ground?"
            Ex: What kind of bike is this person riding? -> "Is this person riding (a)[mountain bike]?"
        ii). "AUX VERB ...?" -> "AUX [ANSWER] VERB ...?"
            Ex: What is covering the ground? -> "Is [snow] covering the ground?"
      c). VERB is INTRANVERB
        i). "AUX ... PRON/NOUN VERB ADP..ADP..?" -> "AUX PRON/NOUN VERB ADP...ADP [ANSWER] ...?"
            Ex: What is the hot dog sitting on top of? -> "Is the hot dog sitting on top of [paper]?"
        (I don't think other cases exist)

TODO:
1. Maybe fix some singular plural AUX problem like:
('Are klm on the airplane ?', 'Are jet blue on the airplane ?')
--> this is rare, from `rephrase("What letters are on the airplane?", 'klm', 'jet blue')`
"""
import spacy
import json 
from prettytable import PrettyTable
from nltk.stem import WordNetLemmatizer
from copy import copy
from tqdm import tqdm

def display(data, ranges, what_only=True):
    x = PrettyTable()
    x.field_names = ["Question", "Answer1", "Answer2"]
    for idx in ranges:
        if 'What' in data[idx]['question']:
            x.add_row([data[idx]['question'], data[idx]['answer1'], data[idx]['answer2']])
    print(x)

def search(data, search_word, limit=5):
    x = PrettyTable()
    cnt = 0
    for d in data:
        if search_word in d['question']:
            x.add_row([d['question'], d['answer1'], d['answer2']])
            cnt += 1
        if cnt == limit:
            break
    print(x)

def check_verb(token):
    """Check verb type given spacy token"""
    if token.pos_ == 'VERB':
        indirect_object = False
        direct_object = False
        for item in token.children:
            if(item.dep_ == "iobj" or item.dep_ == "pobj"):
                indirect_object = True
            if (item.dep_ == "dobj" or item.dep_ == "dative"):
                direct_object = True
        if indirect_object and direct_object:
            return 'DITRANVERB'
        elif direct_object and not indirect_object:
            return 'TRANVERB'
        elif not direct_object and not indirect_object:
            return 'INTRANVERB'
        else:
            return 'VERB'
    else:
        return token.pos_

wnl = WordNetLemmatizer()

def is_noun_plural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma

aux_verb_get_dual = {
    "is": "are",
    "are": "is",
    "does": "do",
    "do": "does"
}

def unify_answer(answer, aux_verb):
    noun_plural, _ = is_noun_plural(answer)
    if noun_plural and aux_verb in {'is', 'does'}:
        aux_verb = aux_verb_get_dual[aux_verb]
    if not noun_plural and aux_verb in {'are', 'do'}:
        aux_verb = aux_verb_get_dual[aux_verb]
    return aux_verb

def show_pos(sent):
    print(sent)
    print(" ".join([token.pos_ for token in nlp(sent)]))

def join_cap_sent(list_of_words, answer):
    # We unify AUX verb with answer plurality here
    # because different answer has different plurality!
    aux_verb = unify_answer(answer, list_of_words[0])
    list_of_words[0] = aux_verb
    
    return " ".join(list_of_words).capitalize()

def check_pron_or_noun_before_verb(pos_start_from_aux):
    pron_idx, noun_idx = -1, -1
    if 'PRON' in pos_start_from_aux:
        pron_idx = pos_start_from_aux.index("PRON")
    if 'NOUN' in pos_start_from_aux:
        noun_idx = pos_start_from_aux.index("NOUN")
        
    pron_or_noun_idx = min(noun_idx, pron_idx)
    
    verb_idx = pos_start_from_aux.index("VERB")
    return pron_or_noun_idx < verb_idx

def check_adp_immediately_after_verb(pos_start_from_aux):
    # this can suggest transitivity
    # "sitting on top of" vs "riding" / "say"
    adp_idx = -1
    if 'ADP' in pos_start_from_aux:
        adp_idx = pos_start_from_aux.index("ADP")
    verb_idx = pos_start_from_aux.index("VERB")
    return adp_idx - verb_idx == 1

def get_right_most_idx(pos_start_from_aux, pos_tag):
    return next(i for i in reversed(range(len(pos_start_from_aux))) if pos_start_from_aux[i] == pos_tag)
    
def rephrase(question, answer1, answer2):
    """
    Return (pragmatic_question1, pragmatic_question2) or (None, None)
    """
    nlp_sent = nlp(question)
    
    # Filter out questions that do not start with "WHAT"
    if nlp_sent[0].text != 'What' or "What's" in question:
        return None, None
    
    pos_per_tokens = [token.pos_ for token in nlp_sent]
    
    # 0). No AUX found (do nothing)
    if 'AUX' not in pos_per_tokens:
        return None, None
    
    aux_idx = pos_per_tokens.index("AUX")
    sent_start_from_aux = [token.text for token in nlp_sent][aux_idx:]
    pos_start_from_aux = pos_per_tokens[aux_idx:]
    
    # Then we go into branches 
    
    # No verb situation
    if 'VERB' not in pos_start_from_aux:
        # 2). "AUX ADP...?" -> "AUX [ANSWER] ADP ...?"
        # This assumes no NOUN, we insert answer as NOUN
        if 'ADP' in pos_start_from_aux:
            return join_cap_sent([sent_start_from_aux[0], answer1] + sent_start_from_aux[1:], answer1), join_cap_sent([sent_start_from_aux[0], answer2] + sent_start_from_aux[1:], answer2)
        # 1). "AUX..NOUN?" -> "AUX..NOUN [ANSWER]"
        # directly append to the last part before PUNCT
        elif 'NOUN' in pos_start_from_aux:
            return join_cap_sent(sent_start_from_aux[:-1] + [answer1, '?'], answer1), join_cap_sent(sent_start_from_aux[:-1] + [answer2, '?'], answer2)
    else:
        # 3). "AUX..VERB..?"
        # a). "AUX PRON/NOUN doing" -> "AUX PRON/NOUN [ANSWER]...?" (special case)
        verb_idx = pos_per_tokens.index('VERB')
        VERB_FORM = check_verb(nlp_sent[verb_idx])

        if 'doing' in sent_start_from_aux:
            # replace "doing" with the answer
            new_sent_1 = copy(sent_start_from_aux)
            new_sent_2 = copy(sent_start_from_aux)
            new_sent_1[new_sent_1.index('doing')] = answer1
            new_sent_2[new_sent_2.index('doing')] = answer2
            return join_cap_sent(new_sent_1, answer1), join_cap_sent(new_sent_2, answer2)
        
        # d). "AUX ... PRON/NOUN VERB ADP..ADP..?" -> "AUX PRON/NOUN VERB ADP...ADP [ANSWER] ...?"
        elif check_adp_immediately_after_verb(pos_start_from_aux) and check_pron_or_noun_before_verb(pos_start_from_aux) and VERB_FORM == 'INTRANVERB':
            right_most_adp_idx = get_right_most_idx(pos_start_from_aux, 'ADP')
            return join_cap_sent(sent_start_from_aux[:right_most_adp_idx+1] + [answer1] + sent_start_from_aux[right_most_adp_idx+1:], answer1), \
                        join_cap_sent(sent_start_from_aux[:right_most_adp_idx+1] + [answer2] + sent_start_from_aux[right_most_adp_idx+1:], answer2)
        # c). "AUX VERB ...?" -> "AUX [ANSWER] VERB ...?"
        elif pos_start_from_aux.index("VERB") - pos_start_from_aux.index("AUX") == 1:
            verb_idx = pos_start_from_aux.index("VERB")
            # insert answer before the verb!
            return join_cap_sent(sent_start_from_aux[:verb_idx] + [answer1] + sent_start_from_aux[verb_idx:], answer1), \
                    join_cap_sent(sent_start_from_aux[:verb_idx] + [answer2] + sent_start_from_aux[verb_idx:], answer2)
        # b). "AUX ... PRON/NOUN VERB...?" -> "AUX PRON/NOUN VERB [ANSWER] ...?"
        elif check_pron_or_noun_before_verb(pos_start_from_aux):
            verb_idx = pos_start_from_aux.index("VERB")
            # insert answer right after the verb
            return join_cap_sent(sent_start_from_aux[:verb_idx+1] + [answer1] + sent_start_from_aux[verb_idx+1:], answer1), \
                    join_cap_sent(sent_start_from_aux[:verb_idx+1] + [answer2] + sent_start_from_aux[verb_idx+1:], answer2)

    return None, None

if __name__ == "__main__":

    nlp = spacy.load("en_core_web_sm")

    import json
    train_data = json.load(open('./data/vqa/pragmatic_other_train.json'))
    val_data = json.load(open('./data/vqa/pragmatic_other_val.json'))
    display(train_data, range(20))

    p_train_data = []

    for d in tqdm(train_data):
        pq1, pq2 = rephrase(d['question'], d['answer1'], d['answer2'])
        if pq1 is not None:
            d['literal_question1'] = pq1 
            d['literal_question2'] = pq2
            p_train_data.append(d)
    
    p_val_data = []

    for d in tqdm(val_data):
        pq1, pq2 = rephrase(d['question'], d['answer1'], d['answer2'])
        if pq1 is not None:
            d['literal_question1'] = pq1 
            d['literal_question2'] = pq2
            p_val_data.append(d)

    print("Saving json...")
    print(len(p_train_data))
    print(len(p_val_data))

    json.dump(p_train_data, open("./data/vqa/pragmatic_other_train_what_rephrased.json", 'w'))
    json.dump(p_val_data, open("./data/vqa/pragmatic_other_val_what_rephrased.json", 'w'))