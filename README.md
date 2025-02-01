# Interfaccia-Tesi

## Introduction

A simple wizard-like application to automate the data acquisition and analysis process for my thesis research.

The intent of the research is to analyze the effects on viewers of AI Generated Videos in education. The application shows the viewer two short educational videos, asking them generic experience-evaluation questions, with answers on a scale from 1 to 5, and open questions specific about the topic discussed in the videos.

The program will establish what video the user will watch for their first and second video based on the participant's number (ID). Both a real and fake video are always showed, meaning, if the first video is real, the second video will be fake, and viceversa. The videos are also divided into `Male` and `Female`, based on the gender of the speaker featured in the video. If in the first video the speaker was a male, in the second video it will be a female, and viceversa. This is to ensure the *within-subject* experiment design pattern.

The application uses the [PANAS (Positive and Negative Affect Schedule)](https://en.wikipedia.org/wiki/Positive_and_Negative_Affect_Schedule) test to allow users to self-report their positive and negative affect before and after watching each video. In addition, the [Video Engagement Scale (VES)](https://www.researchgate.net/profile/Marij-Hillen/publication/282130705_Assessing_engagement_while_viewing_video_vignettes_validation_of_the_Video_Engagement_Scale_VES/links/61e941ef9a753545e2e4fdbf/Assessing-engagement-while-viewing-video-vignettes-validation-of-the-Video-Engagement-Scale-VES.pdf) questionnaire is administered after each video.

The whole session is recorded via the built-in webcam and data about the experiment is saved to a `.csv` file, like the time of start and end of the session, the answers to each question, what videos were showed, if they were real or fake, male or female, and the timestamps of each event.

The program makes use of the built-in webcam (necessary) to capture the whole session. Please make sure at least one valid webcam is connected to the machine before running the application.

## Videos

The videos are stored in and picked from the `videos` folder, where every subfolder represents a video lesson. For each lesson, you can have:
- **Real** videos presented by a **male** speaker
- **Real** videos presented by a **female** speaker
- **Fake** videos presented by a **male** speaker
- **Fake** videos presented by a **female** speaker

The different type of videos are separated by a hierarchical folder structure. They are separated first by type (`real` or `fake`), then by gender (`M` or `F`).

For example, for a video lesson called `LessonA`, the necessary subfolders are:
- `LessonA/real/M`
- `LessonA/real/F`
- `LessonA/fake/M`
- `LessonA/fake/F`

In each of these folders you can have as many videos as you want, but a video will be picked randomly. It is recommended to have one video for folder. As participants use the program, the program cycles through all the possible video combinations, ensuring that, with given enough captures, all videos have been selected equally over the course of the experiment.

### Video Questions

You can add multiple choice questions about the topics of the video. The answers' order will be randomized, and it will be saved the selected answer, wether it was correct or not, and its relative timestamp. To specify questions, create a `questions.json` file in your video lesson's folder. The file must follow the following structure:

``` json
{
    "Question?": {
        "RIGHT_ANSWER": "Right answer",
        "WRONG_ANSWERS": [
            "Wrong answer 1",
            "Wrong answer 2"
        ]
    }
}
```

You can have as many wrong answers you want per question, but there can only be one right answer. The structure can be repeated. For example, for a three-question poll, your json structure would look like:

``` json
{
    "Question 1?": {
        "RIGHT_ANSWER": "Right answer",
        "WRONG_ANSWERS": [
            "Wrong answer 1",
            "Wrong answer 2"
        ]
    },
    "Question 2?": {
        "RIGHT_ANSWER": "Right answer",
        "WRONG_ANSWERS": [
            "Wrong answer 1",
            "Wrong answer 2"
        ]
    },
    "Question 3?": {
        "RIGHT_ANSWER": "Right answer",
        "WRONG_ANSWERS": [
            "Wrong answer 1",
            "Wrong answer 2"
        ]
    }
}
```

If no `questions.json` is provided for a specific video, no multiple choice questions will be asked were that video be picked.

### Adding Videos

To add videos you can simply add another directory in the `videos` folder. It is **very important** that you setup the folder structure properly when adding new videos.

A video folder must contain:
- `real/M/`: a folder containing the real video performed by a **male** presenter *(`.mp4` or `.avi`)*
- `real/M/`: a folder containing the real video performed by a **female** presenter *(`.mp4` or `.avi`)*
- `fake/M/`: a folder containing the **male** fakes generated from the real video *(`.mp4` or `.avi`)*
- `fake/F/`: a folder containing the **female** fakes generated from the real video *(`.mp4` or `.avi`)*
- `questions.json`: a JSON file containing the multiple choice questions to ask about the topic discussed in the video. (Can be omitted)

The videos can be in `.mp4` or `.avi` format. You can technically put more than one video in each folder, a random one will be picked for display.

## Empatica 

The software is designed to be used in parallel with an Empatica EmbracePlus watch worn on the user wrist, to monitor non-invasely values like Heart Rate (HR) and ElectroDermal Activity (EDA). If you wish to use Empatica to accompany the data capture process, please make sure to setup the watch and start capturing data with Empatica **before** running the application.

It is included with the application a script for automating the process of downloading the recorded data from Empatica after the session and synchronizing it with the video capture.

To automatically download and synchronize the Empatica data make sure you have installed Python >= 3.9 and all the required dependencies, then run the script:

```
python download_empatica_data.py
```

Then follow the instructions on screen.

### AWS Authentication

Empatica uses an AWS S3 bucket to store data and make it accessible to the user. The script uses the AWS SDK for Python to access the bucket and download the data from the Empatica servers.

Please make sure you have downloaded the AWS CLI and used it to save your access credentials (`AWS ACCESS KEY ID, AWS SECRET ACCESS KEY`) before running the script, so that you can be authenticated at download, otherwise it will not be able to download any data.

#### Step 1

Download and Install the AWS CLI:
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

- direct download for Windows:  https://awscli.amazonaws.com/AWSCLIV2.msi

#### Step 2

Setup your credentials in AWS CLI.

Open any terminal, then run:

```
> aws configure
> AWS Access Key ID [None]: <YOUR_ACCESS_KEY_ID>
> AWS Secret Access Key [None]: <YOU_SECRET_ACCESS_KEY_ID>
> Default region name [None]: <LEAVE_EMPTY>
> Default output format [None]: <LEAVE_EMPTY>
```

If you still have problems accessing Empatica Data, please refer to their official guide for Data Access (https://manuals.empatica.com/ehmp/careportal/data_access/v2.7e/en.pdf).

# Config File

The behaviour of the application is customizable by modifying the config file `config.json`.

A brief summary of implemented fields follows.

For the main application:
- `""DATA_FOLDER"`: the folder where recorded data will be saved, it contains the folders for each subject/session
- `"VIDEO_FOLDER"`: the folder where videos are selected for playback, refer to the "Videos" section for more details
- `"QUESTIONS"`: dictionary specifying what questionnaires to administer and when

For downloading data from Empatica:
- `"BUCKET_NAME"`: The S3 Data Bucket of your organization provided by Empatica
- `"PREFIX"`: The tail of the data bucket url (ex. `"v2/716/"`)
- `"PARTICIPANT_ID"`: The ID of the participant used to collect data with Empatica. Can be max 10 characters long, only capital letters and numbers
- `"ORG_ID"`: The ID of your organization provided by Empatica
- `"STUDY_ID":`The ID of the study

## Specifying Questionnaires

You can use the `config.json` file to specify what questionnaires to administer.

The field `"QUESTIONS"` is a dictionary, containing two lists, `BEFORE` and `AFTER`:
- All questionnaires specified inside the `BEFORE` list will be administered, in the order specified within the list, **before** the first video.
- All questionnaires specified inside the `AFTER` list will be administered, in the order specified within the list, **after each video**. There is no option at the moment for a questionnaire administered at the end of the whole experiment.

A Questionnaire (dictionary contained within the `BEFORE` or `AFTER` list) is a dictionary with the keys:
- `"TITLE"` (str): title of the questionnaire, the title displayed on the question page 
- `"INTRO"` (str): optional, a description of the questionnaire, specifying for example scale range, scale values. To omit, use the empty string `""`
- `"ITEMS"` (list): a list of dictionaries representing each item of the questionnaire

An Item (dictionary contained within the `ITEMS` list) is a dictionary with two keys:
- `"QUESTION"` (str): the question/item in question.
- `"SCALE"` (list[str]): a list of strings, representing the scale associated with the question. It can be of any length.

### Example Questionnaire

Here's an example of a questionnaire, constructed with the instructions above, specified inside the `AFTER` list:

``` json
{
    "AFTER": [
        {
            "TITLE": "Title of your questionnaire",
            "INTRO": "For each of the following questions, select an appropriate answer.",
            "ITEMS": [
                {"QUESTION": "Question 1.", "SCALE": ["Strongly disagree", "Disagree", "Neutral", "Agree" , "Strongly Agree"]},
                {"QUESTION": "Question 2.", "SCALE": ["Strongly disagree", "Disagree", "Neutral", "Agree" , "Strongly Agree"]},
                {"QUESTION": "Question 3.", "SCALE": ["Strongly disagree", "Disagree", "Neutral", "Agree" , "Strongly Agree"]}
            ]   
        }
    ]
}
```

Since it's inside the `AFTER` list, it will be administered after each video.

## JSON Schema

This is the [JSON Schema](https://json-schema.org) associated with the `config.json` file:


``` json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
      "app": {
        "type": "object",
        "properties": {
          "DATA_FOLDER": { "type": "string" },
          "VIDEO_FOLDER": { "type": "string" },
          "QUESTIONS": {
            "type": "object",
            "properties": {
              "PANAS": {
                "type": "object",
                "properties": {
                  "SCALE": {
                    "type": "array",
                    "items": { "type": "string" }
                  },
                  "EMOTIONS": {
                    "type": "array",
                    "items": { "type": "string" }
                  },
                  "POSITIVE": {
                    "type": "array",
                    "items": { "type": "integer" }
                  },
                  "NEGATIVE": {
                    "type": "array",
                    "items": { "type": "integer" }
                  }
                },
                "required": ["SCALE", "EMOTIONS", "POSITIVE", "NEGATIVE"]
              },
              "BEFORE": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "TITLE": { "type": "string" },
                    "INTRO": { "type": "string" },
                    "ITEMS": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "QUESTION": { "type": "string" },
                          "SCALE": {
                            "type": "array",
                            "items": { "type": "string" }
                          }
                        },
                        "required": ["QUESTION", "SCALE"]
                      }
                    }
                  },
                  "required": ["TITLE", "ITEMS"]
                }
              },
              "AFTER": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "TITLE": { "type": "string" },
                    "INTRO": { "type": "string" },
                    "ITEMS": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "QUESTION": { "type": "string" },
                          "SCALE": {
                            "type": ["array"],
                            "items": {
                              "type": ["string"]
                            }
                          }
                        },
                        "required": ["QUESTION", "SCALE"]
                      }
                    }
                  },
                  "required": ["TITLE", "ITEMS"]
                }
              }
            },
            "required": ["PANAS", "BEFORE", "AFTER"]
          }
        },
        "required": ["DATA_FOLDER", "VIDEO_FOLDER", "QUESTIONS"]
      },
      "empatica": {
        "type": "object",
        "properties": {
          "BUCKET_NAME": { "type": "string" },
          "PREFIX": { "type": "string" },
          "PARTICIPANT_ID": { "type": "string" },
          "ORG_ID": { "type": "string" },
          "STUDY_ID": { "type": "string" }
        },
        "required": ["BUCKET_NAME", "PREFIX", "PARTICIPANT_ID", "ORG_ID", "STUDY_ID"]
      }
    },
    "required": ["app", "empatica"]
}
```

It's specified in the `schema.json` file and it specifies data type for each field and required fields.

# Installation

## Detailed Installation (Python Environment Setup)

Python version 3.9 is required. It is recommended to create a conda virtual environment using the python version 3.9.

### Dependencies installation

For the time being the dependencies are, for the GUI:
- PyQt5
- OpenCV
- pandas
- jsonschema
- mss
- sr-research-pylink

For the data analyisis:
- numpy
- boto3
- avro
- py-feat
- jsonschema

```
pip install PyQt5 opencv-python pandas numpy boto3 avro py-feat jsonschema mss sr-research-pylink
```

Or you can also simply use the `requirements.txt` file:

```
pip install -r requirements.txt
```

# Usage

Install the application dependencies, then run:

```
python Program.py
```

If you are on Windows, you can also launch the application by running via file explorer the included `run.bat` file.

# License
Distributed under the MIT License. See `LICENSE` for more information.


# Credits
- The AI generated videos were created with [HeyGen](https://www.heygen.com/).
- The list of countries to select nationality was taken from [this repository](https://github.com/umpirsky/country-list).