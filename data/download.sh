#!/usr/bin/env bash

mkdir -p vqa  # only make the folder if none exists
cd vqa

wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_other_train.json
wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_other_val.json
wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_train.json
wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_val.json

wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_other_val_what_rephrased.json
wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_other_train_what_rephrased.json
