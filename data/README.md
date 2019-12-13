# How to download the data

We provide a way to download preprocessed data. 

```
bash download.sh
```

The downloaded `json` file has the following format:

```
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

# Display Question-Answer Pairs

After downloading the data, you can run `display(train_data, range(20))` in `data_rephrase.py` to show questions!

```
+-------------------------------------------------------------------+--------------------+------------+
|                              Question                             |      Answer1       |  Answer2   |
+-------------------------------------------------------------------+--------------------+------------+
|         What type of fruit is in the bottom right corner?         |       apples       |   orange   |
|                    Is their hair long or short?                   |       short        |    long    |
|                     What type of food is this?                    |      sandwich      |   pizza    |
|                      What color is the plate?                     |   blue and white   |   white    |
|           What type of meat do you see in the sandwich?           |      chicken       |    ham     |
|            What color is the spot below the cat's nose?           |       black        |   white    |
|               What does the photo say at the bottom?              |     dutchsimba     |  nothing   |
|                      What color is the bowl?                      |       brown        |   white    |
|                  What does it say on the ground?                  |      no entry      |   clear    |
|           What color is the lamp post on the left side?           |       yellow       |    gray    |
|              What kind of bike is this person riding?             |   mountain bike    | motorcycle |
| What other passive activity is the skateboarder participating in? | listening to music |    none    |
|                    What is on the window sill?                    |  apple and banana  |    cat     |
|     Is the tree in the forefront of the picture alive or dead?    |        dead        |   alive    |
|                   What is the name of this Inn?                   |      hobo inn      |    none    |
|                     What color is the trailer?                    |       orange       |   white    |
|                What kind of vehicle is on the left?               |       truck        |   train    |
|                   What kind of tools are these?                   |      wrenches      | toothbrush |
|                    What is covering the ground?                   |        snow        |    sand    |
|                      What kind of bird is it?                     |        crow        |  seagull   |
+-------------------------------------------------------------------+--------------------+------------+
```

# How to run data processing script

You must be under the parent level directory, if you cloned the github to your home directory, such as `~/PragmaticVQA/`, then execute the following command from there:

```python
python data/data_prep.py
```

In order for this script to run successfully, you need to edit a few variables (such as pointing to the right directory path on your system!)

You do not need to run this script if you just download the preprocessed data!