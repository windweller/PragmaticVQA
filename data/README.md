# How to download the data

We provide a way to download preprocessed data. 

```
bash download.sh
```

The downloaded `json` file has the following format:

```json
{
    'question': str,
    'answer1': str,
    'image1': corresponding MSCOCO image file ID,
    'answer2': str,
    'image2': corresponding MSCOCO image file ID,
    'answer_type1': type of answers from 'other' or 'yes/no' or 'number',
    'answer_type2': type of answers from 'other' or 'yes/no' or 'number',
    'question_type': first few words of a question
}
```

The script will download 4 JSON files, we will focus on `pragmatic_other_train.json` and `pragmatic_other_val.json`.

To download the MSCOCO training/validation images and unzip them, use the following script:

```
bash download_mscoco.sh
```

The file is quite large (13G training file, 6.2G validation file), the download and unzipping can take a long time. These files are only needed for model training purpose.

# How to run data processing script

You must be under the parent level directory, if you cloned the github to your home directory, such as `~/PragmaticVQA/`, then execute the following command from there:

```python
python data/data_prep.py
```

In order for this script to run successfully, you need to edit a few variables (such as pointing to the right directory path on your system!)

You do not need to run this script if you just download the preprocessed data!