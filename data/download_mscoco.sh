#!/usr/bin/env bash

cd vqa 
# mkdir -p vqa2_raw
# cd vqa2_raw
# mkdir -p mscoco
# cd mscoco
# wget http://images.cocodataset.org/zips/train2014.zip
# wget http://images.cocodataset.org/zips/val2014.zip
# wget http://images.cocodataset.org/zips/test2015.zip

# echo "unzipping a 13GB large zipped file will take a while"
# echo "unzip training files"

# unzip train2014.zip &> /dev/null

# echo "unzipping validation files"

# unzip val2014.zip &> /dev/null
cd vqa2_raw/mscoco/

wget http://images.cocodataset.org/annotations/annotations_trainval2014.zip
unzip annotations_trainval2014.zip