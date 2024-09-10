# Interfaccia-Tesi

A simple wizard-like application to automate the experimentation process for my thesis research.

The program makes use of the built-in webcam (necessary) to capture the whole session. Please make sure a valid webcam is connected to the machine before running the application.

# Adding Videos

To add videos you can simply add another directory in the `videos` folder. It is **very important** that you setup the folder structure properly when adding new videos.

A video folder must contain:
- `real/`: a folder containing the original video *(.mp4, .avi, ...)*
- `fake/`: a folder containing all the fakes generated from the real video *(.mp4, .avi, ...)*
- `questions.txt` : a file containing five questions associated with the video, the questions are in natural language, line separated
- `script.txt` (optional): a file containing the script of the video. Currently unused, could be useful in future developments

## Examples

A valid `questions.txt` might look like this:
```
Question number 1?
Question number 2?
Question number 3?
Question number 4?
Question number 5?
```
For now the number of questions is hard-coded to be five. This is partly a side effect of working with `.csv` files, which require e predetermined number of columns. Hopefully this can be improved.

The videos can be in any common video format (es. .mp4, .avi, ...), and in different formats. You can technically put more than one video in the `real` folder, if there are more real videos that follow the same script.

# Installation

## Detailed Installation (Python Environment Setup)

Python version 3.9 is required. It is recommended to create a conda virtual environment using the python version 3.9.

### Dependencies installation

For the time being the dependencies are:
- PyQt5
- OpenCV
- pandas

```
pip install PyQt5 opencv-python pandas
```

# Usage

Install the application dependencies, then run:

```
python Program.py
```

# License
Distributed under the MIT License. See `LICENSE` for more information.
