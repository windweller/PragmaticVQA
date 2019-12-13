#!/usr/bin/env bash

mkdir -p vqa  # only make the folder if none exists
cd vqa

wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_other_train.json
wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_other_val.json
wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_train.json
wget https://nlp-corpus-collection.s3-us-west-2.amazonaws.com/vqa2/pragmatic_val.json

mkdir -p vqa2_raw
cd vqa2_raw
wget http://images.cocodataset.org/zips/train2014.zip
wget http://images.cocodataset.org/zips/val2014.zip
wget http://images.cocodataset.org/zips/test2015.zip

echo "unzipping a 13GB large zipped file will take a while"
echo "unzip training files"

unzip train2014.zip &> /dev/null

echo "unzipping validation files"

unzip val2014.zip &> /dev/null