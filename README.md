# Interfaccia-Tesi

## Introduction

A simple wizard-like application to automate the data acquisition and analysis process for my thesis research.

The intent of the research is to analyize the effects on viewers of AI Generated Videos in education. The application shows the viewer a short educational video, asking generic experience-evaluation questions, with answers on a scale from 1 to 5, and open questions specific about the topic discussed in the videos. The video displayed will be randomly picked to be a real video or a "fake" video, as in a video generated with Artificial Intelligence (AI).

The application also uses the [PANAS (Positive and Negative Affect Schedule)](https://en.wikipedia.org/wiki/Positive_and_Negative_Affect_Schedule) test to allow users to self-report their positive and negative affect before and after watching the video. 

The whole session is recorded via the built-in webcam and data about the experiment is saved to a `.csv` file, like the time of start and end of the session, the answers to each question, what video was showed, if it was real or fake, and the timestamps of each event.

The program makes use of the built-in webcam (necessary) to capture the whole session. Please make sure a valid webcam is connected to the machine before running the application.

## Videos

The videos are stored in and picked from the `videos` folder, where every subfolder represents a video, and inside each subfolder there are is real video and its fake AI Generated copies, along with the questions associated with the video.

### Adding Videos

To add videos you can simply add another directory in the `videos` folder. It is **very important** that you setup the folder structure properly when adding new videos.

A video folder must contain:
- `real/`: a folder containing the original video *(`.mp4` or `.avi`)*
- `fake/`: a folder containing all the fakes generated from the real video *(`.mp4` or `.avi`)*
- `questions.json`: a JSON file containing the multiple choice questions to ask about the topic discussed in the video. (Can be omitted)

The videos can be in `.mp4` or `.avi` format. You can technically put more than one video in the `real` folder, if there are more real videos that follow the same script. A random video will be picked for display.

### Adding questions

You can add multiple choice questions about the topics of the video. The answers' order will be randomized, and it will be saved the selected answer, wether it was correct or not, and its relative timestamp. To specify questions, create a `questions.json` file in your video's folder. The file must follow the following structure:

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

You can have as many wrong answers you want per question, but there can only be one right answer. The structure can be repeated. For example for a three-question test, your json structure would look like:

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

## Empatica 

The software is designed to be used in parallel with an Empatica EmbracePlus watch worn on the user wrist, to monitor non-invasely values like Heart Rate (HR), Respiratory Rate (RR) and ElectroDermal Activity (EDA). If you wish to use Empatica to accompany the data capture process, please make sure to setup the watch and start capturing data with Empatica **before** running the application.

It is included with the application a script for automating the process of downloading the recorded data from Empatica after the session and synchronizing it with the video capture.

To automatically download and synchronize the Empatica data make sure you have installed Python >= 3.9 and all the required dependencies, then run the script:

```
python prepare_data.py
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
- `"QUESTIONS"`: dictionary containing the keys `"BEFORE"` and `"AFTER"`, for specifying the questions to be asked before and after watching the video. The questions and its relative answers are automatically saved inside the CSV file, with answers on a scale from 1 to 5
- `"[QUESTIONS"]["BEFORE"]`: list of questions to ask before watching the video, with answers on a scale from 1 to 5
- `"[QUESTIONS"]["AFTER"]`: list of questions to ask after watching the video, with answers on a scale from 1 to 5 
- `"[QUESTIONS"]["PANAS"]"`: dictionary containing the keys `"EMOTIONS"`, `"SCALE"`, `"POSITIVE"` and `"NEGATIVE"`, for building the PANAS self-evaluation questionnaire
- `"[QUESTIONS"]["PANAS"]["EMOTIONS"]`: list of emotions to build the PANAS self-evaluation questionnaire
- `"[QUESTIONS"]["PANAS"]["SCALE"]`: verbal frequency scale for the PANAS self-evaluation questionnaire (ie. "from not at all" to "very much")
- `"[QUESTIONS"]["PANAS"]["POSITIVE"]`: indexes (*starting from 1*) of **positive** emotions in the list of emotions provided
- `"[QUESTIONS"]["PANAS"]["NEGATIVE"]`:indexes (*starting from 1*) of **negative** emotions in the list of emotions provided

For downloading data from Empatica:
- `"BUCKET_NAME"`: The S3 Data Bucket of your organization provided by Empatica
- `"PREFIX"`: The tail of the data bucket url (ex. `"v2/716/"`)
- `"PARTICIPANT_ID"`: The ID of the participant used to collect data with Empatica. Can be max 10 characters long, only capital letters and numbers
- `"ORG_ID"`: The ID of your organization provided by Empatica
- `"STUDY_ID":`The ID of the study

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
                            "items": { "type": "string" }
                        },
                        "AFTER": {
                            "type": "array",
                            "items": { "type": "string" }
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
    "required": ["app","empatica"]
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

For the data analyisis:
- numpy
- boto3
- avro
- PyWavelets
- scipy
- py-feat
- jsonschema

```
pip install PyQt5 opencv-python pandas numpy boto3 avro PyWavelets scipy py-feat jsonschema mss
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

# License
Distributed under the MIT License. See `LICENSE` for more information.


# Credits
- The AI generated videos were created with [HeyGen](https://www.heygen.com/).
- The list of countries to select nationality was taken from [this repository](https://github.com/umpirsky/country-list).
