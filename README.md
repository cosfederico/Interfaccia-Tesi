# Interfaccia-Tesi

## Data Acquisition

A simple wizard-like application to automate the experimentation process for my thesis research.

The program makes use of the built-in webcam (necessary) to capture the whole session. Please make sure a valid webcam is connected to the machine before running the application.

### Adding Videos

To add videos you can simply add another directory in the `videos` folder. It is **very important** that you setup the folder structure properly when adding new videos.

A video folder must contain:
- `real/`: a folder containing the original video *(`.mp4` or `.avi`)*
- `fake/`: a folder containing all the fakes generated from the real video *(`.mp4` or `.avi`)*
- `questions.txt` : a file containing five questions associated with the video, the questions are in natural language, line separated
- `script.txt` (optional): a file containing the script of the video. Currently unused, could be useful in future developments

#### Examples

A valid `questions.txt` might look like this:
```
Question number 1?
Question number 2?
Question number 3?
Question number 4?
Question number 5?
```
For now the number of questions is hard-coded to be five. This is partly a side effect of working with `.csv` files, which require e predetermined number of columns. Hopefully this can be improved.

The videos can be in `.mp4` or `.avi` format, and in different formats. You can technically put more than one video in the `real` folder, if there are more real videos that follow the same script.

### Capturing Data

To start capturing data, make sure you haveinstalled Python >= 3.9 and all the required dependencies, then run:

```
python Program.py
```

## Data Analysis

I have included a script for automating the process of downloading third-party data from Empatica and synchronizing it with the sessions captured with this program.

To automatically synchronize data, make sure you have installed Python >= 3.9 and all the required dependencies, then run the script:

```
python prepare_data.py
```

Then follow the instructions on screen.

### Empatica Authentication

The script uses the AWS SDK for Python to download data from the Empatica servers.

Please make sure you have downloaded the AWS CLI and used it to save your access credentials (`AWS ACCESS KEY ID, AWS SECRET ACCESS KEY`) before running the script, otherwise it will not be able to download any data.

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

# Installation

## Detailed Installation (Python Environment Setup)

Python version 3.9 is required. It is recommended to create a conda virtual environment using the python version 3.9.

### Dependencies installation

For the time being the dependencies are, for the GUI:
- PyQt5
- OpenCV
- pandas

For the data analyisis:
- numpy
- boto3
- avro
- pywt
- scipy
- libreface

```
pip install PyQt5 opencv-python pandas numpy boto3 avro pywt scipy libreface
```

You can also simply use the requirements.txt file:

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
