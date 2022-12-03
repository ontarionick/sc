# Data Engineering Takehome Exam

This Github repo is my submission for the Statistics Canada Data Science Fellowship Program's Takehome Exam. I chose the Data Engineering stream, and my solutions to the individual tasks are entirely contained here. This readme contains instructions on how to run the code for each task, as well as any required documentation.

## Dependencies

I've included a `requirements.txt` that you can use to install required Python dependencies. I'll be using Python 3.10.8 for this assignment.

## Installation

The following installation instructions are intended for use on macOS 12.5.1, but should be adaptable to other versions / operating systems. It is assumed that you have Python and pip already installed.

Run the following in your console in the root of this repository:

```
pip install -r requirements.txt
```

## Usage

### Task 1
```
python3.10 download_data.py
```

### Task 2

```
python3.10 create_mapping.py
```

You should see console output as the mapping for each variable of interest for each month of the downloaded data is created and saved to disk.

It's worth noting that there was a typo in one of the column names ("Start / Fin" instead of "End / Fin") for January - April. This doesn't have any effect on this or any other tasks, though.

## Task Documentation

TBD